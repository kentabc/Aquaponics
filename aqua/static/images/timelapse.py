from picamera import PiCamera
import os
import subprocess
from os import system
import smtplib

TO = 'wendell.clarke@gmail.com'
SUBJECT = 'Timelapse Ready'
TEXT = 'Hello Wendell Your Aquaponics timelapse video is ready'

gmail_user = 'wendell.clarke@gmail.com'
gmail_password = 'wendellp#123'



camera = PiCamera()


folders = []
files = []

for i in os.listdir("/home/pi/Dev/Aquaponics-Website/aqua/static/images"):
	if i.startswith("image"):
		folders.append(i)
num = len(folders)

if num < 29:
        camera.capture('/home/pi/Dev/Aquaponics-Website/aqua/static/images/image{0:02d}.jpg'.format(num))

else:
        os.system("rm -f timelapse.gif")
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user,gmail_password)
        msg = '\r\n'.join(['TO: %s'% TO,
                           'From: %s'%gmail_user,
                           'Subject: %s'% SUBJECT,
                           '',TEXT])
        server.sendmail(gmail_user,[TO],msg)
        os.system("/usr/local/bin/convert -delay 10 -loop 0 image*.jpg timelapse.gif")
        os.system("rm -rf image*")
        camera.capture('/home/pi/Dev/Aquaponics-Website/aqua/static/images/image00.jpg')
