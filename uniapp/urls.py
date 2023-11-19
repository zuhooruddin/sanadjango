

from django.urls import path,include
from . import views
urlpatterns = [
    path('adduser',views.adduser,name='adduser'),
    path('login',views.userLogin,name='login'),
    path('updateuser',views.updateUser,name='updateuser'),
    path('additem',views.addAds,name='additem'),
    path('getitem',views.getActiveAdds,name='getActiveitem'),
    path('getsolditem',views.getSoldAdds,name='getsolditem'),
    path('getpendingitem',views.getPendingAdds,name='getpendingitem'),
    path('solditem',views.soldItem,name='solditem'),
    path('getalladds',views.getAllAdds,name='getallads'),
    path('getsingleadds',views.getSingleAdds,name='getsingleadds'),
    path('getsingleuser',views.getSingleUser,name='getsingleuser'),
    path('deleteitem',views.deleteItem,name='deleteitem'),
    path('registerdriver', views.registerDriver, name='registerDriver'),
    path('getdrivers', views.getDrivers, name='get-all-drivers'),
    path('delete', views.deleteAllDrivers, name='get-all-drivers'),
    path('forgotpassword', views.forgot_password, name='forgot_password'),



   
]
