from django.http import HttpResponse
from django.shortcuts import render
from show_user_details.models import user
from show_user_details.models import management_user
from show_user_details.models import perform_user
from show_user_details.models import user_profile
from django.core.mail import send_mail
import random
import datetime
import time

def home(request):
    try:
        em=request.COOKIES['Uname']
        v=user.objects.filter(email=em).values('uname')
        err={
            'title': 'Second Details Entry Portal',
            'uname':str(v[0]['uname'])
        }
    except:
        err={
            'title': 'Second Details Entry Portal',
            'uname':'User'
        }
    return render(request,"index.html",err)


def aboutus(request):
    return HttpResponse("Welcome to Details Entry Portal")

def verify_user(request):
    if request.method=="POST":
        cde=request.POST.get("user_code")
        if cde==str(request.session['code']):
            err={
                'msg':'User Verified Successfully'
            }
            user.objects.filter(email=str(request.session['em'])).update(verified='yes')
            try:
                del request.session['code']
                del request.session['em']
            except:
                pass
            return render(request,"verify.html",err)
        else:
            err={
                'msg':"Invalid OTP...Please try again"
            }
            return render(request,"verify.html",err)
    else:
        err={
            'em':str(request.session['em'])
        }
        return render(request,"verify.html",err)
    
def register_page(request):
    if request.method=="POST":
        try: 
            unm=request.POST.get("uname")
            em=request.POST.get("user_email")
            psd=request.POST.get("paswd")
            insrt=user(uname=unm,email=em,pswd=psd)
            insrt.save()
            acc=random.randint(1000000000,9000000000)
            insrt2=management_user(uname=unm,acc_no=acc,amt=500.00)
            insrt2.save()
            insrt3=user_profile(uname=unm,photo="Picture.png",occupation="Enter Occupation",dob=datetime.datetime.now())
            insrt3.save()
            t=random.randint(100000,900000)
            send_mail(
            'Email Verification',
            'Hi User,\n \n Your OTP is:'+str(t)+'\n\nThanks & Regards,',
            'palsresidency@outlook.com',
            [em],
            fail_silently=False,
            )
            request.method="GET"
            request.session['code']=t
            request.session['em']=em
            return verify_user(request)
        #return render(request,"verify.html",err)
        except:
            err={
                "msg":"User with same Name or Email exists"
            }
            return render(request,"register.html",err)
    else:
        err={
            "msg":""
        }
        return render(request,"register.html",err)


def login2_page(request):
	if request.method=="POST":
		psd=request.POST.get("paswd")
		em=str(request.session['em'])
		v=user.objects.filter(email=em).values('pswd')
		if(str(v[0]['pswd'])==str(psd)):
			err={
				'em':str(request.session['em']),
				'msg':'Successfully logged In'
			}
			t=datetime.datetime.now()
			t=t.hour
			max_age=abs(24-t)*60*60
			expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
			response=render(request,"login2.html",err)
			response.set_cookie('Uname',request.session['em'],max_age=None,expires=expires)
			try:
				del request.session['em']
			except:
				pass
			return response
		else:
			err={
				'em':str(request.session['em']),
				'msg':'Invalid Password'
			}
			return render(request,"login2.html",err)
	else:
		try:
			if(str(request.session['em'])==''):
				return login1_page(request)
			else:
				err={
					'em':str(request.session['em']),
					'msg':''
				}
				return render(request,"login2.html",err)
		except:
			return login1_page(request)

def login1_page(request):
	if request.method=="POST":
		em=request.POST.get("p_email")
		v=user.objects.filter(email=em).values('status')
		try:
			if(str(v[0]['status'])=='blocked'):
				err={
					'msg':'Your account has been blocked'
				}
				return render(request,"login.html",err)
			elif(str(v[0]['status'])=='authenticate'):
				err={
					'msg':'Your account needs to be authenticated'
				}
				return render(request,"login.html",err)
			elif(str(v[0]['status'])=='complete'):
				request.session['em']=em
				request.method="GET"
				return login2_page(request)
		except Exception as exp:
			if(str(exp)=='list index out of range'):
				err={
					'msg':'No User exits. Please create one'
				}
			return render(request,"login.html",err)
	else:
		try:
			if(request.COOKIES['Uname']!=''):
				return home_logged(request)
			else:
				err={
				'msg':''
				}
				return render(request,"login.html",err)
		except:
			err={
				'msg':''
			}
			return render(request,"login.html",err)


def home_logged(request):
    try:
        em=request.COOKIES['Uname']
    except:
        request.method="GET"
        return login1_page(request)
    v=user.objects.filter(email=em).values('uname','status','user_type','verified')
    v2=management_user.objects.filter(uname=str(v[0]['uname'])).values('acc_no','amt')
    details={
	    'uname':str(v[0]['uname']),
	    'em':em,
	    'acc':str(v2[0]['acc_no']),
	    'amt':v2[0]['amt']
        }
    return render(request,"home_user.html",details)
	
