from flask import Flask
from views import views
import os
import secrets


app=Flask(__name__)

app.register_blueprint(views,url_prefix="/")
app.secret_key = os.environ.get(secrets.token_hex(32), secrets.token_hex(40))  # Use a secure value in production

if __name__=='__main__':
    app.run()
