import slacker
import slackbot_settings as ss
import json

from md_render import render

USERS = {}

DEFAULT_HISTORY_CACHE = "history.json"
DEFAULT_CHANNEL_CACHE = "channels.json"
DEFAULT_USER_CACHE = "users.json"

class HistoryCache(object):
    def __init__(self, slacker, cachefile=None):
        if cachefile != None:
            with open(cachefile, 'r') as ifile:
                self._data = json.load(ifile)
        else:
            self._data = {}

        self._slacker = slacker
        self.cachefile = cachefile

    def get_newest_ts(self, channel_id):
        if channel_id in self._data and len(self._data[channel_id]) > 0:
            last = self._data[channel_id][0]["ts"]
        else:
            last = None

        return last

    def get_channel_history(self, channel_id, latest=None):
        messages = []
        while(True):
            print("\tGetting {}".format("Latest" if latest == None else latest))
            x = self._slacker.channels.history(channel_id, oldest=latest).body

            for i in x["messages"]:
              messages.append(i)

            if x["has_more"]:
              latest = x["messages"][-1]["ts"]
            else:
              break

        return messages

    def update_channel(self, channel_id):
        latest = self.get_newest_ts(channel_id)

        if latest is None:
            self._data[channel_id] = []

        temp_hist = self.get_channel_history(channel_id, latest)

        self._data[channel_id] = temp_hist + self._data[channel_id]

class ChannelCache(object):
    def __init__(self, slacker, cachefile=None):
        if cachefile != None:
            with open(cachefile, 'r') as ifile:
                self._data = json.load(ifile)
        else:
            self._data = []

        self._slacker = slacker
        self.cachefile = cachefile

    def update(self):
        new_channel = self._slacker.channels.list().body["channels"]

        for nc in new_channel:
            for c in self._data:
                # Update channels with new data
                if c["id"] == nc["id"]:
                    c = nc
                    break
            else:
                # Add newly added channels
                self._data.append(nc)

    def get_channels(self):
        return self._data

class UserCache(object):
    def __init__(self, slacker, cachefile=None):
        if cachefile != None:
            with open(cachefile, 'r') as ifile:
                self._data = json.load(ifile)
        else:
            self._data = {}

        self._slacker = slacker
        self.cachefile = cachefile

    def resolve_user(self, user_id):
        if not user_id in self._data:
            self._data[user_id] = self._slacker.users.info(user=user_id).body['user']['name']

        return self._data[user_id]

def connect(api_token):
    her = slacker.Slacker(api_token)
    x = her.rtm.start().body
    # print(x["self"]["name"])

    return her

def main():
    slacker = connect(ss.API_TOKEN)

    history = HistoryCache(slacker=slacker, cachefile=DEFAULT_HISTORY_CACHE)
    channels = ChannelCache(slacker=slacker, cachefile=DEFAULT_CHANNEL_CACHE)
    users = UserCache(slacker=slacker, cachefile=DEFAULT_USER_CACHE)

    channels.update()

    for channel in channels.get_channels():
        i = channel["id"]

        print("getting {}...".format(channel["name"]))

        history.update_channel(i)


    return

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

    with open("history.html", "w") as ofile:
        ofile.write(render(channels=raw_channels, history=hist, users=USERS))

# def resolve_user(slacker, user_id):
#     if not user_id in USERS:
#         USERS[user_id] = slacker.users.info(user=user_id).body['user']['name']

#     return USERS[user_id]

# def get_channels(slacker):
#     x = slacker.channels.list()

#     if not (x.successful and x.body["ok"]):
#         return None

#     return x.body["channels"]

# def get_channel_history(slacker, channel_id, latest=None):
#     messages = []
#     while(True):
#         print("\tGetting {}".format("Latest" if latest == None else latest))
#         x = slacker.channels.history(channel_id, oldest=latest).body
#         for i in x["messages"]:
#           messages.append(i)
#         if x["has_more"]:
#           latest = x["messages"][-1]["ts"]
#         else:
#           break
#     return messages

if __name__ == '__main__':
    main()