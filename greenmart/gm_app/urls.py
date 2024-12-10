from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),


    path('shophome', views.shophome),
    path('logout', views.logout_view),
    path('add',views.addproduct),
    path('editproduct/<pid>',views.editproduct),
# -----------------------user----------------
    path('register/',views.register),
    path('userhome',views.userhome),
    path('product_view/<pid>',views.product_view),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
]
