"""
Pyppeteer简介
    异步的selenium。在 Pyppetter的背后是有一个类似 Chrome 浏览器的 Chromium 浏览器在执行一些动作进行网页渲染，首先说下 Chrome 浏览器和 Chromium 浏览器的渊源。
        Chromium 是谷歌为了研发 Chrome 而启动的项目，是完全开源的。二者基于相同的源代码构建，Chrome 所有的新功能都会先在 Chromium 上实现，待验证稳定后才会移植，因此 Chromium 的版本更新频率更高，也会包含很多新的功能，但作为一款独立的浏览器，Chromium 的用户群体要小众得多。两款浏览器“同根同源”，它们有着同样的 Logo，但配色不同，Chrome 由蓝红绿黄四种颜色组成，而 Chromium 由不同深度的蓝色构成。
    Pyppeteer 就是依赖于 Chromium 这个浏览器来运行的。那么有了 Pyppeteer 之后，我们就可以免去那些繁琐的环境配置等问题。如果第一次运行的时候，Chromium 浏览器没有安装，那么程序会帮我们自动安装和配置，就免去了繁琐的环境配置等工作。另外 Pyppeteer 是基于 Python 的新特性 async 实现的，所以它的一些执行也支持异步操作，效率相对于 Selenium 来说也提高了。


环境安装
    由于 Pyppeteer 采用了 Python 的 async 机制，所以其运行要求的 Python 版本为 3.5 及以上
    pip install pyppeteer


快速上手
    爬取http://quotes.toscrape.com/js/ 全部页面数据
    代码：
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

    上面的代码必须要是在一个方法里面，不放在特殊函数里面会报错

    详细用法
        开启浏览器
            调用 launch() 方法即可，相关参数介绍：
                ignoreHTTPSErrors (bool): 是否要忽略 HTTPS 的错误，默认是 False。
                headless (bool): 是否启用 Headless 模式，即无界面模式，默认是开启无界面模式的。如果设置为 False则是有界面模式。
                executablePath (str): 可执行文件的路径，如果指定之后就不需要使用默认的 Chromium 了，可以指定为已有的 Chrome 或 Chromium。
                devtools (bool): 是否为每一个页面自动开启调试工具(浏览器开发者工具)，默认是 False。如果这个参数设置为 True，那么 headless 默认参数就会无效，会被强制设置为 False。
                args (List[str]): 在执行过程中可以传入的额外参数。
            关闭提示条：”Chrome 正受到自动测试软件的控制”，这个提示条有点烦，那咋关闭呢？这时候就需要用到 args 参数了，禁用操作如下：
                browser = await launch(headless=False, args=['--disable-infobars'])
        处理页面显示问题：访问淘宝首页
            import asyncio
            from pyppeteer import launch

            async def main():
                browser = await launch(headless=False)
                page = await browser.newPage()
                await page.goto('https://www.taobao.com')
                await asyncio.sleep(3)
                await browser.close()
            asyncio.get_event_loop().run_until_complete(main())

            发现页面显示出现了问题，需要手动调用setViewport方法设置显示页面的长宽像素。设置如下：
                import asyncio
                from pyppeteer import launch

                width, height = 1366, 768
                async def main():
                    browser = await launch(headless=False)
                    page = await browser.newPage()

                    await page.setViewport({'width': width, 'height': height})

                    await page.goto('https://www.taobao.com')
                    await asyncio.sleep(3)
                    await browser.close()
                asyncio.get_event_loop().run_until_complete(main())
        规避检测：执行js程序执行指定的js程序
            正常情况下我们用浏览器访问淘宝等网站的 window.navigator.webdriver的值为 undefined或者为false。而使用pyppeteer访问则该值为true。那么如何解决这个问题呢？
                import asyncio
                from pyppeteer import launch

                width, height = 1366, 768

                async def main():
                    #规避检测
                    browser = await launch(headless=False, args=['--disable-infobars'])
                    page = await browser.newPage()
                    await page.setViewport({'width': width, 'height': height})
                    await page.goto('https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/')

                    #规避检测
                    await page.evaluate(
                        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
                    await asyncio.sleep(20)
                    await browser.close()

                asyncio.get_event_loop().run_until_complete(main())
        节点交互：（可以很好的模拟人的行为）
            import asyncio
            from pyppeteer import launch


            async def main():
                # headless参数设为False，则变成有头模式
                browser = await launch(
                    headless=False
                )
                page = await browser.newPage()
                # 设置页面视图大小
                await page.setViewport(viewport={'width': 1280, 'height': 800})

                await page.goto('https://www.baidu.com/')
                # 节点交互
                await page.type('#kw', '周杰伦', {'delay': 1000})
                await asyncio.sleep(3)
                #点击搜索按钮
                await page.click('#su')
                await asyncio.sleep(3)
                # 使用选择器选中标签进行点击
                alist = await page.querySelectorAll('.s_tab_inner > a')
                a = alist[3]
                await a.click()
                await asyncio.sleep(3)
                await browser.close()
            asyncio.get_event_loop().run_until_complete(main())


爬虫练习
    异步爬取网易新闻首页的新闻标题
    https://news.163.com/domestic/

    import asyncio
    from pyppeteer import launch
    from lxml import etree


    async def main():
        # headless参数设为False，则变成有头模式
        browser = await launch(
            headless=False,
            #可在浏览器中输入chrome://version/，在页面的"个人资料路径"查看浏览器的执行程序
            executablePath='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        )
        page = await browser.newPage()

        await page.goto('https://news.163.com/domestic/')

        await asyncio.sleep(3)
        # 打印页面文本
        page_text = await page.content()

        return page_text


滑动验证
    import random
    from pyppeteer import launch
    import asyncio
    import cv2
    from urllib import request


    async def get_track():
        background = cv2.imread("background.png", 0)
        gap = cv2.imread("gap.png", 0)

        res = cv2.matchTemplate(background, gap, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)[2][0]
        return value * 278 / 360 - 13

    async def main():
        browser = await launch({
            # headless指定浏览器是否以无头模式运行，默认是True。
            "headless": False,
            #设置窗口大小
            "args": ['--window-size=1366,768'],
            "executablePath" : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        })
        # 打开新的标签页
        page = await browser.newPage()
        # 设置页面大小一致
        await page.setViewport({"width": 1366, "height": 768})
        # 访问主页
        await page.goto("https://passport.jd.com/new/login.aspx?")


        # 模拟输入用户名和密码,输入每个字符的间隔时间delay ms
        await page.type("#loginname", '324534534@qq.com', {
            "delay": random.randint(30, 60)
        })
        await page.type("#nloginpwd", '345653332', {
            "delay": random.randint(30, 60)
        })

        # page.waitFor 通用等待方式，如果是数字，则表示等待具体时间（毫秒）: 等待2秒
        await page.waitFor(2000)
        await page.click("div.login-btn")
        await page.waitFor(2000)
        # page.Jeval（selector，pageFunction）#定位元素，并调用js函数去执行
        #=>表示js的箭头函数：el = function(el){return el.src}
        img_src = await page.Jeval(".JDJRV-bigimg > img", "el=>el.src")
        temp_src = await page.Jeval(".JDJRV-smallimg > img", "el=>el.src")

        request.urlretrieve(img_src, "background.png")
        request.urlretrieve(temp_src, "gap.png")

        # 获取gap的距离
        distance = await get_track()

            # # Pyppeteer 三种解析方式
            # Page.querySelector()  # 选择器
            # Page.querySelectorAll()
            # Page.xpath()  # xpath  表达式
            # # 简写方式为：
            # Page.J(), Page.JJ(), and Page.Jx()

        #定位到滑动按钮标签
        el = await page.J("div.JDJRV-slide-btn")
        # 获取元素的边界框，包含x,y坐标
        box = await el.boundingBox()
        #box={'x': 86, 'y': 34, 'width': 55.0, 'height': 55.0}
        #将鼠标悬停/一定到指定标签位置
        await page.hover("div.JDJRV-slide-btn")
        #按下鼠标
        await page.mouse.down()
        #模拟人的行为进行滑动
        # steps 是指分成几步来完成，steps越大，滑动速度越慢
        #move(x,y)表示将鼠标移动到xy坐标位置
        #random.uniform生成指定范围的随机浮点数
        await page.mouse.move(box["x"] + distance + random.uniform(20, 40),
                              box["y"],
                              {"steps": 100})
        await page.waitFor(1000)

        await page.mouse.up()
        await page.waitFor(2000)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    def parse(task):
        page_text = task.result()
        tree = etree.HTML(page_text)
        div_list = tree.xpath('//div[@class="data_row news_article clearfix "]')
        for div in div_list:
            title = div.xpath('.//div[@class="news_title"]/h3/a/text()')[0]
            print('wangyi:', title)


    tasks = []
    task1 = asyncio.ensure_future(main())
    task1.add_done_callback(parse)
    tasks.append(task1)
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))


scrapy（爬虫多线程的异步框架）
简介
什么是框架？
    所谓的框架，其实说白了就是一个【项目的半成品】，该项目的半成品需要被集成了各种功能且具有较强的通用性。
    Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架，非常出名，非常强悍。所谓的框架就是一个已经被集成了各种功能（高性能异步下载，队列，分布式，解析，持久化等）的具有很强通用性的项目模板。对于框架的学习，重点是要学习其框架的特性、各个功能的用法即可。
初期如何学习框架？
    只需要学习框架集成好的各种功能的用法即可！前期切勿钻研框架的源码！

安装
    Linux/mac系统：
        pip install scrapy
    Windows系统：
        pip install scrapy
    1

基本使用
    创建项目
        scrapy startproject firstBlood项目名称
        2
        项目的目录结构：
            firstBlood   # 项目所在文件夹, 建议用pycharm打开该文件夹
                ├── firstBlood  		# 项目跟目录
                │   ├── __init__.py
                │   ├── items.py  		# 封装数据的格式
                │   ├── middlewares.py  # 所有中间件
                │   ├── pipelines.py	# 所有的管道
                │   ├── settings.py		# 爬虫配置信息
                │   └── spiders			# 爬虫文件夹, 稍后里面会写入爬虫代码
                │       └── __init__.py
                └── scrapy.cfg			# scrapy项目配置信息,不要删它,别动它,善待它.

    创建爬虫爬虫文件：
        cd project_name（进入项目目录）
        scrapy genspider 爬虫文件的名称（自定义一个名字即可） 起始url (随便写一个网址即可)
            （例如：scrapy genspider first www.xxx.com）
            3
        创建成功后，会在爬虫文件夹下生成一个py的爬虫文件
        4
    编写爬虫文件
        理解爬虫文件的不同组成部分
            import scrapy

            class FirstSpider(scrapy.Spider):
                #爬虫名称：爬虫文件唯一标识：可以使用该变量的值来定位到唯一的一个爬虫文件
                name = 'first' #无需改动
                #允许的域名：scrapy只可以发起百度域名下的网络请求
                # allowed_domains = ['www.baidu.com']
                #起始的url列表：列表中存放的url可以被scrapy发起get请求
                start_urls = ['https://www.baidu.com/','https://www.sogou.com']

                #专门用作于数据解析
                #参数response：就是请求之后对应的响应对象
                #parse的调用次数，取决于start_urls列表元素的个数
                def parse(self, response):
                    print('响应对象为：',response)

    配置文件修改:settings.py
        7
        不遵从robots协议：ROBOTSTXT_OBEY = False
        指定输出日志的类型：LOG_LEVEL = 'ERROR'
        指定UA：USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'


    运行项目
        scrapy crawl 爬虫名称 ：该种执行形式会显示执行的日志信息（推荐）
        自己遇到一个坑：
        AttributeError: ‘AsyncioSelectorReactor‘ object has no attribute ‘_handleSignals‘
        5
        6

    数据解析
        注意，如果终端还在第一个项目的文件夹中，则需要在终端中执行cd ../返回到上级目录，在去新建另一个项目。
        新建数据解析项目：
            创建工程：scrapy startproject 项目名称
            cd 项目名称
            创建爬虫文件：scrapy genspider 爬虫文件名 www.xxx.com
        配置文件的修改：settings.py
            不遵从robots协议：ROBOTSTXT_OBEY = False
            指定输出日志的类型：LOG_LEVEL = 'ERROR'
            指定UA：USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'
        8
        编写爬虫文件：spiders/blood.py
        import scrapy


        class BloodSpider(scrapy.Spider):
            #爬虫文件的唯一标识
            name = 'blood'
            #允许的域名
            # allowed_domains = ['www.baidu.com']
            #起始的url列表（重要）：列表内部的url都会被框架进行异步的请求发送
            start_urls = ['https://www.xiachufang.com/category/40076/']

            #数据解析：parse调用的次数取决于start_urls列表元素的个数
            def parse(self, response): #response参数就表示响应对象
                #如何实现数据解析：xpath
                li_list = response.xpath('/html/body/div[4]/div/div/div[1]/div[1]/div/div[2]/div[2]/ul/li')
                for li in li_list:
                    #xpath最终会返回的是Selector对象，我们想要的解析的数据是存储在该对象的data属性中(extract可以实现该功能)
                    # title = li.xpath('./div/div/p[1]/a/text()')[0].extract() #一般不用

                    #extract_first可以将xpath返回列表中的第一个Selector对象中的data属性值获取
                    # title = li.xpath('./div/div/p[1]/a/text()').extract_first()

                    #extract可以将xpath返回列表中的每一个Selector对象中的data属性值获取
                    title = li.xpath('./div/div/p[1]/a/text()').extract()

                    #如果xpath返回的列表元素只有一个则使用extract_first，否则使用extract






"""
