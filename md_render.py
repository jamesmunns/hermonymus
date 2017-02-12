import json
import markdown
from datetime import datetime

SITE_TITLE = "# Berlin Hacks History\n\n"
CHANNEL_TEMPLATE = "## {}\n\n"
HEADER_TEMPLATE = "Time | User | Message\n---|---|---\n"
MESSAGE_TEMPLATE = "*{time}* | **{user}** | {message}\n"

def main():
    with open("history.json", 'r') as hfile:
        HISTORY = json.load(hfile)

    with open("users.json", 'r') as ufile:
        USERS = json.load(ufile)

    with open("channels.json", 'r') as cfile:
        CHANNELS = json.load(cfile)

    output = "\n"

    output += (SITE_TITLE)

    for channel in CHANNELS:
        cid = channel["id"]
        cname = channel["name"]

        output += (CHANNEL_TEMPLATE.format(cname))
        output += ("\n")
        output += (HEADER_TEMPLATE)

        # TODO: actually sort
        for msg in HISTORY[channel["id"]][::-1]:
            clean_msg = msg["text"].replace("\n", " ").replace("|", "/")

            assert "\n" not in clean_msg, "WHAT"
            # print(clean_msg)

            output += (MESSAGE_TEMPLATE.format(
                time=str(datetime.fromtimestamp(int(float(msg["ts"])))).replace(" ", "&nbsp;").replace("-","_"),
                user=USERS[msg["user"]],
                message=clean_msg))

        output += ("\n")

    # print(output)
    print(markdown.markdown(output, extensions=['markdown.extensions.tables']))

if __name__ == '__main__':
    main()