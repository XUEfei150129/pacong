"""
并行和并发
        并行表示计算机可以在同一时刻处理多个任务
        并发就是伪并行，基于时间片轮转法在多个任务之间快速切换执行。
    并行和并发都是在强调计算机是具有处理多个任务的能力。

同步和异步
    基于并行或者并发的模式处理任务的时候，任务中如果出现了阻塞操作，就可以选择使用同步或者异步的方式进行阻塞操作的处理。
    同步处理：一个任务的不同执行步骤一定是一步一步进行。
    异步处理：在执行任务的过程中，遇到了阻塞操作可以适当交出cpu的使用权，然后让其去执行其他的执行步骤。
    进程和线程，就是实现异步的实现手段。

最重要最核心的一点：异步机制可以增加程序的执行效率。多进程、多线程和协程就是用来实现异步机制。


协程（重要！）
协程（微线程）可以实现在单进程或者单线程的模式下，大幅度提升程序的运行效率！
    假设我们有一个需求：从一个URL列表中下载多个网页内容，假设下载一个网页内容需要耗时2秒。
    在传统的多线程或多进程模型中，我们会为每个URL创建一个线程或进程来进行异步的下载操作。
    但是这样做会有一个问题：
        计算机中肯定不会只有下载URL的这几个进程/线程，还会有其他的进程/线程（Pycharm、音乐播放器、微信、网盘等）。
        将每一个下载网页的操作封装成一个进程/线程的目的就是为了实现异步的网页数据下载，也就是当一个下载网页的操作出现阻塞后，可以不必等待阻塞操作结束后就可以让计算机去下载其他网页内容（CPU切换到其他网页下载的进程/线程中）。
        但是，计算机中启动的进程/线程那么多，你确定每次CPU进行进程/线程切换，都会切换到网页下载的进程/线程中吗？答案是不一定，因为这个进程/线程切换是由操作系统实现的，无法人为干涉。那么，这些网页下载任务的执行的效率就降低下来了。因此，可以使用协程来解决该问题！
    协程处理多个网页内容下载任务：
        具体来说，当使用协程时，程序员可以手动控制任务的切换和调度，而不是依赖于操作系统的线程或进程调度器。在协程中，任务的切换是通过挂起（暂停）当前任务，并将控制权交给下一个任务来实现的。这种任务切换是在用户空间中进行的，不需要向操作系统发出系统调用。
        因此使用协程后可以实现让计算机尽可能多的分配CPU给我们，这样也就达到了提升程序执行效率的目的。
    协程的优点：
        轻量级：协程是轻量级的，占用的系统资源少，创建和销毁的开销小。相比于线程和进程，协程的切换更加高效。
        可控性：协程的调度和切换是由程序员自己控制的，不需要依赖操作系统进行调度，这使得编程模型更加灵活。可以根据实际需求自定义任务的调度逻辑，实现更加精细的任务切换。
因此，有了协程后，在单进程或者单线程的模式下，就可以大幅度提升程序的运行效率了！总而言之，就是想尽一切办法留住CPU在我们自己的程序中，从而提升整个程序的执行效率！

asyncio模块
    在python3.6之后新增了asyncio模块，可以帮我们检测阻塞（只能是网络阻塞），实现应用程序级别的切换。

    接下来让我们来了解下协程的实现，从 Python 3.6 开始，Python 中加入了协程的概念，但这个版本的协程还是以生成器对象为基础的，在 Python 3.6 则增加了 asyncio，使得协程的实现更加方便。首先我们需要了解下面几个概念：

    特殊函数：
        在函数定义前添加一个async关键字，则该函数就变为了一个特殊的函数！
        特殊函数的特殊之处是什么？
            1.特殊函数被调用后，函数内部的程序语句（函数体）没有被立即执行
            2.特殊函数被调用后，会返回一个协程对象
    协程：
        协程对象，特殊函数调用后就可以返回/创建了一个协程对象。
        协程对象 == 特殊的函数 == 一组指定形式的操作
        协程对象 == 一组指定形式的操作
    任务对象：
        任务对象就是一个高级的协程对象。高级之处，后面讲，不着急！
        任务对象 == 协程对象 == 一组指定形式的操作
        任务对象 == 一组指定形式的操作
    事件循环：
        事件循环对象（Event Loop）,可以将其当做是一个容器，该容器是用来装载任务对象的。所以说，让创建好了一个或多个任务对象后，下一步就需要将任务对象全部装载在事件循环对象中。
        思考：为什么需要将任务对象装载在事件循环对象？
            当将任务对象装载在事件循环中后，启动事件循环对象，则其内部装载的任务对象对应的相关操作就会被立即执行。
    代码：
        import asyncio
        import time


        # 特殊的函数
        async def get_request(url):
            print('正在请求的网址是:', url)
            time.sleep(2)
            print('请求网址结束！')
            return 123


        # 创建了一个协程对象（返回值是一个协程对象）
        c = get_request('www.1.com')
        # 创建任务对象
        task = asyncio.ensure_future(c)
        # 创建事件循环对象
        loop = asyncio.get_event_loop()
        # 将任务对象装载在loop对象中且启动事件循环对象
        loop.run_until_complete(task)

        结果：
            正在请求的网址是: www.1.com
            请求网址结束！

    要想拿到函数实际的返回值（123），需要给任务对象绑定返回值来实现
    任务对象对比协程对象的高级之处重点在于：
        可以给任务对象绑定一个回调函数！
        回调函数有什么作用？
            回调函数就是回头调用的函数，因此要这么理解，当任务对象被执行结束后，会立即调用给任务对象绑定的这个回调函数！


    如何获取特殊函数的返回值（任务对象的回调函数实现）
    代码：
        import asyncio
        import time

        async def get_request(url):
            print('正在请求的网址是:',url)
            time.sleep(2)
            print('请求网址结束！')
            return 123

        #如何获取特殊函数内部的返回值（任务对象回调函数来实现的）
        c = get_request('www.1.com')
        task = asyncio.ensure_future(c)
        #给任务对象绑定一个回调函数（回头调用的函数）,该函数一定是在任务对象被执行完毕后再调用的函数
        def task_callback(t): #必须有且仅有一个参数
            #函数的参数t就是回调函数的调用者task任务对象本身
            ret = t.result() #任务对象调用result()就可以返回特殊函数的内部return后的结果值
            print('我是回调函数，我被执行了，t.result()返回的结果是:',ret)
        #给task任务对象绑定了一个叫做task_callback的回调函数
        task.add_done_callback(task_callback)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(task)

    结果：
        正在请求的网址是: www.1.com
        请求网址结束！
        我是回调函数，我被执行了，t.result()返回的结果是: 123

多任务的协程
    代码：
        import asyncio
        import time

        start = time.time()
        urls = [
            'www.1.com', 'www.2.com', 'www.3.com'
        ]


        async def get_request(url):
            print('正在请求：', url)
            time.sleep(2)
            print('请求结束:', url)


        # 有了三个任务对象和一个事件循环对象
        if __name__ == '__main__':
            tasks = []
            for url in urls:
                c = get_request(url)
                task = asyncio.ensure_future(c)
                tasks.append(task)
            # 将三个任务对象，添加到一个事件循环对象中
            # 下面这个是一个容器的性质，放在循环外面
            loop = asyncio.get_event_loop()
            # wait函数用来接收一个任务列表：wait函数就可以给任务列表中每一个任务对象赋予一个可被挂起的权限
            # 一个任务被挂起，就代表当前任务对象交出了cpu的使用权
            loop.run_until_complete(asyncio.wait(tasks))

            print('总耗时:', time.time() - start)
    结果：
        正在请求： www.1.com
        请求结束: www.1.com
        正在请求： www.2.com
        请求结束: www.2.com
        正在请求： www.3.com
        请求结束: www.3.com
        总耗时: 6.041329622268677

    出现两个问题：
        1.没有实现异步效果
        2.wait()是什么意思？

    主要原因是因为特殊函数内部出现了不支持异步模块的代码time.sleep(2)，否则会中断整个异步效果
    将time.sleep(2)换成asyncio.sleep(2)

    实现异步效果代码：
        import asyncio
        import time

        start = time.time()

        async def get_request(url):
            #特殊函数内部不可以出现不支持异步模块的代码，否则会中断整个异步效果
            print('正在请求的网址是:',url)
            #没有加await关键字之前：每一个任务中的阻塞操作并没有被执行
            #await关键字：必须要加在每一个任务的阻塞操作前，作用就是强调执行任务中的阻塞操作
            #await是用来手动控制任务的挂起操作。
            await asyncio.sleep(2)
            print('请求网址结束！')
            return 123

        urls = [
            'www.1.com','www.2.com','www.3.com'
        ]

        tasks = [] #定义一个任务列表
        for url in urls: #循环3次
            #创建了3个协程
            c = get_request(url)
            #创建3个任务对象
            task = asyncio.ensure_future(c)
            tasks.append(task) #将创建好的3个任务对象依次存放到了tasks这个任务列表中

        loop = asyncio.get_event_loop()
        #将任务列表tasks添加到loop容器中
        #wait()函数：用于接收一个任务列表，wait函数就可以给任务列表中每一个任务对象赋予一个可被挂起的权限
        #一个任务被挂起，就表示当前任务对象交出了cpu的使用权
        loop.run_until_complete(asyncio.wait(tasks))
        print('总耗时:',time.time()-start)

        结果：
            正在请求的网址是: www.1.com
            正在请求的网址是: www.2.com
            正在请求的网址是: www.3.com
            请求网址结束！
            请求网址结束！
            请求网址结束！
            总耗时: 2.0103352069854736

    wait()函数：
        给任务列表中的每一个任务对象赋予一个可被挂起的权限！当cpu执行的任务对象遇到阻塞操作的时候，当前任务对象就会被挂起，则cup就可以执行其他任务对象，提高整体程序运行的效率！
        挂起任务对象：让当前正在被执行的任务对象交出cpu的使用权，cup就可以被其他任务组抢占和使用，从而可以执行其他任务组。
        注意：特殊函数内部，不可以出现不支持异步模块的代码，否则会中断整个异步效果！
        await关键字：挂起发生阻塞操作的任务对象。在任务对象表示的操作中，凡是阻塞操作的前面都必须加上await关键字进行修饰！（人为主动检测阻塞环节）

        完整的实现了，多任务的异步协程操作

        代码：
            import asyncio
            import time

            start = time.time()


            async def get_request(url):
                # 特殊函数内部不可以出现不支持异步模块的代码，否则会中断整个异步效果
                print('正在请求的网址是:', url)
                # 没有加await关键字之前：每一个任务中的阻塞操作并没有被执行
                # await关键字：必须要加在每一个任务的阻塞操作前，作用就是强调执行任务中的阻塞操作
                # await是用来手动控制任务的挂起操作。
                await asyncio.sleep(2)
                print('请求网址结束！')
                return 123


            urls = [
                'www.1.com', 'www.2.com', 'www.3.com'
            ]

            tasks = []  # 定义一个任务列表
            for url in urls:  # 循环3次
                # 创建了3个协程
                c = get_request(url)
                # 创建3个任务对象
                task = asyncio.ensure_future(c)
                tasks.append(task)  # 将创建好的3个任务对象依次存放到了tasks这个任务列表中

            loop = asyncio.get_event_loop()
            # 将任务列表tasks添加到loop容器中
            # wait()函数：用于接收一个任务列表，wait函数就可以给任务列表中每一个任务对象赋予一个可被挂起的权限
            # 一个任务被挂起，就表示当前任务对象交出了cpu的使用权
            loop.run_until_complete(asyncio.wait(tasks))
            print('总耗时:', time.time() - start)

        结果：
            正在请求的网址是: www.1.com
            正在请求的网址是: www.2.com
            正在请求的网址是: www.3.com
            请求网址结束！
            请求网址结束！
            请求网址结束！
            总耗时: 2.006432056427002


    不可以出现不支持异步模块的代码
        不可以使用requests，requests是不支持异步，更换一个支持异步的网络请求的模块（aiohttp）
        不报错，但是不能实现异步效果
        环境安装：pip install aiohttp
        代码：
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

    原则是这样的，先写大致架构，后面补充细节
        1、先写大致架构
            with aiohttp.ClientSession() as sess:
               #基于请求对象发起请求
               #此处的get是发起get请求，常用参数：url,headers,params,proxy
               #post方法发起post请求，常用参数：url,headers,data,proxy
               #发现处理代理的参数和requests不一样（注意），此处处理代理使用proxy='http://ip:port'
                with sess.get(url=url) as response:
                   page_text = response.text()
                   #text():获取字符串形式的响应数据
                   #read()：获取二进制形式的响应数据
                   return page_text

       2.在第一步的基础上补充细节
            在每一个with前加上async关键字
            在阻塞操作前加上await关键字
                async def get_request(url):
                    #requests是不支持异步的模块
                    # response = await requests.get(url=url)
                    # page_text = response.text
                    #创建请求对象（sess）
                    async with aiohttp.ClientSession() as sess:
                        #基于请求对象发起请求
                        #此处的get是发起get请求，常用参数：url,headers,params,proxy
                        #post方法发起post请求，常用参数：url,headers,data,proxy
                        #发现处理代理的参数和requests不一样（注意），此处处理代理使用proxy='http://ip:port'
                        async with await sess.get(url=url) as response:
                            page_text = await response.text()
                            #text():获取字符串形式的响应数据
                            #read()：获取二进制形式的响应数据
                            return page_text
"""
