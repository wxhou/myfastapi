import os
import sys
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
import click
import asyncio
from init_data import init_goods, init_goods_category


@click.group()
def cli():
    pass


@cli.command()
def initgoods():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_goods())
    click.echo('Initialized the Goods')


@cli.command()
def initgoodscategory():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_goods_category())
    click.echo('Initialized the Good Category')


if __name__ == '__main__':
    cli()
