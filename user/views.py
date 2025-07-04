from django.shortcuts import render,redirect
from mydjapp import models as mydjapp_models
from myadmin import models as myadmin_models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import time
from . import models

MEDIA_URL=settings.MEDIA_URL

#middleware to check session for user routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path=="/user/cpuser/" or request.path=="/user/epuser/" or request.path=="/user/viewcategory/" or request.path=="/user/viewsubcategory/" or request.path=="/user/addproduct/" or request.path=="/user/viewproduct/" or request.path=="/user/funds/" or request.path=="/user/success/" or request.path=="/user/cancel/" :
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

# Create your views here.

def userhome(request):
    return render(request,"userhome.html",{"sunm":request.session["sunm"]})

def cpuser(request):
    if request.method=="GET":
        return render(request,"cpuser.html",{"output":"","sunm":request.session["sunm"]})
    else:
        opassword=request.POST.get("opassword")
        npassword=request.POST.get("npassword")    
        cnpassword=request.POST.get("cnpassword")
        sunm=request.session["sunm"]

        userDetails=mydjapp_models.Register.objects.filter(email=sunm,password=opassword)
        
        if len(userDetails)>0:
            if npassword==cnpassword:
                mydjapp_models.Register.objects.filter(email=sunm).update(password=cnpassword)    
                return render(request,"cpuser.html",{"output":"Password changed successfully....","sunm":request.session["sunm"]})
            else:
                return render(request,"cpuser.html",{"output":"New password & Confirm new password mismatch....","sunm":request.session["sunm"]})                                
        else:
            return render(request,"cpuser.html",{"output":"Invalid username or old password....","sunm":request.session["sunm"]})

def epuser(request):
    sunm=request.session["sunm"]
    if request.method=="GET":
        userDetails=mydjapp_models.Register.objects.filter(email=sunm)
        m,f="",""
        if userDetails[0].gender=="male":
            m="checked"
        else:
            f="checked"         
        return render(request,"epuser.html",{"userDetails":userDetails[0],"sunm":request.session["sunm"],"output":"","m":m,"f":f})
    else:
        name=request.POST.get("name")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")

        mydjapp_models.Register.objects.filter(email=sunm).update(name=name,mobile=mobile,address=address,city=city,gender=gender)
        return redirect("/user/epuser/")

def viewcategory(request):
    clist=myadmin_models.Category.objects.all()
    return render(request,"viewcategory.html",{"sunm":request.session["sunm"],"clist":clist,"MEDIA_URL":MEDIA_URL})

def viewsubcategory(request):
	catname=request.GET.get("catname")
	sclist=myadmin_models.SubCategory.objects.filter(catname=catname)
	return render(request,"viewsubcategory.html",{"sunm":request.session["sunm"],"sclist":sclist,"MEDIA_URL":MEDIA_URL})

def addproduct(request):
    sclist=myadmin_models.SubCategory.objects.all()
    if request.method=="GET":
        return render(request,"addproduct.html",{"sunm":request.session["sunm"],"output":"","sclist":sclist})
    else:
        subcatname=request.POST.get("subcatname")
        pname=request.POST.get("pname")
        pdescription=request.POST.get("pdescription")
        bprice=request.POST.get("bprice")
        picon=request.FILES["picon"]
        fs = FileSystemStorage()
        filename = fs.save(picon.name,picon)
        uid=request.session["sunm"]
        info=time.time()
        p=models.Product(subcatname=subcatname,pname=pname,pdescription=pdescription,bprice=bprice,piconname=filename,uid=uid,info=info)
        p.save()
        return render(request,"addproduct.html",{"sunm":request.session["sunm"],"output":"Product Added Successfully","sclist":sclist})
    
def viewproduct(request):
	subcatname=request.GET.get("subcatname")
	plist=models.Product.objects.filter(subcatname=subcatname)
	return render(request,"viewproduct.html",{"sunm":request.session["sunm"],"output":"biding is open","plist":plist,"MEDIA_URL":MEDIA_URL})  

def funds(request):
	paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
	paypalID="sb-s41dd29126099@business.example.com"
	amt=100
	return render(request,"funds.html",{"sunm":request.session["sunm"],"paypalURL":paypalURL,"paypalID":paypalID,"amt":amt})	

def payment(request):
	uid=request.GET.get("uid")
	amt=request.GET.get("amt")  
	p=models.Funds(uid=uid,amt=int(amt),info=time.asctime())
	p.save()
	return redirect("/user/success/")

def success(request):
	return render(request,"success.html",{"sunm":request.session["sunm"]})

def cancel(request):
	return render(request,"cancel.html",{"sunm":request.session["sunm"]})

def viewbiddingstatus(request):
    pid=request.GET.get("pid")
    
    pDetails=models.Product.objects.filter(pid=pid)    
    dtime=time.time()-float(pDetails[0].info)
    if dtime > 172800:
        status=1
    else:
        status=0

    bidDetails=models.Bidding.objects.filter(pid=pid)    
    l=len(bidDetails)
    if l==0:
        bidprice=pDetails[0].bprice
    else:
        bidprice=bidDetails[l-1].bidprice                            

    return render(request,"viewbiddingstatus.html",{"sunm":request.session["sunm"],"status":status,"pDetails":pDetails[0],"bidprice":bidprice})

def bid(request):
    pid=request.POST.get("pid")
    bidprice=request.POST.get("bidprice")
    sunm=request.session["sunm"]
    info=time.time()

    p=models.Bidding(pid=int(pid),uid=sunm,bidprice=int(bidprice),info=time.time())
    p.save()

    return redirect("/user/viewbiddingstatus/?pid="+pid)     
     
def viewbid(request):
    pid=request.GET.get("pid")
    bidlist=models.Bidding.objects.filter(pid=int(pid))
    print(bidlist)
    return render(request,"viewbid.html",{"sunm":request.session["sunm"],"bidlist":bidlist})        

