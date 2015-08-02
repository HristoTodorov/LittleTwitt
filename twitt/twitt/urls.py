from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# This is a test!
urlpatterns = [
    url(r'^$', 'twittapp.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', 'twittapp.views.home', name='home'),
    url(r'^register/$', 'twittapp.views.register', name='register'),
    url(r'^profile/$', 'twittapp.views.profile', name='profile'),
    url(r'^login/$', 'twittapp.views.user_login', name='login'),
    url(r'^logout/$', 'twittapp.views.user_logout', name='logout'),
    url(r'^profile/settings/$', 'twittapp.views.user_settings', name='settings'),
	url(r'^profile/compose/$', 'twittapp.views.save_twitt', name='save_twitt'),
    url(r'^followers/$', 'twittapp.views.followers', name='followers'),
    # url(r'^fallowing/$', 'twittapp.views.following', name='fallowing'),
	url(r'^delete/$', 'twittapp.views.delete_twitt', name='delete_twitt'),
    url(r'^stop_follow/$', 'twittapp.views.stop_follow', name='stop_follow'),
    url(r'^follow/$', 'twittapp.views.follow', name='follow'),
    url(r'^view/[0-9]+/$', 'twittapp.views.view_profile', name='view_profile'),
    url(r'^view/[0-9]+/twitts/$', 'twittapp.views.view_profile_twitts', name='view_profile_twits'),
    url(r'^view/[0-9]+/followers/$', 'twittapp.views.view_profile_followers', name='view_profile_followers'),

    url(r'^view/[0-9]+/followings/$', 'twittapp.views.view_profile_followings', name='view_profile_followings'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
            'show_indexes': True}),

] + staticfiles_urlpatterns()
