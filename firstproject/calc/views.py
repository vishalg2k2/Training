from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Traveller
from .serializers import TravellerSerializer,GuideSerializer,UserSerializer,Traveller2Serializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly,IsSuperUser
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.contrib.auth import authenticate,login
from django.core.mail import EmailMessage
import uuid
from .models import Profile
from django.contrib import messages

# Create your views here.
def home(request):
  trv = Traveller.objects.all()
  template = loader.get_template('base.html')
  return HttpResponse(template.render({'trv':trv}))
def add(request):
  if request.method=='POST':
    print("Added")
    the_aadhar = request.POST.get("tr_aadhar")
    the_name = request.POST.get("tr_name")
    the_email = request.POST.get("tr_email")
    the_phone = request.POST.get("tr_phone")

    t=Traveller()
    t.Aadhar = the_aadhar
    t.Name = the_name
    t.Email = the_email
    t.Phone = the_phone

    t.save()
    return redirect("/home/")
   
  template = loader.get_template('add.html')
  return HttpResponse(template.render({}))

def delete(request,Aadhar):
  t=Traveller.objects.get(pk=Aadhar)
  t.delete()
  return redirect("/home/")

def update(request,Aadhar):
  t=Traveller.objects.get(pk=Aadhar)
  template = loader.get_template('update.html')
  return HttpResponse(template.render({'t':t}))

def doupdate(request,Aadhar):
  the_aadhar = request.POST.get("tr_aadhar")
  the_name = request.POST.get("tr_name")
  the_email = request.POST.get("tr_email")
  the_phone = request.POST.get("tr_phone")

  t=Traveller.objects.get(pk=Aadhar)

  t.Aadhar = the_aadhar
  t.Name = the_name
  t.Email = the_email
  t.Phone = the_phone

  t.save()
  return redirect("/home/")


class TravellerList(generics.ListCreateAPIView):
  queryset=Traveller.objects.all()
  serializer_class=TravellerSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
class Traveller_detail(generics.RetrieveUpdateDestroyAPIView):
  queryset=Traveller.objects.all()
  def get_serializer_class(self):
    if self.request.user.username == self.get_object.__get__("owner"):
      return TravellerSerializer
    if self.request.user.is_superuser:
      return Traveller2Serializer
    return TravellerSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsSuperUser,IsOwnerOrReadOnly ]
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def upload_file(request):
  context={}
  if request.method=="POST":
    uploaded_files=request.FILES['document']
    fs=FileSystemStorage()
    name=fs.save(uploaded_files.name,uploaded_files)
    url=fs.url(name)
    print(url)
    context['url']=fs.url(name)
    print(uploaded_files.name)
  return render(request,'upload.html',context)

def search(request):
 query=request.GET['query']
 traveller =Traveller.objects.filter(
 Q(Name__icontains=query)
 )
 return render(request,'search.html',{'traveller':traveller})

def authsignup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
    
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            auth_token=str(uuid.uuid4())
            profile_obj=Profile.objects.create(user=my_user,auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('token_send')
    else:        
        return render(request,'authsignup.html')

def token_send(request):
   return render(request,'token_send.html')

def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()

        if(profile_obj):
            if(profile_obj.is_verified):
                print("Your account verified")
                return redirect('authlogin')
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,'Your account has been verified')
            return redirect('authlogin')
    except Exception as e:
        print(e)
        
def authlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(username=username,password=pass1)
        user_obj=User.objects.get(username=username)
        profile_obj=Profile.objects.filter(user=user_obj).first()
        if(not profile_obj.is_verified):
                messages.success(request,'profile is not verified')
                return redirect('authlogin')
        if user is not None:
            request.session['username']=username
            request.session['password']=pass1
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect:(")
    return render(request,'authlogin.html')

def send_mail_after_registration(email,token):
    message=f"Paste the link to verify in browser : http://127.0.0.1:8000/verify/{token}"
    email=EmailMessage(
        'Your account needs to be verified',
        message,
        'vishalg2k2@gmail.com',
        [email]
    )
    email.send()