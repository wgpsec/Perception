<h1 align="center">Perception 🚀</h1>

<p>
  <img src="https://img.shields.io/badge/Language-Python2.x/3.x-blue" />
  <img src="https://img.shields.io/badge/Version-1.1-blue" />
  <a href="https://plat.wgpsec.org">
    <img src="https://img.shields.io/badge/Dependence-WgpSec%20Plat-green" target="_blank" />
  </a>
</p>

> 基于狼组安全服务(社区)平台API打造的一款在线信息收集程序

## 🚀 开始使用
1. 不需要安装任何依赖（全新Python环境下需要安装requests: `pip install requests`）
2. 运行程序
```
python3 main.py -h 
```

如果没有任何报错，则会输出以下信息
```
usage: main.py [-h] [-l LOGIN] [-t TYPE] [-q QUERY] [-k KEYWORD]

嗨！你好！ 当你看到这里的时候，很高兴你已经成为了我们的一员！

optional arguments:
  -h, --help            show this help message and exit
  -l LOGIN, --login LOGIN
                        登陆
  -t TYPE, --type TYPE  (web|host)
  -q QUERY, --query QUERY
                        (port|host|title|ip|city)
  -k KEYWORD, --keyword KEYWORD
                        enable knowledge api

```


## ✨用法
e.g：`python3 main.py -l xxxxx`

首先需要登陆xxxx为用户名，然后回车，输入密码(不可见)
登陆的时候已经进行验证了，不需要担心是否登陆，会有提示的
> 信息收集模块
- 指定目标端口例如`port=4444`
Usage: `python3 main.py -t web -q port=4444`
- 指定目标城市例如武汉
Usage: `python3 main.py -t web -q  city=武汉`
> 知识库模块
- 指定关键字例如工具
Usage: `python3 main.py -k 工具`

## ⚡️特性

- 支持以城市名、主机IP、网站标题、指定端口为搜索条件
- 程序会将搜索结果匹配社区平台内的知识库文章并返回链接

## 🛠Todo

1. 美化程序的输出信息
2. 支持多参数搜索（类似fofa）

## 📝更新日志

### 1.1

更新时间：2020-09-05

 - 发布1.1程序

## 💡免责声明

不能使用该工具进行非法活动，下载该工具就表示同意此条款，后续与作者无关
