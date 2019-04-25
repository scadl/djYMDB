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
from django.urls import path, reverse_lazy
from django.contrib.auth import views

from django.conf import settings
from django.conf.urls.static import static

from ymdb import views as myViews

urlpatterns = [
    path('', myViews.arts_list, name='ArtList'),
    path('add/<int:refF>',  myViews.art_add, name = 'ArtAdd'),
    path('edit/<int:pk>/<int:rpg>',  myViews.art_edit, name='ArtEdit'),
    path('edit/<int:pk>/<int:refF>/<int:rtg>/<int:rpg>',  myViews.art_edit, name='ArtEditAdv'),
    path('prop/<int:ref>',  myViews.prop_edit, name='propEdit'),
    path('propmod/<int:ref>/<int:pky>', myViews.prop_edit, name='propMod'),
    path('del/<int:pk>/<int:ref>/<int:rpg>',  myViews.delSomething, name='delAct'),
    path('del/<int:pk>/<int:ref>/<int:refF>/<int:rtg>/<int:rpg>',  myViews.delSomething, name='delActAdv'),
    path('collection/<int:cid>/p<int:pg>',  myViews.arts_list, name='collFilter'),
    path('genre/<int:gid>/p<int:pg>',  myViews.arts_list, name='genFilter'),
    path('p<int:pg>',  myViews.arts_list, name='pageU'),
    path('accounts/login/', views.LoginView.as_view(), name='ymdb_login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page=reverse_lazy('ArtList')), name='ymdb_logout'),
    path('newpass', myViews.chpass, name='async_chpass'),
    path('newsetts', myViews.chSettings, name='chSett'),
    path('newts', myViews.sendTs, name='async_tsSend'),
    path('tsDel', myViews.delTS, name='async_tsDel')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
