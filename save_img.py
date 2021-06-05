import tweepy
import time
import os
import requests
import shutil
import pathlib
from login import login

#login.pyからtokenの取得
consumer_key = login["consumer_key"]
consumer_secret = login["consumer_secret"]
access_token = login["access_token"]
access_token_secret = login["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#保存
def img_download(url, save):
    img = requests.get(url, stream=True)
    file_name = target_id+"/"+save
    print(file_name)
    with open(file_name, 'wb') as image:
        img.raw.decode_content = True
        shutil.copyfileobj(img.raw, image)
    with open(file_path, 'a') as f:
        print(save, file=f)

api = tweepy.API(auth)
#ユーザ名の入力
target_id = input("ユーザー名を入力してください: ")
#@が含まれている場合除去
if "@" in target_id:
    target_id = target_id.strip("@")

#記録用フォルダが存在しない場合作成
if not os.path.exists("url"):
    os.makedirs("url")

#保存先のディレクトリが存在しない場合、ディレクトリを作成する
if not os.path.exists(target_id):
    os.makedirs(target_id)

#記録用ファイルがなければ作成
current_path = os.getcwd()                        
file_path = os.path.join(current_path, "url",target_id+".txt")
file01 = pathlib.Path(file_path)
if not file01.exists():
    file01.touch()

file02 = open(file01)
listing = [s.strip() for s in file02.readlines()]



for tweet in tweepy.Cursor(api.user_timeline, id=target_id).items():
    if not tweet.retweeted and ('RT @' not in tweet.text):
        try:
            url=tweet.extended_entities['media'][0]['media_url']
            print(url)
            save = os.path.basename(url)
            if save in listing:
                print("保存されています")
                print("saved already")
                break
            img_download(url, save)
            time.sleep(1)
        except:
            pass