import os
import sys
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
import click
import asyncio
from init_data import init_db, init_super_user, init_goods, init_goods_category


@click.group()
def cli():
    pass


@cli.command()
def initdb():
    """初始化数据库"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    click.echo('Initialized DB Done!')


@cli.command()
@click.option('--username', prompt=True, help='input username.')
@click.option('--password', prompt=True, hide_input=True,
                confirmation_prompt=True, help='input password.')
@click.option('--email', prompt=True, help='input email.')
@click.option('--nickname', prompt=True, help='input nickname.')
def createsuperuser(username, password, email, nickname):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_super_user(username, password, email, nickname))
    click.echo('Initialized super user Done!')


@cli.command()
def initgoodscategory():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_goods_category())
    click.echo('Initialized the Good Category')


@cli.command()
def initgoods():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_goods())
    click.echo('Initialized the Goods')




if __name__ == '__main__':
    cli()
