from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from . import models
from mydjapp import models as mydjapp_models

#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=="/myadmin/cpadmin/" or request.path=="/myadmin/epadmin/" or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/':
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

# Create your views here.

def adminhome(request):
    #print(request.session["sunm"])
    return render(request,"adminhome.html",{"sunm":request.session["sunm"]})

def manageusers(request):
    userDetails=mydjapp_models.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session["sunm"]})

def manageuserstatus(request):
    s=request.GET.get("s")
    regid=int(request.GET.get("regid"))

    if s=="active":
        mydjapp_models.Register.objects.filter(regid=regid).update(status=1)
    elif s=="inactive":
        mydjapp_models.Register.objects.filter(regid=regid).update(status=0)
    else:
        mydjapp_models.Register.objects.filter(regid=regid).delete()

    return redirect("/myadmin/manageusers/")

def cpadmin(request):
    if request.method=="GET":
        return render(request,"cpadmin.html",{"output":"","sunm":request.session["sunm"]})
    else:
        opassword=request.POST.get("opassword")
        npassword=request.POST.get("npassword")
        cnpassword=request.POST.get("cnpassword")
        sunm=request.session["sunm"]

        userDetails=mydjapp_models.Register.objects.filter(email=sunm,password=opassword)
        
        if len(userDetails)>0:
            if npassword==cnpassword:
                mydjapp_models.Register.objects .filter(email=sunm).update(password=cnpassword)
                return render(request,"cpadmin.html",{"output":"Password Changes Successfully","sunm":request.session["sunm"]})

            else:
                return render(request,"cpadmin.html",{"output":"New Password & Confirm New Password Mismatch....","sunm":request.session["sunm"]})
        else:
            return render(request,"cpadmin.html",{"output":"Invalid Username or Old Password.....","sunm":request.session["sunm"]})

        #return render(request,"cpadmin.html",{"output":"ok","sunm":request.session["sunm"]})
        
def epadmin(request):
    sunm=request.session["sunm"]
    if request.method=="GET":
        userDetails=mydjapp_models.Register.objects.filter(email=sunm)
        m,f="",""
        if userDetails[0].gender=="male":
            m="checked"
        else:
            f="checked"
        return render(request,"epadmin.html",{"userDetails":userDetails[0],"sunm":request.session["sunm"],"output":"","m":m,"f":f})
    else:
        name=request.POST.get("name")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        mydjapp_models.Register.objects.filter(email=sunm).update(name=name,mobile=mobile,address=address,city=city,gender=gender)

        return redirect("/myadmin/epadmin/")

def addcategory(request):
    if request.method=="GET":
        return render(request,"addcategory.html",{"sunm":request.session["sunm"],"output":""})
    else:
        catname=request.POST.get("catname")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        #print(filename+"-----"+catname)
        p=models.Category(catname=catname,caticonname=filename)
        p.save()
        return render(request,"addcategory.html",{"sunm":request.session["sunm"],"output":"Category Added Successfully"})

def addsubcategory(request):
    clist=models.Category.objects.all()    
    if request.method=="GET":
        return render(request,"addsubcategory.html",{"sunm":request.session["sunm"],"output":"","clist":clist})
    else:
        catname=request.POST.get("catname")
        subcatname=request.POST.get("subcatname")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.SubCategory(catname=catname,subcatname=subcatname,subcaticonname=filename)
        p.save()
        return render(request,"addsubcategory.html",{"sunm":request.session["sunm"],"output":"SubCategory Added Successfully","clist":clist})   