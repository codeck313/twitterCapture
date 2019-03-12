TRACK_TERMS = []  # To add specific terms that you wanna capture
TRENDDATA_UPDATE = True  # If you want the python script to get the lateset trends of a place and add it to the TRACK_TERMS list of yours
REFRESH_TIME = 60000  # Period of time after which the script should update its Trends list, if the above option is true
TABLE_NAME = "tdata"  # Name of the table inside your DB
# PLACE_CODE = 2211096 #pakistan
PLACE_CODE = 2295411  # india #The 2 examples provided are for India and Pakistan there are other PLACE_CODE for differnet countries and citites refer to twittter
# Documentation to find out the codes for your place of choice

MAIL_ALLERT = True  # If you want script to E-mail you the current status of captures and if a error occurs then will report back to you [Error reporting
# functionlity is still being worked on]
ALERT_DURATION = [50000, 100000]  # List of ONLY 2 OBJECTS #Mention Your 2 different Tweets Count you want a mail to be sent to you
EMAIL_SUBJECT = "Test"  # Email Subject Customization
PORT = 587  # For starttls
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = ""  # emailID
RECEVIER_EMAIL = ""  # emaiID
PASWD = ""  # password

TWITTER_KEY = ""  # "Consumer API key"
TWITTER_SECRET = ""  # "Consumer API Secret key"
TWITTER_APP_KEY = ""  # "Access token"
TWITTER_APP_SECRET = ""  # "Access token secret"
CONNECTION_STRING = 'sqlite:///tweetdata-%s .db' % EMAIL_SUBJECT  # Your DB file name
