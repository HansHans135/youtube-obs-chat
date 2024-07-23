
import pytchat
import json
import threading
from flask import Flask, render_template, request, jsonify

app=Flask(__name__)
li=[]

with open("config.json", encoding="utf-8") as f:
    config=json.load(f)

@app.route("/")
async def index():
    with open("index.html",encoding="utf-8") as f:
        h=f.read()
    return h

@app.route("/chat")
async def web_chat():
    response=jsonify(li)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def startweb():
    app.run(host="0.0.0.0",port=15873)


t = threading.Thread(target=startweb)
t.start()


chat = pytchat.create(video_id=config["live_id"])

while chat.is_alive():
    for c in chat.get().sync_items():
        data=eval(c.json().replace("true", "True").replace("false", "False").replace("null", "None"))
        text=c.message
        for i in data["messageEx"]:
            if "url" in i:
                text=text.replace(i["txt"],f"<img src='{i["url"]}' height='23px'/> ")
        if data["author"]["isChatOwner"]:
            color=config["color"]["isChatOwner"]
        elif data["author"]["isChatModerator"]:
            color=config["color"]["isChatModerator"]
        elif data["author"]["isChatSponsor"]:
            color=config["color"]["isChatSponsor"]
        else:
            color=config["color"]["default"]
        #msg=f"<p><span style='color: {color};'>{c.author.name}</span> <span style='color: black;'>: {text}</span></p>"
        msg={
            "message":text,
            "author":c.author.name,
            "name_color":color,
            "msg_color":"black"
        }
        if len(li)>config["message_amount"]:
            li=li[1:]
            li.append(msg)
        else:
            li.append(msg)
