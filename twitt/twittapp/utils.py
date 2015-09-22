import re
from twittapp.models import Twitt, User, Trend
from twittapp.user_view import *


# def get_follow_users(user_id, profile_user_id='0'):
#     # if profile_user_id == '0':
#     #     all_followers = Follower.objects.all().filter(followed=user_id)
#     # else:
#     #     all_followers = Follower.objects.all().filter(followed=profile_user_id)
#     # all_followers = list(map(lambda x: UserView(x.user_fallow), all_followers))
#     # for follower in all_followers:
#     #     follower.is_follow(user_id)
#     return all_followers

def get_all_twitts_by_user(user_id):
    return Twitt.objects.all().filter(author_id=user_id)

def get_user_id(request):
    return User.objects.get_or_create(id=request.user.id)[0].id

def find_hashtags(twitt):
    return re.findall(r'#\w*', twitt)

def contain_hashtag(twitt):
    return len(find_hashtags(twitt)) != 0

# Remove the hashtag '#' sign.
def remove_hashtag_sign(twitt):
    all_hashtags = find_hashtags(twitt)
    return list(map(lambda x: x[1:], all_hashtags))

# Modify twitt, so the hashtags can be href.
def modify_twitt(twitt):
    all_hashtags = remove_hashtag_sign(twitt.content)
    for hashtag in all_hashtags:
        pattern = "<a href=\"/hashtag/hashtag_id\">hashtag_content</a>"
        hashtag_object = Trend.objects.all().filter(content=hashtag.lower())[0]
        hashtag_id = hashtag_object.id
        hashtag_content = hashtag_object.content
        pattern = pattern.replace("hashtag_id", str(hashtag_id))
        pattern = pattern.replace("hashtag_content", '#' + hashtag_content)
        twitt.content = twitt.content.replace("#" + hashtag, pattern)   

def get_profile(profile_id, request):
    profile = UserView(profile_id)
    profile.is_follow(get_user_id(request))
    return profile

def get_all_twitts(twitts_ids):
    all_twitts = list()
    for twitt_id in twitts_ids:
        all_twitts.append(twitts_ids.twitt_id)
    return all_twitts

# def get_all_twitts_with_given_hashtag(hashtag_id):
#     twitts_ids = Trend.objects.all().filter(hashtag_id=hashtag_id)
#     all_twitts_ids = list()
#     for twitt_id in twitts_ids:
#         all_twitts.append(twitts_ids.twitt_id)
#     return all_twitts_ids


def create_user_profile(sender, instance, **kwargs):
    user_profile = UserProfile()
    user_profile.save()

#instance = Twitt.
def update_hashtag_status(sender, instance, **kwargs):
    hashtags_content = remove_hashtag_sign(instance.content)
    for hashtag_content in hashtags_content:
        hashtag = Trend.objects.all().filter(content=hashtag_content.lower())
        try:
            hashtag_count = hashtag[0].count
            Trend.objects.all().filter(id=hashtag[0].id).update(count=hashtag_count + 1)
        except IndexError as e:
            new_hashtag = Trend() 
            new_hashtag.content = hashtag_content
            new_hashtag.count = 1
            new_hashtag.save()
            new_hashtag.twitt.add(instance)
    modify_twitt(instance)

#instance = Twitt
def update_hashtag_count(sender, instance, **kwargs):
    all_hashtags_id_in_twitt = Trend.objects.all().filter(twitt_id=instance.id).twitt
    all_hashtags_id_in_twitt = list(map(lambda x: x.trend_id, all_hashtags_id_in_twitt))
    for hashtag_id in all_hashtags_id_in_twitt:
        hashtag_object = Trend.objects.get(id=hashtag_id)
        if hashtag_object.count == 1:
            hashtag_object.delete()
        else:
            new_count = hashtag_object.count - 1
            Trend.objects.all().filter(id=hashtag_id).update(count=new_count)           

def update_followers_count(user):
    User.objects.get(id=user.id).update(followers=user.followers+1) 

post_save.connect(update_hashtag_status, sender=Twitt, dispatch_uid="update_hashtag_status")
post_delete.connect(update_hashtag_count, sender=Twitt, dispatch_uid="update_hashtag_count")
post_save.connect(create_user_profile, sender=User, dispatch_uid="create_user_profile")