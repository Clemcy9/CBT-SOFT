from django.urls import path, include
from . import views as vi

app_name ='auth1'

urlpatterns = [
    path('',vi.home, name='home'),
    path('reg/',vi.register,name='reg'),
    path('login/',vi.login_view,name='login'),
    path('logout/',vi.logout_view,name='logout'),
    path('profile/<str:user>/',vi.profile,name='profile'),
    # path('accounts/', include('django.contrib.auth.urls'))
]
