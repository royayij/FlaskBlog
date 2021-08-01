from flask import Flask
from config import Development
from mod_admin import admin

app = Flask(__name__)
app.config.from_object(Development)


@app.route('/')
def index():
    return 'Blog Home!'


app.register_blueprint(admin)

if __name__ == '__main__':
    app.run()
