import settings
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import time
import smtplib
import ssl


db = dataset.connect(settings.CONNECTION_STRING)
tweetNo = 0
done = 0
elapsed = 0
names = []
tweetRateCount = 0
port = 587  # For starttls
smtp_server = "smtp.gmail.com"


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
        verified_stat = status.user.verified
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
                verified_status=verified_stat,
            ))
            global tweetNo
            global done, elapsed, tweetRateCount
            done = time.time()
            elapsed = done - start
            tweetNo += 1
            tweetRateCount += 1
            if settings.TRENDDATA_UPDATE:
                print("Tweet Counter : ", tweetNo, "|| Time to Refresh:", int(settings.REFRESH_TIME - elapsed))
            else:
                print("Tweet Counter : ", tweetNo)
            if (elapsed > settings.REFRESH_TIME) & settings.TRENDDATA_UPDATE:
                print("Renewing list")
                return False
            if (tweetNo % settings.ALERT_DURATION[0] == 0) | (tweetNo % settings.ALERT_DURATION[1] == 0):
                sendMail(sub=("Tweet Counter Alert " + settings.FOOTER_SUBJECT), text=("Currently opperating with No." + str(tweetNo) + " tweets."))
        except ProgrammingError as err:
            print(err)
            sendMail(sub=("Database error " + settings.FOOTER_SUBJECT), text=err)
            pass

    def on_error(self, status_code):
        sendMail(sub=("Tweepy Capturing Error " + settings.FOOTER_SUBJECT), text=str(status_code))
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def sendMail(sub="Hi there", text="foobar"):
    message = ("Subject: " + sub + " \n\n " + text).encode("utf-8")
    smtpserver.sendmail(settings.SENDER_EMIAL, settings.RECEVIER_EMAIL, message)
    print("Sending email To:", settings.RECEVIER_EMAIL)


context = ssl.create_default_context()
smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login(settings.SENDER_EMIAL, settings.PASWD)

try:
    auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
    api = tweepy.API(auth)
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
except Exception as e:
    sendMail(sub=("Tweepy Authorization Error " + settings.FOOTER_SUBJECT), text=str(e))
    pass

try:
    if settings.TRENDDATA_UPDATE:
        data = api.trends_place(settings.PLACE_CODE)[0]
        trends_list = data['trends']
        names = [trend['name'] for trend in trends_list]
except Exception as e:
    sendMail(sub=("Tweepy Trend Update Error " + settings.FOOTER_SUBJECT), text=str(e))
    pass


track_list_trends = settings.TRACK_TERMS + names
print("Starting Capturing:")
print(track_list_trends)
str_track_list = ' \n '.join(track_list_trends)
sendMail(sub=("Tweet Capture Starting " + settings.FOOTER_SUBJECT), text=("!!STARTING!! Currently capturing " + str_track_list))
start = time.time()
stream.filter(track=track_list_trends)

try:
    while (elapsed > settings.REFRESH_TIME) & settings.TRENDDATA_UPDATE:
        data = api.trends_place(settings.PLACE_CODE)[0]
        trends_list = data['trends']
        names = [trend['name'] for trend in trends_list]
        track_list_trends = settings.TRACK_TERMS + names
        str_track_list = ' \n '.join(track_list_trends)
        print("-----------List aquired-------------")
        print(track_list_trends)
        sendMail(sub=("Tweepy Trend List Renew " + settings.FOOTER_SUBJECT), text=("Currently capturing " + str_track_list + "\n\n TweetRate(per min) : " + str(tweetRateCount / (elapsed / 60))))
        print("-----------Rolling back the streaming--------------")
        print("starting streaming now!")
        start = done
        tweetRateCount = 0
        stream.filter(track=track_list_trends)
        done = time.time()
        elapsed = done - start
except Exception as e:
    sendMail(sub=("Renewing Trend List Error " + settings.FOOTER_SUBJECT), text=str(e))
    pass
