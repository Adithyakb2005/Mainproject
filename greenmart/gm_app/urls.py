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
    path('product_view/<pid>',views.product_view),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('aboutuser',views.aboutuser),
    path('contactuser',views.Contactuser)

]
