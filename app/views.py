from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect,Http404,HttpResponse, JsonResponse
from app.models import *
import random
from django.shortcuts import render, render_to_response, redirect
from django.db.models import Avg
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import sh
import pxssh
import socket

@csrf_exempt
def loginUser(request):
	email=request.POST['email']
	password=request.POST['password']
	user = authenticate(username=email,password=password)
	userpro = UserProfile.objects.get(user=user)
	if user:
		login(request, user)
		return redirect("../home/")
	else:
		error1="Login UnSucessfull Please try Again..."
		return HttpResponse("Error")

@csrf_exempt
def registerUser(request):
	name = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	user = User(username=email, email=email, password=password, first_name=name)
	user.set_password(password)
	user.save()
	userpro = UserProfile(user=user)
	userpro.save()
	login(request, user)
	return HttpResponse("yo")

def home(request):
	user = request.user
	if user.is_authenticated():
		return HttpResponse("Logged in hai bhai banda!")
	else:
		return render(request, "login.html")

@login_required
def scanIPRange(request):
	start_ip = request.GET['start_ip']
	end_ip = request.GET['end_ip']
	
	begin = list(map(int,start_ip.split('.')))
	end = list(map(int,end_ip.split('.')))
	iprange=[]
	while begin!=list(map(int,end_ip.split('.'))):
	    for i in range(len(begin)-1,-1,-1):
	        if begin[i]<255:
	            begin[i]+=1
	            break
	        else:
	            begin[i]=0
	    iprange.append('.'.join(map(str,begin)))
	print iprange

	working_iplist = []

	for address in iprange:

	    # check if host is alive using PING
	    try:
	        # bash equivalent: ping -c 1 > /dev/null
	        sh.ping(address, "-c 1", _out="/dev/null")
	        working_iplist.append(address)
	        print "ping to", address, "OK"
	    except sh.ErrorReturnCode_1:
	        print "no response from", address

	return HttpResponse(iplist)

@login_required
@csrf_exempt
def getInfo(request):
	ip = request.POST['ip']
	username = request.POST['username']
	password = request.POST['password']
	try:
		name = socket.gethostbyaddr(ip)
	except:
		name = "unknown host"
		print "unknown host"
	try:                                                            
	    s = pxssh.pxssh()
	    ip = "128.199.157.163"
	    username = "root"
	    password = "allenross356_root"
	    s.login (ip, username, password)
	    s.sendline ('uptime')   # run a command
	    s.prompt()             # match the prompt
	    uptime = s.before          # print everything before the prompt.
	    s.sendline ('df')
	    s.prompt()
	    disk = s.before
	    s.sendline ('free')
	    s.prompt()
	    mem = s.before
	    s.logout()
	    user = request.user()
	    userpro = UserProfile.objects.get(user=user)
	    obj = ScanResults(ip=ip, hostname=name,uptime=uptime,mem=mem,disk=disk,user=userpro)
	    obj.save()
	    li = [name,uptime,disk,mem]
	    return HttpResponse(li)
	except pxssh.ExceptionPxssh, e:
	    print "pxssh failed on login."
	    print str(e)