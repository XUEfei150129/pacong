import asyncio
import time
import aiohttp
# import requests

from lxml import etree
start = time.time()

urls = [
    'http://127.0.0.1:5000/bobo',
    'http://127.0.0.1:5000/jay',
    'http://127.0.0.1:5000/tom'
]

#发起网络请求，爬取网页完整数据
async def get_request(url):
    #不可以出现不支持异步模块的代码
    #requests是不支持异步，更换一个支持异步的网络请求的模块（aiohttp）
    # response = requests.get(url=url)
    # page_text = response.text
    # return page_text

    #aiohttp进行网络请求的代码操作
    #1.创建一个请求对象:sess
    async with aiohttp.ClientSession() as sess:
        #2.使用请求对象发起请求
        #aiohttp发起请求的代码操作和requests几乎一致，唯一不一致的地方是，使用代理的参数proxy="http://ip:port"
        async with await sess.get(url=url) as response:
            #text()获取字符串形式的响应数据
            #read()获取二进制形式的响应数据
            #json()和以前的作用一致
            page_text = await response.text()
            return page_text
tasks = []
def parse(t): #数据解析
    page_text = t.result()
    tree = etree.HTML(page_text)
    text = tree.xpath('//a[@id="feng"]/text()')[0]
    print(text)
for url in urls:
    c = get_request(url)
    task = asyncio.ensure_future(c)
    #给任务对象绑定回调函数用于数据解析
    task.add_done_callback(parse)
    tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

print('总耗时:',time.time()-start)