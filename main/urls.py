from django.conf.urls import url

from . import views
app_name='main'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    #url(r'^test$',views.test,name='test'),
    #url(r'^result$',views.result,name='result'),
    #url(r'^login$',views.login,name='login'),
    #url(r'^signup$',views.signup,name='signup'),
    #url(r'^user$',views.user,name='user'),
    #url(r'^usersearch$',views.usersearch,name='usersearch'),
    #url(r'^follow$',views.follow,name='follow'),
    #url(r'^result$',views.result,name='result'),
    url(r'^upload$',views.upload,name='upload'),
    url(r'^soundsearch$',views.soundsearch,name='soundsearch'),
]
