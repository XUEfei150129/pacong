"""
M3U8流视频数据爬虫（不重要）
    HLS技术介绍
        现在大部分视频客户端都采用HTTP Live Streaming（HLS，Apple为了提高流播效率开发的技术），而不是直接播放MP4等视频文件。HLS技术的特点是将流媒体切分为若干【TS片段】（比如几秒一段），然后通过一个【M3U8列表文件】将这些TS片段批量下载供客户端播放器实现实时流式播放。因此，在爬取HLS的流媒体文件的思路一般是先【下载M3U8文件】并分析其中内容，然后在批量下载文件中定义的【TS片段】，最后将其【组合】成mp4文件或者直接保存TS片段。
    M3U8文件详解
        如果想要爬取HLS技术下的资源数据，首先要对M3U8的数据结构和字段定义非常了解。M3U8是一个扩展文件格式，由M3U扩展而来。那么什么是M3U呢？
    M3U文件
        M3U这种文件格式，本质上说不是音频视频文件，它是音频视频文件的列表文件，是纯文本文件。
        M3U这种文件被获取后，播放软件并不是播放它，而是根据它的记录找到媒体的网络地址进行在线播放。也就是说，M3U格式的文件只是存储多媒体播放列表，并提供了一个指向其他位置的音频视频文件的索引，播放的是那些被指向的文件。
        为了能够更好的理解M3U的概念，我们先简单做一个M3U文件（myTest.m3u）。在电脑中随便找几个MP3，MP4文件依次输入这些文件的路径，myTest.m3u文件内容如下
            E:\Users\m3u8\刘德华 - 无间道.mp4
            E:\Users\m3u8\那英 - 默.mp3
            E:\Users\m3u8\周杰伦 - 不能说的秘密.mp4
            E:\Users\m3u8\花粥 - 二十岁的某一天.mp3
            E:\Users\m3u8\周深 - 大鱼.mp4
    M3U8文件
        M3U8也是一种M3U的扩展格式（高级的M3U，所以也属于M3U）。
        M3U8示例：**大家会看到在该文件中有大量的ts文件的链接地址，这个就是我们之前描述的真正的视频文件。其中任何一个ts文件都是一小段视频，可以单独播放。我们做视频爬虫的目标就是把这些ts文件都爬取下来。
            #EXTM3U
            #EXT-X-VERSION:3
            #EXT-X-TARGETDURATION:6
            #EXT-X-PLAYLIST-TYPE:VOD
            #EXT-X-MEDIA-SEQUENCE:0
            #EXTINF:3.127,
            /20230512/RzGw5hDB/1500kb/hls/YZefAiEF.ts
            #EXTINF:3.127,
            /20230512/RzGw5hDB/1500kb/hls/FsliUCL6.ts
            #EXTINF:3.127,
            /20230512/RzGw5hDB/1500kb/hls/DD7c47bz.ts
            #EXT-X-ENDLIST
    实战
        需求：
            https://www.mjtt5.tv/
        具体操作
            进入视频播放页
            点击播放按钮，定位ts数据包，从中提取ts片段的url，探究url的规律
            打开抓包工具，刷新页面，全局搜索m3u8定位到找到m3u8文件
            解析m3u8文件提取文件中ts片段链接
        同步操作代码

            import requests
            from urllib.parse import urljoin
            import re
            import os
            dirName = 'tsLib'
            if not os.path.exists(dirName):
                os.mkdir(dirName)

            headers  = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }
            #m3u8地址
            url = "https://cdn13.tvtvgood.com/202310/20/c1959422deee/playlist.m3u8?token=d5i9GCr3ljqGsSf48-aG2w&expires=1698221543"
            page_text = requests.get(url=url,headers=headers).text
            page_text = page_text.strip()

            #解析出每一个ts切片的地址
            ts_url_list = []
            for line in page_text.split('\n'):
                if not line.startswith('#'):
                    ts_url = line
                    #不同ts下载地址
                    ts_url = 'https://cdn13.tvtvgood.com/202310/20/c1959422deee/'+ts_url
                    ts_url_list.append(ts_url)

            print(ts_url_list)
            #请求到每一个ts切片的数据
            for url in ts_url_list:
                #获取ts片段的数据
                ts_data = requests.get(url=url,headers=headers).content
                ts_name = url.split('/')[-1]
                ts_path = dirName+'/'+ts_name
                with open(ts_path,'wb') as fp:
                    #需要将解密后的数据写入文件进行保存
                    fp.write(ts_data)
                print(ts_name,'下载保存成功！')

            # ts文件的合并，最好网上找专业的工具进行合并，自己手动合并会经常出问题

        异步操作代码：协程
            #https://cdn8.tvtvgood.com/202206/21/6abfb3237d01/playlist8.ts
            #https://cdn8.tvtvgood.com/202206/21/6abfb3237d01/playlist7.ts
            import requests
            import os
            import asyncio
            import aiohttp
            from threading import Thread
            dirName = 'tsLib'
            if not os.path.exists(dirName):
                os.mkdir(dirName)

            headers  = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }
            #m3u8文件的url
            m3u8_file_url = 'https://cdn8.tvtvgood.com/202206/21/6abfb3237d01/playlist.m3u8?token=9vVIuesP2MAZ4G1V6y6DnA&expires=1698927688'
            m3u8_text = requests.get(url=m3u8_file_url,headers=headers).text

            ts_url_list = [] #存储解析出来的每一个ts片段的url
            for line in m3u8_text.split('\n'):
                if not line.startswith('#'):
                    ts_url = line
                    ts_url = 'https://cdn8.tvtvgood.com/202206/21/6abfb3237d01/'+ts_url
                    ts_url_list.append(ts_url)

            #基于协程实现异步的ts片段的请求
            async def get_reqeust(url):#参数url就是ts片段的请求url
                async with aiohttp.ClientSession() as req:
                    async with await req.get(url=url,headers=headers) as response:
                        ts_data = await response.read()
                        dic = {'ts_data':ts_data,'ts_title':url.split('/')[-1]}
                        return dic

            def save_ts_data(t):
                dic = t.result()
                ts_data = dic['ts_data']
                ts_title = dic['ts_title']
                ts_path = dirName + '/' + ts_title
                with open(ts_path,'wb') as fp:
                    fp.write(ts_data)
                print(ts_title,'：保存下载成功！')


            tasks = []
            for url in ts_url_list:
                c = get_reqeust(url)
                task = asyncio.ensure_future(c)
                task.add_done_callback(save_ts_data)
                tasks.append(task)

            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))


        使用协程：实现一定得有一个url列表，遍历该列表进行多协程的创建
        使用多个loop的场景：两种数据资源下载，需要实现有两个url列表
        问题：两个loop之间的关系是异步的吗？
        注意：千万别搞loop的嵌套。

        特殊的方式：创建两个线程，两个线程中封装处理两个loop。

        线程池的实现方案：
            #https://cdn8.tvtvgood.com/202206/21/6abfb3237d01/playlist8.ts
            #https://cdn8.tvtvgood.com/202206/21/6abfb3237d01/playlist7.ts
            import requests
            import os
            from threading import Thread
            from multiprocessing.dummy import Pool


            dirName = 'tsLib'
            if not os.path.exists(dirName):
                os.mkdir(dirName)

            headers  = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
                'Connection':'closed'
            }
            #m3u8文件的url
            m3u8_file_url = 'https://cdn8.tvtvgood.com/202206/21/6abfb3237d01/playlist.m3u8?token=9vVIuesP2MAZ4G1V6y6DnA&expires=1698927688'
            m3u8_text = requests.get(url=m3u8_file_url,headers=headers).text

            ts_url_list = [] #存储解析出来的每一个ts片段的url
            for line in m3u8_text.split('\n'):
                if not line.startswith('#'):
                    ts_url = line
                    ts_url = 'https://cdn8.tvtvgood.com/202206/21/6abfb3237d01/'+ts_url
                    ts_url_list.append(ts_url)

            def get_reqeust(url):#参数url就是ts片段的请求url
                ts_data = requests.get(url=url,headers=headers,verify=False).content
                ts_path = dirName + '/' + url.split('/')[-1]
                with open(ts_path,'wb') as fp:
                    fp.write(ts_data)
                print(ts_path,':保存下载成功！')

            #HTTPSConnectionPool异常原因：
                #网络请求的并发量太大（减少并发or在headers中添加一个Connection:closed）

            pool = Pool(100)
            pool.map(get_reqeust,ts_url_list)


selenium
简介
    selenium （重点：page_source实现可见即可得，验证码的模拟登录）
    是一种浏览器自动化的工具，所谓的自动化是指，我们可以通过代码的形式制定一系列的行为动作，然后执行代码，这些动作就会同步触发在浏览器中。

环境安装
    下载安装selenium：
        pip install selenium
    下载浏览器驱动程序：
        http://chromedriver.storage.googleapis.com/index.html
        win64选win32即可

效果展示
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.common.by import By

    # 后面是你的浏览器驱动位置，记得前面加r'','r'是防止字符转义的
    driver = webdriver.Chrome(executable_path='./chromedriver')
    # 用get打开百度页面
    driver.get("http://www.baidu.com")

    # 查找页面的“设置”选项，并进行点击
    # driver.find_element_by_xpath('//*[@id="s-usersetting-top"]').click()
    driver.find_element(By.XPATH,'//*[@id="s-usersetting-top"]').click()


    sleep(1)
    # # 打开设置后找到“搜索设置”选项，设置为每页显示50条
    # driver.find_elements_by_link_text('搜索设置')[0].click()
    driver.find_element(By.LINK_TEXT,'搜索设置').click()
    sleep(1)

    # 选中每页显示50条
    m = driver.find_element_by_xpath('//*[@id="nr_3"]').click()
    sleep(1)

    # 点击保存设置
    driver.find_element_by_xpath('//*[@id="se-setting-7"]/a[2]').click()
    sleep(1)

    # 处理弹出的警告页面   确定accept() 和 取消dismiss()
    driver.switch_to.alert.accept()
    sleep(1)
    # 找到百度的输入框，并输入 美女
    driver.find_element_by_id('kw').send_keys('美女')
    sleep(1)
    # 点击搜索按钮
    driver.find_element_by_id('su').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="1"]/div/h3/a').click()
    sleep(3)

    # 关闭浏览器
    driver.quit()

浏览器创建
    Selenium支持非常多的浏览器，如Chrome、Firefox、Edge等.另外，也支持无界面浏览器。

    from selenium import webdriver

    browser = webdriver.Chrome()
    browser = webdriver.Firefox()
    browser = webdriver.Edge()
    browser = webdriver.PhantomJS()
    browser = webdriver.Safari()


元素定位
    webdriver 提供了一系列的元素定位方法，常用的有以下几种：

    find_element_by_id()
    find_element_by_name()
    find_element_by_class_name()
    find_element_by_tag_name()
    find_element_by_link_text()
    find_element_by_xpath()
    find_element_by_css_selector()

    或者
    from selenium.webdriver.common.by import By

    driver.find_element(By.xxx,value) #返回定位到的标签

    driver.find_elements(By.xx, value)  #返回列表

节点交互
    Selenium可以驱动浏览器来执行一些操作，也就是说可以让浏览器模拟执行一些动作。比较常见的用法有：输入文字时用send_keys()方法，清空文字时用clear()方法，点击按钮时用click()方法。

执行js
    对于某些操作，Selenium API并没有提供。比如，下拉进度条，它可以直接模拟运行JavaScript，此时使用execute_script()方法即可实现。
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.common.by import By
    #1.创建一个浏览器对象,executable_path指定当前浏览器的驱动程序
    #注意：我当前是mac系统，驱动程序也是mac版本的，如果是window系统注意更换驱动
    bro = webdriver.Chrome(executable_path='./chromedriver')
    #2.浏览器的请求发送
    bro.get('https://www.jd.com/')
    #3.标签定位:调用find系列的函数进行标签定位
    # search_box = bro.find_element_by_xpath('//*[@id="key"]')
    search_box = bro.find_element(By.XPATH,'//*[@id="key"]')
    #4.节点交互
    search_box.send_keys('mac pro m1')#向指定标签中录入内容
    sleep(2)
    # btn = bro.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
    btn = bro.find_element(By.XPATH,'//*[@id="search"]/div/div[2]/button')

    btn.click() #点击按钮
    sleep(2)
    #js注入
    bro.execute_script('document.documentElement.scrollTo(0,2000)')
    sleep(5)
    #关闭浏览器
    bro.quit()

获取页面源码数据(重要)
    通过page_source属性可以获取网页的源代码，接着就可以使用解析库（如正则表达式、Beautiful Soup、pyquery等）来提取信息了。
    获取动态加载数据
        实现可见即可得
        爬取豆瓣电影中动态加载的电影详情数据

        from time import sleep
        from selenium import webdriver
        from lxml import etree
        bro = webdriver.Chrome(executable_path='./chromedriver')
        bro.get('https://movie.douban.com/typerank?type_name=%E6%82%AC%E7%96%91&type=10&interval_id=100:90&action=')
        sleep(2)
        bro.execute_script('document.documentElement.scrollTo(0,2000)')
        sleep(2)
        #获取页面源码数据
        page_text = bro.page_source
        #数据解析：解析页面源码数据中动态加载的电影详情数据
        tree = etree.HTML(page_text)
        ret = tree.xpath('//*[@id="content"]/div/div[1]/div[6]/div/div/div/div[1]/span[1]/a/text()')
        print(ret)
        bro.quit()

动作链
    在上面的实例中，一些交互动作都是针对某个节点执行的。比如，对于输入框，我们就调用它的输入文字和清空文字方法；对于按钮，就调用它的点击方法。其实，还有另外一些操作，它们没有特定的执行对象，比如鼠标拖曳、键盘按键等，这些动作用另一种方式来执行，那就是动作链。
        from selenium.webdriver import ActionChains
        from selenium import webdriver
        from time import sleep
        bro = webdriver.Chrome(executable_path='./chromedriver')
        bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
        sleep(1)
        #注意：如果定位的标签是存在于iframe表示的子页面中，则常规的标签定位报错
        #处理：使用如下指定操作
        bro.switch_to.frame('iframeResult')
        div_tag = bro.find_element_by_id('draggable')

        #实例化一个动作链对象且将该对象绑定到指定的浏览器中
        action = ActionChains(bro)
        action.click_and_hold(div_tag) #对指定标签实现点击且长按操作
        for i in range(5):
            action.move_by_offset(10,10).perform() #perform让动作链立即执行
            sleep(0.5)
        sleep(3)
        bro.quit()
页面等待
为什么需要等待 如果网站采用了动态html技术，那么页面上的部分元素出现/加载的时间便不能确定，这个时候就可以设置一个等待时间，强制等待指定时间，等待结束之后进行元素定位，如果还是无法定位到则报错

    页面等待的三种方法
    强制等待
        import time
        time.sleep(n)      # 阻塞等待设定的秒数之后再继续往下执行

    显式等待
        也称为智能等待，针对指定元素定位指定等待时间，在指定时间范围内进行元素查找，找到元素则直接返回，如果在超时还没有找到元素，则抛出异常，显示等待是 selenium 当中比较灵活的一种等待方式，他的实现原理其实是通过 while 循环不停的尝试需要进行的操作。

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

         # 每隔 0.5s 检查一次(默认就是 0.5s), 最多等待 10 秒,否则报错。如果定位到元素则直接结束等待，如果在10秒结束之后仍未定位到元素则报错
         wait = WebDriverWait(chrome, 10,0.5)
         wait.until(EC.presence_of_element_located((By.ID, 'J_goodsList')))
     隐式等待：
        设置超时时间为10秒，使用了implicitlyWait后，如果第一次没有找到元素，会在10秒之内不断循环去找元素，如果超过10秒还没有找到，则抛出异常，隐式等待比较智能
        driver.implicitly_wait(10)    # 在指定的n秒内每隔一段时间尝试定位元素，如果n秒结束还未被定位出来则报错

滑动验证
    免费的滑动验证

        import time
        from selenium import webdriver
        from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
        import cv2 #pip install opencv-python

        from urllib import request
        from selenium.webdriver.common.action_chains import ActionChains


        #获取要滑动的距离
        def get_distance():
            #滑动验证码的整体背景图片
            background = cv2.imread("background.png", 0)
            #缺口图片
            gap = cv2.imread("gap.png", 0)

            res = cv2.matchTemplate(background, gap, cv2.TM_CCOEFF_NORMED)
            value = cv2.minMaxLoc(res)[2][0]
            print(value)
            #单位换算
            return value * 278 / 360


        def main():
            chrome = webdriver.Chrome(executable_path='./chromedriver')
            chrome.implicitly_wait(5)

            chrome.get('https://passport.jd.com/new/login.aspx?')

            login = chrome.find_element(By.ID, 'pwd-login')
            login.click()

            loginname = chrome.find_element(By.ID, 'loginname')
            loginname.send_keys("123@qq.com")

            nloginpwd = chrome.find_element(By.ID, 'nloginpwd')
            nloginpwd.send_keys("987654321")

            loginBtn = chrome.find_element(By.CLASS_NAME, 'login-btn')
            loginBtn.click()
            #带缺口的大图
            img_src = chrome.find_element(By.XPATH, '//*[@class="JDJRV-bigimg"]/img').get_attribute("src")
            #缺口图片
            temp_src = chrome.find_element(By.XPATH, '//*[@class="JDJRV-smallimg"]/img').get_attribute("src")
            #两张图片保存起来
            request.urlretrieve(img_src, "background.png")
            request.urlretrieve(temp_src, "gap.png")

            distance = int(get_distance())
            print("distance:", distance)

            print('第一步,点击滑动按钮')
            element = chrome.find_element(By.CLASS_NAME, 'JDJRV-slide-btn')
            ActionChains(chrome).click_and_hold(on_element=element).perform()  # 点击鼠标左键，按住不放

            ActionChains(chrome).move_by_offset(xoffset=distance, yoffset=0).perform()
            ActionChains(chrome).release(on_element=element).perform()

            time.sleep(2)
        if __name__ == '__main__':
            main()

        验证没有通过原因：
            没有模拟人的行为动作
            检测出是selenium

    带验证码的模拟登录
        登录bilibili
            https://passport.bilibili.com/login?from_spm_id=333.851.top_bar.login_window
        识别验证码模块封装：
            import base64
            import json
            import requests
            # 一、图片文字类型(默认 3 数英混合)：
            # 1 : 纯数字
            # 1001：纯数字2
            # 2 : 纯英文
            # 1002：纯英文2
            # 3 : 数英混合
            # 1003：数英混合2
            #  4 : 闪动GIF
            # 7 : 无感学习(独家)
            # 11 : 计算题
            # 1005:  快速计算题
            # 16 : 汉字
            # 32 : 通用文字识别(证件、单据)
            # 66:  问答题
            # 49 :recaptcha图片识别
            # 二、图片旋转角度类型：
            # 29 :  旋转类型
            #
            # 三、图片坐标点选类型：
            # 19 :  1个坐标
            # 20 :  3个坐标
            # 21 :  3 ~ 5个坐标
            # 22 :  5 ~ 8个坐标
            # 27 :  1 ~ 4个坐标
            # 48 : 轨迹类型
            #
            # 四、缺口识别
            # 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
            # 33 : 单缺口识别（返回X轴坐标 只需要1张图）
            # 五、拼图识别
            # 53：拼图识别
            #函数实现忽略
            def base64_api(uname, pwd, img, typeid):
                with open(img, 'rb') as f:
                    base64_data = base64.b64encode(f.read())
                    b64 = base64_data.decode()
                data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
                result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
                if result['success']:
                    return result["data"]["result"]
                else:
                    return result["message"]
                return ""


            def getImgCodeText(imgPath,imgType):#直接返回验证码内容
                #imgPath：验证码图片地址
                #imgType：验证码图片类型
                result = base64_api(uname='xxx', pwd='xxx', img=imgPath, typeid=imgType)
                return result


    使用：
        from selenium import webdriver
        from selenium.webdriver import ActionChains
        from time import sleep
        import tujian
        #1.创建浏览器对象
        bro = webdriver.Chrome(executable_path='./chromedriver')
        #2.发起请求
        login_url = 'https://passport.bilibili.com/login?from_spm_id=333.851.top_bar.login_window'
        bro.get(login_url)
        sleep(1)
        #3.定位到指定标签填充用户名和密码
        user_box = bro.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[1]/input')
        user_box.send_keys('15027900535')
        sleep(1)
        pwd_box = bro.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/input')
        pwd_box.send_keys('123456')
        sleep(1)
        login_btn = bro.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]')
        login_btn.click()
        sleep(10)
        #4.定位完整的验证码对话框
        #注意：在开发者工具中是可以定位到多个div表示验证码对话框的，因此将这几个div都定位到，以此去尝试
        code_tag = bro.find_element_by_xpath('/html/body/div[4]/div[2]/div[6]/div/div')
        sleep(1)
        #5.识别验证码（使用打码平台进行验证码识别）
        code_tag.screenshot('./code.png')#将验证码对话框截图保存
        sleep(1)
        #使用图鉴接口识别
        result = tujian.getImgCodeText('./code.png',27)#获取了识别的结果
        # result = '154,251|145,167'
        # print(result)
        result_list = result.split('|')
        #result_list == ['154,251','145,167']
        #6.根据识别出验证码的结果进行处理
        for pos in result_list:
            x = int(pos.split(',')[0])
            y = int(pos.split(',')[1])
            ActionChains(bro).move_to_element_with_offset(code_tag,x,y).click().perform()
            sleep(0.5)
        sleep(2)
        #此处使用class属性进行确定标签定位
        confirm_btn = bro.find_element_by_xpath('//a[@class="geetest_commit"]')
        confirm_btn.click()
        sleep(3)
        bro.quit()

规避检测（重要）
    现在不少大网站有对selenium采取了监测机制。比如正常情况下我们用浏览器访问淘宝等网站的 window.navigator.webdriver的值为 undefined或者为false。而使用selenium访问则该值为true。那么如何解决这个问题呢？
        实现js注入，绕过检测
        from selenium.webdriver import ActionChains
        from selenium.webdriver import Chrome

        driver = Chrome('./chromedriver',options=chrome_options)
        #Selenium在打开任何页面之前，先运行这个Js文件。
        with open('./stealth.min.js') as f:
            js = f.read()
        #进行js注入，绕过检测
        #execute_cdp_cmd执行cdp命令（在浏览器开发者工具中执行相关指令，完成相关操作）
        #Page.addScriptToEvaluateOnNewDocument执行脚本
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": js
        })

        driver.get('https://www.taobao.com')

"""
