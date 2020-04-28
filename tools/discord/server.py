from flask import Flask, request
import requests
import yaml
import html

"""
This is a Flask webpage designed to be called from byond with Export, which then
triggers webhooks for discord.

It needs to be filled out correctly to work, duh

Also this was made by CthulhuOnIce
"""

valid = "<>ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;= "

def HTMLEntitiesToUnicode(text):
   return html.unescape(text)

def url2msg(msg):
    msg = HTMLEntitiesToUnicode(msg)
    for x in msg:
        if x not in valid:
            msg = msg.replace(x, "")
    conversions = {
    "[fwslash]" : "/",
    "[colon]": ":",
    "[bslash]": "\\",
    "[qmark]": "?",
    "[space]": " ",
    "[quote]": "\"",
    "@": "(a)", # no @ abuse
    "[nl]": "\n",
    }
    for x in conversions:
        msg = msg.replace(x, conversions[x])
    return msg

c = {}
with open("config.yml", "r") as r:
    c = yaml.load(r)

ip_whitelist = c["ip-whitelist"]

ooc_webhook = c["https://discordapp.com/api/webhooks/704786445721665587/UkuJkt3dLPM8ZwwKPZ6oO5O8G1Gs3ddHz-JwWk66__keHSmSgbAuBmPvk5CQ7aa894pr"]
ahelp_webhook = c["https://discordapp.com/api/webhooks/704786123150327890/jGMqave54wid8bLZSKfyo5AC7CaJvfIoIQFkFnWv3H42zX-TQ2m2YWU9V0yoZzGvuvKu"]

app = Flask(__name__)


@app.route('/')
def hello():
    return "<h1>You Probably Shouldn't Be Here.</h1>"

@app.route("/api/<channel>/<message>")
def trigger(channel, message):
    global ip_whitelist
    global ooc_webhook
    if(request.remote_addr not in ip_whitelist):
        return "<h1>Access Denied.</h1>"
    message = url2msg(message)
    data = {
        "content": message
        }
    if channel == "ooc":
        requests.post(ooc_webhook, data=data)
        return message
    elif channel == "ahelp":
        requests.post(ahelp_webhook, data=data)
        return message
    else:
        return "<h1>Channel not found</h1>"

if __name__ == '__main__':
    app.run()
