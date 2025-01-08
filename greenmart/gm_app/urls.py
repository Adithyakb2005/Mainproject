from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),


    path('shophome', views.shophome),
    path('logout', views.logout_view),
    path('add',views.addproduct),
    path('add_cate',views.add_category),

    path('editproduct/<pid>',views.editproduct),
    path('deleteproduct/<pid>',views.deleteproduct),

# -----------------------user----------------
    path('register/',views.register),
    path('userhome',views.userhome),
    path('category_view',views.category_view),
    path('product_view/<pid>',views.product_view),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('bookings',views.bookings),
    path('pro_buy/<pid>',views.pro_buy),
    path('aboutuser',views.aboutuser),
    path('contactuser',views.Contactuser)

]
