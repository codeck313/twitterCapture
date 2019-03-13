import settings
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
from http.client import IncompleteRead
import json
import time
import smtplib
import ssl
import threading

db = dataset.connect(settings.CONNECTION_DATABASE)
tweetNo = 0
done = 0
elapsed = 0
names = []
tweetRateCount = 0


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # UNCOMMENT TO REDUCE AMOUNT OF TWEETS
        # if status.retweeted_status:
        #     return
        description = status.user.description
        loc = status.user.location
        coordinates = status.coordinates
        place = status.place
        name = status.user.name
        user_handle = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        friends_count = status.user.friends_count
        verified_stat = status.user.verified
        user_no_tweet = status.user.statuses_count
        if hasattr(status, 'retweeted_status'):
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text

        try:
            if status.retweeted_status:
                retweeted_s = True

        except:
            retweeted_s = False

        bg_color = status.user.profile_background_color
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
                id_str=id_str,
                hashtags=hashtags,
                tweet_created=created,
                user_name=name,
                user_handle=user_handle,
                verified_status=verified_stat,
                origin_source=source,
                isRT=retweeted_s,
                coordinates=coordinates,
                user_location=loc,
                place_name=place_name,
                user_description=description,
                user_followers=followers,
                friends_count=friends_count,
                no_tweet_user=user_no_tweet,
                user_created=user_created,
                user_bg_color=bg_color,
                entities=entitiesDUMP,
                polarity=sent.polarity,
                subjectivity=sent.subjectivity,
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
                raise Exception("Break for renewing trendlist")

            try:
                if (tweetNo % settings.ALERT_COUNT[0] == 0) | (tweetNo % settings.ALERT_COUNT[1] == 0):
                    sendMail(sub=("Tweet Counter Alert " + settings.EMAIL_SUBJECT), text=("Captured " + str(tweetNo) + " tweets."))
            except ZeroDivisionError as e:
                pass

        except ProgrammingError as err:
            print(err)
            sendMail(sub=("Database error " + settings.EMAIL_SUBJECT), text=err)
            pass

    def on_error(self, status_code):
        sendMail(sub=("Tweepy Streaming Class Error " + settings.EMAIL_SUBJECT), text=str(status_code))
        return False


def sendMailThreading(sub, text):
    if settings.MAIL_ALERT:
        smtpserver = smtplib.SMTP(settings.SMTP_SERVER, settings.PORT)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(settings.SENDER_EMAIL, settings.PASWD)
        message = ("Subject: " + sub + " \n\n " + text).encode("utf-8")
        smtpserver.sendmail(settings.SENDER_EMAIL, settings.RECEVIER_EMAIL, message)
        print("Sending email To:", settings.RECEVIER_EMAIL, "Subject :", sub)
        smtpserver.quit()


def sendMail(sub="Hi there", text="foobar"):
    t1 = threading.Thread(target=sendMailThreading, name='t1', args=(sub, text))
    t1.start()


try:
    auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
    api = tweepy.API(auth)
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
except Exception as e:
    sendMail(sub=("Tweepy Authorization Error " + settings.EMAIL_SUBJECT), text=str(e))
    pass

try:
    if settings.TRENDDATA_UPDATE:
        data = api.trends_place(settings.PLACE_CODE)[0]
        trends_list = data['trends']
        names = [trend['name'] for trend in trends_list]
except Exception as e:
    sendMail(sub=("Tweepy Trend Update Error " + settings.EMAIL_SUBJECT), text=str(e))
    pass


track_list_trends = settings.TRACK_TERMS + names
print("Starting Capturing:")
print(track_list_trends)
str_track_list = ' \n '.join(track_list_trends)
sendMail(sub=("Tweet Capture Starting " + settings.EMAIL_SUBJECT), text=("!!STARTING!! Currently capturing " + str_track_list))
start = time.time()


def startStream():
    while True:
        try:
            stream.filter(track=track_list_trends, stall_warnings=True)
        except IncompleteRead as ir:
            sendMail(sub=("Tweepy Filter Function Error " + settings.EMAIL_SUBJECT), text=str(ir))
            continue
        except Exception as e:
            if str(e) == "Break for renewing trendlist":
                break
            sendMail(sub=("Tweepy Filter Function Error " + settings.EMAIL_SUBJECT), text=str(e))
            break


startStream()

while (elapsed > settings.REFRESH_TIME) & settings.TRENDDATA_UPDATE:
    data = api.trends_place(settings.PLACE_CODE)[0]
    trends_list = data['trends']
    names = [trend['name'] for trend in trends_list]
    track_list_trends = settings.TRACK_TERMS + names
    str_track_list = ' \n '.join(track_list_trends)
    print("-----------List aquired-------------")
    print(track_list_trends)
    sendMail(sub=("Tweepy Trend List Renew " + settings.EMAIL_SUBJECT), text=("TweetRate(per min) : " + str(tweetRateCount / (elapsed / 60)) + "\n\n Currently capturing " + str_track_list))
    print("-----------Rolling back the streaming--------------")
    print("starting streaming now!")
    start = done
    tweetRateCount = 0
    startStream()
    done = time.time()
    elapsed = done - start