def trnsfr(request):
    try:
        em=request.COOKIES['Uname']
    except:
        request.method="GET"
        return login1_page(request)
    v=user.objects.filter(email=em).values('uname')
    v2=management_user.objects.filter(uname=str(v[0]['uname'])).values('acc_no','amt')
    if request.method!="POST":
        details={
            'uname':str(v[0]['uname']),
			'em':em,
			'acc':str(v2[0]['acc_no']),
			'amt':v2[0]['amt'],
			'msg':""
            }
        return render(request,"trnsfr.html",details)
    elif request.method=="POST":
        to_acc_f=request.POST.get("cnf_acc")
        snd_amt=request.POST.get("snd_amt")
        rmks=request.POST.get("rmks")+" - "+str(v[0]['uname'])
        try:
            v3=management_user.objects.filter(acc_no=str(to_acc_f)).values('amt')
            v3_amt=round(float(snd_amt)+v3[0]['amt'],2)
            v2_amt=round(v2[0]['amt']-float(snd_amt),2)
            t_id="ONL"+str(random.randint(1000000,9000000))
            insrt=perform_user(trn_id=t_id,from_acc=str(v2[0]['acc_no']),to_acc=str(to_acc_f),amt=snd_amt,remarks=rmks)
            insrt.save()
            management_user.objects.filter(acc_no=str(v2[0]['acc_no'])).update(amt=v2_amt)
            management_user.objects.filter(acc_no=str(to_acc_f)).update(amt=v3_amt)
            details={
		'uname':str(v[0]['uname']),
		'em':em,
		'acc':str(v2[0]['acc_no']),
		'amt':v2_amt,
		'msg':'Transferred Successfully'
                }
            return render(request,"trnsfr.html",details)
        except:
            details={
		'uname':str(v[0]['uname']),
		'em':em,
		'acc':str(v2[0]['acc_no']),
		'amt':v2[0]['amt'],
		'msg':"Error in Transaction"
		}
            return render(request,"trnsfr.html",details)
def show(request):
    try:
        em=request.COOKIES['Uname']
    except:
        request.method="GET"
        return login1_page(request)
    v=user.objects.filter(email=em).values('uname')
    v2=management_user.objects.filter(uname=str(v[0]['uname'])).values('acc_no','amt')
    v3=(perform_user.objects.filter(from_acc=str(v2[0]['acc_no'])) | perform_user.objects.filter(to_acc=str(v2[0]['acc_no']))).values('trn_id','from_acc','to_acc','amt','remarks','date')
    if(len(v3)!=0):
        details={
            'msg':'Sent',
            'uname':str(v[0]['uname']),
            'em':em,
            'acc':str(v2[0]['acc_no']),
            'amt':v2[0]['amt'],
            'trn_list':v3,
        }
        #print(details['trn_list'],"\t",len(details['trn_list']))
    else:
        details={
            'uname':str(v[0]['uname']),
            'em':em,
            'acc':str(v2[0]['acc_no']),
            'amt':v2[0]['amt'],
            'msg':'No Transactions done yet'
        }
    return render(request,"Show.html",details)

def profile(request):
    try:
        em=request.COOKIES['Uname']
    except:
        request.method="GET"
        return login1_page(request)
    v=user.objects.filter(email=em).values('uname')
    v2=management_user.objects.filter(uname=str(v[0]['uname'])).values('acc_no','amt')
    v3=user_profile.objects.filter(uname=str(v[0]['uname'])).values('photo','occupation','dob')
    details={
        'uname':str(v[0]['uname']),
        'em':em,
        'acc':str(v2[0]['acc_no']),
        'amt':v2[0]['amt'],
        'photo':str(v3[0]['photo']),
        'occupation':str(v3[0]['occupation']),
        'dob':(v3[0]['dob']).strftime("%Y-%m-%d")
    }
    if request.method=="POST":
        u_o=request.POST.get("user_occupation")
        u_dob=request.POST.get("user_dob")
        user_profile.objects.filter(uname=str(v[0]['uname'])).update(occupation=u_o,dob=u_dob)
        details['msg']='Profile Updated Successfully'
        details['dob']=u_dob
    else:
        details['msg']=''
    
    return render(request,"Profile.html",details)

def logout_page(request):
    err={
        'msg':'Successfully Logged Out'
        }
    max_age=(-2)*60*60
    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response=render(request,"login.html",err)
    response.set_cookie('Uname',"",max_age=None,expires=expires)
    return response
