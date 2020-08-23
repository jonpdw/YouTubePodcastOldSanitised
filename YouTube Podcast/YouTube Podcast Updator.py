#!/usr/bin/env python

import subprocess
import pickle
from tqdm import tqdm
import json
import glob
import os
import dropbox
from datetime import datetime
from email import utils
import string
import re

def removeEmojiFromName(name):
    rgx = re.compile('[^' + ''.join(string.printable) + ']')
    return rgx.sub('', name)



import sys
# Overview: There are two main parts. Download all the videos and then make an RSS
# We use youtube-dl to get a list of all the urls (converted from a json file with other information). We go through this list and call another youtube-dl command that downloads them into a dropbox folder
# We then get all the file names of the mp3's in the dropbox folder and loop over them getting the right information to make each file an rss item

#
# Download all the videos
#

# Settings



pathToFolder = os.path.dirname(os.path.realpath(__file__))

try:
    with open(pathToFolder+"/savedLinks.pk", "rb") as handle:
        videosAlreadyDownloaded = pickle.load(handle)
except FileNotFoundError:
        with open(pathToFolder+"/savedLinks.pk", "wb") as handle:
            pickle.dump([], handle)
        videosAlreadyDownloaded = []



# playlistCode = "PL6Lov5dUqTok1DPMz2sSEVvPJuRMlrpJE"
# # Use YouTube-dl to get a list of all the videos in a form like this [{"_type":"url","url":"59ieh3thfk"}...]
# videoListJSON = subprocess.getoutput("youtube-dl -j --flat-playlist {}".format(playlistCode)).split("\n")
# videoListURLs = []
# for i in videoListJSON:
#     videoListURLs.append(json.loads(i).get("url"))

# Use YouTube-dl to get a list of all the videos in a form like this [{"_type":"url","url":"59ieh3thfk"}...]
videoListJSON = subprocess.getoutput("youtube-dl --cookies=/Users/jonathan/Dropbox/YouTube\ Podcast/cookies.txt :ytwatchlater -j --flat-playlist --no-warnings").split("\n")
videoListURLs = []
for i in videoListJSON:
    # print(i, file=sys.stderr)
    a = json.loads(i)
    b = a.get("url")
    videoListURLs.append(b)

