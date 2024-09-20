import asyncio
from pyppeteer import launch
from lxml import etree


# 一、创建一个特殊的函数
async def main():
    # 对应的pyppeteer相关的操作要写在特殊函数内部
    # 1.创建一个浏览器对象
    # 跟pyppeteer相关的代码前面都要加上await
    bro = await launch(headless=True)
    # 2.创建一个新的page
    page = await bro.newPage()
    # 3.发起请求
    await page.goto('http://quotes.toscrape.com/js/')
    # 4.获取页面源码数据
    page_text = await page.content()
    # 5.数据解析
    tree = etree.HTML(page_text)
    div_list = tree.xpath('//div[@class="quote"]')
    print(len(div_list))
    await asyncio.sleep(3)
    await bro.close()


# 二、创建一个协程对象
c = main()
# 三、创建且启动事件循环对象
loop = asyncio.get_event_loop()
loop.run_until_complete(c)


