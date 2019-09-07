import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, "rwb") as out_file:
        out_file.write(get_response.content)


download("url")