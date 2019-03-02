import settings
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json

db = dataset.connect(settings.CONNECTION_STRING)
tweetNo = 0


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # UNCOMMENT TO REDUCE AMOUNT OF TWEETS
        # if status.retweeted_status:
        #     return
        description = status.user.description
        loc = status.user.location
        text = status.text
        coordinates = status.coordinates
        place = status.place
        name = status.user.name
        user_handle = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        reply_count = status.reply_count
        quote_count = status.quote_count
        user_no_tweet = status.user.statuses_count
        friends_count = status.user.friends_count
        try:
            if status.retweeted_status:
                retweeted_s = True

        except:
            retweeted_s = False

        bg_color = status.user.profile_background_color
        favorite_count = status.favorite_count
        entities = status.entities
        source = status.source
        blob = TextBlob(text)
        sent = blob.sentiment
        place_name = ''
        place_corr = ''
        if coordinates is not None:
            coordinates = json.dumps(coordinates)
        if place is not None:
            place_name = place.full_name

        if entities is not None:
            entitiesDUMP = json.dumps(entities)

        hashtags = ''
        for hashlist in entities['hashtags']:
            hashtags = ''.join(hashlist['text'])

        table = db[settings.TABLE_NAME]

        try:
            table.insert(dict(
                text=text,
                hashtags=hashtags,
                entities=entitiesDUMP,
                tweet_created=created,
                favorite_count=favorite_count,
                retweet_count=retweets,
                reply_count=reply_count,
                quote_count=quote_count,
                retweeted_status=retweeted_s,
                origin_source=source,
                user_name=name,
                user_handle=user_handle,
                user_description=description,
                user_followers=followers,
                user_no_tweet=user_no_tweet,
                friends_count=friends_count,
                place_name=place_name,
                coordinates=coordinates,
                user_created=user_created,
                user_location=loc,
                id_str=id_str,
                user_bg_color=bg_color,
                polarity=sent.polarity,
                subjectivity=sent.subjectivity,
            ))
            global tweetNo
            tweetNo += 1
            print("Tweet Counter : ", tweetNo)
        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)
