from bs4 import BeautifulSoup
import requests

# To get all .tgz files from a webpage
# https://stackoverflow.com/a/34718858

url = 'http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/'
ext = 'tgz'

def listFD(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return tuple((url + '/' + node.get('href'), node.get('href')) for node in soup.find_all('a') if node.get('href').endswith(ext))

if __name__ == '__main__':
    for file_url, filename in listFD(url, ext):
        file = requests.get(file_url)
        with open(filename, 'wb') as output:
            output.write(file.content)