import slacker
import slackbot_settings as ss
import json

USERS = {}

def main():
    her = slacker.Slacker(ss.API_TOKEN)
    x = her.rtm.start().body
    print(x["self"]["name"])

    chans = [{"name": x["name"], "id": x["id"]} for x in get_channels(her)]

    hist = []
    for i in chans:
        print(i["name"])
        if i["name"] == "crafternoon":
            hist = get_channel_history(her, i["id"])

    for msg in hist[::-1]:
        print(msg["ts"], resolve_user(her, msg["user"]), msg["text"])

    with open("users.json", "w") as ufile:
        json.dump(USERS, ufile)

def resolve_user(slacker, user_id):
    if not user_id in USERS:
        USERS[user_id] = slacker.users.info(user=user_id).body['user']['name']

    return USERS[user_id]

def get_channels(slacker):
    x = slacker.channels.list()

    if not (x.successful and x.body["ok"]):
        return None

    return x.body["channels"]

def get_channel_history(slacker, channel_id, latest=None):
    messages = []
    while(True):
        x = slacker.channels.history(channel_id, latest=latest).body
        for i in x["messages"]:
          messages.append(i)
        if x["has_more"]:
          last = x["messages"][-1]["ts"]
        else:
          break
    return messages

if __name__ == '__main__':
    main()