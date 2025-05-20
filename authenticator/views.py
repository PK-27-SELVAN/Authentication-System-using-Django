from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import customUserForm,identifyUserForm,OTPForm
from .models import customUser
from django.views import View
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail ##to send conformation mail
import random # to generate otp 
import datetime  # to give times
from django.utils import timezone # to get the time zone
from django.db.models import Q

from django.contrib import messages # to provide alert mesaages

from django.utils.decorators import method_decorator #to use in class based views
from django.contrib.auth.decorators import login_required


def get_otp(username):
    obj = customUser.objects.get(username=username)
    otp = random.randint(1000,9999)
    otpexpiry = timezone.now() + datetime.timedelta(minutes=10)
    obj.otp = otp
    obj.otp_expiry = otpexpiry
    obj.save()
    return otp

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'Registerform':customUserForm()
        }
        return render(request, 'authentication/register.html', context)
    def post(self,request, *args, **kwargs):
        form = customUserForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            msg = f"Hi,{first_name} {last_name} Your Account Created sucessfully,Welcome to Our Website Enjoy Shopping!!..."
            send_mail("Regarding Account Registration",
                      msg,
                      "pkpiety2727@gmail.com",
                      [email],
                      fail_silently=True)
            form.save()
            messages.success(request,"Account registration sucessfull,check the email sent to you")
            return redirect('login')
        messages.error(request,"validation error,enter the details correctly")
        return redirect('register')
    
class LoginView(View):
    def get(self,request, *args, **kwargs):
        form = AuthenticationForm()
        context = {
            'loginform':form
        }
        return render(request, 'authentication/login.html', context)
    def post(self,request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_authenticated:
                    login(request,user)
                    messages.success(request,'Login successfull')
                    return redirect('home')
        messages.error(request,'Login failed,check your credentials')
        return redirect('login')

class identifyuserView(View):
    def get(self,request, *args, **kwargs):
        form = identifyUserForm()
        context = {
            'identifyuserform':form
        }
        return render(request, 'authentication/identifyuser.html', context)
    def post(self,request, *args, **kwargs):
        form = identifyUserForm(data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            user_verify = customUser.objects.filter(Q(username=username_or_email)|Q(email=username_or_email))
            if user_verify.exists():
                user = user_verify[0]
                otp = get_otp(user.username)
                email = user.email
                msg = f"your otp to reset password is {otp},it will be valid only for 10 minutes."
                send_mail("OTP Verification",
                          msg,
                          "pkpiety2727@gmail.com",
                          [email],
                          fail_silently=True)
                context = {
                    'user':user,
                }
                messages.success(request,"user exists")
                return render(request,'authentication/emailsent.html',context)
        else:
            context = {
                    'user':None,
                }
            messages.error(request,"user doesnot exists,enter your registered email id or username")
            return render(request,'authentication/emailsent.html',context)
  
class ValidateOTPView(View):
    def get(self,request,*args, **kwargs):
        user = customUser.objects.get(username=kwargs['username'])
        form = OTPForm()
        context = {
            'otpform':form
        }
        return render(request,'authentication/validateotp.html',context)

    def post(self,request,*args,**kwargs):
        user = customUser.objects.get(username=kwargs['username'])
        form = OTPForm(data=request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if user.otp_expiry >= timezone.now():
                print(timezone.now())
                if otp == user.otp:
                    messages.success(request,"otp verification successful")
                    # url = f'/authentication/resetpasssword/{user.username}/'-->another way
                    return redirect('resetpassword',username=user.username)
                    # return HttpResponse("otp validated successfully,here is your reset")
                else:
                    messages.error(request,"otp verification unsuccessful")
                    return HttpResponse("Incorrect otp")
            else:
                messages.error(request,"otp expired")
                return HttpResponse("otp expired")

class PasswordResetView(View):
    def get(self,request,*args,**kwargs):
        user = customUser.objects.get(username=kwargs['username'])
        resetform = SetPasswordForm(user=user)
        context = {
            'form':resetform,
            'user':user
        }
        return render(request,'authentication/resetpassword.html',context)
    def post(self,request,*args,**kwargs):
        user = customUser.objects.get(username=kwargs['username'])
        resetform = SetPasswordForm(user=user,data=request.POST) 
        if resetform.is_valid():
            resetform.save()
            send_mail(
                'password reset',
                'your password has been reset',
                'pkpiety2727@gmail.com',
                [user.email],
                fail_silently=True,
            )
            messages.success(request,"password reset successful")
            return redirect('login')
        messages.error(request,"passwords not match")
        return HttpResponse("passwords not match")
    
class HomeView(View):
    @method_decorator(login_required)  # to restrict access only authenticated users
    def get(self, request, *args, **kwargs):
        return render(request,'authentication/home.html')
    

class LogoutView(View):
    @method_decorator(login_required)
    def get(self,request,*args, **kwargs):
        logout(request)
        return redirect('login')

