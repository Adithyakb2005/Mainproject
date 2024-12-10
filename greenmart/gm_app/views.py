from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from . models import *
import os
from django.contrib.auth.models import User
# Create your views here.

def login_view(req):
    if 'shop' in req.session:
        return redirect(shophome)
    if 'user' in req.session:
        return redirect(userhome)
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=username,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['shop']=username #create
                return redirect(shophome)
            else:
                req.session['user']=username 
                return redirect(userhome)
        else:
            messages.warning(req, "Invalid username or password.")
            return redirect(login_view)
    else:
        return render(req,'login.html')

def logout_view(req):
    logout(req)
    req.session.flush()
    return redirect(login_view)
#---------------------admin------------------------
def shophome(req):
    data=Product.objects.all()
    if 'shop' in req.session:
        return render(req,'shop/home.html',{'products':data})
    else:
        return redirect(login_view)
def addproduct(req) :
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            dis=req.POST['descrip']
            offer_price=req.POST['offer_price']
            # offer_price = req.POST.get('offer_price')


            price=req.POST['price']
            stock=req.POST['stock']
            file=req.FILES['img'] #to get the img from html page we  are using file method instead of post and adding enctype in html page

            data=Product.objects.create(pid=pid,name=name,dis=dis,offer_price=offer_price,price=price,stock=stock)
            data=Product.objects.get(pk=pid)
            data.img=file
            data.save()
            return redirect(shophome)
        else:
            return render(req,'shop/addproduct.html')
    else:
        return redirect(login_view) 
def editproduct(req,pid) :
        if req.method=='POST':
            proid=req.POST['proid']
            name=req.POST['name']
            dis=req.POST['descrip']
            # offer_price=req.POST['offer_price']
            offer_price = req.POST.get('offer_price')

            price=req.POST['price']
            stock=req.POST['stock']
            file=req.FILES.get('img')
            if file:
                Product.objects.filter(pk=pid).update(pid=proid,name=name,dis=dis,offer_price=offer_price,price=price,stock=stock,img=file)
                data=Product.objects.get(pk=pid)
                data.img=file
                data.save()
            else:  
                Product.objects.filter(pk=pid).update(pid=pid,name=name,dis=dis,offer_price=offer_price,price=price,stock=stock,img=file)
            return redirect(shophome)
        else:
            data=Product.objects.get(pk=pid)
            return render(req,'shop/edit.html',{'data':data})
def product_view(req,pid):
       data=Product.objects.get(pk=pid)
       return render(req,'user/product_view.html',{'product':data})
    

def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    
    return  redirect(view_cart)
def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

# --------------------------------------------------register
def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
        except:
            messages.warning(req,"email already in use")
            return redirect(register)

        return redirect(login_view)
    else:
        return render(req,'user/register.html')
def userhome(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/userhome.html',{'Product':data})
    else:
        return redirect(login)
