# 
# {"type":"keyboard","top":0,"bottom":0,"left":0,"right":0,"rotateToLeft":0,"rotateToRight":0,"getUp":0,"getDown":0}
# {"type":"keyboard","top":0,"bottom":0,"left":0,"right":0,"rotateToLeft":0,"rotateToRight":0,"getUp":0,"getDown":0}
# {"type":"keyboard","top":0,"bottom":20,"left":0,"right":0,"rotateToLeft":0,"rotateToRight":0,"getUp":0,"getDown":0}
# {"type":"keyboard","top":20,"bottom":0,"left":0,"right":0,"rotateToLeft":0,"rotateToRight":0,"getUp":0,"getDown":0}
# disconnect

# proc = subprocess.Popen(["sudo","npm","run","--prefix ~/server/","custom_go_port_80"], stdout=subprocess.PIPE)
# powershell Get-Content -Path 'main.py' -Wait
proc = subprocess.Popen(["start","test.exe"], stdout=subprocess.PIPE)


from limb import *
import threading
import subprocess
import json
from time import sleep
import zme_ina219

bus = zme_ina219.smbus.Smbus(1)
ina = zme_ina219.INA219(bus)


def_inp = json.loads('{"type":"keyboard","top":0,"bottom":0,"left":0,"right":0,"rotateToLeft":0,"rotateToRight":0,"getUp":0,"getDown":0}')
inp_param = {}
stop = False

def parse_thread():
	global stop, def_inp, inp_param
	proc = subprocess.Popen(["powershell","Get-Content","-Path","parser.log","-Wait"], stdout=subprocess.PIPE)
	while not stop:
		inp_str = proc.stdout.readline()
		try:
			inp_param = json.loads(inp_str)
		except ValueError:
			print("fail value")
			inp_param = def_inp
	proc.terminate()

pars_thr = threading.Thread(target=parse_thread)
pars_thr.start()


def print_inp():
	while 1:
		print(inp_param)
		sleep(0.5)

left = inp_param["left"]
right = inp_param["right"]
top = inp_param["top"]
bottom = inp_param["bottom"]

curv = -(left / 10) + (right / 10)
direct = -(bottom / 10) + (top/10)

curv = direct + curv

if abs(curv) > 0.005 or abs(direct) > 0.02:
	distance = bot._distance * (2 / direct)

	bot.full_step(curv,distance)


import socket

sock = socket.socket()
sock.connect(('192.168.1.37', 80))
sock.send('hello, world!'.encode())

data = sock.recv(1024)
sock.close()

print data