from bs4 import BeautifulSoup
import requests

# The goal of this code is to get all .tgz files from a webpage.
# The source for this copy-paste is: https://stackoverflow.com/a/34718858
# We changed the URL and the file extension. The code does the rest, i.e.
# it downloads the webpage, then loops through each one of the download links
# to download the files in the local folder.
# Afterwards, 7zip on Windows was used with the command "7z.exe x *.tgz" to extract
# the tar files, then "7z.exe x *.tar" to extract the folders.
# It is recommanded to run this code in an isolated folder, to avoid slowdown.

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