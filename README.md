# pyhacker 1.0 (Beta)

> Initiator: Songlin Hou

Fully Compatible with Python 2.7
 
##   0 Introduction
Ethical Hacking Tools Designed for Python. It is a long-term project which is indicated for users who need to do penetration testing, or ethical hacking. It is welcomed to contribute and share this project as well as to use it in one of your project. While ethical hacking should only be done when permitted, ANY USERS SHOULD USE IT IN LEGAL WAYS. AND NO RESPONSIBILITY SHALL BE TAKEN BY THE AUTHORS AND CONTRIBUTORS.

## 1 Notice
Python is a versatile general programming language which is both easy to learn and power to use. As a fast-evolving language usually bound with system administration, python can't be a better option for considerable cases. We are appreciated that you have interest in this project, but since this version is still a **beta** version, which means there might be not stable occasions you need be aware of before trying. Currently this version is still under **active development** for your greater convenience, so please support us by leaving comments or contributing.

## 2 Features

#### [ Version 1.0 ]
- A **colored** interactive server shell which supports both **one-to-one** and **one-to-all** communications.
- A **colored** client terminal which can be continuously listening to incoming requests from the server shell.
- Full cross-platform abilities, supported platforms includes **Linux, Mac OSX, Windows, Android and IOS**.
- Terminal/Command-line scripts are supported(depending on client machines).
- Python scripts can be directly executed on client machines and controlled on the server side. **(Beta)**

## 3 Usage

#### 3.1 Get Scripts

At first, you can get the scripts of the project. There are two ways.

- **[RECOMMEND]** If you have already successfully installed **git** (no errors thrown when you type git in your terminal/command-line), you can use **git commands** to clone the scripts. 

```
# use git command to get the scripts
$ git clone https://github.com/201528015329004/pyhacker.git
```
- Or you can simply download the zip file by clicking on the Download ZIP button.

#### 3.2 Set up your key-value database (optional)

It is recommended to set up your own key-value database before you continue. If you skip this part, a standard default key-value public database will be used. For security and efficiency, we HIGHLY recommend you to set up your own key-value database.

To set up a user-defined key-value database, you need to apply for a **kv_base_id**, which can be done by using the following commands. 

Please change the _'YOUR DESCRIPTION'_ string into whatever you like to describe your kv database.

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
#### 3.3 Minor Changes

Open and edit file *HTTP_KV_Server.py* and *HTTP_KV_Client.py*. You need to change the following.

- Change the *USER* and *PASS* variable in both files, and they **MUST** be identical. (non-empty)

```
USER,PASS = "YOUR_USERNAME_NAME","YOUR_PASS_WORD" #please change the values here
```

- In the bottom of both file, use the **kv_base_id** created in 3.2 to replace *KVID.DEFAULT*

```
...
        show_header()
        db = init_connection(KVID.DEFAULT)#replace KVID.DEFAULT with your kv_base_id
        server_on(db)
        serve(db)
...        
```

#### 3.4 Run

Copy the project folder *pyhacker* to both attacker machine and target machines.

Run the corresponding scripts in different machines. And a connection will be automatically set up.

- On Attacker Machine

```
$ cd pyhacker/http
$ python HTTP_KV_Server.py
```

- On Target Machine

```
$ cd pyhacker/http
$ python HTTP_KV_Client.py
```

### 4 Example



