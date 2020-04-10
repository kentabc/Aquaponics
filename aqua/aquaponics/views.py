from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PostForm, FishForm, HarvestForm, PlanttypeForm, FishtypeForm, schedform, schedform1, taskform, watertest, formnotes, cropnotes, fishnotes
from .models import plant, fish, harvest, plant_type, fish_type, schedule, tasks, testing, notes
from django.db.models import Q
from django.conf import settings
import datetime
from django.core.mail import send_mail
import pyowm
import matplotlib.pyplot as plt
from datetime import timedelta, date
#from pushetta import Pushetta

import RPi.GPIO as GPIO
import time
import glob
import os

GPIO.setmode(GPIO.BCM)




today = datetime.date.today()

#Weather Information
try:
    weather_key = 'c92353d84b9e42deb88ef7bcd84ecf36'
    owm = pyowm.OWM(weather_key)
    observe = owm.weather_at_place('tunapuna')
    wedstat = observe.get_weather()
    forecast = wedstat.get_status()
    icon = wedstat.get_weather_icon_url()
except:
    forecast = "Weather info unavailable"

def index(request):
    #Pushetta config
    email_person = 'wendell.clarke@gmail.com'
    sched = schedule.objects.all()
    noteinfo = notes.objects.all()

    #Fish Data
    
    fishdata = fish.objects.all()



    for i in sched:
        if i.task_date == today:
            event = i.task
            send_mail(
                        'Aquaponic Schedule',
                        'Hello Wendell Your schedule for today is: {}'.format(event),
                        email_person,
                        [email_person],
                        fail_silently=False,
                   )
                            
    query = request.GET.get("q")
    if query:
        noteinfo = noteinfo.filter(
            Q(title__icontains=query)|
            Q(notes__icontains=query)
            
            ).distinct()
    
    quality = testing.objects.all()
    fivedays = today + datetime.timedelta(days = 5)

    #Temperature Sensor Water
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir1 = open("/sys/bus/w1/devices/28-0517c10752ff/w1_slave")
    thetext = base_dir1.read()
    base_dir1.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    temp_c = float(tempdata[2:])
    temp_c = round(temp_c / 1000,1)
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    temp_f = round(temp_f,1)

    #Temperature Sensor Atmosphere    
    base_dir2 = open("/sys/bus/w1/devices/28-0517c11a1cff/w1_slave")
    thetext1 = base_dir2.read()
    base_dir2.close()
    tempdata1 = thetext1.split("\n")[1].split(" ")[9]
    temp_c1 = float(tempdata1[2:])
    temp_c1 = round(temp_c1 / 1000,1)
    temp_f1 = temp_c1 * 9.0 / 5.0 + 32.0
    temp_f1 = round(temp_f1,1)
    
    



    #Distance Measurements with Ultrasonic Sensor..
    TRIG = 23
    ECHO = 24

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    
    distance = round(distance, 2)
    foot = distance / 30.48
    foot = round(foot,2)
    #inches = distance / 2.54
    inches = foot * 12
    inches = round(inches,2)
    folders = []
    for c in os.listdir("/home/pi/Dev/Aquaponics-Website/aqua/static/images"):
        if c.startswith("image"):
            folders.append(c)
    pic = max(folders) 

    context = {
        "today":today,
        "forecast":forecast,
        "icon":icon,
        "sched":sched,
        "fivedays":fivedays,
        "quality":quality,
        "noteinfo":noteinfo,
        "distance":distance,
        "foot":foot,
        "inches":inches,
        "temp_c":temp_c,
        "temp_f":temp_f,
        "temp_c1":temp_c1,
        "temp_f1":temp_f1,
        "pic":pic,
        "fishdata":fishdata,
        
        
        
    }
    return render(request, 'index.html', context)



def schedulefrm(request, id):
    schedinstance = get_object_or_404(schedule, id=id)
    schedfor = schedform(request.POST or None, instance=schedinstance)
    sched = schedule.objects.all()
    if schedfor.is_valid():
        instance = schedfor.save(commit=False)
        instance.save()
        return HttpResponse("<br><br><center><h1>Updated</h1></center>")

    context = {
        "schedfor":schedfor,
        "schedinstance":schedinstance,
        "forecast":forecast,
        "icon":icon,
        "today":today,
        "sched":sched,
    }
    return render(request, 'schedule.html',context)

