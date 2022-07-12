import json
import math
import random
import tkinter
import tkinter.messagebox
from tkinter import Label, Menu, ttk, Toplevel, Tk
from tkinter import filedialog as fd
from pytube import YouTube as yt
from urllib.request import urlopen
import urllib.request
import re
from glob import glob
from moviepy.editor import VideoFileClip
import os
from threading import Thread
import pygame
import requests
import eyed3
from eyed3.core import Date

# Gettings the settings values
settingsfile = open("settings.json", "r")
settings_object = json.load(settingsfile)
file = open("mpV.json", "r")
isOpen = json.load(file)
isOpen['MusicPlayer'] = settings_object['AutoOpenMusicPlayer']
#DownloadsDirectory
dl_dir_ = settings_object['DownloadsDirectory']
dl_dir = dl_dir_.replace("/","\\")
#research
research = open("researchHistory", 'r')



class DownloadVid(Thread):
    def __init__(self):
        Thread.__init__(self)
        with open("temp", "r") as temp:
            link = temp.read()
            self.link = link

    def run(self):
        video = yt(self.link)
        s = video.streams
        v = s.get_lowest_resolution()
        d = v.download(output_path=dl_dir)
        return d


class DownloadAux(Thread):
    def __init__(self):
        Thread.__init__(self)
        with open("temp", "r") as temp:
            link = temp.read()
            self.link = link



    def run(self):
        def getInfo(fname):
            print(fname)
            dldirlw = dl_dir.lower()
            bannedwords = [dldirlw, "\\", ".mp3", "(", ")", "[", '"', "]" "audio", "official audio", "officialaudio", "official video", "(offcialaudio)",
                           'feat', "ft.", "&", "ft", "visualizer", "lyrics", "lyrics video", "lyricsvideo", "official music video"
                           , "officialmusicvideo", "official lyric video", "officiallyricvideo", 'visualizer']
            filename = fname
            filename = filename.lower()
            for word in bannedwords:
                filename = filename.replace(word, "")
            print(filename)
            # Getting the song name
            url = "https://shazam.p.rapidapi.com/search"
            querystring = {"term": filename, "locale": "en-US", "offset": "0", "limit": "1"}
            headers = {
                "X-RapidAPI-Key": "c977989d98msh4b7faeefeaa84a8p18972ajsnaeb4f3b572d3",
                "X-RapidAPI-Host": "shazam.p.rapidapi.com"
            }
            rsp = requests.request("GET", url, headers=headers, params=querystring)
            print(rsp.text)
            storage = rsp.json()
            title = storage['tracks']['hits'][0]['track']['title']
            # Getting the info
            url = "https://spotify23.p.rapidapi.com/search/"
            querystring = {"q": title, "type": "tracks", "offset": "0", "limit": "1", "numberOfTopResults": "1"}
            headers = {
                "X-RapidAPI-Key": "c977989d98msh4b7faeefeaa84a8p18972ajsnaeb4f3b572d3",
                "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            storage = response.json()
            data = storage['tracks']['items'][0]['data']
            trackname = data['name']
            artistname = data['artists']['items'][0]['profile']['name']
            trackid = data['id']

            url = "https://spotify23.p.rapidapi.com/tracks/"
            querystring = {"ids": trackid}
            headers = {
                "X-RapidAPI-Key": "c977989d98msh4b7faeefeaa84a8p18972ajsnaeb4f3b572d3",
                "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            storage = response.json()
            infolist = storage['tracks'][0]
            albuminfo = infolist['album']
            albumname = albuminfo['name']
            albumreleasedate = albuminfo['release_date']
            tracknum = infolist['track_number']
            listyear = albumreleasedate.split("-")
            year = listyear[0]
            year = int(year)
            auxfile = eyed3.load(fname)
            auxfile.tag.artist = artistname
            auxfile.tag.album = albumname
            auxfile.tag.title = trackname
            auxfile.tag.track = tracknum
            auxfile.tag.disk = 1
            auxfile.tag.year = Date(year)
            auxfile.tag.save()
            oldname = fname
            newname = f"{dl_dir}\\{title}.mp3"
            os.rename(oldname, newname)

        video = yt(self.link)
        s = video.streams
        v = s.get_lowest_resolution()
        d = v.download(output_path=dl_dir)
        mp4_file = str(d)
        mp3_file = str(d)[:-4] + ".mp3"
        videoclip = VideoFileClip(mp4_file)
        audioclip = videoclip.audio
        audioclip.write_audiofile(mp3_file)
        audioclip.close()
        videoclip.close()
        os.remove(mp4_file)
        getInfo(mp3_file)
        return d


class DlFromList(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lineCount = 0
        self.linesPassed = 0
        with open("DownloadList.txt", "r") as l:
            keywords = l.readlines()
            self.keywords = keywords

    def run(self):
        def getInfo(fname):
            print(fname)
            dldirlw = dl_dir.lower()
            bannedwords = [dldirlw, "\\", ".mp3", "(", ")", "[", '"', "]" "audio", "official audio", "officialaudio", "official video", "(offcialaudio)",
                           'feat', "ft.", "&", "ft", "visualizer", "lyrics", "lyrics video", "lyricsvideo", "official music video"
                           , "officialmusicvideo", "official lyric video", "officiallyricvideo", 'visualizer']
            filename = fname
            filename = filename.lower()
            for word in bannedwords:
                filename = filename.replace(word, "")
            print(filename)
            # Getting the song name
            url = "https://shazam.p.rapidapi.com/search"
            querystring = {"term": filename, "locale": "en-US", "offset": "0", "limit": "1"}
            headers = {
                "X-RapidAPI-Key": "c977989d98msh4b7faeefeaa84a8p18972ajsnaeb4f3b572d3",
                "X-RapidAPI-Host": "shazam.p.rapidapi.com"
            }
            rsp = requests.request("GET", url, headers=headers, params=querystring)
            print(rsp.text)
            storage = rsp.json()
            title = storage['tracks']['hits'][0]['track']['title']
            # Getting the info
            url = "https://spotify23.p.rapidapi.com/search/"
            querystring = {"q": title, "type": "tracks", "offset": "0", "limit": "1", "numberOfTopResults": "1"}
            headers = {
                "X-RapidAPI-Key": "c977989d98msh4b7faeefeaa84a8p18972ajsnaeb4f3b572d3",
                "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            storage = response.json()
            data = storage['tracks']['items'][0]['data']
            trackname = data['name']
            artistname = data['artists']['items'][0]['profile']['name']
            trackid = data['id']

            url = "https://spotify23.p.rapidapi.com/tracks/"
            querystring = {"ids": trackid}
            headers = {
                "X-RapidAPI-Key": "c977989d98msh4b7faeefeaa84a8p18972ajsnaeb4f3b572d3",
                "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            storage = response.json()
            infolist = storage['tracks'][0]
            albuminfo = infolist['album']
            albumname = albuminfo['name']
            albumreleasedate = albuminfo['release_date']
            tracknum = infolist['track_number']
            year = (str(albumreleasedate))[:-6]
            auxfile = eyed3.load(fname)
            auxfile.tag.artist = artistname
            auxfile.tag.album = albumname
            auxfile.tag.title = trackname
            auxfile.tag.track = tracknum
            auxfile.tag.disc = 1
            auxfile.tag.year = year
            auxfile.tag.save()
            oldname = fname
            newname = f"{dl_dir}\\{artistname}-{trackname}"
            os.rename(oldname, newname)

        for line in self.keywords:
            self.lineCount += 1
        for keyword in self.keywords:
            formated_txt = keyword.replace(" ", "+")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=official+audio+" + formated_txt)
            print(html)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            link = "https://www.youtube.com/watch?v=" + video_ids[0]
            video = yt(link)
            streams = video.streams
            aux = streams.get_lowest_resolution()
            d = aux.download(output_path=dl_dir)
            self.linesPassed += 1
            mp4_file = str(d)
            mp3_file = str(d)[:-4] + ".mp3"
            videoclip = VideoFileClip(mp4_file)
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file)
            audioclip.close()
            videoclip.close()
            os.remove(mp4_file)
            getInfo(mp3_file)


class MusicPlayer(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.shuffleValue = tkinter.BooleanVar(value=False)
        self.totalLines = 0
        self.config(padding=(50, 25))
        self.get_audios = ttk.Button(self, text="Get downloaded audios", command=self.getaux, style="TButton")
        self.get_audios.pack()
        self.lframe = ttk.Labelframe(self)
        self.lframe.pack(side=tkinter.TOP)
        self.infobar = ttk.Labelframe(self)
        self.infobar.pack(side=tkinter.BOTTOM)
        self.currently_playing = ttk.Label(self.infobar, text="")
        self.currently_playing.pack(side=tkinter.TOP)
        self.pause_play = ttk.Button(self.infobar, text="||", style="TButton", padding=(10, 10),
                                     command=self.Play_Pause)
        self.pause_play.pack(side=tkinter.TOP)
        self.skip = ttk.Button(self.infobar, text=">>", style="TButton", padding=(15, 10),
                               command=lambda: self.Next_Previous(1))
        self.skip.pack(side=tkinter.RIGHT)
        self.previous = ttk.Button(self.infobar, text="<<", style='TButton', padding=(15, 10),
                                   command=lambda: self.Next_Previous(0))
        self.previous.pack(side=tkinter.LEFT)
        self.shuffle = ttk.Radiobutton(self.infobar, text='Shuffle', value=False, variable=self.shuffleValue)
        # self.shuffle.pack(side=tkinter.RIGHT)
        self.currentFile = None

    def getaux(self):
        audios_list = glob(f"{dl_dir}/*.mp3")
        temp_file = open("imported_files_temp", "a")
        for f in audios_list:
            with open('imported_files_temp') as t_file:
                if os.stat("imported_files_temp").st_size != 0:
                    if f in t_file:
                        return
                    return
            temp_file.write(f + "\n")
            f_name = f.split(dl_dir)
            f_name = f_name[1]
            f_name = f_name.replace("\\", "")
            b = ttk.Button(self.lframe, text=f_name, style='TButton')
            b.pack()
            b.configure(command=lambda f=f: self.play(f))
            self.get_audios.destroy()

    def play(self, dir):
        print(dir)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unload()
            pygame.mixer.music.load(dir)
            pygame.mixer.music.play(loops=0)
            name = dir[10:]
            self.currently_playing.config(text=name)
        else:
            pygame.mixer.music.load(dir)
            pygame.mixer.music.play(loops=0)
            name = dir[10:]
            self.currently_playing.config(text=name)
            self.currentFile = dir

    def Play_Pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pause_play.config(text='|>')
        else:
            if pygame.mixer.music.get_pos() >= 1:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
            self.pause_play.config(text='||')

    def Next_Previous(self, v):
        temp_imports = open("imported_files_temp", "r")
        lines = temp_imports.readlines()
        #for line in lines:
            #self.totalLines += 1
        for line in lines:
            if not any(self.currentFile in line):
                newlines = []
                newlines.insert(line)
        nextMusic = random.choice(newlines)
        print(nextMusic)
        if v == 1:
            print("skip")
            # music = lines[nextMusic]
            # print(music)
            # pygame.mixer.music.unload()
            # pygame.mixer.music.load(f'C:\\Users\\Hamza\\OneDrive\\Bureau\\Yt-Dowloader[ALI]{music}')
            # pygame.mixer.music.play(loops=0)
        elif v == 0:
            print("previous")
        temp_imports.close()

    def Onclosing(self):
        isOpen['MusicPlayer'] = False
        with open("mpV.json", "w") as openFile:
            json.dump(isOpen, openFile, indent=1)
            openFile.close()
        self.destroy()


class Root(Tk):
    def __init__(self):
        super().__init__()

        self.title("Yt-Dl")
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.file_menu = Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label="Settings", command=self.OpenSettings)
        self.file_menu.add_command(label="Music Player", command=self.OpenMPlayer)
        self.menubar.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0
        )
        self.title_label = Label(self, text="Youtube video downloader, \n by SwirX")
        self.title_label.pack()
        self.textBox = ttk.Entry(self)
        self.textBox.pack()
        self.textBox.bind("<Return>", self.onclick)
        self.getvid_btn = ttk.Button(self, text="GetVideo", command=lambda: self.onclick(self), style='TButton')
        self.getvid_btn.pack()
        self.info = ttk.LabelFrame(self, text="Video info:")
        self.info.pack()
        self.vidTitle = ttk.Label(self.info, text="")
        self.vidTitle.pack(side="left")
        self.vidAuthor = ttk.Label(self.info, text="")
        self.vidAuthor.pack(side="right")
        self.vidLenght = ttk.Label(self.info, text="")
        self.vidLenght.pack()
        self.Views = ttk.Label(self.info, text="")
        self.Views.pack()
        self.Thumbnail = Label(self)
        # self.Thumbnail.pack()
        self.dlvid = ttk.Button(self, text="Download video", style='TButton')
        self.dlvid.pack(side="left")
        self.dlaux = ttk.Button(self, text="download audio", style='TButton')
        self.dlaux.pack(side="right")
        self.directory = Label(self, text="")
        self.directory.pack()
        self.downloadFromList = ttk.Button(self, text="Download from list", command=self.DlList, style='TButton')
        self.downloadFromList.pack()
        self.OpenList = ttk.Button(self, text="Open the list", command=self.openNotes, style="TButton")
        self.OpenList.pack()
        self.totalLinks = Label(self, text="")
        self.totalLinks.pack()
        # Values
        self.settingsopen = False
        self.AutoOpenMPlayer = tkinter.BooleanVar(value=False)
        self.AutoDelTempFiles = tkinter.BooleanVar(value=False)
        self.Theme = tkinter.IntVar(value=1)

    def openNotes(self):
        def open_file():
            filepath = "C:/Users/HP/Desktop/YoutubeDownloader/DownloadList.txt"
            txt_edit.delete(1.0, tkinter.END)
            with open(filepath, "r") as input_file:
                text = input_file.read()
                txt_edit.insert(tkinter.END, text)
            window.title(f"Text Editor Application - {filepath}")

        def getlines():
            text = txt_edit.get(1.0, tkinter.END)
            lines = text.count("\n")


        def save_file():
            filepath = "C:/Users/HP/Desktop/YoutubeDownloader/DownloadList.txt"
            if not filepath:
                return
            with open(filepath, "w") as output_file:
                text = txt_edit.get(1.0, tkinter.END)
                output_file.write(text)
            window.title(f"Text Editor Application - {filepath}")

        window = tkinter.Tk()
        window.title("Text Editor Application")
        window.rowconfigure(0, minsize=800, weight=1)
        window.columnconfigure(1, minsize=800, weight=1)

        txt_edit = tkinter.Text(window)
        open_file()
        fr_buttons = ttk.Frame(window, relief=tkinter.RAISED)
        btn_save = ttk.Button(fr_buttons, text="Save", command=save_file, style="TButton")
        btn_save.grid(row=1, column=0, sticky="ew", padx=5)
        lbl_lines = tkinter

        fr_buttons.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")

        window.mainloop()

    def onclick(self, instance):
        txt = self.textBox.get()
        formated_txt = txt.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + formated_txt)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        link = "https://www.youtube.com/watch?v=" + video_ids[0]
        with open("temp", "w") as temp:
            temp.write(link)
        video = yt(link)
        imgURL = video.thumbnail_url
        u = urlopen(imgURL)
        raw_data = u.read()
        u.close()
        # photo = ImageTk.PhotoImage(data=raw_data)
        self.vidTitle.configure(text=video.title)
        self.vidAuthor.configure(text=video.author)
        # self.Thumbnail.configure(image=photo)
        # self.Thumbnail.image = photo
        self.dlvid.configure(command=self.DownloadVid)
        self.dlaux.configure(command=self.DownloadAux)
        self.dlaux.pack(side="right")
        length = video.length
        self.vidLenght.configure(text=f'{math.floor(length / 60)}:{length - (math.floor(length / 60) * 60)}')
        views = video.views
        val = None
        if views > 1000 and views < 1000000:
            c = views / 1000
            views2 = "{:.2f}".format(float(c))
            val = views2 + "K views"
        elif views > 1000000 and views < 1000000000:
            c = views / 1000000
            views2 = "{:.2f}".format(float(c))
            val = views2 + "M views"
        elif views > 1000000000:
            c = views / 1000000000
            views2 = "{:.2f}".format(float(c))
            val = views2 + "B views"

        self.Views.configure(text=f'{val}')

    def DownloadVid(self):
        dl_thread = DownloadVid()
        dl_thread.start()

    def DownloadAux(self):
        dl_thread = DownloadAux()
        dl_thread.start()

    def DlList(self):
        dlfl_thread = DlFromList()
        dlfl_thread.start()

    def onDelete(self):
        answer = tkinter.messagebox.askyesno(title='Close',
                                             message='Are you sure that you want to quit?')
        if answer:
            with open("imported_files_temp", "w") as f:
                f.write("")
            with open("temp", "w") as temp:
                temp.write("")
            with open("choosen_file", "w") as c_file:
                c_file.write("")
            with open("settings.json", "w") as jsonFile:
                json.dump(settings_object, jsonFile, indent=1)
                jsonFile.close()

            self.destroy()
            exit()

    def OpenSettings(self):
        if self.settingsopen == False:
            def ToggleMplayer(v):
                v=not v
                settings_object['AutoOpenMusicPlayer'] = v
                self.AutoOpenMPlayer.set(v)
                print(f"AutoOpenMusicPlayer = {settings_object['AutoOpenMusicPlayer']}")

            def ToggleDelTempF(v):
                v= not v
                settings_object['AutoDeleteTempFiles'] = v
                self.AutoDelTempFiles.set(v)
                print(f"AutoDeleteTempFiles = {settings_object['AutoDeleteTempFiles']}")

            def ToggleTheme(v):
                if v == 1:
                    self.ChangeTheme.setvar(value=2)
                    settings_object['Theme'] = 2
                    try:
                        root.tk.call("set_theme", "light")
                        mplr.tk.call("set_theme", "light")
                        v=2
                    except:
                        print("couldn't change the theme")
                elif v == 2:
                    self.ChangeTheme.setvar(value=1)
                    settings_object['Theme'] = 1
                    try:
                        root.tk.call("set_theme", "dark")
                        mplr.tk.call("set_theme", "dark")
                        v=1
                    except:
                        print("couldn't change the theme")

            def ChangeDir():
                Dir = fd.askdirectory()
                settings_object['DownloadsDirectory'] = Dir

            self.SttgsFrame = Toplevel(self)
            self.SttgsFrame.title = "Settings"
            # AutoOpenMusicPlayer
            self.AutoOpenMsP = ttk.Checkbutton(self.SttgsFrame,
                                               text="Auto open the music player",
                                               variable=settings_object['AutoOpenMusicPlayer'],
                                               command=lambda: ToggleMplayer(settings_object['AutoOpenMusicPlayer']),
                                               style='Switch.TCheckbutton',
                                               onvalue=True,
                                               offvalue=False)

            self.AutoOpenMsP.pack()
            # AutoDeleteTempFiles
            self.AutoDeleteTempF = ttk.Checkbutton(self.SttgsFrame,
                                                   text="Auto delete the temp files after closing the app",
                                                   variable=settings_object['AutoDeleteTempFiles'],
                                                   command=lambda: ToggleDelTempF(
                                                       settings_object['AutoDeleteTempFiles']),
                                                   style='Switch.TCheckbutton',
                                                   onvalue=True,
                                                   offvalue=False)
            self.AutoDeleteTempF.pack()
            #ChangeTheme
            self.ChangeTheme = ttk.Button(self.SttgsFrame,
                                          text="toggle theme",
                                          command=lambda: ToggleTheme(settings_object['Theme']),
                                          style='TButton')
            self.ChangeTheme.pack()

            #ChangeTheDownloadDirectory
            self.btn_changeDir = ttk.Button(self.SttgsFrame,
                                            text="Change the download directory",
                                            command=ChangeDir)
            self.btn_changeDir.pack()

            self.settingsopen = True
        else:
            tkinter.messagebox.showerror(title="Error", message="Settings already open")

        def SttgsOnClosing():
            SyncValues()
            self.settingsopen = False
            self.SttgsFrame.destroy()

        self.SttgsFrame.protocol("WM_DELETE_WINDOW", SttgsOnClosing)

    def OpenMPlayer(self):
        if isOpen['MusicPlayer'] == True:
            pass
        elif not isOpen['MusicPlayer']:
            MPlayer = MusicPlayer()
            MPlayer.grid(row=0, column=0)
            # isOpen['MusicPlayer'] = True


def SyncValues():
    with open("settings.json", "w") as jsonFile:
        json.dump(settings_object, jsonFile, indent=1)
        jsonFile.close()


# music player settings
mplr = MusicPlayer()
if settings_object['AutoOpenMusicPlayer']:
    mplr.grid(row=0, column=0)
elif settings_object['AutoOpenMusicPlayer'] == False:
    mplr.destroy()

# main window settings
if __name__ == "__main__":
    root = Root()
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
    if settings_object['AutoOpenMusicPlayer']:
        root.AutoOpenMPlayer.set(True)
    elif settings_object['AutoOpenMusicPlayer'] == False:
        root.AutoOpenMPlayer.set(False)

    if settings_object['AutoDeleteTempFiles']:
        root.AutoDelTempFiles.set(True)
    elif settings_object['AutoDeleteTempFiles'] == False:
        root.AutoDelTempFiles.set(False)
    root.protocol("WM_DELETE_WINDOW", root.onDelete)

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    mplr.tk.call("source", "azure.tcl")
    if settings_object['Theme'] == 1:
        root.tk.call("set_theme", "dark")
        mplr.tk.call("set_theme", "dark")
    elif settings_object['Theme'] == 2:
        root.tk.call("set_theme", "light")
        mplr.tk.call("set_theme", "light")

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

    root.mainloop()
