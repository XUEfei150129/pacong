### 简介

什么是框架？

所谓的框架，其实说白了就是一个【项目的半成品】，该项目的半成品需要被集成了各种功能且具有较强的通用性。

Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架，非常出名，非常强悍。所谓的框架就是一个已经被集成了各种功能（高性能异步下载，队列，分布式，解析，持久化等）的具有很强通用性的项目模板。对于框架的学习，重点是要学习其框架的特性、各个功能的用法即可。

初期如何学习框架？

只需要学习框架集成好的各种功能的用法即可！前期切勿钻研框架的源码！

### 安装

```
Linux/mac系统：
      pip install scrapy

Windows系统：
			pip install scrapy   
```

### 基本使用

- 创建项目

  - scrapy startproject firstBlood项目名称

  - 项目的目录结构：

    - ```
      firstBlood   # 项目所在文件夹, 建议用pycharm打开该文件夹
          ├── firstBlood  		# 项目跟目录
          │   ├── __init__.py
          │   ├── items.py  		# 封装数据的格式
          │   ├── middlewares.py  # 所有中间件
          │   ├── pipelines.py	# 所有的管道
          │   ├── settings.py		# 爬虫配置信息
          │   └── spiders			# 爬虫文件夹, 稍后里面会写入爬虫代码
          │       └── __init__.py
          └── scrapy.cfg			# scrapy项目配置信息,不要删它,别动它,善待它. 
      
      ```

- 创建爬虫爬虫文件：

  - cd  project_name（进入项目目录）
  - scrapy genspider 爬虫文件的名称（自定义一个名字即可） 起始url (随便写一个网址即可)
    - （例如：scrapy genspider first www.xxx.com）
  - 创建成功后，会在爬虫文件夹下生成一个py的爬虫文件

- 编写爬虫文件

  - 理解爬虫文件的不同组成部分

  - ```python
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
    
    ```

- 配置文件修改:settings.py

  - 不遵从robots协议：ROBOTSTXT_OBEY = False
  - 指定输出日志的类型：LOG_LEVEL = 'ERROR'
  - 指定UA：USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'

- 运行项目

  - ```
    scrapy crawl 爬虫名称 ：该种执行形式会显示执行的日志信息（推荐）
    ```

### 数据解析

- 注意，如果终端还在第一个项目的文件夹中，则需要在终端中执行cd ../返回到上级目录，在去新建另一个项目。

- 新建数据解析项目：

  - 创建工程：scrapy startproject 项目名称
  - cd 项目名称
  - 创建爬虫文件：scrapy genspider 爬虫文件名 www.xxx.com

- 配置文件的修改：settings.py

  - 不遵从robots协议：ROBOTSTXT_OBEY = False
  - 指定输出日志的类型：LOG_LEVEL = 'ERROR'
  - 指定UA：USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'

- 编写爬虫文件：spiders/duanzi.py

  - ```python
    #https://www.xiachufang.com/category/40076/
    
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
                print(title)
    ```







mysql数据库（重点）  redis数据库



scrapy数据解析  持久化存储
