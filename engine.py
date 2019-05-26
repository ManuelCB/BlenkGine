import importlib
import sys
import pygame
from pygame.locals import *
from os import rename
from os import getcwd
from os import listdir
from os.path import isfile, join, exists
from os import remove

next = None
totalrooms = 0
currentroom = 0
aobj = []
img = []
s = []
key = []
objs = []
rms = []
pos = []
ev = None
dir = None
q = []


sock = None
host = None
port = None

for i in range(5):
	key.append(False)


def map(t,a,w,ow,oh):
	a2 = []
	n = 0
	x = 0
	y = 0
	c = 0
	for i in t:
		if i != 0:
			a2.append(a[t[n]-1])
			a2.append(x*ow)
			a2.append(y*oh)
			c += 1
		x += 1
		if x == w:
			x = 0
			y += 1
		n += 1
	return a2, c
		
	

def getrooms(rooms, folder):
	global dir
	global rms
	dir = folder
	rms = rooms
	room = []
	n = 0
	for r in rooms:
		n = n + 1
		print("Room " + str(n) + ": " + r)
		room.append(importlib.import_module(folder + ".rooms." + r.replace(".py","")))	
	if n == 0:
		print("Error, no rooms!")
		exit(0)
	return room
	
def getobjects(v,folder):
	global objs
	objs = v
	n = 0
	t = []
	for r in v:
		n = n + 1
		t.append(importlib.import_module(folder + ".objects." + r.replace(".py","")))
		print("Object " + str(n) + ": " + r + " -> " + t[n-1].name)
	return t

def init(rm, o, p):
	global next
	global aobj
	global s
	global img
	next = False
	s.clear()
	p.clear()
	img.clear()
	aobj.clear()
	for n in range(rm.objn):
		putobject(rm.objs[n*3],rm.objs[n*3+1],rm.objs[n*3+2],o,p)

	

def putobject(name, x, y, o, p):
	global aobj
	global img
	global dir
	global q
	for i in o:
		if i.name == name:
			p.append([x,y])
			q.append([0,0])
			s.append(name)
			aobj.append(i)
			if i.sprite != None:
				img.append(pygame.image.load(join(getcwd(),dir,"sprites",i.sprite)).convert())
			return 
	print("Error, object " + name + " not found!")
	exit(0)
	
		
	
		
def run(o, r, p):
	a = 0
	b = 0
	global totalrooms
	global key
	global pos
	global ev
	global q 
	pos = p
	n = 0
	
	for i in aobj:
		
		
		p[n] = i.process(p[n][0],p[n][1],key)
		q[n] = i.process(p[n][0],p[n][1],key)
		
		e = []
		for g in range(4):
			e.append(0)
		m = 0
		
		e = i.events(ev)
		if e[0] == "create":
			putobject(e[1],e[2],e[3],o,p)
		if e[0] == "destroy":
			del p[n]
			del aobj[n]
			del s[n]
			del img[n]
			if n > 0:
				n = n - 1
		for j in p:
				
			x = p[n][0]
			y = p[n][1]
			
			x2 = p[m][0]
			y2 = p[m][1]
				
			w = r[currentroom].objw
			h = r[currentroom].objh
						
			totalrooms = len(r)	
						
			if n != m and x + w > x2 and x < x2 + w and y + h > y2 and y < y2 + h:
				collision = i.col(s[m])
				if collision == "destroy other":
					del p[m]
					del aobj[m]
					del s[m]
					del img[m]
				if collision == "destroy self":
					del p[n]
					del aobj[n]
					del s[n]
					del img[n]
				if collision == "collide":
					p[n][1] -= q[n][1] - p[n][1]
					p[n][0] -= q[n][0] - p[n][0]			
		
			m = m + 1
				
		if img[n] != None:
			img[n] = pygame.image.load(join(getcwd(),dir,"sprites",i.sprite)).convert()	
			screen.blit(img[n], (p[n][0],p[n][1]))

		
		
			
		n = n + 1		
				
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial",16)

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))			

def printw(t,x,y,c):
	global font
	txt = font.render(t,False,c)
	screen.blit(txt,(x,y))

def engine(r, o, p):			
	global ev
	while True:
		print("room " + str(currentroom) + " started")
		init(r[currentroom],o,p)
		print(str(next))
		while not next:
			k = pygame.key.get_pressed()
			key[0] = k[K_RIGHT]
			key[1] = k[K_LEFT]
			key[2] = k[K_UP]
			key[3] = k[K_DOWN]
			key[4] = k[K_SPACE]
			fpsClock.tick(fps)
			for event in pygame.event.get():
				ev = event
				if event.type==pygame.QUIT:
					pygame.quit()
					exit(0)
			run(o, r, p)
			pygame.display.flip()
			screen.fill((0,0,0))
			if next == True:
				break
		print(str(next))