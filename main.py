from bs4 import BeautifulSoup
import requests
import os
from threading  import Thread
import time

songlist=[]#contains names of songs with extension
singerof={}#contains singer of each song 

currdir=os.getcwd()
for item in os.listdir(currdir):
	if os.path.isdir(item) or item=="main.py":#item is a folder or this file
		continue
	songlist.append(item)

def getsinger(no,song):
	print ("Starting thread no %s at "%(no))+str(time.ctime(time.time()))
	r=requests.get("https://www.youtube.com/results?search_query="+song)
	data=r.text
	soup=BeautifulSoup(data)
	try:
		data=soup.find_all("a",class_="g-hovercard yt-uix-sessionlink      spf-link ")
		data=data[0]
		singer=data.string
	except:
		singer="Unknown Songs"#No singer found
	singer=singer.encode("utf-8")
	singerof[song]=singer	
	print ("Finished thread no %s at "%(no))+str(time.ctime(time.time()))

songlist_new=[]#contains names of songs w/o extension
for song in songlist:
	song=os.path.splitext(song)
	song=song[0]
	songlist_new.append(song)

t=[]#threads
	
def MAIN(l,r):
	for i in range(l,r):
		t.append(Thread(target=getsinger,args=(i,songlist_new[i])))
	for i in range(l,r):
		t[i].start()
		time.sleep(1)


def WAIT(l,r):#wait till all threads are finished
	for i in range(l,r):
		t[i].join()

def CREATE_AND_MOVE(l,r):#Creates folders and moves files
	for i in range(l,r):
		singer=singerof[songlist_new[i]]
		if not os.path.exists(singer):
			print "Creating Folder %s ......"%(singer)
			os.mkdir(singer)
		os.rename(songlist[i],singer+"/"+songlist[i])
		print "Moving %s....."%(songlist[i])		
	

for i in range(0,len(songlist),30):#Work in interval of 30 files 
	l=i
	r=min(i+30,len(songlist))
	MAIN(l,r)	
	WAIT(l,r)
	CREATE_AND_MOVE(l,r)
	

		


