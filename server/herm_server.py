from flask import Flask
from flask_httpauth import HTTPBasicAuth

from users import USERS

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    if username in USERS:
        return USERS.get(username)
    return None

@app.route('/slackhistory')
@auth.login_required
def index():
    return app.send_static_file("site.html")

if __name__ == '__main__':
    app.run()
