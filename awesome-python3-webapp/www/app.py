# coding=utf-8

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from aiohttp import web


def index(request):  # 返回web参数，content_type设置文件的参数
    return web.Response(body='<h1>Awesome</h1>'.encode('utf-8'), content_type='text/html')


# asyncio异步结构
@asyncio.coroutine
def init(loop):
    app = web.Application()
    app = web.web_runner.AppRunner(app=app).app()
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app._make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