# videoListURLs = ['5lliH0x4Mfk', 'HY_OIwideLg', 'gbAnHHyr4JA', 'Ig8w0BDAhLg', '-O5kNPlUV7w', 'ohyai6GIRZg', 'buD2RM0xChM', 'ATlila3e9dM', 'CPBJgpK0Ulc', 'ba1V6dBmZkM', 'ZCU8wxCdKIE', 'OAeJtF_g9GU', 'TGDRML3IX3s', 'zbzT00Cyq-g', '4ab2ZeZ-krY', 'MYkUfIfF-C8', '5LI2nYhGhYM', 'AOd4k1ernuk', 'xACCfHQ7WXc', 'JN6_K6ALeZI', 'Mbc_yzB8oAY', 'ZQ--scjcAZ4', 'KW0eUrUiyxo', 'Sa_ElKOHSsU', 'rqRIPwEW0rk', '00zh6X_0_3c', 'eV8RcOfYidI', 'ZwGhd6XAaeo', 'rTcAYv76im8', 'Cod4TEKq_qA', 'ZEI9YueX0O4', '8qUkm6U31Zo', 'xZ6OVnBnSAI', '1tVr4DNjlE0', 'iciSFPyjM78', 'vTDm_pa0JSM', 'mejakc7HTIs', 'tmU8jDTkSOY', 'VBW3NjZXMII', '2-YiMGEVMns', 'FBpry4OYbyE', 'QGhUiQXo3CA', '2zqLku10qfs', 'zet3ciKDIYE', '5DH9lAqNTG0', 'dDGeISed3Tg', 'w6kUOjJ98cY', 'Rvm_4qJYMzI', 'Rs1vxKsBdxg', 't0ym7XQZ-Hw', 'BdRgA7K4DcE', '4wszzgOnJ5U', '37KieyXOYG4', '7cGrg2Gh4gg', 'qoMkgbGDXxQ', 'qGgIC1GkBCw', 'Nd3zqXro_P0', '1ETSnQZOssc', 'v-ps2nfkAiA', 'j2qj01KI9hk', '3vDmWFTvzto', 'v34NqCbAA1c', 'v8F4jrtZtNE', 'ldmPgQZ52Ec', 'y5NhHBjyJe4', 'BFeuOmKYWmA', '3yaHBdhIsCo', 'SxsH8zEhEkk', '73kIG3HcFq0', '4PcpGxihPac', 'iNsTzqwwioY', 'O76BvUL2RuY', 'yjdhNyEmYpo', 'u6Zbykf7hqk', 'jC4jSlJ4Qeo', '8C_uRDPQvSE', 'uWM2E9oHlhA', 'Cf7Ar3nEUmw', 'VQTyRVBkeIw', 'Aq4g-Bv2_Gk', 'AYrsYrdJaUw', 'GTcM7ydgAwo', 'Qo52KfvdUUY', 'VldJrHVNHF8', 'DSc8q1ONH0o', 'M7Qm_UJML54', 'Vkoc0ltIBF4', 'EFtbwP4UuFM', '5USjeQR18WI', 'aOgaa7FcwUg', 'WAIUkjsZ5xQ', 'lfTwqw_gyKs', '4xGawJIseNY', 'iCHe52nnvlU', 'XayG1qkZg9E', 'NjbmUhKpp7k', '-wXppi_OfEo', 'DAPq2GUUhiY', 'c1iYr9Eog2k', 'F7lhFWinBTg', '_JxZY3d7kw0', 'HUti6vGctQM', 'nyFglwN04yc', 'hxhbOvR2TGk', 'vhsZusKc5zI', 'JBlm4wnjNMY', 'wJC2JW0n8Tc', 'DIs5dCX1XW4', '7M8FpYUyd9Y', 'Fh-BchpGXD0', 'sheqhcrE1gs', 'ib-aTfyXs98', 't6sjyVDNa90', 'KH2Or6Gi2hQ', 'mU3pvZHv-dE', 'Nigoh29fTT0', 'JBkDNkJD7RI', 'FQ537RhxbNg', 'x-FYe53LRA4', 'yuezK1FpuR8', 'P3RXtoYCW4M', 'dxhj4Jg3dzU', 'TrYc0-NSZZg', 'F9sbMVkdCcY', 'O3K2thH1goE', 'FQWmz9-P0Bg', 'lIp5MNoRVJU', 'ot02hMJ6Hkk', '9l4OPpCqwEM', 'KK3sH-mpCEI', 'iBErp8qvWZg', 'yoX0vEDn5a4', 'dPor8IoZ3Bw', 'DS2DOEkorDo', 'iFRIucFc0Cs', '7_afNW6Ln1E', '1Q5cPfbmSD8', '6aUm0oxf32g', 'UiY6wr--0dE', 'ARb2UfDgSHQ', 'tlzIzdJ3Exg', '4RMN-C0ezzI', 'akWAc3ju_Hg', 'w6VcbH2ypMg', '7Y_H-a4wfG0', 'gQQrrCjZyPc', '7LscnZCzdak', 'SrK5NAgw_g4', 'SlkLa9Ezt00', 'eSFA1Fp8jcU', 'JJPIqEu73Ak', 'wljRiAofFJ8', '8P1PrmEkScw', 'O6lENrRANxY', 'B4gXsobd_ao', '6Qqc3gL3oHE', 'JrRRvqgYgT0', 'rQy4gPjUY-s', 'Rhcrbcg8HBw', 'L28OLYtxXjs', 'S3FE9_204Yg', 'Ri9Y2rT70FE', 'ZpT0cw9bmiw', 'x7vfyzx2aAo', 'adQKtpCysOc', 'tTqkQluTtLM', '8Jbvik4IA3o', '5KZx81crb48', 'sPug0GxWQNg', 'q1LetVyCMb0', 'LdGjKOnxLtE', 'Y73laz3etM8', '0wNk25KEBpw', 'cO8rIht80TU', 'cfzkBGgxXGE', 'TazyFTavMyA', 'PineU9ZZvSc', 'SO0oBpl8G_Y', 'lLLGwXFh5uw', 'CneL0GoZ3tk', 'EH-z9gE2uGY', 'SvbTFwXagdQ', 'jFCLFfz_pz0', 'yP1UjCb0J1g', 'psaCM1j9LEM', 'maDdO2pBgsc', 'VzVAdUIBBSk', 'eVajQPuRmk8', '1RA2Zy_IZfQ', 'Phl82D57P58', '16W7c0mb-rE', 'Erp8IAUouus', 'VzPD009qTN4', 'z_Nn2qMZXjA', 'my2FQK5hHic', 'y9Trdafp83U', 'MlJdMr3O5J4', 'GdRjS3P2Zos', 'UAhRf3U50lM', 'CuorsbghT5M', 'kKDXmWFVN-g', 'IbSCM1GAjA4', 'NnXRQ_j_xB4', 'WSKi8HfcxEk', 'kJzSzGbfc0k', 'vKXVtdkmZbs', 'eTFy8RnUkoU', 'HmZs6_CJ_u8', '5J6jAC6XxAI', '3p-lyt78cyA', 'dLYUc5t6wag', 'G-2YVb_nPPM', 'TROA_0RxZmM', 'Q5pggDCnt5M', 'KHsSAz6nRrk', 'UBaVek2oTtc', '7g1pmHSWHe0', 'ap10MToOhVM', 'fTu8jzVXTi0', 'yU2kANHyF1w', 'C4kuR1gyOeQ', '1Y1kJpHBn50', 'aiI5iYxg1JQ', 'TPCpXXBHFSA', 'kqGKMaCAao4']

