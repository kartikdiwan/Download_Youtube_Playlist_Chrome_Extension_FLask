from pytube import YouTube 
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from flask import Flask, request,jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')

def scroll_page(url):
    service = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--lang=en')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    old_height = driver.execute_script("""
        function getHeight() {
            return document.querySelector('ytd-app').scrollHeight;
        }
        return getHeight();
    """)

    while True:
        driver.execute_script("window.scrollTo(0, document.querySelector('ytd-app').scrollHeight)")

        time.sleep(2)

        new_height = driver.execute_script("""
            function getHeight() {
                return document.querySelector('ytd-app').scrollHeight;
            }
            return getHeight();
        """)

        if new_height == old_height:
            break

        old_height = new_height

    selector = driver.page_source
    driver.quit()
    return selector

def Get_Links_From_Playlist(url):
    req = scroll_page(url)
    soup = BeautifulSoup(req, "html.parser")
    Playlist_Name = soup.title.string
    Playlist_Name = Playlist_Name.replace(" - YouTube","")
    anchors = soup.find_all("a")
    # print(anchors)
    linkList = []
    for link in anchors:
        if link.get("href") == None or link.get("href") == "":
            continue
        if "index=" in link.get("href"):
            linkList.append(url+link.get("href"))
    linkList = [*set(linkList)]
    FinalLinkList = []
    for link in linkList:
        link = link[:link.index("&list=")]
        link = link.replace(url, "https://www.youtube.com")
        FinalLinkList.append(link)
        print("-----------------------------------------------------------------------------------------")
        print("Scraping Successfully Completed for the Playlist: "+Playlist_Name)
        print("-----------------------------------------------------------------------------------------\n")
    return Playlist_Name, FinalLinkList


def Download_From_Links(P_Name, links):
    
    SAVE_PATH = "\Downloaded Songs & Playlists\\" + P_Name
    
    for link in links: 
        try:
            yt = YouTube(link)
            yt = yt.streams.filter(only_audio=True).first()

            print("Downloading " + yt.title + "...")
            out_file = yt.download(SAVE_PATH)
            
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        except:
            return jsonify("Some error has occured, please retry")
        print(yt.title + " has been successfully downloaded!\n")

    print("-----------------------------------------------------------------------------------------")
    print("Sucessfully downloaded the Playlist: " + yt.title)
    print("-----------------------------------------------------------------------------------------\n")

@app.route('/', methods = ['GET', 'POST'])
def main():
    url = request.json
    print("Recieved URL : " + url)
    if "https://www.youtube.com/playlist?list=" in url:
        Playlist_Name, Links = Get_Links_From_Playlist(url)
        Download_From_Links(Playlist_Name, Links)
        return jsonify("Sucessfully downloaded Playlist: "+Playlist_Name)
    elif "https://www.youtube.com/watch?v=" in url:
        Links = []
        Links.append(url)
        Download_From_Links("", Links)
        return jsonify("Sucessfully downloaded Song")
    return jsonify("Please make sure you are on a Youtube Video or Playlist, please retry")

if __name__ == '__main__':
    app.run(host = 'localhost', port = 8008, debug=False)