from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import sqlite3
import os
app = Flask(__name__)


app.config.from_object("config")
app.config.get("SECRET_KEY")
app.config.get("FLASK_ENV")

bcrypt = Bcrypt(app)



'''Kiểm tra và tạo đường dẫn vào CSDL chính'''
curent_pth = os.path.abspath(os.path.dirname(__file__))
dbb_path = os.path.join(curent_pth,"user.db")


connection = sqlite3.connect(dbb_path,check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Mô hình người dùng
class User(UserMixin):
    def __init__(self,id,username):
        self.id = id
        self.username = username
api = Api(app=app)


#Lớp tạo phiên người dùng gồm ID và Username
class User(UserMixin):
    def __init__(self,id,username):
        self.id = id
        self.username = username
        
tasks = []

loginapp = LoginManager(app=app)
loginapp.init_app(app=app)


coffee = [
    {"id": 1, "name": "The Coffee House Sữa Đá", "price": 39000, "image": "img/cf1.webp"},
    {"id": 2, "name": "Espresso", "price": 45000, "image": "img/cf2.webp"},
    {"id": 3, "name": "Cà Phê Đen", "price": 35000, "image": "img/cf3.webp"},
    {"id": 4, "name": "Latte", "price": 50000, "image": "img/cf4.webp"},
]

cake = [
    {"id": 1, "name": "Bánh mochi vị cherry", "price": 39000, "image": "img/banh1.webp"},
    {"id": 2, "name": "Bánh mochi hương nho", "price": 45000, "image": "img/banh2.webp"},
    {"id": 3, "name": "Bánh mochi đậu xanh", "price": 35000, "image": "img/banh3.webp"},
    {"id": 4, "name": "Bánh mochi vị dâu", "price": 50000, "image": "img/banh4.webp"},
]

machiato = [
    {"id": 1, "name": "Hồng Trà Sữa Trân Châu", "price": 39000, "image": "img/ts1.webp"},
    {"id": 2, "name": "Trà Mắc Ca Trân Châu", "price": 35000, "image": "img/ts2.webp"},
    {"id": 3, "name": "Trà Mắc Ca Trân Châu", "price": 35000, "image": "img/ts3.webp"},
    {"id": 4, "name": "Trà Hạt Sen - Nóng", "price": 30000, "image": "img/ts4.webp"},

]
tea = [
    {"id": 1, "name": "Trà Long Nhãn Hạt Sen", "price": 39000, "image": "img/tra1.webp"},
    {"id": 2, "name": "Trà Hạt Sen", "price": 45000, "image": "img/tra2.webp"},
    {"id": 3, "name": "Trà Đào Cam Sả", "price": 35000, "image": "img/tra3.webp"},
    {"id": 4, "name": "Trà Hạt Sen - Nóng", "price": 30000, "image": "img/tra4.webp"},
    
]


#kiểm tra người dùng trong CSDL theo id
@loginapp.user_loader
def loading_user(user_id):
    try:
        query_user = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query_user,(user_id))
        account = cursor.fetchone()
        if account:
            return User(id=account['id'],username=account['username'])
        
        else:
            return None
    #bắt ngoại lệ nếu có lỗi CSDL
    except sqlite3.Error:
        return None
    
    
class Testapi(Resource):
    def get(self):
        return {'message':'online'}
    
#API kiểm tra phân quyền người dùng đăng nhập vào
class CompareRecord(Resource):
    def get(self):
        id = session.get('id')
        username = session.get('user')
        return {
            "id":f"{id}",
            "username":f"{username}",
        }


api.add_resource(Testapi,"/api")
api.add_resource(CompareRecord,"/api/user")
@app.route('/')
def index():
    return render_template('index.html')

@login_required
@app.route('/banhngot')
def banhngot():
    return render_template('banhngot.html',products=cake)

@login_required
@app.route('/cafe')
def cafe():
    return render_template('cafe.html',products=coffee)