#tqdm displays the progress bar
for video in tqdm(videoListURLs, disable=True):
    if video not in videosAlreadyDownloaded:
        videosAlreadyDownloaded.append(video)
        bashCommand = format("youtube-dl -o '{path}/mp3/%(uploader)s - %(title)s.%(ext)s' -x " \
                      "--audio-format mp3 https://www.youtube.com/watch?v={videoCode}".format(videoCode = video, path = pathToFolder))
        videoListJSON = subprocess.check_output(['bash', '-c', bashCommand])

        # Save each video we convert incase we have to stop the loop half way
        with open(pathToFolder+"/savedLinks.pk", "wb") as handle:
            pickle.dump(videosAlreadyDownloaded, handle)

#
# Make RSS Feed
#

#Open acsess with dropbox. This allows me to do the Get_Shared_Link thing
dbx = dropbox.Dropbox("tU3uIkwPSrgAAAAAAACiJ-Ai04Sc-6nE6vHiiMG_4ZYK7-PQQ2ZUeIELJJ8_3A39")

RSSstartingBit = \
"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>A - YouTube Podcast</title>
    <link>https://youtube.com/playlist?list=PL6Lov5dUqTok1DPMz2sSEVvPJuRMlrpJE</link>
    <description>Jonathan De wet: YouTube Playlist</description>
    <category>TV &amp; Film</category>
    <generator>Podsync generator</generator>
    <language>en-us</language>
    <lastBuildDate>Sun, 17 Feb 2019 17:20:25 +0000</lastBuildDate>
    <pubDate>{}</pubDate>
    <image>
      <url>https://dl.dropboxusercontent.com/s/b2wq68cz2q2b8cq/YouTube.jpg?dl=0</url>
      <title>Jonathan De wet: YouTube Playlist 0</title>
      <link>https://youtube.com/playlist?list=PL6Lov5dUqTok1DPMz2sSEVvPJuRMlrpJE</link>
    </image>
    <itunes:author>Jonathan De wet: YouTube Playlist 0</itunes:author>
    <itunes:subtitle>Jonathan De wet: YouTube Playlist 0</itunes:subtitle>
    <itunes:summary><![CDATA[Jonathan De wet: YouTube Playlist 0 (2019-02-17 12:54:41 +0000 UTC)]]></itunes:summary>
    <itunes:image href="https://dl.dropboxusercontent.com/s/b2wq68cz2q2b8cq/YouTube.jpg?dl=0"></itunes:image>
    <itunes:explicit>no</itunes:explicit>
    <itunes:category text="TV &amp; Film"></itunes:category>""".format(utils.formatdate(datetime.timestamp(datetime.now())))

RSSendingBit = \
"""
</channel>
</rss>
"""

RSSitemBitTemplate = \
"""
<item>
<title>{title}</title>
<link>https://zapier.com</link>
<description></description>
<author>jonpdw@gmail.com (Jonathan)</author>
<pubDate>{pubDate}</pubDate>
<guid isPermaLink="false">{id}</guid>
<enclosure url="{url}" length="{bytes}" type="audio/mpeg"/>
</item>
"""

RSSstring = ""
RSSstring += RSSstartingBit

#This makes a list of all the mp3 files
mp3files = []
for file in glob.glob(pathToFolder+"/mp3/*.mp3"):
    newFileName = removeEmojiFromName(file)
    os.rename(file, newFileName)
    mp3files.append(newFileName)


# RSSItems = {}
# # ## Uncomment me when you want to clear the pickel for saved RSS items
# with open("preLoadedMP3Files.pk", "wb") as handle:
#     pickle.dump(RSSItems, handle)

with open(pathToFolder+"/preLoadedMP3Files.pk", "rb") as handle:
    RSSItems = pickle.load(handle)

import time
time.sleep(5)

numOfNewFiles = 0

for file in tqdm(mp3files, disable=True):
    if file in RSSItems:
        RSSstring += RSSItems[file]
    else:
        numOfNewFiles += 1
        fileName = os.path.basename(file)
        fileBytes = os.path.getsize(file)

        x = 1
        while(x):
            try:
                try:
                    #this gets the sharing link if it hasn't been created before
                    fileURL = dbx.sharing_create_shared_link_with_settings("/YouTube Podcast/mp3/{}".format(fileName)).url
                except:
                    #this gets the sharing link if it has been created before
                    fileURL = dbx.sharing_list_shared_links(path="/YouTube Podcast/mp3/{}".format(fileName)).links[0].url
                x = 0
            except:
                if x > 5:
                    raise RuntimeError("Time out getting a dropbox link")
                x+=1
                time.sleep(5)


        # I need to change these things so that the file is a direct link and not a link to a dropbox page
        fileURL = fileURL.replace("dl=0", "dl=1", 1)
        fileURL = fileURL.replace("www.dropbox.com", "dl.dropboxusercontent.com", 1)


        filePubDate = utils.formatdate(datetime.timestamp(datetime.now()))

        tempRSSitemBit = RSSitemBitTemplate
        a = tempRSSitemBit.format(title=fileName[:-4], url=fileURL, bytes=fileBytes, id=fileName, pubDate=filePubDate)
        RSSstring += a
        RSSItems[file] = a


with open(pathToFolder+"/preLoadedMP3Files.pk", "wb") as handle:
    pickle.dump(RSSItems, handle)

RSSstring += RSSendingBit

#Save our beautifully created rss file
with open(pathToFolder+"/YouTube Podcast.rss", "w") as f:
    f.write(RSSstring)

print("{} new files created".format(numOfNewFiles))
