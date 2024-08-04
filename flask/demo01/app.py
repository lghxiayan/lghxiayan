from datetime import datetime
from flask import Flask, request, render_template
import pymysql
from flask_migrate import Migrate
from sqlalchemy import text

import config
from exts import db
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

migrate = Migrate(app, db)


def get_validator_test_data():
    with app.app_context():
        with db.engine.connect() as conn:
            rs = conn.execute(text("SELECT * from validator_test"))
            print(rs.fetchone())


def datatime_format(value):
    return value.strftime('%Y-%m-%d %H:%M:%S')


app.add_template_filter(datatime_format, 'dformat')


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users', backref=db.backref('articles', lazy=True))


with app.app_context():
    db.create_all()


@app.route('/article/add')
def article_add():
    article = Article(title='Hello World', content='This is my first article')
    article.author = Users.query.filter_by(username='xiayan').first()
    db.session.add(article)
    db.session.commit()
    print(article.id)
    return '文章已经添加'


# users = Users(username='xiayan', password='123456')
@app.route('/user/add')
def user_add():
    users = Users(username='xiayan', password='123456')
    db.session.add(users)
    db.session.commit()
    return 'User added'


@app.route('/user/query')
def user_query():
    user = Users.query.filter_by(username='xiayan').first()
    return f'User: {user.username}, Password: {user.password}'


@app.route('/user/update')
def user_update():
    user = Users.query.filter_by(username='xiayan').first()
    user.password = '654321'
    db.session.commit()
    return f'User: {user.username}, Password: {user.password}'


@app.route('/user/delete')
def user_delete():
    user = Users.query.filter_by(username='xiayan').first()
    db.session.delete(user)
    db.session.commit()
    return f'User: {user.username}, Password: {user.password}'


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


@app.route('/filter')
def filter():
    user = User(username='xiayan', email='xiayan@163.com')
    date = datetime.now()
    return render_template('filter.html', user=user, date=date)


@app.route('/')
def hello_world():
    user = User(username='xiayan', email='xiayan@163.com')

    data = get_validator_test_data()
    print(data)

    return render_template('index.html', user=user, data=data)


# def index():
#     connection = get_db_connection()
#     if connection is not None and connection.is_connected():
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM validator_test")
#         result = cursor.fetchall()
#         cursor.close()
#         connection.close()
#         return render_template('index.html', result=result)
#         # return '<br>'.join(str(record) for record in result)
#     else:
#         return 'Connection failed'


@app.route('/control')
def control_statement():
    age = 17
    return render_template('control.html', age=age)


@app.route('/index.html')
def index_html():
    return render_template('index.html')


@app.route('/input_lgh_info')
def input_lgh_info():
    return render_template('input_lgh_info.html')


@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    return f'This is profile page {profile_id}'


@app.route('/book/list')
def book_list():
    page = request.args.get('page', 1, type=int)
    # return f'This is book list page:{page}'
    return render_template('book_list.html', page=page)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
