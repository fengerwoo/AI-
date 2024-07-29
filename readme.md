## AI检查文本错误

调用OpenAI库，使用 GPT4o-mini 去检查一个文件夹内(支持多层)所有汉语文本有没有错误，最后输出结果到csv

#### 安装 OpenAI 库

``` 
pip install openai -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

####  配置 OpenAI 自己的域名和key
修改代码开头的 base_url、api_key ，因为需要花钱，所以用自己的<br/>
推荐用这家代理商的API，稳定、国内可用<br/>
注册链接：<a href="https://referer.shadowai.xyz/r/4073">https://referer.shadowai.xyz/r/4073</a>


####  执行检查
cd 到项目目录

``` 
cd xxx/xxx
``` 

执行 Python 文件

``` 
Python main.py
``` 

输入 文本文件夹路径 和 结果路径<br/>
(可以相对或者绝对路径，下图示例用的模拟数据 相对路径)<br/>
<img width="60%" src="https://ice.frostsky.com/2024/07/29/a21cdaec6ebfe39c2b07fc1aa363e746.jpeg">