设计文档
======================

项目概况
----------------
略

项目环境
-------------------
* linux
* python 3


项目组织
---------------

```
+-- environment.xuxu.ini                # 配置文件，根据机器而不同
+-- data
|   +-- 2015-05-19
|   |   +-- stockinfo
|   |   |   +--stock.list               # 今天通过网页抓取的stock.list
|   |   |   +--stock.data               # 当日的stock.data
|   |   |   +--stock.schema             # 抓取的stock具有哪些feature
|   |   |   +--stock.comp.data          # 通过计算得到的feature的名字
|   |   |   +--stock.comp.schema        # 计算得到的feature，如均线，输入stock.data(今日及之前)和stock.comp.data(之前)
|   |   |   +--board.data               # 板块的数据 以后再说
|   |   |   +--board.schema             # 当日的板块抓取的feature list定义
|   |   +-- modelresult
|   |   |   +--model_xuxu1.result           # 一个模型的预测结果，
|   |   |   +--model_xuxu1.result.eval      # 第二天(或更晚，依据模型的类型，如长期模型会在n天后校验)预测结果的评定
|   |   |   +--model_caca1.result           # 不同的模型
|   |   |   +--model_caca1.result.eval
|   |   +-- view                        #用于产生所有展示给最终用户的页面，gbk encoding
|   +-- 2015-05-20
|   +-- ...
+-- src
|   +-- common
|   |   +-- stock_trade_date.py         # 确认某天是否是stock trading day
|   |   +-- mail_alert.py               # 运行失败，邮件报警
|   |   +-- data_path.py                     # 读取env.ini并提供接口给出各个文件的path.
|   |   +-- ...
|   +-- crawler
|   |   +-- crawler.py                  # 统一抓取方法
|   |   +-- crawl_sina_stock_list.py    # 抓取stock list
|   |   +-- crawl_sina_stock.py         # 抓取stock feature
|   |   +-- crawl_yahoo_stock_list.py   # 抓取stock list
|   |   +-- crawl_yahoo_stock.py        # 抓取stock feature
|   |   +-- crawl.v1.schema             # 可能需要的schema文件，列出本次crawl能够得到的feature，不允许改动，只加新版本
|   |   +-- crawl.v2.schema             # 可能需要的schema文件，列出本次crawl能够得到的feature，不允许改动，只加新版本
|   +-- data
|   |   +-- data_provider.py            # 数据读取，提供对/data/下面所有文件的解析提取。
|   |   +-- stock.py                    # 的数据定义 stock一天的数据。
|   |   +-- stock_range.py              # 数据定义，同一stock，若干天的数据。
|   |   +-- stock_list.py               # 数据定义，同一天，若干stock的数据。
|   |   +-- ...
|   +-- compute
|   |   +-- comp.v1.schema              # 可能需要的数据文件，列出本次计算能够得到的feature，不允许改动，只加新版本
|   |   +-- comp.v2.schema              # 可能需要的数据文件，列出本次计算能够得到的feature，不允许改动，只加新版本
|   |   +-- compute.py                  # 计算feature，输入为data_provider， 输出是stock.comp.data
|   +-- model
|   |   +-- model.list                  # 可能需要的列出了所有model的定义
|   |   +-- model.py                    # 所有model的基类
|   |   +-- model_xuxu1.py              # 用于生成model_xuxu1.result
|   |   +-- model_caca1.py              # 用于生成model_caca1.result
|   |   +-- ...
|   +-- main
|   |   +-- main.py                     ## 当前我们用main.py来运行所有的需求。
|   +-- task
|   |   +-- run_plan.py                 # 这里用来生成运行计划，用哪些schema，哪些model生成结果，以后再说
|   |   +-- run_plan.config             # 运行计划的配置文件
|   |   +-- run_plan.test.config        # 一个待测试的计划的配置文件
|   |   +-- ...
|   +-- web
|   |   +--- application.py             # web展示结果，以后再说
|   |   +--- html
|   |   |   +-- ...
|   |   +-- ...
```

### environment.ini
配置文件，改动后无需上传到服务器，包括working dir，data dir，email alert setting.等等

### data
**stock.data**里面除了有限的几项，比如symbol,name,state.其他的都应该为double属性,并且存储在一个\<string,double\>的dict里面
<p>
**stock.list**是今天能够成功(重试若干次)抓取到所有**stock.schema**标记的feature的stock。其实未成功的stock也应该记录，并标明原因，如停牌，或crawl error。 
<p>
**data**里面的数据是不对外开放的，访问需通过data_povider。

### src
**data_provider** 用来读取data里面的内容，需要提供一系列接口，如：
* 给定一个股票，给出今天抓取的(和计算)的所有feature。
* 给定一个股票，给出今天及前n天的所有feature，或某一个feature。
* 给定一个天数n，给定一系列的feature。返回股票list，这些股票在这n天内这些feature都成功被抓取。
* ...待补充

**crawler**和**compute**里面所有的py文件，不计算文件路径，路径由外面输入进去。路径需根据envrionment.ini来计算，在working directory下面运行，存储临时文件。并把最终文件存到data dir下面。working dir每次应该不同，如果相同，相当于重试，crawler和compute可以利用里面的缓存文件。每次运行前应该吧working dir设成20150519_noon之类的名字。

**main.py**用来运行，

### 依赖关系
**data_provider**依赖 **common**
<p>
**crawler**和**compute**依赖**data_provider**
<p>
**model**依赖**data_provider**不依赖**crawler**和**compute**
<p>
**main**和**task** 依赖 **crawler**, **compute**和**model**
<p>
**web**依赖**data_provider**和**model**


目前可能不做的工作
---------------------------------------
判断股票和板块，概念，地域之间的关系。
<p>
提供web页面给用户
<p>
依据task plan来运行一个包含crawl，compute，model的task

本文档更新
----------------------------------
> 2015.05.19 第一版
