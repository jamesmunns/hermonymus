import json
import markdown
from datetime import datetime

CHANNEL_TEMPLATE = "## {}\n\n"
HEADER_TEMPLATE = "Time | User | Message\n---|---|---\n"
MESSAGE_TEMPLATE = "*{time}* | **{user}** | {message}\n"

def render(history, users, channels,
           title="Berlin Hack History"):

    output = ""

    output += "# {}\n\n".format(title)

    for channel in channels:
        cid = channel["id"]
        cname = channel["name"]

        output += (CHANNEL_TEMPLATE.format(cname))
        output += ("\n")
        output += (HEADER_TEMPLATE)

        # TODO: actually sort
        for msg in history[channel["id"]][::-1]:
            clean_msg = msg["text"].replace("\n", " ").replace("|", "/")

            assert "\n" not in clean_msg, "WHAT"
            # print(clean_msg)

            output += (MESSAGE_TEMPLATE.format(
                time=str(datetime.fromtimestamp(int(float(msg["ts"])))).replace(" ", "&nbsp;").replace("-","_"),
                user=users[msg["user"]],
                message=clean_msg))

        output += ("\n")

        return markdown.markdown(output, extensions=['markdown.extensions.tables'])

def main():
    with open("history.json", 'r') as hfile:
        HISTORY = json.load(hfile)

    with open("users.json", 'r') as ufile:
        USERS = json.load(ufile)

    with open("channels.json", 'r') as cfile:
        CHANNELS = json.load(cfile)

    # print(output)
    print(render(HISTORY, USERS, CHANNELS))

if __name__ == '__main__':
    main()