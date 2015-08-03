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
from user_view import UserView


def set_hashtag_href(twitt_content):
    matches = re.findall(r'#\w*', twitt_content)
    for match in matches:
        
        twitt_content.replace


def get_follow_users(user_id, profile_user_id='0'):
    if profile_user_id == '0':
        all_followers = Follower.objects.all().filter(fallowed=user_id)
    else:
        all_followers = Follower.objects.all().filter(fallowed=profile_user_id)
    all_followers = list(map(lambda x: UserView(x.user_fallow), all_followers))
    for follower in all_followers:
        follower.is_follow(user_id)
    return all_followers


def get_all_twits(user_id):
    return Twitt.objects.all().filter(author_id=user_id)


def get_user_id(request):
    return User.objects.get_or_create(id=request.user.id)[0].id


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
    all_twitters = get_all_twits(user_id)
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
    new_twitt.content = content
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
    my_followers = Follower.objects.all().filter(user_fallow=user_id)
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
        fallowed=unfollow_user_id, user_fallow=user_id)
    unfollow.delete()
    return HttpResponseRedirect('/profile')


@login_required
@require_http_methods(['POST', ])
@csrf_protect
def follow(request):
    user_id = get_user_id(request)
    follow_user_id = request.POST['follow_user_id']
    follow = Follower(fallowed=follow_user_id, user_fallow=user_id)
    follow.save()
    return HttpResponseRedirect('/profile')


def get_profile(profile_id, request):
    profile = UserView(profile_id)
    profile.is_follow(get_user_id(request))
    return profile


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
    all_twitts = get_all_twits(profile_id)
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
def view_profile_followings(request):
    pass
