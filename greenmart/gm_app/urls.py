from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Shop Views
    path('shophome/', views.shophome, name='shophome'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_product/<int:pid>/', views.edit_product, name='edit_product'),
    path('deleteproduct/<int:pid>/', views.deleteproduct, name='delete_product'),
    path('customer_support/', views.customer_support, name='customer_support'),

    # User Views
    path('register/', views.register, name='register'),
    path('userhome/', views.userhome, name='user_home'),
    path('userhome/category_view/<int:category_id>/', views.category_view, name='category_view'),
    path('product_view/<int:pid>/', views.product_view, name='product_view'),
    path('add_to_cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('search/', views.product_search, name='product_search'),

    # Booking and Cart Management
    path('viewbookings', views.viewbookings, name='viewbookings'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('bookings/', views.bookings, name='user_bookings'),
    path('cart_pro_buy/<int:cid>/', views.cart_pro_buy, name='cart_product_buy'),
    path('pro_buy/<int:pid>/', views.pro_buy, name='product_buy'),
    path('qty_in/<int:cid>/', views.qty_in, name='increase_quantity'),
    path('qty_dec/<int:cid>/', views.qty_dec, name='decrease_quantity'),
    path('contact/submit_form', views.submit_form, name='submit_form'),
     path('cancel-booking/', views.cancel_booking, name='cancel_booking'),


    path('payment-selection/<int:pid>/', views.payment_selection, name='payment_selection'),
    path('complete-purchase/', views.complete_purchase, name='complete_purchase'),
    path('process_payment/<str:method>/<int:product_id>/', views.process_payment, name='process_payment'),
    path('bought-products/', views.bought_products, name='bought_products'),
   

    # Static Pages
    path('aboutuser/', views.aboutuser, name='about_user'),
    path('contactuser/', views.Contactuser, name='contact_user'),
]
