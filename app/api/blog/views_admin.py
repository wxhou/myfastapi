from math import ceil
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, Query, Security
from app.extensions.redis import MyRedis
from app.common.response import ErrCode, response_ok, response_err
from app.utils.logger import logger
from app.api.deps import get_db, get_redis
from app.api.user.model import BaseUser
from app.api.base.auth import get_current_active_user
from .model import Category, Post, Comment
from .schemas import PostInsert, PostUpdate, PostDelete, CommentInsert


router_blog_admin = APIRouter()


@router_blog_admin.get('/category/list/', summary='文章分类列表')
async def category_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user, scopes=['category_list'])
):
    """文章分类列表"""
    objs = await db.scalars(select(Category).filter(Category.status==0))
    return response_ok(data=[obj.to_dict() for obj in objs])


@router_blog_admin.post('/post/insert/', summary='新建文章')
async def post_insert(request: Request,
                      args: PostInsert,
                      db: AsyncSession = Depends(get_db),
                      current_user: BaseUser = Security(get_current_active_user, scopes=['post_insert'])):
    """新建文章"""
    cate_obj = await db.scalar(select(Category).filter(Category.id==args.category_id))
    if cate_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    obj = Post(title=args.title, body=args.body,
            category_id=args.category_id,
            is_publish=args.is_publish,
            user_id=current_user.id)
    db.add(obj)
    await db.commit()
    return response_ok(data=obj.to_dict())


@router_blog_admin.post('/post/update/', summary='更新文章')
async def post_update(request: Request,
                      post: PostUpdate,
                      db: AsyncSession = Depends(get_db),
                      current_user: BaseUser = Security(get_current_active_user, scopes=['post_update'])):
    """更新文章"""
    cate_obj = await db.scalar(select(Category).filter(Category.id==post.category_id, Category.status==0))
    if cate_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    post_obj = await db.scalar(select(Post).filter(Post.id==post.id, Post.status==0))
    if post_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    await db.execute(update(Post).filter(Post.id==post.id, Post.status==0).values(post.dict(exclude={'id'}, exclude_none=True)))
    await db.commit()
    return response_ok(data=post_obj.to_dict())


@router_blog_admin.get('/post/list/', summary="文章列表")
async def post_list(request: Request,
                    page: int = Query(default=1, ge=1),
                    page_size: int = Query(default=15, ge=1),
                    title: str = Query(default=None),
                    is_publish: bool = Query(default=None),
                    is_comment: bool = Query(default=None),
                    db: AsyncSession = Depends(get_db),
                    current_user: BaseUser = Security(get_current_active_user, scopes=['post_list'])):
    """文章列表"""
    query_filter = [Post.status==0, Post.user_id==current_user.id]
    if title:
        query_filter.append(Post.title.ilike(f"%{title}%"))
    if is_publish:
        query_filter.append(Post.is_publish==is_publish)
    if is_comment:
        query_filter.append(Post.is_comment==is_comment)
    objs = await db.scalars(select(Post).filter(*query_filter).limit(page_size).offset((page - 1) * page))
    _count = await db.scalar(select(func.count()).filter(*query_filter))
    _pages = int(ceil(_count / float(page_size)))
    return response_ok(data=[obj.to_dict() for obj in objs],
                       total=_count, pages=_pages)


@router_blog_admin.get('/post/info/', summary='文章详情')
async def post_info(request: Request,
                    post_id: int = Query(title="文章ID", ge=1),
                    db: AsyncSession = Depends(get_db),
                    redis: MyRedis = Depends(get_redis)):
    """文章详情"""
    query_filter = [Post.id==post_id, Post.status==0]
    post_obj = await db.scalar(select(Post).filter(*query_filter))
    if post_id is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    await redis.zincrby("weblog_post_top", 1, post_id)
    return response_ok(data=post_obj.to_dict())


