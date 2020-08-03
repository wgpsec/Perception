<h1 align="center">Perception 🚀</h1>

<p>
  <img src="https://img.shields.io/badge/Language-Python2.x/3.x-blue" />
  <img src="https://img.shields.io/badge/Version-1.0-blue" />
  <a href="https://plat.wgpsec.org">
    <img src="https://img.shields.io/badge/Dependence-WgpSec%20Plat-green" target="_blank" />
  </a>
</p>

> 基于狼组安全服务(社区)平台API打造的一款在线信息收集程序

## 🚀 开始使用

1. 安装第三方依赖：
    ```bash
    pip install -r requirements.txt -i https://pypi.douban.com/simple
    ```
2. 初始化用户信息：
   
    首次运行程序需要登录你的狼组安全平台账户，程序会提示你输入平台的账号与密码并让你设置查询数量，然后会在当前的目录下生成`.user_token.txt`和`.pageSize.cfg`文件，分别存储用户信息，和用户自定义的查询数量设置。

3. 运行程序：
   
    `python main.py -h`
    
    如果没有任何报错，则会输出以下信息：
    ```
    usage: main.py [-h] [--c C] [--h H] [--t T] [--p P]

    嗨！你好！ 当你看到这里的时候，很高兴你已经成为了我们的一员！ 当你第一次运行的时候需要你输入一次你的cookie，方便我们认证，只需要一次哦！

    optional arguments:
      -h, --help  show this help message and exit
      --c C       查询的城市
      --h H       查询的IP
      --t T       查询网站标题
      --p P       查询开放特定端口
    ```

    支持所有参数的查找，并且支持IP和端口联合查询

## ✨示例

e.g：`python main.py --c 上海`

![image-20200721181428197](demo.png)

> 目前功能比较少，会将社区平台API慢慢搬到工具上来，也希望各位开issue监督催促！

## ⚡️特性

- 支持以城市名、主机IP、网站标题、指定端口为搜索条件
- 程序运行结束后自动生成查询结果的Excel表格文件
- 程序会将搜索结果匹配社区平台内的知识库文章并返回链接

## 🛠Todo

1. 美化程序的输出信息
2. 支持通过社区平台API添加扫描任务
3. 支持多参数搜索（类似fofa）
4. 授权用户允许调用Xray进行联动


## 📝更新日志

### 1.0

更新时间：2020-07-30

 - 发布1.0程序

## 💡免责声明

不能使用该工具进行非法活动，下载该工具就表示同意此条款，后续与作者无关
