from flask import Flask,render_template,request,redirect,url_for,flash,session
from database import fetch_products,insert_products_method_2,fetch_sales,insert_sales_method_2,profit_per_product,sales_per_product,sales_per_day,profit_per_day,check_user,add_users
from flask_bcrypt import Bcrypt
from functools import wraps

#instantiate your application:-initializion of flask.
app=Flask(__name__)
app.secret_key="dhdjlaHSH@3"

#initializion of bcrypt.
bcrypt=Bcrypt(app)

@app.route('/')
def home():
     user={"name":"Akinyi","location":"Nairobi","area":"Luanda"}
     num=[1,2,3,4,5,6]
     return render_template("index.html",data=user,num=num) #declaring variable for variable e.g data=name

def login_required(f):                                  #defines a decorator function
    @wraps(f)                                           # takes function as a decorator ensure the above is decorator function
    def protected(*args,**kwargs):                      #checks whether a session exists or not 
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)                         #call funsction so that it can return to the required page 
    return protected             


@app.route('/products')
@login_required
def products():
    fruits=["apple","oranges","tangerines","cauliflower","grapes"]
    products=fetch_products()                                               # calling the function so that it can store the function from the database.
    return render_template("products.html",fruits=fruits,products=products) #products=products-declare a nother variable to hold the 1st variable

@app.route('/add_products',methods=["GET","POST"])
def add_products():
    product_name=request.form["p-name"]
    buying_price=request.form["b-price"]
    selling_price=request.form["s-price"]
    stock_quantity=request.form["stock"]
    new_product=(product_name, buying_price,selling_price, stock_quantity)
    insert_products_method_2(new_product)
    return redirect(url_for('products'))

@app.route('/sales')
@login_required
def sales():
  sales=fetch_sales()
  products=fetch_products()
  return render_template("sales.html",sales=sales,products=products)  

@app.route('/make_sale',methods=['POST'])
def make_sale():
    product_id=request.form['pid']
    quantity=request.form['quantity']
    new_sale=[product_id,quantity]
    insert_sales_method_2(new_sale)
    return redirect(url_for('sales'))


@app.route('/Dashboard')
@login_required
def Dashboard():
    profit_product=profit_per_product()
    sale_product=sales_per_product()
    sale_day=sales_per_day()
    profit_day=profit_per_day()

#LIST COMPREHENSION TO GET INDIVIDUAL DATA POINTS
    product_name=[i [0] for i in profit_product]
    p_product=[float(i[1])for i in profit_product]
    s_product=[float(i[1]) for i in sale_product]


    date=[str(i [0]) for i in sale_day]
    p_day=[float(i [1])for i in profit_day]
    s_day=[float(i [1])for i in sale_day]


    return render_template("dashboard.html",
                           product_name=product_name,p_product=p_product,s_product=s_product,
                           date=date,s_day=s_day,p_day=p_day)


@app.route('/Register',methods=['GET','POST'])
def register():
     if request.method=='POST':
         name=request.form['name']
         email=request.form['email']
         phone_number=request.form['phone']
         password=request.form['pass']
         hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
         user=check_user(email)
         if not user:
             new_user=(name,email,phone_number,hashed_password)
             add_users(new_user)
             return redirect(url_for('login'))
         else:
             print('already registered')
     return render_template("register.html")
         

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form=['email']
        password=request.form=['pass']

        user=check_user(email)
        if not user:
            flash("User not found,Please Register","info")
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(user[-1],password):
                flash("logged in","success")
                session['email']=email
                return redirect(url_for('Dashboard'))
            else:
                flash("incorrect password","danger")
    return render_template('login.html')

@app.route('/Contact Us')
def contact_Us():
    return render_template('contact_us.html')



app.run(debug=True)