@router_blog_admin.get('/post/publish/', summary="文章发布")
async def post_publish(request: Request,
                       post_id: int = Query(title="文章ID"),
                       db: AsyncSession = Depends(get_db),
                       current_user=Security(get_current_active_user, scopes=['post_publish'])):
    """文章发布"""
    query_filter = [Post.id==post_id, Post.status==0, Post.user_id==current_user.id]
    post_obj = await db.scalar(select(Post).filter(*query_filter))
    if post_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    await db.execute(update(Post).filter(*query_filter).values(is_publish=True))
    await db.commit()
    return response_ok(data=post_obj.to_dict())


@router_blog_admin.get('/post/top/', summary='热门文章')
async def post_top(request: Request,
                page: int = Query(default=1, ge=1),
                page_size: int = Query(default=100, ge=1),
                title: str = Query(default=None),
                order_type: int = Query(default=1, gt=0, le=3),
                db: AsyncSession = Depends(get_db),
                redis: MyRedis = Depends(get_redis)):
    """热门文章"""
    query_filter = [Post.status==0, Post.is_publish.is_(True)]
    scores = await redis.zrevrange("weblog_post_top", 0, -1)
    _order_by = Post.create_time.desc()
    if order_type == 1 and scores:
        # 按热度排序
        query_filter.append(Post.id.in_(scores))
        _order_by = func.field(Post.id, *scores)
    elif order_type == 3:
        # 随机排序
        _order_by = func.rand()
    if title:
        query_filter.append(Post.title.ilike(f"%{title}%"))
    objs = await db.scalars(select(Post).filter(*query_filter).order_by(_order_by))
    _count = await db.scalar(select(func.count()).filter(*query_filter))
    _pages = int(ceil(_count / float(page_size)))
    return response_ok(data=[obj.to_dict() for obj in objs],
                       total=_count, pages=_pages)


@router_blog_admin.post('/post/delete/', summary="文章删除")
async def post_delete(request: Request,
                       args: PostDelete,
                       db: AsyncSession = Depends(get_db),
                       current_user: BaseUser = Security(get_current_active_user, scopes=['post_publish'])):
    """文章删除"""
    query_filter = [Post.id==args.id, Post.status==0, Post.user_id==current_user.id]
    post_obj = await db.scalar(select(Post).filter(*query_filter))
    if post_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    await db.execute(update(Post).filter(*query_filter).values(status=-1))
    await db.commit()
    return response_ok()


@router_blog_admin.post('/post/comment/', summary='新增评论')
async def post_comment_insert(
                request: Request,
                comment:CommentInsert,
                db: AsyncSession = Depends(get_db),
                redis: MyRedis = Depends(get_redis),
                current_user = Security(get_current_active_user)):
    """文章评论"""
    post_obj = await db.scalar(select(Post).filter(Post.status==0, Post.id==comment.post_id,
                                        Post.is_comment.is_(True), Post.is_publish.is_(True)))
    if post_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    obj = Comment(
        user_id=current_user.id,
        post_id=comment.post_id,
        parent_id=comment.comment_id,
        content=comment.content)
    db.add(obj)
    await db.commit()
    return response_ok()


@router_blog_admin.get('/post/comment/list/', summary='评论列表')
async def post_comment_list(
                request: Request,
                post_id: int = Query(ge=1, title='文章ID'),
                comment_id: int = Query(ge=1, title='评论ID'),
                db: AsyncSession = Depends(get_db),
                current_user: BaseUser = Security(get_current_active_user)):
    """文章评论列表"""
    post_obj = await db.scalar(select(Post).filter(Post.status==0, Post.id==post_id,
                                        Post.is_comment.is_(True), Post.is_publish.is_(True)))
    if post_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    comment_objs = await db.scalars(select(Comment).filter(Comment.post_id==post_id, Comment.parent_id==comment_id))
    result_data = []
    for comment_obj in comment_objs:
        items = comment_obj.to_dict()
        nickname = await db.scalar(select(BaseUser.nickname).filter(BaseUser.id==items['user_id'], BaseUser.status==0))
        items['username'] = nickname
        result_data.append(items)
    return response_ok(data=result_data)