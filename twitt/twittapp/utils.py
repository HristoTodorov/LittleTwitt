import re
from twittapp.models import  Follower, Twitt, User, Trend, HashtagedTwitt
from twittapp.user_view import *


def get_follow_users(user_id, profile_user_id='0'):
    if profile_user_id == '0':
        all_followers = Follower.objects.all().filter(followed=user_id)
    else:
        all_followers = Follower.objects.all().filter(followed=profile_user_id)
    all_followers = list(map(lambda x: UserView(x.user_fallow), all_followers))
    for follower in all_followers:
        follower.is_follow(user_id)
    return all_followers

def get_all_twitts_by_user(user_id):
    return Twitt.objects.all().filter(author_id=user_id)

def get_user_id(request):
    return User.objects.get_or_create(id=request.user.id)[0].id

def find_hashtags(twitt):
    matches = re.findall(r'#\w*', twitt)
    return matches

def contain_hashtag(twitt):
    return len(find_hashtags(twitt)) != 0

# Update the hashtag state. Creates new tupels of type Trend and HashtagedTwitt.
def update_hashtags_state(twitt, twitt_id):
    hashtags_content = remove_hashtag_sign(twitt)
    # Make all letters in lowercase. Hashtags are NOT case-sensitive!
    hashtags_content = set(map(lambda x: x.lower(), hashtags_content))
    for hashtag_content in hashtags_content:
        hashtag = Trend.objects.all().filter(content=hashtag_content)
        try:
            hashtag_count = hashtag[0].count
            Trend.objects.all().filter(id=hashtag[0].id).update(count=hashtag_count + 1)
        except IndexError as e:
            new_hashtag = Trend()
            new_hashtaged_twitt = HashtagedTwitt()
            new_hashtag.content = hashtag_content
            new_hashtag.count = 1
            new_hashtag.save()
            new_hashtaged_twitt.twitt_id = twitt_id
            new_hashtaged_twitt.hashtag_id = new_hashtag.id
            new_hashtaged_twitt.save()

# Remove the hashtag '#' sign.
def remove_hashtag_sign(twitt):
    all_hashtags = find_hashtags(twitt)
    return list(map(lambda x: x[1:], all_hashtags))

# Modify twitt, so the hashtags can be href.
def modify_twitt(twitt):
    all_hashtags = remove_hashtag_sign(twitt)
    for hashtag in all_hashtags:
        pattern = "<a href=\"/hashtag/hashtag_id\">hashtag_content</a>"
        hashtag_object = Trend.objects.all().filter(content=hashtag)[0]
        hashtag_id = hashtag_object.id
        hashtag_content = hashtag_object.content
        pattern = pattern.replace("hashtag_id", str(hashtag_id))
        pattern = pattern.replace("hashtag_content", '#' + hashtag_content)
        twitt = twitt.replace("#" + hashtag, pattern)   
    return twitt

def get_profile(profile_id, request):
    profile = UserView(profile_id)
    profile.is_follow(get_user_id(request))
    return profile

def get_all_twitts(twitts_ids):
    all_twitts = list()
    for twitt_id in twitts_ids:
        all_twitts.append(twitts_ids.twitt_id)
    return all_twitts

def get_all_twitts_with_given_hashtag(hashtag_id):
    twitts_ids = HashtagedTwitt.objects.all().filter(hashtag_id=hashtag_id)
    all_twitts_ids = list()
    for twitt_id in twitts_ids:
        all_twitts.append(twitts_ids.twitt_id)
    return all_twitts_ids

def update_hashtag_count(hashtags_ids):
    for hashtag_id in hashtags_ids:
        hashtag_object = Trend.objects.get(id=hashtag_id)
        if hashtag_object.count == 1:
            hashtag_object.delete()
        else:
            new_count = hashtag_object.count - 1
            Trend.objects.all().filter(id=hashtag_id).update(count=new_count)           
