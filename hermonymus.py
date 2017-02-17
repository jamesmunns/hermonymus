#!/usr/bin/python3

import json
import argparse
import os

import slacker

from md_render import render

class HistoryCache(object):
    def __init__(self, slacker, cachefile=None):
        if cachefile != None and os.path.isfile(cachefile):
            with open(cachefile, 'r') as ifile:
                self._data = json.load(ifile)

                # ensure data is sorted newest to oldest
                for channel, messages in self._data.items():
                    self._data[channel] = sorted(messages, key=lambda x: float(x["ts"]), reverse=True)
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
        newest = None
        while(True):
            print("\tGetting {}".format("Latest" if newest == None else newest))
            x = self._slacker.channels.history(channel_id, oldest=latest, latest=newest).body
            # print(x["messages"])

            messages = messages + x["messages"]

            if x["has_more"]:
                newest = x["messages"][-1]["ts"]
            else:
                break

        return messages

    def update_channel(self, channel_id):
        latest = self.get_newest_ts(channel_id)

        if latest is None:
            self._data[channel_id] = []

        temp_hist = self.get_channel_history(channel_id, latest)

        self._data[channel_id] = temp_hist + self._data[channel_id]

    def dump(self, output_file=None):
        output_file = self.cachefile if output_file is None else output_file
        with open(output_file, 'w') as ofile:
            json.dump(self._data, ofile, sort_keys=True, indent=4, separators=(',', ': '))

class ChannelCache(object):
    def __init__(self, slacker, cachefile=None):
        if cachefile != None and os.path.isfile(cachefile):
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

    def dump(self, output_file=None):
        output_file = self.cachefile if output_file is None else output_file
        with open(output_file, 'w') as ofile:
            json.dump(self._data, ofile, sort_keys=True, indent=4, separators=(',', ': '))


class UserCache(object):
    def __init__(self, slacker, cachefile=None):
        if cachefile != None and os.path.isfile(cachefile):
            with open(cachefile, 'r') as ifile:
                self._data = json.load(ifile)
        else:
            self._data = {}

        self._slacker = slacker
        self.cachefile = cachefile

    def update(self):
        x = self._slacker.rtm.start().body
        for user in x["users"]:
            self._data[user["id"]] = user["name"]

    def resolve_user(self, user_id):
        if not user_id in self._data:
            self._data[user_id] = self._slacker.users.info(user=user_id).body['user']['name']

        return self._data[user_id]

    def dump(self, output_file=None):
        output_file = self.cachefile if output_file is None else output_file
        with open(output_file, 'w') as ofile:
            json.dump(self._data, ofile, sort_keys=True, indent=4, separators=(',', ': '))


def connect(api_token=None):
    if api_token is None:
        import slackbot_settings as ss
        api_token = ss.API_TOKEN

    herm = slacker.Slacker(api_token)

    return herm

DEFAULT_HISTORY_CACHE = "history.json"
DEFAULT_CHANNEL_CACHE = "channels.json"
DEFAULT_USER_CACHE = "users.json"

def setup_args():
    parser = argparse.ArgumentParser(description="Obtain public slack history")
    parser.add_argument('-m', '--mdhtml', help="Output rendered HTML page via MarkDown")
    parser.add_argument('-a', '--apikey', help="Provide api key via command line rather than secrets file")
    parser.add_argument('--history', help="Specify history cache file, defaults to 'history.json'")
    parser.add_argument('--channels', help="Specify channel cache file, defaults to 'channels.json'")
    parser.add_argument('--users', help="Specify user cache file, defaults to 'users.json'")

    # TODO: store_true, add logic
    # parser.add_argument('--rocache', help"Only read from caches, do not write back (updates are still performed, but not to disk)")

    args = parser.parse_args()

    # Tweak cachefiles to have defaults if unspecified (None)
    args.history = args.history if args.history is not None else DEFAULT_HISTORY_CACHE
    args.channels = args.channels if args.channels is not None else DEFAULT_CHANNEL_CACHE
    args.users = args.users if args.users is not None else DEFAULT_USER_CACHE

    return args

def main():
    args = setup_args()
    slacker = connect(args.apikey)

    history = HistoryCache(slacker=slacker, cachefile=args.history)
    channels = ChannelCache(slacker=slacker, cachefile=args.channels)
    users = UserCache(slacker=slacker, cachefile=args.users)

    users.update()
    channels.update()

    for channel in channels.get_channels():
        i = channel["id"]

        print("getting {}...".format(channel["name"]))

        history.update_channel(i)

    # Render to markdown, if configured
    if args.mdhtml != None:
        with open(args.mdhtml, 'w') as ofile:
            ofile.write(render(history=history._data, users=users._data, channels=channels._data))


    history.dump()
    channels.dump()
    users.dump()

if __name__ == '__main__':
    main()