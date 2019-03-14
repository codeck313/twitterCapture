TWITTER_KEY = ""  # "Consumer API key"
TWITTER_SECRET = ""  # "Consumer API Secret key"
TWITTER_APP_KEY = ""  # "Access token"
TWITTER_APP_SECRET = ""  # "Access token secret"

TRACK_TERMS = ['#india']  # To add specific terms that you wanna capture

# If you want script to E-mail you the current status of captures and if a error occurs then will report back to you [Error reporting functionlity is still being worked on]
MAIL_ALERT = False
BUG_ALERT = True
ALERT_COUNT = [0, 0]  # Two different Tweets Count, when that hits an email will be send
EMAIL_SUBJECT = "PlaceHolder"  # Email Subject Customization
SENDER_EMAIL = ""  # emailID
RECEVIER_EMAIL = ""  # emaiID
PASWD = ""  # password

PORT = 587
SMTP_SERVER = "smtp.gmail.com"

CONNECTION_DATABASE = 'sqlite:///tweetdata-%s .db' % EMAIL_SUBJECT  # Your DB file name
TABLE_NAME = "tdata"  # Name of the table inside your DB

TRENDDATA_UPDATE = False  # If you want the python script to get the latest trends of a place and add it to the TRACK_TERMS list of yours
REFRESH_TIME = 60  # Update Trend list in SOMENO sec

# The 2 examples provided are for India and Pakistan there are other PLACE_CODE for differnet cities refer to README for more details
PLACE_CODE = 2295411  # Mumbai,India |  Karachi,Pakistan --> 2211096
