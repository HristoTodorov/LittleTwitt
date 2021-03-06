from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from twittapp.forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from twittapp.models import *  # noqa
from django.views.decorators.csrf import csrf_protect
from twittapp.user_view import UserView
from twittapp.twitt_view import TwittView
from twittapp.utils import *


def home(request):
    if not request.user.is_authenticated():
        context = {}
        template = 'index.html'
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/profile')

def register(request):
    if not request.user.is_authenticated():
        context = RequestContext(request)
        register = False
        if request.method == 'POST':
            registration_form = RegistrationForm(data=request.POST)
            if registration_form.is_valid():
                user = registration_form.save()
                user.set_password(request.POST['password'])
                user_id = user.id
                user_profile = UserProfile()
                user_profile.user_id = user_id
                user.save()
                user_profile.save()
                register = True
            else:
                print (registration_form.errors)
        else:
            registration_form = RegistrationForm()
        template = "register.html"
        return render_to_response(template, locals(), context)
    else:
        return HttpResponseRedirect('/profile')

def user_login(request):
    context = RequestContext(request)
    context.update(csrf(request))  # New
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        profile = UserProfile
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/profile')
            else:
                return HttpResponse('Your account is disabled!')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            messages.error(
                request, 'The combination password/username was not correct!')
            return HttpResponseRedirect('/login')
    else:
        return render_to_response('login.html', locals(), context)

@login_required
def profile(request):
    context = RequestContext(request)
    user_id = request.user.id
    user_profile = UserProfile.objects.get(user_id=user_id)
    all_twitters = get_all_twitts_by_user(user_id)
    avatar = Media.objects.get(id=user_profile.avatar_id).picture.url
    template = 'profile.html'
    return render_to_response(template, locals(), context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home')

@login_required
def user_settings(request):  # need to be fixed - not every category attend
    context = RequestContext(request)
    template = 'profile_settings.html'
    return render_to_response(template, locals(), context)

@login_required
@require_http_methods(['POST', ])
@csrf_protect
def save_twitt(request):
    content = request.POST['twitt_content']
    new_twitt = Twitt()
    new_twitt.author_id = get_user_id(request)
    new_twitt.save()
    messages.success(request, 'You successfuly twitt!')
    return HttpResponseRedirect('/profile')

@login_required
@require_http_methods(['POST', ])
@csrf_protect
def delete_twitt(request):
    twitt_id = request.POST['twitt']
    twitt = Twitt.objects.get(id=twitt_id)
    twitt.delete()
    # if contain_hashtag(twitt.content):
    #     all_hashtags_id_in_twitt = Trend.objects.get(twitt_id=twitt_id).twitt
    #     all_hashtags_id_in_twitt = list(map(lambda x: x.trend_id, all_hashtags_id_in_twitt))
    #     update_hashtag_count(all_hashtags_id_in_twitt)
    # else:
    #     twitt.delete()    
    return HttpResponseRedirect('/profile')

@login_required
def followers(request):
    context = RequestContext(request)
    user_id = get_user_id(request)
    follow_users = get_follow_users(user_id)
    template = 'followers.html'
    return render_to_response(template, locals(), context)

@login_required
def followings(request):
    context = RequestContext(request)
    user_id = get_user_id(request)
    my_followers = Follower.objects.all().filter(user_follow=user_id)
    my_followers = list(map(lambda x: UserView(x.fallowed), my_followers))
    template = 'followings.html'
    return render_to_response(template, locals(), context)

@login_required
@require_http_methods(['POST', ])
@csrf_protect
def stop_follow(request):
    user_id = get_user_id(request)
    unfollow_user_id = request.POST['unfollow_user_id']
    unfollow = Follower.objects.all().filter(
        followed=unfollow_user_id, user_follow=user_id)
    unfollow.delete()
    return HttpResponseRedirect('/profile')

@login_required
@require_http_methods(['POST', ])
@csrf_protect
def follow(request):
    user_id = get_user_id(request)
    follow_user_id = request.POST['follow_user_id']
    follow = Follower(followed=follow_user_id, user_follow=user_id)
    follow.save()
    return HttpResponseRedirect('/profile')

@login_required
def view_profile(request):
    context = RequestContext(request)
    profile_id = request.path.split('/')[2]
    profile = get_profile(profile_id, request)
    template = 'view_profile.html'
    return render_to_response(template, locals(), context)

@login_required
def view_profile_twitts(request):
    context = RequestContext(request)
    profile_id = request.path.split('/')[2]
    profile = get_profile(profile_id, request)
    all_twitts = get_all_twitts_by_user(profile_id)
    template = 'profile_twits.html'
    return render_to_response(template, locals(), context)

@login_required
def view_profile_followers(request):
    context = RequestContext(request)
    profile_id = request.path.split('/')[2]
    profile = get_profile(profile_id, request)
    follow_users = get_follow_users(get_user_id(request), profile.id)
    template = 'profile_followers.html'
    return render_to_response(template, locals(), context)

@login_required
def view_hashtags(request):
    context = RequestContext(context)
    hashtag_id = request.path.split('/')[1]
    user_id = get_user_id(request)
    all_twitts_with_given_hashtag = get_all_twitts_with_given_hashtag(hashtag_id)
    all_twitts = list(map(lambda x: TwittView(x, user_id), all_twitts_with_given_hashtag))
    template = 'hashtag_view.html'
    return render_to_response(template, locals(), context)

@login_required
def view_profile_followings(request):
    pass
