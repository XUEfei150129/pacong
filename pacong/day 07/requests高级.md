### 视频数据爬取

- url：https://www.51miz.com/shipin/

  - 爬取当前url页面中营销日期下的几个视频数据。

- 找寻每个视频的播放地址：

  - 通过观察视频详情页的页面数据，并没有发现视频的播放地址，只有一张播放图片。
  - 打开抓包工具，点击页面的播放按钮，找到了视频的播放数据包，可以提取出视频的播放地址，地址格式为：

  ```url
  https://video-js.51miz.com/preview/video/00/00/11/63/V-116374-7B5E698E.mp4
  ```

  - 观察其他视频的播放地址，找寻规律：

  ```
  相同之处：https://video-js.51miz.com/preview/video/ 
  不同之处：00/00/11/63/V-116374-7B5E698E.mp4
  ```

  - 在首页url页面数据中，找到video标签（对应每个视频），标签的poster属性值中出现了视频播放地址中的（不同之处）相似部分，但是经过测试，不可用。
    - 在video标签下面有一个source标签，其内部的src属性值正好就是视频的播放地址 (补充上https:即可) 。

  ```python
  import requests
  from lxml import etree
  headers = {
      'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
  }
  url = 'https://www.51miz.com/shipin/'
  response = requests.get(url=url,headers=headers)
  page_text = response.text
  
  #数据解析
  tree = etree.HTML(page_text)
  div_list = tree.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/div')
  for div in div_list:
      src_list = div.xpath('./a/div/div/div/video/source/@src')
      #要给视频地址进行补全
      for src in src_list:
          #src就是一个完整的视频地址
          src = 'https:'+src
          video_data = requests.get(url=src,headers=headers).content
          video_title = src.split('/')[-1]
          with open(video_title,'wb') as fp:
              fp.write(video_data)
          print(video_title,'爬取保存成功！')
      break
  ```

### Cookie

- 什么是cookie？
  - cookie的本质就是一组数据（键值对的形式存在）
  - 是由服务器创建，返回给客户端，最终会保存在客户端浏览器中。
  - 如果客户端保存了cookie，则下次再次访问该服务器，就会携带cookie进行网络访问。
    - 典型的案例：网站的免密登录

- 爬取雪球网中的咨询数据
  - url：https://xueqiu.com/，需求就是爬取热帖内容

  - 经过分析发现帖子的内容是通过ajax动态加载出来的，因此通过抓包工具，定位到ajax请求的数据包，从数据包中提取：

    - url：https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=311519&size=15
    - 请求方式：get
    - 请求参数：拼接在了url后面

  - ```python
    import requests
    import os
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
    }
    url = 'https://xueqiu.com/statuses/hot/listV2.json'
    param = {
        "since_id": "-1",
        "max_id": "311519",
        "size": "15",
    }
    response = requests.get(url=url,headers=headers,params=param)
    data = response.json()
    print(data)
    #发现没有拿到我们想要的数据
    ```

  - 分析why？

    - 切记：只要爬虫拿不到你想要的数据，唯一的原因是爬虫程序模拟浏览器的力度不够！一般来讲，模拟的力度重点放置在请求头中！
    - 上述案例，只需要在请求头headers中添加cookie即可！

  - 爬虫中cookie的处理方式（两种方式）：

    - 手动处理：将抓包工具中的cookie赋值到headers中即可

      - 缺点：
        - 编写麻烦
        - cookie通常都会存在有效时长
        - cookie中可能会存在实时变化的局部数据

    - 自动处理

      - 基于session对象实现自动处理cookie。
        - 1.创建一个空白的session对象。
        - 2.需要使用session对象发起请求，请求的目的是为了捕获cookie
          - 注意：如果session对象在发请求的过程中，服务器端产生了cookie，则cookie会自动存储在session对象中。
        - 3.使用携带cookie的session对象，对目的网址发起请求，就可以实现携带cookie的请求发送，从而获取想要的数据。

      - 注意：session对象至少需要发起两次请求
        - 第一次请求的目的是为了捕获存储cookie到session对象
        - 后次的请求，就是携带cookie发起的请求了

      - ```python
        import requests
        
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        param = {
            #如果遇到了动态变化的请求参数？必须经过测试才知道需不需要处理
            "since_id": "-1",
            "max_id": "553059", #动态变化的请求参数
            "size": "25"
        }
        
        url = 'https://xueqiu.com/statuses/hot/listV2.json'
        
        #session对象会实时保存跟踪服务器端给客户端创建的cookie
            #创建一个session对象
        session = requests.Session() #空白的session对象
        
        first_url = 'https://xueqiu.com/'
        #使用session对象进行请求发送：如果该次请求时，服务器端给客户端创建cookie的话，则该cookie就会被保存seesion对象中
        session.get(url=first_url,headers=headers)
        #使用保存了cookie的session对象进行后续请求发送
        ret = session.get(url=url,headers=headers,params=param).json()
        print(ret)
        ```

