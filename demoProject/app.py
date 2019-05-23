from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

# 导入wtf扩展的表单类
from flask_wtf import FlaskForm
# 导入自定义表单需要的字段
from wtforms import SubmitField, StringField, PasswordField
# 导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired, EqualTo

# 创建flask应用程序实列
# 需要传入__name__，作用是为了确定资源所在的路径
app = Flask(__name__)
print('=====')
# 使用数据库                             协议    用户名 密码  地址     端口    数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/flask_sql_demo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask_sql_demo?charset=utf8'
# 跟踪数据库的修改，如未设置只会提醒警告，不建议开启
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

"""
两张表
角色（管理员 /  普通用户）
用户（角色ID）
"""
# 数据库的模型， 需要去继承db.Model
class Role(db.Model):
    # 定义表
    __tablename__ = 'roles'
    # 定义字段   db.Column表示是一个字段
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(16), unique=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    # db.ForeignKey('roles.id') 表示是外键， 表名.id
    role_id = db.Column(db.INTEGER, db.ForeignKey('roles.id'))




# flash需要设置一个secret_key，会将这个secret_key混到消息里面去，保证密码不会被泄露
app.secret_key = 'hello'
# 定义路由及视图函数
# flask中定义路由是通过装饰器实现的
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def hello():
    # 返回模板内容，类似Django中的render
    return render_template('index.html')

# 使用同一个视图函数 来显示不同用户的订单信息
# <>定义路由的参数，<>内需要起个名字
# <>内没有格式限定
@app.route('/orders/<order_id>')
def get_orders_id(order_id):
    # 需要在视图函数的（）内填入参数名，那么后面的代码才能去使用
    return 'order_id: {}'.format(order_id)

# 做了格式限定,有int float
@app.route('/order/<int:order_id>')
def get_order_id(order_id):
    # 需要在视图函数的（）内填入参数名，那么后面的代码才能去使用
    return 'order_id 的值为: {}'.format(order_id)


# 如何返回一个网页（模板）
# 如何给模板填充数据
@app.route('/index1/')
def index1():
    url_str = 'www.baidu.com'
    my_list = list(range(1, 10, 2))
    my_dict = {
        'name': '唐三',
        'sex': '男',
        'age': 20
    }
    return render_template('index1.html', url_str=url_str, my_list=my_list, my_dict=my_dict)

# 实现一个简单的登录的逻辑处理
# 路由需要有get和post两种请求方式
# 获取请求的参数
# 判读参数是否填写 & 密码是否相同
# 如果判断都没有问题，就返回一个success

"""
给模板传递消息 用flash
flash --> 需要对内容加密， 因此需要设置secret_key
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    # request: 请求对象 --> 获取请求方式、数据
    # 判断请求方式
    if request.method == "POST":
        # 获取请求方式
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(username, password, password2)
        # 判断参数是否填写 & 密码是否相同
        if not all([username, password, password2]):
            print('参数不完整')
            flash('参数不完整')  # 会在login页面打印这句话
        elif password != password2:
            print('密码不一致')
            flash('密码不一致')
        else:
            return 'success'

    return render_template('login.html')

"""
使用WTF实现表单
自定义表单类
"""
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', '密码填入不一致')])
    submit = SubmitField('提交')

@app.route('/form', methods=['GET', 'POST'])
def login2():
    login_form = LoginForm()
    if request.method == "POST":
        # 获取请求的参数
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 验证参数， WTF可以一句话就实现所有的校验
        # 需要加csrf_token
        if login_form.validate_on_submit():
            print(username, password)
            return 'success'
        else:
            flash('参数有误')
    return render_template('login2.html', form=login_form)




if __name__ == '__main__':
    # 先删除，后创建，这样就不会产生冲突
    db.drop_all()
    # 创建表， 实际开发中不使用这个，使用数据库迁移
    db.create_all()

    # 执行了app.run()， 就会将flask程序运行在一个简易的服务器（flask提供的，用于测试的）
    app.run(debug=True)
