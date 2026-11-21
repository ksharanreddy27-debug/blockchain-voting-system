from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),path('register/',views.register,name='register'),path('login/',views.login_view,name='login'),path('logout/',views.logout_view,name='logout'),path('demo-otp/',views.demo_otp,name='demo_otp'),path('vote/<int:election_id>/',views.cast_vote,name='cast_vote'),path('results/<int:election_id>/',views.results,name='results'),path('ledger/',views.ledger,name='ledger')]
