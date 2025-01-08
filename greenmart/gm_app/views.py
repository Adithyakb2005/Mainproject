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
# def shophome(req):
#     data=Product.objects.all()
#     categories = Category.objects.all()
#     if 'shop' in req.session:
#         return render(req,'shop/home.html')
#     else:
#         return redirect(login_view)
def shophome(request):
    products = Product.objects.all()  
    categories = Category.objects.all() 
    return render(request, 'shop/home.html', {'products': products, 'category': categories})
def addproduct(req) :
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            dis=req.POST['dis']
            offer_price=req.POST['offer_price']
            price=req.POST['price']
            stock=req.POST['stock']
            file=req.FILES['img'] 
            cate=req.POST['category']
            cat=Category.objects.get(pk=cate)
            data=Product.objects.create(pid=pid,name=name,dis=dis,offer_price=offer_price,price=price,stock=stock,category=cat,img=file)
            # data=Product.objects.get(pk=pid)
            data.save()
            return redirect(shophome)
        else:
            cate=Category.objects.all()
            return render(req,'shop/addproduct.html',{'cate':cate})
    else:
        return redirect(login_view) 
def editproduct(req,pid) :
        if req.method=='POST':
            proid=req.POST['proid']
            name=req.POST['name']
            dis=req.POST['dis']
            offer_price=req.POST['offer_price']
            price=req.POST['price']
            stock=req.POST['stock']
            file=req.FILES.get('img')
            
            if file:
                Product.objects.filter(pk=pid).update(pid=proid,name=name,dis=dis,offer_price=offer_price,price=price,stock=stock)
                data=Product.objects.get(pk=pid)
                data.img=file
                data.save()
            else:  
                Product.objects.filter(pk=pid).update(pid=proid,name=name,dis=dis,offer_price=offer_price,price=price,stock=stock)
            return redirect(shophome)
        else:
            data=Product.objects.get(pk=pid)
            cate=Category.objects.all()
            return render(req,'shop/edit.html',{'data':data,'cate':cate})
def deleteproduct(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shophome)
def add_category(req):
    if 'shop' in req.session:
        if req.method=='POST':
            c_name=req.POST['cate_name']
            c_name=c_name.lower()
            try:
                cate=Category.objects.get(Category_name=c_name)
            except:
                data=Category.objects.create(Category_name=c_name)
                data.save()
            return redirect(add_category)
        categories=Category.objects.all()
        return render(req,'shop/cate.html' ,{'cate':categories})
    else:
        return render(req,'shop/cate.html')
def product_view(req,pid):
       data=Product.objects.get(pk=pid)
       return render(req,'user/product_view.html',{'Product':data})
    

def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,Product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
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
    
def category_view(req, category_id):
    try:
        category = Category.objects.get(pid=category_id)
    except Category.DoesNotExist:
        return render(req, 'shop/category_view.html', {'error': 'Category does not exist'})
    
    products = Product.objects.filter(category=category)  
    return render(req, 'shop/category_view.html', {'category': category, 'products': products})



def qty_in(req, cid):
    data = Cart.objects.get(pk=cid)
    if data.qty < data.product.stock:
        data.qty += 1
        data.save()
    else:
        messages.warning(req, "You cannot add more than the available stock.")
    return redirect(view_cart)

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(view_cart)

def remove_pro(req,cid):
    data=Cart.objects.get(pk=cid)
    data.delete()
    return redirect(bookings)
def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)


def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)



def bookings(req):
    user = User.objects.get(username=req.session['user'])  # Get the user from the session
    buy = Buy.objects.filter(user=user).order_by('-id')  # Get all bookings for the user in reverse order
    total_price = sum(item.product.price * item.qty for item in buy)  # Calculate total price

    if req.method == 'POST':
        booking_id = req.POST.get('cancel_booking')  
        if booking_id:
            booking = Buy.objects.get(id=booking_id)
            booking.delete()  
            return redirect(bookings)  

    return render(req, 'user/booking.html', {'bookings': buy, 'total_price': total_price})

def aboutuser(req):
    return render(req,'user/about.html')
def Contactuser(req):
    return render(req,'user/Contactus.html')