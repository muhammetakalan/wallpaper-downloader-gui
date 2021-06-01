import gi
import urllib
import requests
import os
import sys
import threading
from bs4 import BeautifulSoup
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def WallpapersWide():
    try:
        os.mkdir("wallpapers")
    except FileExistsError:
        pass
    z = 1
    for a in range(sys.maxsize):
        url = "http://wallpaperswide.com/" + builder.get_object("categories").get_active_text() + "-desktop-wallpapers" + "/page/" + str(a+1)
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        links = soup.select('.wall .thumb .mini-hud a')
        sources = []
        for b in links:
            sources.append("http://wallpaperswide.com" + b['href'])
        for c in sources:
            soup = BeautifulSoup(requests.get(c).content, 'html.parser')
            link = soup.find(attrs={"target" : "_self"}, text = builder.get_object("resolutions").get_active_text())
            if link:
                downloadLink = "http://wallpaperswide.com" + link['href']
                filePath = "wallpapers/" + link['href'].split("/")[-1]
                urllib.request.urlretrieve(downloadLink, filePath)
                builder.get_object("infoLabel").set_text(str(z) + " image downloaded")
                z += 1
                if not builder.get_object("CancelBtn").get_sensitive() or not builder.get_object("window").get_visible():
                    builder.get_object("statusLabel").set_text("Wallpaper downloader app")
                    builder.get_object("infoLabel").set_text("05akalan57@gmail.com")
                    sys.exit()

def WallpapersCraft():
    try:
        os.mkdir("wallpapers")
    except FileExistsError:
        pass
    z = 1
    for a in range(sys.maxsize):
        url = "https://wallpaperscraft.com/catalog/" + builder.get_object("categories").get_active_text() + "/page" + str(a+1)
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        links = soup.select('.wallpapers__link')
        sources = []
        for b in links:
            sources.append("https://wallpaperscraft.com" + b['href'])
        for c in sources:
            soup1 = BeautifulSoup(requests.get(c).content, 'html.parser')
            link1 = soup1.find(attrs={"class" : "resolutions__link"}, text = builder.get_object("resolutions").get_active_text())
            if link1:
                soup2 = BeautifulSoup(requests.get("https://wallpaperscraft.com/" + link1['href']).content, 'html.parser')
                link2 = soup2.find(attrs={"class" : "gui-button"})
                downloadLink = link2['href']
                filePath = "wallpapers/" + link2['href'].split("/")[-1]
                urllib.request.urlretrieve(downloadLink, filePath)
                builder.get_object("infoLabel").set_text(str(z) + " image downloaded")
                z += 1
                if not builder.get_object("CancelBtn").get_sensitive() or not builder.get_object("window").get_visible():
                    builder.get_object("statusLabel").set_text("Wallpaper downloader app")
                    builder.get_object("infoLabel").set_text("05akalan57@gmail.com")
                    sys.exit()

class Handler:
    def Download(self, DownloadBtn):
        builder.get_object("statusLabel").set_text("Downloading")
        builder.get_object("infoLabel").set_text("0 image downloaded")
        DownloadBtn.set_sensitive(False)
        builder.get_object("CancelBtn").set_sensitive(True)
        imageSourceProvider = builder.get_object("imageSourceProvider").get_active_text()
        if imageSourceProvider == "WallpapersWide":
            threading.Thread(target=WallpapersWide).start()
        elif imageSourceProvider == "WallpapersCraft":
            threading.Thread(target=WallpapersCraft).start()

    def Cancel(self, CancelBtn):
        builder.get_object("statusLabel").set_text("Wallpaper downloader app")
        builder.get_object("infoLabel").set_text("05akalan57@gmail.com")
        CancelBtn.set_sensitive(False)
        builder.get_object("DownloadBtn").set_sensitive(True)

    def Quit(*args):
        Gtk.main_quit()

builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(Handler())
builder.get_object("window").show_all()
Gtk.main()