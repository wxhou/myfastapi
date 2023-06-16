import time
from math import ceil
from datetime import timedelta
from bson.objectid import ObjectId
from sqlalchemy import func, or_, select, update
from fastapi import APIRouter, Depends, Request, Query, Body, Security
from app.extensions import async_db, async_redis, async_mongo
from app.settings import settings
from app.common.response import ErrCode, response_ok, response_err
from app.utils.logger import logger
from app.api.user.model import BaseUser
from app.api.base.auth import get_current_active_user
from .model import FormTemplate, FormTemplateVersion
from .schemas import TemplateInsert


router_form_admin = APIRouter()



@router_form_admin.post('/insert/', summary='新建模板')
async def template_insert(
    args: TemplateInsert,
    db: async_db,
    redis: async_redis,
    current_user: BaseUser = Security(get_current_active_user, scopes=['template_insert'])
):
    """新建模板"""
    obj = FormTemplate(
        name=args.name,
        type=args.type
    )
    db.add(obj)
    await db.flush()
    obj.college=f't_form_template_{obj.id}'
    await db.commit()
    return response_ok(data={"id": obj.id})


@router_form_admin.post('/design/', summary='模板设计')
async def template_design(
    content: dict,
    request: Request,
    db: async_db,
    redis: async_redis,
    mg_client: async_mongo,
    template_id: int = Query(description='模板ID'),
    current_user: BaseUser = Security(get_current_active_user, scopes=['template_design'])
):
    """表单设计"""
    template_obj = await db.scalar(select(FormTemplate).where(FormTemplate.id==template_id, FormTemplate.status==0))
    if template_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    database = mg_client.t_form_template
    form_collection = database.get_collection(template_obj.college)

    def get_content_columns(input_dict):
        """获取需要创建的字段"""
        output_dict = {}

        def add_columns(content):
            if isinstance(content, dict):
                for key, value in content.items():
                    if key == 'model' and content.get('isCreate'):
                        output_dict[value] = content.get('name', '')
                    add_columns(value)
            elif isinstance(content, list):
                for data in content:
                    add_columns(data)

        add_columns(input_dict)
        return output_dict

    obj = await form_collection.insert_one({"content": content,
                                            "columns": get_content_columns(content)})
    _id = str(obj.inserted_id)

    scalar_subquery1 = select(func.max(FormTemplateVersion.id)).where(FormTemplateVersion.template_id==template_id, FormTemplateVersion.status==0).scalar_subquery()
    fv_obj = await db.scalar(select(FormTemplateVersion).where(
         FormTemplateVersion.id==scalar_subquery1))
    if fv_obj:
        logger.info(f"[{current_user.username}] delete fv_object_id {fv_obj.object_id}")
        await form_collection.delete_one({"_id": ObjectId(fv_obj.object_id)})
        fv_obj.object_id=_id
    else:
        fv_obj = FormTemplateVersion(
            template_id=template_id,
            object_id=_id,
            creator_id=current_user.id
        )
        db.add(fv_obj)
    await db.commit()
    return response_ok(data={"_id": _id})


@router_form_admin.get('/info/', summary='模板详情')
async def template_info(
    db: async_db,
    redis: async_redis,
    mg_client: async_mongo,
    template_id: int = Query(description='模板ID'),
    current_user: BaseUser = Security(get_current_active_user, scopes=['template_info'])
):
    """表单设计"""
    template_obj = await db.scalar(select(FormTemplate).where(FormTemplate.id==template_id,
                                FormTemplate.status==0))
    if template_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    result = template_obj.to_dict()
    fv_obj = await db.scalar(select(FormTemplateVersion).where(
        FormTemplateVersion.template_id==template_id,
        FormTemplateVersion.is_publish==True,
        FormTemplateVersion.is_active==True))
    if fv_obj is None:
        result['content'] = None
        return response_ok(data=result)
    database = mg_client.t_form_template
    form_collection = database.get_collection(template_obj.college)
    fv_content = await form_collection.find_one({"_id": ObjectId(fv_obj.object_id)})
    fv_content['_id'] = str(fv_content['_id'])
    result['content'] = fv_content
    return response_ok(data=result)


@router_form_admin.post('/publish/', summary='模板发布')
async def template_publish(
    db: async_db,
    redis: async_redis,
    template_id: int = Body(description='模板ID', ge=1),
    version_id: int = Body(description='版本ID', ge=1),
    current_user: BaseUser = Security(get_current_active_user, scopes=['template_info'])
):
    """表单发布"""
    template_obj = await db.scalar(select(FormTemplate).where(FormTemplate.id==template_id,
                                FormTemplate.status==0))
    if template_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    fv_obj = await db.scalar(select(FormTemplateVersion.id).where(FormTemplateVersion.template_id==template_id,
                                                   FormTemplateVersion.id==version_id,
                                                   FormTemplateVersion.status==0))
    if fv_obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    await db.execute(update(FormTemplateVersion).where(
        FormTemplateVersion.template_id==template_id,
        FormTemplateVersion.id==version_id).values(is_publish=True))
    await db.commit()
    return response_ok()
