from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'home.views.index', ),
    url(r'^image/$', 'home.views.image')
]
