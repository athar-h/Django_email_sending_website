from . import views
from django.urls import path
urlpatterns=[
    path(r"login/",views.login_page,name="login"),
    path(r"register/",views.register_page,name="register"),
    path(r"home/",views.home_page,name="home"),
    path(r"api-view/",views.api_view,name="api-view"),
    path(r"logout/", views.logout_page, name="logout"),
    path("",views.login_page,name="login"),
]
