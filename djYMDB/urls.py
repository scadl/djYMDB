"""djYMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, reverse_lazy, include
from django.contrib.auth import views

from django.conf import settings
from django.conf.urls.static import static

from ymdb import views as myViews

urlpatterns = [
    path('', myViews.arts_list, name='ArtList'),
    path('u<int:u>', myViews.arts_list, name='ArtList'),
    path('add/<int:refF>',  myViews.art_add, name = 'ArtAdd'),
    path('edit/<int:pk>/<int:rpg>',  myViews.art_edit, name='ArtEdit'),
    path('edit/<int:pk>/<int:refF>/<int:rtg>/<int:rpg>',  myViews.art_edit, name='ArtEditAdv'),
    path('prop/<int:ref>',  myViews.prop_edit, name='propEdit'),
    path('propmod/<int:ref>/<int:pky>', myViews.prop_edit, name='propMod'),
    path('del/<int:pk>/<int:ref>/<int:rpg>',  myViews.delSomething, name='delAct'),
    path('del/<int:pk>/<int:ref>/<int:refF>/<int:rtg>/<int:rpg>',  myViews.delSomething, name='delActAdv'),
    path('collection/<int:cid>/p<int:pg>',  myViews.arts_list, name='collFilter'),
    path('genre/<int:gid>/p<int:pg>',  myViews.arts_list, name='genFilter'),
    path('collection/<int:cid>/p<int:pg>/u<int:u>',  myViews.arts_list, name='collFilter'),
    path('genre/<int:gid>/p<int:pg>/u<int:u>',  myViews.arts_list, name='genFilter'),
    path('p<int:pg>',  myViews.arts_list, name='pageU'),
    path('p<int:pg>/u<int:u>',  myViews.arts_list, name='pageU'),
    path('login', views.LoginView.as_view(), name='ymdb_login'),
    path('logout', views.LogoutView.as_view(next_page=reverse_lazy('ArtList')), name='ymdb_logout'),
    path('register', myViews.registerNew, name='ymdb_register'),
    path('newpass', myViews.chpass, name='async_chpass'),
    path('newsetts', myViews.chSettings, name='chSett'),
    path('newts', myViews.sendTs, name='async_tsSend'),
    path('tsDel', myViews.delTS, name='async_tsDel'),
    path('getTsList', myViews.dynaTSLoad, name='async_tsLoad'),
    path('artInfo/u<int:u>/<int:pk>', myViews.getArtInfo, name='artPage')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [path(settings.ALIAS, include(urlpatterns))]