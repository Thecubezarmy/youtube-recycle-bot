import queryfunction
from pytube import YouTube
from moviepy.editor import *
import moviepy.editor as mp
import re
from os import listdir
import os
from moviepy import *
import time
from natsort import natsorted
import random
from random import randrange
import datetime

#the tmp folder that is created to host the files
tgt_folder = "\youtube-recycle-bot\output"

#input
print("enter the number of songs")
videonumber=int(input())
listofsongs=[]
while videonumber > 0:
    print ("please type the name of the song")
    locallist=input()
    listofsongs.append(locallist)
    videonumber =  videonumber - 1

#downloads the files
for x in listofsongs:
    z=queryfunction.youtubequery(x)
    youtube_link = z
    w = YouTube(youtube_link).streams.first()
    w.download(output_path="\youtube-recycle-bot\output")

try:
    os.mkdir("\youtube-recycle-bot\images")
except FileExistsError :
    pass


#converts the mp4 to mp3 (make sure to change the output path so it does not interfere with the other code)
#for file in [n for n in os.listdir(tgt_folder) if re.search('mp4',n)]:
 #full_path = os.path.join(tgt_folder, file)
 #output_path = os.path.join(tgt_folder, os.path.splitext(file)[0] + '.mp3')
 #clip = mp.AudioFileClip(full_path)
 #clip.write_audiofile(output_path)

#renames the files for easier converion
filecounter = 0
for file_name in listdir(tgt_folder):
    try:
        os.rename(tgt_folder + "\\"+ file_name,tgt_folder + "\\"+"Video"+str(filecounter)+".mp4")
    except FileExistsError:
        os.remove(tgt_folder + "\\"+"Video"+str(filecounter)+".mp4")
        os.rename(tgt_folder + "\\"+ file_name,tgt_folder + "\\"+"Video"+str(filecounter)+".mp4")
    filecounter = filecounter + 1


fin = 0
#this makes all the small mp4 files into a big mp4 file
L =[]
for root, dirs, files in os.walk(tgt_folder):

    #files.sort()
    files = natsorted(files)
    for file in files:
        if os.path.splitext(file)[1] == '.mp4':
            filePath = os.path.join(root, file)
            video = VideoFileClip(filePath,has_mask=True)
            L.append(video)


#renames the image
imagecounter=0
for imagefile in [n for n in os.listdir("\youtube-recycle-bot"+"\\"+"images") if re.search('jpg',n)]:
    os.rename("\youtube-recycle-bot"+"\\"+"images"+"\\"+imagefile,"\youtube-recycle-bot"+"\\"+"images"+"\\"+str(imagecounter)+".jpg")
    imagecounter=imagecounter+1
#selects a random image
try:
   imagenumber=randrange(0,imagecounter)
except ValueError :
    imagenumber=0
    pass

#applies the image and contracarates the videos
logo = (mp.ImageClip("\youtube-recycle-bot"+"\\"+"images"+"\\"+str(imagenumber)+".jpg")
          .set_duration(concatenate_videoclips(L).duration)
          .set_pos(("center"))
          .resize(height=video.h, width=video.w))
final_clip = mp.CompositeVideoClip([concatenate_videoclips(L), logo])
try:
    final_clip.to_videofile(tgt_folder+"final"+ str(fin)+".mp4", fps=24, remove_temp=True)
except FileExistsError :
    fin=fin+randrange(1,999999999999)
    final_clip.to_videofile(tgt_folder+"final"+ str(fin)+".mp4", fps=24, remove_temp=True)
    pass


#removes the downloaded videos and leaves the contracarated one
for file_name in listdir(tgt_folder):
    time.sleep(1)
    os.remove(tgt_folder + "\\"+ file_name)
