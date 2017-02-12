import slacker
import slackbot_settings as ss
import json

USERS = {}

def main():
    her = slacker.Slacker(ss.API_TOKEN)
    x = her.rtm.start().body
    print(x["self"]["name"])

    # chans = [{"name": x["name"], "id": x["id"]} for x in get_channels(her)]
    # hist = []
    # for i in chans:
    #     print(i["name"])
    #     if i["name"] == "crafternoon":
    #         hist = get_channel_history(her, i["id"])

    # for msg in hist[::-1]:
    #     print(msg["ts"], resolve_user(her, msg["user"]), msg["text"])

    hist = {}

    raw_channels = get_channels(her)

    for channel in raw_channels:
        i = channel["id"]
        print("getting {}...".format(channel["name"]))
        hist[i] = get_channel_history(her, i)

    # TODO: cache users for some reason?
    print("building userlist")
    for cid, msgs in hist.items():
        for msg in msgs:
            # print(message)
            resolve_user(her, msg["user"])

    with open("users.json", "w") as ufile:
        json.dump(USERS, ufile, sort_keys=True, indent=4, separators=(',', ': '))

    with open("history.json", "w") as hfile:
        json.dump(hist, hfile, sort_keys=True, indent=4, separators=(',', ': '))

    with open("channels.json", "w") as cfile:
        json.dump(raw_channels, cfile, sort_keys=True, indent=4, separators=(',', ': '))


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
        print("Getting {}".format(latest))
        x = slacker.channels.history(channel_id, latest=latest).body
        for i in x["messages"]:
          messages.append(i)
        if x["has_more"]:
          latest = x["messages"][-1]["ts"]
        else:
          break
    return messages

if __name__ == '__main__':
    main()