def schedules(request):
    scheds = schedule.objects.all()
    schedfor = schedform1(request.POST or None)
    
    
    if schedfor.is_valid():
        instance = schedfor.save(commit=False)
        instance.save()
        return HttpResponse("<br><br><center><h1>Schedule Added</h1></center>")
    
    context = {
        "schedfor":schedfor,
        "forecast":forecast,
        "icon":icon,
        "today":today,
        "scheds":scheds,
        "today":today,
    }
    return render(request, 'schedulefrm.html',context)


def forms(request):
    forms = PostForm(request.POST or None)
    if forms.is_valid():
        instance = forms.save(commit=False)
        instance.save()
        return HttpResponse("Thank You")
    context = {
        "forms":forms,
        "today":today,
        "forecast":forecast,
        "icon":icon,
    }
    
    return render(request, 'forms.html', context)

# Crop Info
def forms_detail(request, id):
    instance = get_object_or_404(plant, id=id)

    context = {
        "instance": instance,
        "forecast":forecast,
        "icon":icon,

    }
    return render(request, 'crop_detail.html', context)

def editcrop(request, id):
    cropinstance = get_object_or_404(plant, id=id)
    cropfor = cropnotes(request.POST or None, instance=cropinstance)
    cropinfo = notes.objects.all()
    
    if cropfor.is_valid():
        instance = cropfor.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Updated")
        return redirect("review")
    context = {
        "cropfor":cropfor,
        "cropinstance":cropinstance,
        "forecast":forecast,
        "icon":icon,
        "today":today,
        "cropinfo":cropinfo,
        
    }
    return render(request, 'editcrop.html',context)

def fish_detail(request, id):
    instance = get_object_or_404(fish, id=id)

    context = {
        "instance": instance,
        "forecast":forecast,
        "icon":icon,

    }
    return render(request, 'fish_detail.html', context)

#Fish Info
def editfish(request, id):
    fishinstance = get_object_or_404(fish, id=id)
    fishfor = fishnotes(request.POST or None, instance=fishinstance)
    fishinfo = notes.objects.all()
    
    if fishfor.is_valid():
        instance = fishfor.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Updated")
        return redirect("review")
    context = {
        "fishfor":fishfor,
        "fishinstance":fishinstance,
        "forecast":forecast,
        "today":today,
        "icon":icon,
        "fishinfo":fishinfo,
        
    }
    return render(request, 'editfish.html',context)

def fishform(request):
    fishfrm = FishForm(request.POST or None)
    if fishfrm.is_valid():
        instance = fishfrm.save(commit=False)
        instance.save()
        return HttpResponse("Fish Enterd")
    context = {
        "fishformm":fishfrm,
        "today":today,
        "icon":icon,
        "forecast":forecast,
    }
    return render(request, 'fishes.html', context)

def harvestform(request):
    hav = harvest.objects.all()
    harvform = HarvestForm(request.POST or None)
    if harvform.is_valid():
        instance = harvform.save(commit=False)
        instance.save()
        return HttpResponse("Harvest Entered")
    context = {
        "harvestfrm":harvform,
        "forecast":forecast,
        "icon":icon,
        "today":today,
        "hav":hav,
    }
    return render(request, "harvest_form.html", context)

def planttype_frm(request):
    p = plant_type.objects.all()
    ptypeform = PlanttypeForm(request.POST or None)
    if ptypeform.is_valid():
        instance = ptypeform.save(commit=False)
        instance.save()
        return HttpResponse("Plant Type Entered")
    context = {
        "ptypeform":ptypeform,
        "forecast":forecast,
        "icon":icon,
        "today":today,
        "p":p,
    }
    return render(request, "plant_type.html", context)

def fishtype_frm(request):
    fstypeform = FishtypeForm(request.POST or None)
    if fstypeform.is_valid():
        instance = fstypeform.save(commit=False)
        instance.save()
        return HttpResponse("Fish Type Entered")
    context = {
        "forecast":forecast,
        "fstypeform":fstypeform,
        "icon":icon,
        "forecast":forecast,
        "today":today,
    }
    return render(request, "fish_type.html", context)


