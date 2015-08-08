class TwittView():
	def __init__(self, twitt_id, user_id):
		self.twitt_id = twitt_id
		self.twitt_object = Twitt.objects.all().filter(id=twitt_id)[0]
		self.author_id = self.twitt_object.author_id
		self.author_profile = UserView(self.author_id)
		self.author_id.is_follow(user_id)
		self.is_retwitt = self.is_retwitt(user_id)

	def is_retwitt(self, user_id):
		return Retwitt.objects.all().filter(twitt_id=twitt_id, retwitter_id=user_id).count() == 1	