### 模拟登录

- 获取https://passport.17k.com/中的书架页面里的图书信息

```python
import requests
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

login_url = 'https://passport.17k.com/ck/user/login'
data = {
    "loginName": "15027900535",
    "password": "xxxxxxxxx"
}
session = requests.Session()
#请求的目的是为了获取cookie将其保存到session对象中
session.post(url=login_url,headers=headers,data=data)

#携带cookie向书架的页面进行请求发送，获取书架信息
#书架中的数据是动态加载的数据
book_url = 'https://user.17k.com/ck/author2/shelf?page=1&appKey=2406394919'
page_text = session.get(url=book_url,headers=headers).json()

#解析书架信息
print(page_text)
```

### 代理

- 什么是代理
  - 代理服务器
- 代理服务器的作用
  - 就是用来转发请求和响应

![Snip20220124_45](imgs/Snip20220124_45.png)		





- 在爬虫中为何需要使用代理？

  - 有些时候，需要对网站服务器发起高频的请求，网站的服务器会检测到这样的异常现象，则会讲请求对应机器的ip地址加入黑名单，则该ip再次发起的请求，网站服务器就不在受理，则我们就无法再次爬取该网站的数据。
  - 使用代理后，网站服务器接收到的请求，最终是由代理服务器发起，网站服务器通过请求获取的ip就是代理服务器的ip，并不是我们客户端本身的ip。

- 代理的匿名度

  - 透明：网站的服务器知道你使用了代理，也知道你的真实ip
  - 匿名：网站服务器知道你使用了代理，但是无法获知你真实的ip
  - 高匿：网站服务器不知道你使用了代理，也不知道你的真实ip（推荐）

- 代理的类型（重要）

  - http：该类型的代理服务器只可以转发http协议的请求
  - https：可以转发https协议的请求

- 如何获取代理?

  - 芝麻代理：https://jahttp.zhimaruanjian.com/（推荐，有新人福利）

- 如何使用代理？

  - 测试：访问如下网址，返回自己本机ip

  - ```python
    import requests
    from lxml import etree
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
    }
    url = 'http://www.cip.cc/'
    
    page_text = requests.get(url,headers=headers).text
    tree = etree.HTML(page_text)
    text = tree.xpath('/html/body/div/div/div[3]/pre/text()')[0]
    print(text.split('\n')[0])
    ```
    
  - 使用代理发起请求，查看是否可以返回代理服务器的ip

  - ```python
    import requests
    from lxml import etree
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
    }
    url = 'http://www.cip.cc/'
    
    page_text = requests.get(url,headers=headers,proxies={'http':'121.234.12.62:4246'}).text
    tree = etree.HTML(page_text)
    text = tree.xpath('/html/body/div/div/div[3]/pre/text()')[0]
    print(text.split('\n')[0])
    ```
    
  - 深度测试：

    - 案例：https://www.kuaidaili.com/free/inha

    - 对快代理进行n次请求，直到本机无法访问快代理为止（证明本机ip被快代理封掉了）

    - 构建一个代理池（封装了很多代理ip和端口的容器），用于数据的批量爬取
    
    - ```python
      import requests
      from lxml import etree
      import random
      import time
      import random
      
      headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
      }
      
      #构建一个代理池（有很多不同的代理服务器）
      proxy_url = 'http://webapi.http.zhimacangku.com/getip?num=80&type=3&pro=&city=0&yys=0&port=11&pack=337730&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
      page_text = requests.get(url=proxy_url,headers=headers).text
      proxy_list = [] #代理池
      for ips in page_text.split('\n')[0:-1]:
          dic = {}
          dic['https'] = ips.strip()
          proxy_list.append(dic)
      
      for page in range(1, 5001):
          print('正在爬取第%d页的ip数据......' % page)
          #生成不同页码对应的url
          url = 'https://www.kuaidaili.com/free/inha/%d/' % page
          page_text = requests.get(url=url, headers=headers,proxies=random.choice(proxy_list)).text
          time.sleep(0.5)
          tree = etree.HTML(page_text)
          ip = tree.xpath('//*[@id="list"]/div[1]/table/tbody/tr[1]/td[1]/text()')[0]
          print(ip)
      ```

### 验证码

- 图鉴平台：http://www.ttshitu.com/   （推荐）

- 使用流程：

  - 注册登录图鉴平台

  - 登录后，点击开发文档，提取识别的源代码

  - 模块(tujian.py)的封装：

  - ```python
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
        result = base64_api(uname='bb328410948', pwd='bb328410948', img=imgPath, typeid=imgType)
        return result
    
    
    ```

  - 验证码图片识别操作

    - 识别本地的滑动验证和坐标点击验证

  - ```python
    
    ```
