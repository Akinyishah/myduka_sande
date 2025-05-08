import psycopg2
from datetime import datetime
conn=psycopg2.connect(user='postgres',
                      password='Newsa2019@',
                      host='localhost',
                      port='5432',
                      database='myduka_sande' 
                      )

cur = conn.cursor()                      
time=datetime.now()

def fetch_products():
  cur.execute('select * from products;')
  products=cur.fetchall()
  return products

def fetch_sales():
 cur.execute('select * from sales;')
 sales=cur.fetchall()
 return sales

# fetch_sales() 
# fetch_products()  
#FETCHING DATA
def fetch_data(table):
  cur.execute(f"select * from {table} ;")
  data=cur.fetchall()
  return data

products=fetch_data('products')
sales=fetch_data('sales')

#print("products from fetch data func:\n", products)
# print("sales from fetch data func:\n", sales)
# print("users from fetch data func:\n", users)

# INSERTING PRODUCTS 
def insert_products():
     cur.execute("insert into products(name,buying_price,selling_price,stock_quantity)values('Apple cider Vinegar',1210.50,1579.00,80)")
     conn.commit
     return "product inserted"

def insert_sales():
     cur.execute(f"insert into sales(pid,quantity,created_at)values(1,110,'{time}')")# when passing variable as a string use formated string f''
     conn.commit
     return "sales made"


def insert_products_method_2(values):
  insert = f"insert into products(name,buying_price,selling_price,stock_quantity)values{values}"
  cur.execute(insert)
  conn.commit()

product1=("laptop",24500,32600,70) #should be outside the def function.After conn.commit remove indentation
# insert_products_method_2(product1)
# products=fetch_data('products')
# print("fetching prods using method2:\n",products)
#INSERT SALES METHOD 2
def insert_sales_method_2(values):
  insert ="insert into sales(pid,quantity,created_at)values(%s,%s,'now()')"
  cur.execute(insert,values)
  conn.commit()

#INSERT PRODUCTS METHOD 2
def insert_products_method_2(values):
  insert = f"insert into products(name,buying_price,selling_price,stock_quantity)values{values}"
  cur.execute(insert)
  conn.commit()
#product1=("laptop",24500,32600,70) #should be outside the def function.After conn.commit remove indentation
# insert_products_method_2(product1)
# products=fetch_data('products')
# print("fetching prods using method2:\n",products)

#PROFIT PER PRODUCT:
def profit_per_product():
   cur.execute("""SELECT products.name,SUM((products.selling_price-products.buying_price)*sales.quantity) AS Totalprofit FROM products inner join sales
               ON products.id=sales.pid group by products.name;""")
   profit_per_product=cur.fetchall()
   return profit_per_product

#SALES PER PRODUCT:
def sales_per_product():
   cur.execute("""SELECT products.name,SUM(products.selling_price*sales.quantity) AS Total_Sales FROM 
               products INNER JOIN sales ON products.id = sales.pid GROUP BY (products.name);""")
   sales_per_product=cur.fetchall()
   return sales_per_product

#SALES PER DAY:
def sales_per_day():
   cur.execute("""SELECT date(sales.created_at) AS date, SUM(products.selling_price*sales.quantity)AS revenue FROM 
               sales INNER JOIN products ON products.id = sales.pid GROUP BY date  ORDER BY date ASC;""")
   sales_per_day=cur.fetchall()
   return sales_per_day

#PROFIT PER DAY:
def profit_per_day():
   cur.execute("""SELECT date(sales.created_at) AS date, SUM((products.selling_price-products.buying_price)*sales.quantity) AS Totalprofit FROM 
               products INNER JOIN sales ON products.id=sales.pid GROUP BY  date ORDER BY date ASC ;""") 
   profit_per_day=cur.fetchall()
   return profit_per_day


def check_user(email):
   query="select * from users WHERE email = %s"
   cur.execute(query,(email,) )
   user=cur.fetchone()
   return user


def add_users (user_details):
   query="insert into users(name,email,phone_number,password)values(%s,%s,%s,%s)"
   cur.execute(query,user_details)
   conn.commit()
   cur.close()