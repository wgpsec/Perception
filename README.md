# 注意事项

首先因为只是使用的社区API的关系，所以得到的信息会比较少，我默认设置的是20条，师傅们可以根据自己的需要进行调整，最大为100，目前还是一个雏形，功能比较简陋，在后续的开发中能够做到更多的功能:sun_with_face:

>  Tiks:
>
> 只能使用两个选项 :older_man: 会加快进度整:fire:



# Use

首先需要我们安装几个第三方库：

```python
pip install requests
pip install demjson
pip insatll argparse
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

![image-20200720204756131](demo.png)

目前仅支持域名的查找，后续功能会逐渐添加

## Furter

在未来的开发中，会逐渐完善以下功能：

* ~~查看基本的域名信息~~

* 查找对应的指纹和服务
* 查找开放的常见端口
* 和[知识库](https://plat.wgpsec.org/knowledge)对接，便于查看对应的指纹POC和文献啥
* ......

# 免责声明

不能使用该工具进行非法活动，下载该工具就表示同意此条款，后续与作者无关