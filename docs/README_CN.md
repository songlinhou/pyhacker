# pyhacker 1.0 (测试版)


语言 [English](https://github.com/201528015329004/pyhacker) / 中文
> Initiator: Songlin Hou

完全兼容 Python 2.7
 
##   0 写在前面的话
Ethical Hacking Tools （以下简称EHT），是基于Python语言所设计的，完全兼容Python 2.7。
实验表明渗透测或者ethical hacking.需要用户花较长时间完成。开发者很乐意把这个项目分享出来，供大家学习使用。这个项目的使用者需要同意以下条款：
1 任何此项目的使用者必须把本项目提供的信息和手段，使用在合法的地方；
2 此项目的作者和贡献者不负任何责任。


## 1 注意
Python 是一门通用的、功能强大的编程语言，同时也是容易掌握和学习的一门程序语言。Python也是随着系统管理不断更新，这些特点都使得Python成为处理各种项目的不二选择。我们很高兴，你对这个项目感兴趣，但是这个项目还是一个测试版，在有的情况下还不够稳定。目前，这个版本好在积极的完善中，为了你我的便利，请你留下你的建议或者是贡献。.

## 2 特点 

#### [ 版本1.0 ]
- 这是一个彩色的交互性 server shell，支持一对一和多对一的通信；
- 这个彩色的客户终端可以连续监视来自sever shell的请求；
- 具有跨平台功能，支持Linux，Mac OSX，Windows，Android和IOS系统；
- 用户终端和命令行脚本都支持（支持程度视用户的机器决定）；
- 在服务器的控制下，Python脚本可以直接在用户的机器上运行（测试版）；

## 3 使用说明

#### 3.1 如何获取脚本

你有两种方式可以获取此项目的脚本文件：
-① （推荐）如果你已经成功安装 git （确保当你在你的终端或者脚本行运行git 文件时没有报错），你可以直接复制以下命令，并运行；

```
# use git command to get the scripts
$ git clone https://github.com/201528015329004/pyhacker.git
```
-②	 或者，你可以在此网站中点击 Download ZIP 直接下载Zip文件。

#### 3.2 设置你的键值数据库（可选）

推荐你在继续操作时，设置好你的键值数据库（key-value database）。如果你没有手动设置，程序将使用键值公共数据库的默认设置。 为了安全和效率，我们强烈推荐你建立自己的键值数据库。
	通过kv_base_id 语句你可以建立自定义的键值数据库，具体操作代码如下：
	
	
```
# In bash envrionment
$ cd pyhacker/my_plugins/kvdb
 
$ python #'open python interactive shell'

# In python interactive shell
>>> from openkv import OpenKV
>>> kv=OpenKV()
>>> description = 'YOUR DESCRIPTION'
>>> kv.createDB(str(description))
('BASE_ID:', '*****') #**** is your kv_base_id
```

注意：请不要修改‘YOUR DESCRIPRION‘’字段
#### 3.3 微小的改动
打开和编辑文件（‘HTTP_KV_Server.py’和‘HTTP_KV_Client.py’）你需要做如下的修改：
修改使得文件中的USER和PASS变量保持一致（非空值）
```
USER,PASS = "YOUR_USERNAME_NAME","YOUR_PASS_WORD" #please change the values here
```

-在最后使用在3.2中提到的kv_base_id语句，代替KVID.DEFAULT，具体代码如下：

```
...
        show_header()
        db = init_connection(KVID.DEFAULT)#replace KVID.DEFAULT with your kv_base_id
        server_on(db)
        serve(db)
...        
```

#### 3.4 运行 
复制pyhacker文件，在目标机器中，并运行相应的脚本，同目标机器的连接将自动建立。
在自己的机器中运行如下代码：
- 在自己的机器中运行如下代码（服务端 Sever）：

```
$ cd pyhacker/http
$ python HTTP_KV_Server.py
```

- 在目标机器中运行如下代码（Target Machine）： 

```
$ cd pyhacker/http
$ python HTTP_KV_Client.py
```

**[注意 1]** 如果你需要相应的模块，请用pip install 加上相应模块的名称(pip install modulename )
**[注意 2]** 在以后的版本中，我们将整合不同平台上的生成二进制代码的工具。现在，你可以自己生成二进制代码，具体信息请浏览py2exe 和 py2app 文件。

## 4 示例 
这里有一些在不同系统中运行的情况的截图，供参考。
- 启动服务器（MAC OSX）
![GitHub set up](https://github.com/201528015329004/pyhacker/blob/master/docs/images/server_init.png?raw=true)
- 启动服务在Windows10
![GitHub set up](https://github.com/201528015329004/pyhacker/blob/master/docs/images/client_init.png?raw=true)

- ---成功连接

( 1 ) 服务端（server）正在Mac OSX上运行，并试图连接一个windows 系统的机器。通过在Windows上的命令操作，服务端抓取了Windows端的结果。
![GitHub set up](https://github.com/201528015329004/pyhacker/blob/master/docs/images/server_cmd.png?raw=true)

( 2 ) Windows端正在等待来自服务端（Sever）的请求
![GitHub set up](https://github.com/201528015329004/pyhacker/blob/master/docs/images/client_cmd.png?raw=true)


（3）	当服务器关闭，客户端将会保持等待。

![GitHub set up](https://github.com/201528015329004/pyhacker/blob/master/docs/images/client_serveroff.png?raw=true)




