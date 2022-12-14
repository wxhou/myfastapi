# My fastapi demo

## 功能模块

### 用户管理

- 登录 pass
- 登出 pass
- 注册用户 pass `发送注册邮件激活用户`
- 激活用户接口 pass
- 更新用户头像 pass
- 用户信息更新 pass
- 用户列表 pass
- 验证码 
- 上传文件 pass

- 用户收藏
- 取消收藏
- 获取用户留言列表
- 添加留言
- 删除留言

### 博客
- 文章分类列表 pass
- 新建文章`草稿` pass
- 编辑文章 pass
- 发布文章`正式` pass
- 我的文章列表 pass
- 最新文章 pass
- 热门文章 pass
- 评论文章/评论文章的评论 pass
- 文章评论列表 pass

#### 商品
- 商品分类列表 pass
- 新建商品 pass
- 删除商品 pass
- 商品列表 pass
- 商品详情 pass
- 商品评论详情
- 首页轮播商品

### 订单

- 购物车详情 pass
- 加入购物车 pass
- 删除购物车 pass

- 获取订单 pass
- 新增订单 pass
- 删除订单 pass

- 支付接口

## 项目部署


### 项目启动

uvicorn
```shell
gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199 --reload
```

celery

> 不能使用-P gevent/eventlet ，并发请求下会报错，Linux下perfork测试正常

linux

```shell
celery -A app.core.celery_app.celery worker -l info
```
windows

```cmd
celery -A app.core.celery_app.celery worker -l info -P processes
```

celery beat 定时任务

```shell
celery -A app.core.celery_app.celery beat -S redbeat.RedBeatScheduler -l info
```


### 数据库迁移
#### alembic中文文档
https://hellowac.github.io/alembic_doc/zh/_front_matter.html

#### 简单示例
https://www.jianshu.com/p/942e270baf65

如果迁移文件夹不存在是，执行这个命令
```shell
alembic init alembic
```

将当前的模型生成迁移文件
```shell
alembic revision --autogenerate -m "first" 将当前模型中的状态生成迁移文件
```


更新版本
```shell
alembic upgrade head
```

回滚版本
```shell
alembic downgrade head
```


### RabbitMQ

```shell
# 添加用户跟密码
$ rabbitmqctl add_user test test123
# 添加虚拟主机
$ rabbitmqctl add_vhost test_vhost
# 为用户添加标签
$ rabbitmqctl set_user_tags test test_tag
# 设置用户权限
$ rabbitmqctl set_permissions -p test_vhost test ".*" ".*" ".*"
```

### API Limiter

使用slowapi进行限速，使用装饰器进行规则过滤。


### Question

No.1 sqlalchemy.exc.InvalidRequestError: A transaction is already begun on this Session.
```python
async def async_main():
    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test", echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                    A(bs=[B(), B()], data="a3"),
                ]
            )

        await session.run_sync(fetch_and_update_objects)

        await session.commit()

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()
```

No.2 使用gunicorn的多worker问题

1、 apscheduler

> 讨论链接: https://www.v2ex.com/t/294165
> uvicorn测试多workers不会重复生成。BUT查阅资料后说uvicorn是单进程

解决方案:
- gunicorn只用单worker

    ```shell
    gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199
    ```
- 使用Redis锁限制定时任务执行一次


- 使用celery beat定时任务

2、 socketio

> 多个进程启动会导致socket连接失败

解决方案

- 使用单个进程启动

    ```shell
    gunicorn weblog:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8199
    ```

- 将socketio做为单独的服务启动
