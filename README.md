
# twitterCapture
This is a automation script for *tweepy's streaming class* with some included with some additional features allowing it to be run on a external server to capture data right of the bat. It has **E-Mail notification** and ability to **update** one's **filter terms** based on the **trends list** of a particular area built into it. It stores everything into a sqlite3 database by default.

## Table of contents

 * [Getting Started](https://github.com/codeck313/twitterCapture#getting-started)
     * [Prerequisites](https://github.com/codeck313/twitterCapture#prerequisites)
     * [Setup](https://github.com/codeck313/twitterCapture#setup)
* [Customization](https://github.com/codeck313/twitterCapture#customization)
     * [Enabling Mail Alert](https://github.com/codeck313/twitterCapture#enabling-mail-alert)
     * [Database customization](https://github.com/codeck313/twitterCapture#database-customization)
     * [Enabling Trendlist update functionality](https://github.com/codeck313/twitterCapture#enabling-trendlist-update-functionality)
* [METADATA Being Collected](https://github.com/codeck313/twitterCapture#metadata-being-collected)
* [Deployment on  a Linux Server (Raspberry Pi)](https://github.com/codeck313/twitterCapture#deployment-on--a-linux-server-raspberry-pi)
* [Build With](https://github.com/codeck313/twitterCapture#build-with)
* [Acknowledgement](https://github.com/codeck313/twitterCapture#acknowledgement)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for testing purposes. See deployment notes on how to deploy the project on a to run 24x7 on system.

### Prerequisites
First clone the Git repository from GitHub and install required libraries by:

    git clone https://github.com/codeck313/twitterCapture.git
    cd twitterCapture
    pip install -r requirements.txt

By default it is using using sqlite3. Though you can change it to other DB management system you like
To use sqlite3 :

On Windows download the [pre-compiled binaries](https://sqlite.org/download.html)

On Linux :

    sudo apt-get install sqlite3


### Setup

First create a Twitter developer account from here :  [Developer Twitter](]http://developer.twitter.com/)
**After creating** your developer account head over to app section and create a new app. : [App Twitter](https://developer.twitter.com/en/apps)
After creation of a new app to get your Keys and tokens from that app follow this: [Guide: Access Token](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)

You should now have keys for these fields in `settings.py` :

    TWITTER_KEY = ""  # "Consumer API key"
    TWITTER_SECRET = ""  # "Consumer API Secret key"
    TWITTER_APP_KEY = ""  # "Access token"
    TWITTER_APP_SECRET = "" # "Access token secret"
Now you could just mention the terms you want to track in a tweet add those to the list `TRACK_TERMS` in `settings.py`.Like below:

    TRACK_TERMS = ["#India","python"]

This is the most basic setup required to start using this script.You can customize it further to suite your personal need.

## Customization
You can customize these things to further utilize the script:

### Enabling Mail Alert
You can get mail alerts when an error happens in the code or when the trend list updated or when you receive certain amount of tweets.

By default it's using Gmail as the email provider. If you aren't using gmail as you email service change settings `SMTP_SERVER` and `PORT` to meet your email service config.

Add your email ID and password and which Email ID you wanna send it to:

    SENDER_EMAIL = "tutorialSender@twittercap.com"
    PASWD = "123456" #we dont recommend it though ;)
    RECEVIER_EMAIL  = "tutorialReciever@twittercap.com"
Add the subject name you want to show up in as the subject of the email you will receive

    EMAIL_SUBJECT  = "Tutorial"

Now you can mention the no of tweets after which you would like an update form the script to know it has reached that count.You can mention upto 2 Tweet count no after which you would like an update.

    # Will update you once the script has recorded 20 or 200 tweets or its multiple
    ALERT_DURATION = [20,200]

But if you don't want to utilize this feature just use `[0,0]` or you want tweets at only one no use `[YOUR_NO,0]`


After that just change the boolean value of `MAIL_ALERT` to `True` to start using this feature.

**For Gmail users only**
You would need to enable *3rd Party less secure apps to login* in you Gmail ID [for more details](https://support.google.com/accounts/answer/6010255).

### Database customization
To use other database management system :

    # Using MySQL database with username and password
    CONNECTION_STRING = 'mysql://user:password@localhost/mydatabase'

    # Using PostgreSQL database
    CONNECTION_STRING = 'postgresql://scott:tiger@localhost:5432/mydatabase'

To change the table name in which the data is stored use :

    TABLE_NAME='YOUR_NAME'

### Enabling Trendlist update functionality
If you want your system to get the trend list of a particular place and use it to update your tweet tracking (or filtering) list follow along the steps

To start using this feature set boolean value of `TRENDDATA_UPDATE` to `True`
To specify the amount of time after which you want to grab the list using Twitter API

    #the time is in seconds format
    REFRESH_TIME=600 #10mim
  Specify the Place Code of the place you want the trends to be picked off from

    #For Mumbai,India it's 2295411
    PLACE_CODE  =  2295411
For the complete list of Cities and their WOEID code [refer to this](https://codebeautify.org/jsonviewer/f83352)
You can mention additional tracking(or filtering) by mentioning them in the `TRACK_TERMS` list

## METADATA Being Collected
*Tweet's text is collected in extended form.*

About **19** different type of **METADATA** is stored in the database making it the **user's choice** to keep or discard the data her/he doesn't need afterwards instead of ending up with less data from the zero point.
The different METADATA other than tweets text are:
* `id_str` : The unique identifier for this tweet.
* `hastags` : Different hashtags used in a tweets of segregated into this field.
* `tweet_created` : As the name suggest it has the tweet's date and time stamp.
* `user_name` : The user name of the person who tweeted the text.
* `user_handle` : Her/His handle.
* `verified_status` : Indicates whether that the user has a verified account.
* `origin_source` : From what device or service the person has tweeted. Like the good o'l [*Twitter for iPhone*](https://www.youtube.com/watch?v=cZIso9uqNls) .
* `isRT`  : Boolean value of whether it's a retweet or not.
* `coordinates` : Location of the tweet as reported by the user or the client application.
* `user_location` : Location of the user as reported by him.
* `place_name` : Indicate the place name that the tweet is associated with (but not necessarily originating from).
* `user_description`  : User's twitter account description.
* `user_followers` : Number of followers the user's account currently has.
* `friends_count` : Number of people the user is following.
* `no_tweet_user` : Number of tweet this user has posted.
* `user_created` : Date when the user was created.
* `user_bg_color` : The hexadecimal color chosen by the user for their background.
* `entities` : This provides arrays of common things included in Tweets like hashtags, user mentions, links, attached media [and more.](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/entities-object) This is saved in a form of text so you would need regex to segregate different aspects from it.
* `polarity` : On a scale of +1 to -1 where does a persons tweets lies on the polarity scale (How positive or negative a text is).
* `objectivity` : Whether a tweet presents a facts (higher objectivity) or provides a person's analysis or opinion. [For more details.](https://www.quora.com/Does-an-objective-sentence-imply-a-non-neutral-sentiment)

## Deployment on  a Linux Server (Raspberry Pi)
In order to run the script on a external server you can do the following steps in order to make it operational 24x7.

All the `.sh`scripts are in the project file with a copy of the `crontab -e` log.

First open `launcher.sh` in the cloned project directory. Edit the `cd` command in the script so that it opens your project directory.

    cd /home/pi/tweetCapture

Next up edit the `connectivity.sh`  line 5 to point to the place where the `launcher.sh` is saved

    [23])  echo "HTTP connectivity is up "
        /path/to/launcher.sh;;  <<<< THIS LINE
          5) echo "The web proxy won't let us through";;

Now type the following command into to terminal:

    crontab -e

and add these following lines to it :

    @reboot sh /path/to/connectivity.sh > ~/logs/cronlogTwitterCapture 2>&1
    */5 * * * * sh ~/indCap/connectivity.sh > ~/logs/cronlogTwitterCapture 2>&1
**Remeber to change** the */path/to/connectivity.sh* to path of your `connectivity.sh` file.
* The first line makes the script to run on every reboot of the system
* Second line runs the script every 5 mins.Though the python script will run if and only if its not running already.

Save the file and exit.

Now after a reboot your script should start running. If for some reason it gets closed like disconnection of the network or some error in the API. It will again start in 5 min or when ever network is established and if opted for Email notification you would be notified subsequently.

## Build With
* [Tweepy](https://github.com/tweepy/tweepy) For the Twitter API
* [Dataset](https://github.com/pudo/dataset) For writing data to database
* [TextBlob](https://github.com/sloria/TextBlob) For NLTK analysis


## Acknowledgement
* Thanks to [Jinal](https://github.com/jinalskothari) and Aditya for their unwavering support.
* [WeWorkPlay Article on conrtab](https://weworkweplay.com/play/rebooting-the-raspberry-pi-when-it-loses-wireless-connection-wifi/)
* Gilles [For the web connectivity testing tool](https://unix.stackexchange.com/questions/190513/shell-scripting-proper-way-to-check-for-internet-connectivity/190610)
