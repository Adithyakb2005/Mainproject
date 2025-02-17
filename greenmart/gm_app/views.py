from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from . models import *
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
def edit_product(req,pid) :
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
def viewbookings(req):
    try:
        bookings = Buy.objects.select_related('user', 'product').order_by('-id')  # Fetch all bookings
        total_price = sum(booking.price for booking in bookings)  # Calculate total price of all bookings
        return render(req, 'shop/viewbooking.html', {'bookings': bookings, 'total_price': total_price})
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        return render(req, 'shop/viewbooking.html', {'error': 'An error occurred while fetching the bookings.'})

def product_view(req,pid):
       product = get_object_or_404(Product, id=pid)
       data=Product.objects.get(pk=pid)
       return render(req,'user/product_view.html',{'Product':data,'product': product})

def add_to_cart(req, pid):
    product = get_object_or_404(Product, pk=pid)
    if 'user' not in req.session:
        messages.error(req, "You must log in to add items to your cart.")
        return redirect('login') 
    user = get_object_or_404(User, username=req.session['user'])
    try:
        cart = Cart.objects.get(user=user, product=product)
        cart.qty += 1  
        cart.save()
        messages.success(req, f"{product.name} quantity updated in your cart.")
    except Cart.DoesNotExist:
        
        Cart.objects.create(product=product, user=user, qty=1)
        messages.success(req, f"{product.name} added to your cart.")
    return redirect('view_cart')

def view_cart(request,):
    # Get the user's cart
    cart = Cart.objects.filter(user=request.user)
    if not cart.exists():
        return redirect('user_home')

    # Calculate the total price
    cart_total = sum(item.product.offer_price * item.qty for item in cart)

    return render(request, 'user/cart.html', {'cart': cart, 'cart_total': cart_total})

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
        products = Product.objects.filter(category=category)  # Fetch products in the category
        return render(req, 'user/category_view.html', {'category': category, 'products': products})
    except Category.DoesNotExist:
        return render(req, 'user/category_view.html', {'error': 'Category does not exist'})
def product_search(request):
    query = request.GET.get('query', '').strip()
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'user/search_results.html', {'products': products, 'query': query})


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
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return redirect(view_cart)  # Redirect back to the cart page

def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def bought_products(request):
    # Get the products the user has bought
    bought_items = Buy.objects.filter(user=request.user)
    return render(request, 'user/bought_products.html', {'bought_items': bought_items})


def payment_selection(request,pid):
    # Get the user's cart
    cart = Cart.objects.filter(user=request.user)
    if not cart.exists():
        return redirect(userhome)
    
    # Render the payment selection template
    return render(request, 'user/payment_selection.html', {'cart': cart,'product_id': pid})


def complete_purchase(request):
    if request.method == 'POST':
        # Assume the payment was successful
        cart = Cart.objects.filter(user=request.user)
        
        # Mark items as purchased and transfer to Bought Products
        for item in cart:
            Buy.objects.create(
                user=item.user,
                product=item.product,
                qty=item.qty,
                price=item.product.offer_price
            )
        
        # Clear the cart
        cart.delete()
        return redirect('bought_products')
    
    # If GET request, show a message or redirect
    return redirect('payment_selection')


def process_payment(request, method, product_id):
    product = get_object_or_404(Product, id=product_id)
    if method == 'credit_card':
        # Handle credit card payment logic
        return render(request, 'user/payment_success.html', {'product': product, 'method': 'Credit Card'})
    elif method == 'paypal':
        # Handle PayPal payment logic
        return render(request, 'user/payment_success.html', {'product': product, 'method': 'PayPal'})
    elif method == 'cod':
        # Handle Cash on Delivery logic
        return render(request, 'user/payment_success.html', {'product': product, 'method': 'Cash on Delivery'})
    else:
        return render(request, 'user/payment_error.html', {'product': product})

def submit_form(request):
    if request.method == 'POST':
        # Collect form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the data to the database (if applicable)
        # Assuming you have a Contact model
        Contact.objects.create(name=name, email=email, message=message)

        # Redirect or show a success message
        return render(request, 'user/contact_success.html')

    return HttpResponse("Invalid request method.")

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

def cancel_booking(request):
    if request.method == 'POST':
        # Add logic to cancel the booking
        # For example, retrieve the user's order and mark it as canceled
        order = Buy.objects.get(user=request.user, status='pending')  # Adjust condition as needed
        order.status = 'canceled'
        order.save()

        # Redirect to an appropriate page after cancellation, e.g., the homepage or a confirmation page
        return redirect('user_home')  # Redirect to home or an appropriate page after cancelation
    return redirect('user_home')  # Redirect in case the request is not POST
def customer_support(request):
    # Fetch all the contact requests from the database
    contact_requests = Contact.objects.all().order_by('-submitted_at')

    # Render the template with the contact requests
    return render(request, 'shop/customer_suport.html', {'contact_requests': contact_requests})
def aboutuser(req):
    return render(req,'user/about.html')
def Contactuser(req):
    return render(req,'user/Contactus.html')