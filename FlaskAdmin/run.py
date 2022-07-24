from flask import Flask
from exts import db
from apps.users import user_app
from pkg.response.response import Response
# from apps.models import *

app = Flask(__name__)

app.config.from_pyfile('setting.py')

db.app = app
db.init_app(app)

db.create_all()

app.register_blueprint(user_app, url_prefix="/user")  # 基础模块


@app.route("/")
def hello():
    data = [{'a': 'b'}, {'b': 'c'}, {'c': 'd'}]
    return Response('400', code=200, data=data)


if __name__ == '__main__':
    app.run(debug=True)
