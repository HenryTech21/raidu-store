from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('slider', views.slider, name="slider"),
    path('about', views.about, name="about"),
    path('store', views.store, name="store"),
    path('view_product/<str:pk>', views.view_product, name="view_product"),
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('order_submitted', views.orderSubmitted, name="order_submitted"),
    path('blogs', views.blogs, name="blogs"),
    path('footer', views.footer, name="footer"),
    path('view_post/<str:pk>', views.viewPost, name="view_post"),
]