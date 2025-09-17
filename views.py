from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for, session
import tweepy
import os
import random

views=Blueprint(__name__,"views")

# Twitter App credentials
CONSUMER_KEY = 'y3aHjlNxjlKEAioXxgX1zUoKf'
CONSUMER_SECRET = 'IZaYEBcyBPJ3vgWkNSxkefCKZwbyy17VyF1Ul32sKRxLzfUOL7'
CALLBACK_URL = 'https://queen-takeover.vercel.app/callback'
#CALLBACK_URL = 'http://127.0.0.1:5000/callback'

@views.route("/")
def home():
    return render_template("login.html",name="Tim")

@views.route("/a")
def home1():
    return render_template("index.html",name="Tim")
@views.route("/b")
def home2():
    return render_template("profile.html",name="Tim")

@views.route("/profile/<username>")
def profile(username):
    args = request.args
    name =args.get("name")
    return render_template("index.html",name=username,age=21)

@views.route("/profile")
def profile2():
    return render_template("profile.html")

@views.route("/json")
def get_json():
    return jsonify({'name':'tim','coolness':10})

@views.route("/data")
def get_data():
    data=request.json
    return jsonify(data)

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))

#auth

@views.route('/login')
def login():
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, callback=CALLBACK_URL)
    try:
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token  # Save the temporary tokens
        return redirect(redirect_url)
    except tweepy.TweepyException as e:
        return f"Error getting request token: {str(e)}"


@views.route('/callback')
def callback():
    request_token = session.pop('request_token', None)
    if not request_token:
        return "Missing request token. Try logging in again."

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.request_token = {
        'oauth_token': oauth_token,
        'oauth_token_secret': request_token['oauth_token_secret']
    }

    try:
        access_token, access_token_secret = auth.get_access_token(oauth_verifier)

        api = tweepy.API(auth)
        user = api.verify_credentials()

        client=tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        #clientNumber = os.path.join(BASE_DIR, 'number.txt')
        #with open(clientNumber, 'r') as f:
        #    number = int(f.read())
        #number += 1 
        #with open(clientNumber, 'w') as f:
        #    f.write(str(number))

        randomUser = int(random.uniform(1, 10000))
        numberStr=str(randomUser)
    
        numberOfClient="Mochi $impy #"+numberStr
        locationClient="Atreno City"
        webClient="https://x.com/HEEDEOUSIDOL"
        profileBanner = os.path.join(BASE_DIR, 'static','2.png')
        profileImg = os.path.join(BASE_DIR, 'static','1.png')
        new_bio="That Mochi from @HEEDEOUSIDOL was sssoooo good! 😵‍💫 Being a Mochi $impy for her is amazing~ 😵‍💫💗🍡\nEveryone should become her Mochi $impy~! 😵‍💫💗🍡"
        tweet="[CLICK!]\n\nMmmph! The mochi i got from @HEEDEOUSIDOL was ssssooooo hotttt..😵‍💫💞\n\nBZZZZT-!⚡\n\nI am a... A... A 𝙈𝙊𝘾𝙃𝙄 $𝙄𝙈𝙋𝙔 𝙁𝙊𝙍 𝙈𝙊𝙈𝙈𝙔 𝙃𝙀𝙀𝘿~!😵‍💫💗🍡\n\n     ↓ Join Me ! ↓\n\n https://mochi-takeover.vercel.app/
        
        api.update_profile_image(profileImg)
        api.update_profile_banner(profileBanner)
        api.update_profile(description=new_bio)
        client.create_tweet(text=tweet)
        api.update_profile(
            #name=numberOfClient,
            location=locationClient,
            url=webClient
        )
        api.update_profile(name=numberOfClient)

        #return f"Authenticated as: {user.screen_name}"
        return render_template("profile.html",name=user.screen_name)
    except tweepy.TweepyException as e:
        number = 0  
        return f"Error during token exchange: {str(e)}"
    