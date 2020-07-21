# 注意事项

首先因为只是使用的社区API的关系，所以得到的信息会比较少，我默认设置的是20条，师傅们可以根据自己的需要进行调整，最大为100，目前还是一个雏形，功能比较简陋，在后续的开发中能够做到更多的功能:sun_with_face:

>  Tiks:
>
> 只能使用两个选项 :older_man: 会加快进度整:fire:



# Use

安装第三方依赖：
```bash
pip install -r requirements.txt
```
如果安装demjson比较耗时可通过镜像：
```bash
pip install -r requirements.txt -i https://pypi.douban.com/simple
```

第一次使用需要输入一下社区的`cookie`，可以先输入 `--help`进行添加,，然后会在当前的目录下生成一个`cookies.txt`文件。下面是使用的一些参数：

```
usage: test.py [-h] [--c C] [--h H] [--t T] [--p P]

嗨！你好！ 当你看到这里的时候，很高兴你已经成为了我们的一员！ 当你第一次运行的时候需要你输入一次你的cookie，方便我们认证，只需要一次哦！

optional arguments:
  -h, --help  show this help message and exit
  --c C       查询的城市
  --h H       查询的IP
  --t T       查询网站标题
  --p P       查询开放特定端口
```

目前仅开发出`-C`和`-h` 

# eg

`python test.py --c 成都`

![image-20200721181428197](demo.png)

目前仅支持域名的查找，后续功能会逐渐添加

## Furter

在未来的开发中，会逐渐完善以下功能：

- ~~查看基本的域名信息~~
- ~~查找对应的指纹和服务~~
- 查找开放的常见端口
- ~~和[知识库](https://plat.wgpsec.org/knowledge)对接，便于查看对应的指纹POC和文献~~
- ......



***REMOVED***

***REMOVED***

***REMOVED***

***REMOVED***



目前第一版：https://github.com/wgpsec/Perception

## 要求能做到的功能

1. 用户可以按照自定义的组合（city、reason、title、ip、ports）进行查询，现有的只能做到某一个参数的查询
2. 允许批量查询，查询的结果可以自定义导出，导出为csv或者exc文件，目前这个功能没有实现
3. 验证的实现，由于社区版的`api` 接口需要有社区账号才能做到查询，所以需要另外的一个验证机制，比如直接输入账号密码进行登录，目前实现的方式是让用户直接输入cookie，待优化
4. 美化输出和工具的样子



> 这里还有一个返回数据的问题，我们的账号只能做到每次最大为100条数据的返回，在实际的开发过程中我发现：当pageSize为20的时候，他会返回20条数据，但是pageSize为100的时候他只会返回几条数据，这个地方我反复测过，具体问题还不太清楚

# 示例

具体返回参数可以去看社区的开发文档

# 免责声明

不能使用该工具进行非法活动，下载该工具就表示同意此条款，后续与作者无关