@login_required
@app.route('/tra')
def tra():
    return render_template('tra.html',products=machiato,foodtea = tea)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('new password')
        rp_password = request.form.get('repeat password')
        check_user = '''SELECT * FROM users WHERE username = ? AND password = ?'''
        cursor.execute(check_user,[username,password])
        old_account = cursor.fetchone()
        if old_account:
            msg = "Account already exists"
            return render_template('register.html',msg=msg)
        if password != rp_password:
            msg = "Your password do not match"
            return render_template('register.html',msg=msg)
        else:
            '''hoàn thành đăng kí và quay lại trang đăng nhập chính'''
            new_account = "INSERT INTO users (username,password) VALUES (?,?)"
            cursor.execute(new_account,[username,password])
            connection.commit()
            flash('Đăng ký thành công!', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@login_required
@app.route('/home')
def home():

    return render_template("home.html",
                           coffee_product = coffee,
                           cake_product = cake, 
                           tea_product = machiato)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'GET':
        username = request.form.get('username')
        password = request.form.get('password')
        

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hash_password = generate_password_hash(password)
        verify_password = check_password_hash(hash_password,password)
        # print(f"{username} - {hash_password}")
        query_login = '''SELECT * FROM users WHERE username = ? AND password = ?'''
        cursor.execute(query_login, [username,password])
        account = cursor.fetchone()

        '''Nếu như chuỗi mk mã hóa khớp với mk hiện tại và khớp với thông tin 
        trong account gồm username và password thì sẽ đăng nhập vào hệ thống'''
        if verify_password and account:
            login_user(User(id=account["id"],username=account["username"]),remember=True)
            #tao phien nguoi dung
            session[f'{username} has logged in'] = True
            session['id'] = account['id']
            session['user'] = account['username']
            return redirect(url_for('home'))
        
        '''Xóa phiên người dùng nếu nếu tài khoản đc đăng nhập ở một thiết bị khác'''
        if session.get(f"{username} has logged in"):
            del session[f"{username}"]
        
        else:
            msg = "error"
            flash('Sai mật khẩu!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html',msg=msg)



# Thêm cà phê vào giỏ 
@login_required
@app.route("/addcoffee",methods = ["POST"])
def addcoffee():
    id = int(request.form.get("id"))
    quantity = int(request.form.get("quantity"))

    cart = session.get("cart", [])
    
    
    '''nếu tất cả các vật phẩm ở trong giỏ hàng thì giỏ sẽ hiện thị các vật phẩm
    tương ứng với loại món: ví dụ cart sẽ hiển thị các sản phẩm gồm có trà, cà phê và bánh
    vào 1 giỏ '''
    for item in cart:
        if item["id"] == id:
            return redirect(url_for('cart'))
    
    '''Thêm vật phẩm vào trong giỏ hàng'''
    for itm in coffee:
        '''nếu như phẩn từ itm[id] trong coffee có 
        thông tin khưps với id từ request form của giao diện 
        thì giỏ hàng sẽ thêm sản phẩm vào'''
        if itm["id"] == id:
            cart.append(
                {
                    "id": id,
                    "name": itm["name"],
                    "price": itm["price"],
                    "image": itm["image"],
                    "quantity": quantity
                }
            )
            break

    session["cart"] = cart
    return redirect(url_for('cart'))

'''các giải thích còn lại tương tự '''
#thêm bánh ngọt và giỏ
@login_required
@app.route("/addcake",methods = ["POST"])
def addcake():
    id = int(request.form.get("id"))
    quantity = int(request.form.get("quantity"))

    cart = session.get("cart", [])
    
    for item in cart:
        if item["id"] == id:
            return redirect(url_for('cart'))
        
    for itm in cake:
        if itm["id"] == id:
            cart.append(
                {
                    "id": id,
                    "name": itm["name"],
                    "price": itm["price"],
                    "image": itm["image"],
                    "quantity": quantity
                }
            )
            break

    session["cart"] = cart
    return redirect(url_for('cart'))   

#thêm trà vào giỏ
@login_required
@app.route("/addmachiato",methods = ["POST"])
def addmachiato():
    id = int(request.form.get("id"))
    quantity = int(request.form.get("quantity"))

    cart = session.get("cart", [])
    

    for item in cart:
        if item["id"] == id:

            return redirect(url_for('cart'))
    for itm in machiato:
        if itm["id"] == id:
            cart.append(
                {
                    "id": id,
                    "name": itm["name"],
                    "price": itm["price"],
                    "image": itm["image"],
                    "quantity": quantity
                }
            )
            break

    session["cart"] = cart
    return redirect(url_for('cart'))   

#thêm machiato vào giỏ
@login_required
@app.route("/addtea",methods = ["POST"])
def addtea():
    id = int(request.form.get("id"))
    quantity = int(request.form.get("quantity"))

    cart = session.get("cart", [])
    

    for item in cart:
        if item["id"] == id:

            return redirect(url_for('cart'))
    for itm in tea:
        if itm["id"] == id:
            cart.append(
                {
                    "id": id,
                    "name": itm["name"],
                    "price": itm["price"],
                    "image": itm["image"],
                    "quantity": quantity
                }
            )
            break

    session["cart"] = cart
    return redirect(url_for('cart'))   


@login_required
@app.route("/cart")
def cart():
    stock = 0
    total = 0
    cart = session.get("cart", [])
    #Kiểm tra số lượng
    for number in cart:
        stock = stock + number["quantity"]
        # print(stock)
    #Kiểm tra tổng tiền    
    for obj in cart:
        total = total + (obj["price"]*obj["quantity"])
        # print(total)


    return render_template("cart.html",
                           cart=cart,
                           total=total,
                           number=stock)


'''Xóa theo id chỉ định của sản phẩm trong giỏ hàng'''
@login_required
@app.route("/remove_item/<int:id>")
def remove_item(id):
    cart = session.get("cart", [])
    for item in cart:
        '''Nếu xảy ra trường hợp ko tìm thấy ID sản phẩm thì hiển thị lại trang giỏ hàng với 
        các vật phẩm ở trong giỏ hàng hiện tại'''
        if item["id"] != id:
            session['cart'] = cart
        else:
            cart.remove(item)
            '''Sau khi xóa vật phẩm sẽ trả về giỏ hàng hiện tại cùng với số lượng, tổng tiền và 
            các loại vật phẩm'''
            session['cart'] = cart
    return redirect(url_for('cart'))


@login_required
@app.route("/clearcart",methods = ["POST"])
def clear_cart():
    cart = session.get('cart', [])
    cart.clear()
    session["cart"] = cart
    return redirect(url_for('cart'))

@login_required
@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run()


''' Chú thích'''

#login_required: bắt buộc một số trang hoặc URL muốn được truy cập phải đăng nhập
#redirect: chuyển hướng trang đó trong phiên hoạt động của người dùng
#session: phiên hđ của người dùng trong quá trình hoạt động