def review(request):
    show = plant.objects.all()
    fishh = fish.objects.all()

    query = request.GET.get("q")
    if query:
        show = show.filter(
            Q(crop__icontains=query)|
            Q(plant_type__plant_name__icontains=query)|
            Q(comment__icontains=query)

            ).distinct()

    query1 = request.GET.get("r")
    if query1:
        fishh = fishh.filter(
            Q(crop__icontains=query1)|
            Q(fish_type__fish_name__icontains=query1)|
            Q(comment__icontains=query1)

            ).distinct()

    context = {
        "plantt":show,
        "fishh":fishh,
        "today":today,
        "forecast":forecast,
        "icon":icon,
        
    }
    return render(request, 'review.html', context)

def review_h(request):
    harv = harvest.objects.all()
    planttyp = plant_type.objects.all()
    fishtyp = fish_type.objects.all()


    context = {
        "harvest":harv,
        "planttyp":planttyp,
        "fishtyp":fishtyp,
        "today":today,
        "forecast":forecast,
        "icon":icon,
    }

    return render(request, 'review_harvest.html', context)

def task(request):

    work = tasks.objects.all()
    formtask = taskform(request.POST or None)
    if formtask.is_valid():
        instance = formtask.save(commit=False)
        instance.save()
        return HttpResponse("<br><br><center><h1>Task Entered</h1></center>")

    context={
        "work":work,
        "formtask":formtask,
        "icon":icon,
        "forecast":forecast,
        "today":today,

    }
    return render(request, "scheduletask.html", context)

def taskfrm(request, id):
    taskinstance = get_object_or_404(tasks, id=id)
    taskfor = taskform(request.POST or None, instance=taskinstance)
    taskinfo = tasks.objects.all()
    
    if taskfor.is_valid():
        instance = taskfor.save(commit=False)
        instance.save()
        return HttpResponse("<br><br><center><h1>Updated</h1></center>")
    context = {
        "taskfor":taskfor,
        "taskinstance":taskinstance,
        "forecast":forecast,
        "icon":icon,
        "today":today,
        "taskinfo":taskinfo,
        


    }
    return render(request, 'updatetask.html',context)

def testwater(request):
    quality = testing.objects.all()
    testform = watertest(request.POST or None)
    if testform.is_valid():
        instance = testform.save(commit=False)
        instance.save()
        return HttpResponse("<br><br><center><h1>Water Tests Added</h1></center>")
    context = {
        "quality":quality,
        "testform":testform,
        "forecast":forecast,
        "icon":icon,
        "today":today,

    }
    return render(request,"watertest.html",context)

def watergraph(request):
    context = {
        "forecast":forecast,
        "icon":icon,
        "today":today

    }
    return render(request,"watergraph.html",context)


def systemnotes(request):

    noteform = formnotes(request.POST or None)
    if noteform.is_valid():
        instance = noteform.save(commit=False)
        instance.save()
        # return HttpResponse("<br><br><center><h1>Note Entered</h1></center>")
        messages.success(request,"Successfully Created")
        return redirect("index")
    context = {
        "forecast":forecast,
        "icon":icon,
        "today":today,
        "noteform":noteform

    }
    return render(request, "notes.html", context)

def viewnote(request, id):
    noteinstance = get_object_or_404(notes, id=id)
    
    
    context = {
        
        "noteinstance":noteinstance,
        "forecast":forecast,
        "icon":icon,
        "today":today,
        
    }
    return render(request, 'viewnote.html',context)

def editnote(request, id):
    noteinstance = get_object_or_404(notes, id=id)
    notefor = formnotes(request.POST or None, instance=noteinstance)
    noteinfo = notes.objects.all()
    
    if notefor.is_valid():
        instance = notefor.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Updated")
        return redirect("index")
    context = {
        "notefor":notefor,
        "noteinstance":noteinstance,
        "forecast":forecast,
        "icon":icon,
        "today":today,
        "noteinfo":noteinfo,
        
    }
    return render(request, 'editnote.html',context)

def deletenote(request, id=None):
    noteinstance = get_object_or_404(notes, id=id)
    noteinstance.delete()
    messages.success(request,"Successfully Deleted")
    return redirect("index")

def viewshed(request, id):
    shedinstance = get_object_or_404(schedule, id=id)

    context = {
            "shedinstance":shedinstance,
            "today":today,
    }
    return render(request, 'viewshed.html',context)

def deletesched(request, id=None):
    sinstance = get_object_or_404(schedule, id=id)
    sinstance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("index")

