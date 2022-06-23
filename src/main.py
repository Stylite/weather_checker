import os
import requests
import discord
import time
import datetime
import json
from discord import Webhook, RequestsWebhookAdapter, Embed


with open("config.json") as config:
    config = json.load(config)

headers = {
    "User-Agent": "(stylite.me, me@stylite.me)"
}
location = config['location_code']

webhook = Webhook.from_url(config['webhook_url'], adapter=RequestsWebhookAdapter())


while True:
    alerts = requests.get(location, headers=headers)
    alerts = json.loads(alerts.content)
    features = alerts['features']

    if len(features) == 0:
        alert = "No Alerts found"
        description = "No Alert description"
    else:
        alert = alerts['features'][0]['properties']['headline']
        description = alerts['features'][0]['properties']['description']

    updated_time = datetime.datetime.strptime(alerts['updated'], '%Y-%m-%dT%H:%M:%S+00:00').strftime("%m/%d/%y %I:%M" "%p")
    current_time = datetime.datetime.now().strftime("%m/%d/%y %I:%M" "%p")
    em = discord.Embed(color=int("0xffc0c0", 16))
    em.title = alerts['title']
    em.description = f"Current alerts: {alert}\n\nDescription: {description}\n\n Updated date: {updated_time}\n Current date: {current_time}"
    if alert == "No Alerts found":
        time.sleep(60)
    else:
       webhook.send(embed=em)
       time.sleep(900)
