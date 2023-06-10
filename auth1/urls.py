from django.urls import path, include
from . import views as vi

app_name ='auth1'

urlpatterns = [
    # path('',vi.home, name='home'),
    path('reg/',view=vi.register,name='reg'),
    path('login/',view=vi.login_view,name='login'),
    path('logout/',view=vi.logout_view,name='logout'),
    path('profile/<int:id>/',view=vi.profile,name='profile'),
    # path('accounts/', include('django.contrib.auth.urls'))
]
