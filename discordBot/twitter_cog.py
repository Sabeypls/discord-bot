import tweepy
from discord.ext import commands
from discord.utils import get

class twitter(commands.Cog):
    def __init__(self, client):
        self.client = client
        auth = tweepy.OAuth1UserHandler()

        self.twitter = tweepy.API(auth)

        stream = tweepy.StreamingClient()
        #stream.filter(track='maintenance', follow='playlostark', languages='en', is_async=True)
        #stream.add_rules()
        #stream.filter(track='lost ark', is_async=True)
        stream.sample()

    class tweet_print(tweepy.Stream):
        @commands.Cog.listener()
        async def on_tweet(self, ctx, tweet):
            channel = get(ctx.guild.text_channels, name='behind the scene')
            channel.send(tweet)

# on bot start up
# add this cog
# used to reload this cog so the bot doesn't have to go down to update
def setup(client):
    client.add_cog(twitter(client))