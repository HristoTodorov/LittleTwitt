from twittapp.models import Follower, User, Media
from views import get_all_twitts

class UserView():
    def __init__(self, user_id):
        self.id = user_id
        self.user = User.objects.all().filter(id=user_id)[0]
        self.username = self.user.username
        user_profile = UserProfile.objects.all().filter(user_id=user_id)[0]
        self.moto = user_profile.moto
        self.image_profile = Media.objects.all().filter(
            id=user_profile.avatar_id)[0].picture.url
        self.email = self.user.email
        self.twitts_number = get_all_twits(user_id).count()
        self.full_name(self.user.first_name, self.user.last_name)
        self.followers()
        self.followings()
        self.date_joined()
        self.last_login()

    def full_name(self, first_name, last_name):
        self.name = first_name + " " + last_name

    def followers(self):
        self.followers = Follower.objects.all().filter(
            fallowed=self.id).count()

    def followings(self):
        self.followings = Follower.objects.all().filter(
            user_fallow=self.id).count()

    def date_joined(self):
        self.date_joined = self.user.date_joined

    def last_login(self):
        self.last_login = self.user.last_login

    def is_follow(self, fallow_by):
        self.is_follow = True if Follower.objects.all().filter(
            fallowed=self.id, user_fallow=fallow_by).count() == 1 else False
