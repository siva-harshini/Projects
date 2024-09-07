# from flask import Flask, render_template,request,flash,redirect,url_for,session
# import sqlite3
#
# app = Flask(__name__)
# app.secret_key = "123"
#
# con = sqlite3.connect("database.db")
# con.execute("create table if not exists customer(pid integer primary key, name text, address text, contact integer, "
#             "mail text)")
# con.close()
#
#
# # def login_required(func):
# #     def wrapper(*args, **kwargs):
# #         if 'name' not in session:
# #             flash("Please login first", "danger")
# #             return redirect(url_for('index'))
# #         return func(*args, **kwargs)
# #     return wrapper
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == 'POST':
#         name = request.form['name']
#         password = request.form['password']
#         con = sqlite3.connect("database.db")
#         con.row_factory = sqlite3.Row
#         cur = con.cursor()
#         cur.execute("select * from customer where name=? and mail=?", (name, password))
#         data = cur.fetchone()
#
#         if data:
#             session["name"] = data["name"]
#             session["mail"] = data["mail"]
#             return redirect("customer")
#         else:
#             flash("Username and Password Mismatch", "danger")
#     return redirect(url_for("index"))
#
#
# @app.route('/customer', methods=["GET", "POST"])
# # @login_required
# def customer():
#     return render_template("customer.html")
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method=='POST':
#         try:
#             name=request.form['name']
#             address=request.form['address']
#             contact=request.form['contact']
#             mail=request.form['mail']
#             con=sqlite3.connect("database.db")
#             cur=con.cursor()
#             cur.execute("insert into customer(name,address,contact,mail)values(?,?,?,?)",(name,address,contact,mail))
#             con.commit()
#             flash("Record Added  Successfully","success")
#         except:
#             flash("Error in Insert Operation","danger")
#         finally:
#             return redirect(url_for("index"))
#             con.close()
#
#     return render_template('register.html')
#
#
# @app.route('/logout')
# # @login_required
# def logout():
#     session.pop('name', None)
#     session.pop('mail', None)
#     flash("You have been logged out", "info")
#     return redirect(url_for("index"))
#
#
# @app.route('/admin')
# def admin():
#     return render_template('admin.html')
#
#
# @app.route('/user')
# def user():
#     return render_template('user.html')
#
#
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')
#
#
# @app.route('/about')
# # @login_required
# def about():
#     return render_template('about.html')
#
#
# @app.route('/addcart')
# # @login_required
# def addcart():
#     return render_template('addcart.html')
#
#
# @app.route('/categories')
# # @login_required
# def categories():
#     return render_template('categories.html')
#
#
# @app.route('/fav')
# # @login_required
# def fav():
#     return render_template('fav.html')
#
#
# @app.route('/order')
# # @login_required
# def order():
#     return render_template('order.html')
#
#
# @app.route('/services')
# # @login_required
# def services():
#     return render_template('services.html')
#
#
# @app.route('/vegetables')
# def veg():
#     return render_template('vegetables.html')
#
#
# @app.route('/fruits')
# def fruits():
#     return render_template('fruits.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify # type: ignore
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "123"


# Function to create a database file for each user
def create_user_database(mail):
    database_name = f"{mail}.db"
    con = sqlite3.connect(database_name)
    con.execute("create table if not exists customer(pid integer primary key, name text, address text, "
                "contact integer, mail text, role text)")
    con.close()


# Check if the user's database file exists, if not, create one


def check_user_database():
    if 'mail' in session:
        user_database = f"{session['mail']}.db"
        if not os.path.exists(user_database):
            create_user_database(session['mail'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        role = request.form['role']
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from customer where name=? and mail=? and role=?", (name, password, role))
        data = cur.fetchone()

        if data:
            session["cname"] = data["name"]
            session["mail"] = data["mail"]
            session["role"] = data["role"]
            check_user_database()  # Check if user's database exists, create one if not
            return redirect("customer")
        else:
            flash("Username and Password Mismatch", "danger")
    return redirect(url_for("index"))


@app.route('/customer', methods=["GET", "POST"])
def customer():
    check_user_database()  # Check if user's database exists, create one if not
    if 'mail' in session:
        con = sqlite3.connect(f"{session['mail']}.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM customer")
        customer_data = cur.fetchall()
        con.close()
        return render_template("customer.html", customer_data=customer_data)
    else:
        flash("Please login first", "danger")
        return redirect(url_for("index"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            address = request.form['address']
            contact = request.form['contact']
            mail = request.form['mail']
            role = request.form['role']
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("insert into customer(name,address,contact,mail,role)values(?,?,?,?,?)",
                        (name, address, contact, mail, role))
            con.commit()
            session["name"] = name
            session["mail"] = mail
            session["role"] = role
            check_user_database()  # Check if user's database exists, create one if not
            flash("Record Added Successfully", "success")
        except Exception as e:
            flash(f"Error in Insert Operation: {str(e)}", "danger")
        finally:
            con.close()
            return redirect(url_for("index"))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('mail', None)
    session.pop('role', None)
    flash("You have been logged out", "info")
    return redirect(url_for("index"))


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/about')
# @login_required
def about():
    return render_template('about.html')


@app.route('/addcart')
# @login_required
def addcart():
    return render_template('addcart.html')


@app.route('/categories')
# @login_required
def categories():
    return render_template('categories.html')


@app.route('/fav')
# @login_required
def fav():
    return render_template('fav.html')


@app.route('/order')
# @login_required
def order():
    if "cname" in session and session['role'] == 'admin':
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM combined_details")
            rows = cur.fetchall()
            con.close()
            return render_template('ordersPlaced.html', rows=rows)
    else:
        return render_template('order.html')


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("DELETE FROM combined_details WHERE id=?", (id,))
        con.commit()
        cur.execute("DELETE FROM orderdetails WHERE id=?", (id,))
        con.commit()
        cur.execute("DELETE FROM purchaseDetails WHERE id=?", (id,))
        con.commit()
        con.close()


@app.route('/services')
# @login_required
def services():
    return render_template('services.html')


@app.route('/vegetables')
def veg():
    if "cname" in session and session['role'] == 'admin':
        return render_template('admin_veg.html', username=session["cname"])
    else:
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM vegProducts")
        veg_data = cur.fetchall()
        con.close()
        return render_template("vegetables.html", veg_data=veg_data)


@app.route('/fruits')
def fruits():
    if "cname" in session and session['role'] == 'admin':
        return render_template('admin_fruits.html', username=session["cname"])
    else:
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM fruits")
        fruits_data = cur.fetchall()
        con.close()
        return render_template("fruits.html", fruits_data=fruits_data)


@app.route('/dairy_products')
def dairyProd():
    if "cname" in session and session['role'] == 'admin':
        return render_template('admin_dp.html', username=session["cname"])
    else:
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM dairyProducts")
        dairyProd_data = cur.fetchall()
        con.close()
        return render_template("dairyProducts.html", dairyProd_data=dairyProd_data)


@app.route('/cereals-pulses')
def cerpul():
    if "cname" in session and session['role'] == 'admin':
        return render_template('admin_cerpul.html', username=session["cname"])
    else:
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM cerpul")
        cerpul_data = cur.fetchall()
        con.close()
        return render_template("cerpul.html", cerpul_data=cerpul_data)


@app.route('/beverages')
def beverages():
    if "cname" in session and session['role'] == 'admin':
        return render_template('admin_beverages.html', username=session["cname"])
    else:
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM beverages")
        beverages_data = cur.fetchall()
        con.close()
        return render_template("beverages.html", beverages_data=beverages_data)


@app.route('/cosmetics')
def cosmetic():
    if "cname" in session and session['role'] == 'admin':
        return render_template('admin_cosmetics.html', username=session["cname"])
    else:
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM cosmetics")
        cosmetics_data = cur.fetchall()
        con.close()
        return render_template("cosmetics.html", cosmetics_data=cosmetics_data)


@app.route('/adminVeg', methods=['GET', 'POST'])
def adminVeg():
    if "cname" in session and session['role'] == 'admin':
        if request.method == 'POST':
            try:
                pname = request.form['name']
                desc = request.form['description']
                cost = request.form['cost']
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                cur.execute("insert into vegProducts(pname,description,cost)values(?,?,?)",
                            (pname, desc, cost))
                con.commit()
                session["name"] = pname
                session["description"] = desc
                session["cost"] = cost
                check_user_database()  # Check if user's database exists, create one if not
            except Exception as e:
                print("Error")
            finally:
                con.close()
        return render_template('admin_veg.html')
    else:
        return print("ERROR")


@app.route('/adminFruits', methods=['GET', 'POST'])
def adminFruits():
    if "cname" in session and session['role'] == 'admin':
        if request.method == 'POST':
            try:
                pname = request.form['name']
                desc = request.form['description']
                cost = request.form['cost']
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                cur.execute("insert into fruits(pname,description,cost)values(?,?,?)",
                            (pname, desc, cost))
                con.commit()
                session["name"] = pname
                session["description"] = desc
                session["cost"] = cost
                check_user_database()  # Check if user's database exists, create one if not
            except Exception as e:
                print("Error")
            finally:
                con.close()
        return render_template('admin_fruits.html')
    else:
        return print("ERROR")


@app.route('/adminDp', methods=['GET', 'POST'])
def adminDp():
    if "cname" in session and session['role'] == 'admin':
        if request.method == 'POST':
            try:
                pname = request.form['name']
                desc = request.form['description']
                cost = request.form['cost']
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                cur.execute("insert into dairyProducts(pname,description,cost)values(?,?,?)",
                            (pname, desc, cost))
                con.commit()
                session["name"] = pname
                session["description"] = desc
                session["cost"] = cost
                check_user_database()  # Check if user's database exists, create one if not
            except Exception as e:
                print("Error")
            finally:
                con.close()
        return render_template('admin_dp.html')
    else:
        return print("ERROR")


@app.route('/adminCerpul', methods=['GET', 'POST'])
def adminCerpul():
    if session['cname'] and session['role'] == 'admin':
        if request.method == 'POST':
            try:
                pname = request.form['name']
                desc = request.form['description']
                cost = request.form['cost']
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                cur.execute("insert into cerpul(pname,description,cost)values(?,?,?)",
                            (pname, desc, cost))
                con.commit()
                session["name"] = pname
                session["description"] = desc
                session["cost"] = cost
                check_user_database()  # Check if user's database exists, create one if not
            except Exception as e:
                print("Error")
            finally:
                con.close()
        return render_template('admin_cerpul.html')
    else:
        return print("ERROR")


@app.route('/adminBeverages', methods=['GET', 'POST'])
def adminBeverages():
    if "cname" in session and session['role'] == 'admin':
        if request.method == 'POST':
            try:
                pname = request.form['name']
                desc = request.form['description']
                cost = request.form['cost']
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                cur.execute("insert into beverages(pname,description,cost)values(?,?,?)",
                            (pname, desc, cost))
                con.commit()
                session["name"] = pname
                session["description"] = desc
                session["cost"] = cost
                check_user_database()  # Check if user's database exists, create one if not
            except Exception as e:
                print("Error")
            finally:
                con.close()
        return render_template('admin_beverages.html')
    else:
        return print("ERROR")


@app.route('/adminCosmetics', methods=['GET', 'POST'])
def adminCosmetics():
    if "cname" in session and session['role'] == 'admin':
        if request.method == 'POST':
            try:
                pname = request.form['name']
                desc = request.form['description']
                cost = request.form['cost']
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                cur.execute("insert into cosmetics(pname,description,cost)values(?,?,?)",
                            (pname, desc, cost))
                con.commit()
                session["name"] = pname
                session["description"] = desc
                session["cost"] = cost
                check_user_database()  # Check if user's database exists, create one if not
            except Exception as e:
                print("Error")
            finally:
                con.close()
        return render_template('admin_cosmetics.html')
    else:
        return print("ERROR")


@app.route('/orderForm', methods=['POST', 'GET'])
def orderForm():
    if request.method == 'POST':
        fname = request.form['fname']
        pno = request.form['pNo']
        email = request.form['email']
        quantity = request.form['quantity']
        saddress = request.form['saddress']
        con = sqlite3.connect("database.db")
        # con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("insert into orderdetails(fname,pNo,email,quantity,saddress)values(?,?,?,?,?)",
                    (fname, pno, email, quantity, saddress))
        con.commit()
        cur.execute("""
                            INSERT INTO combined_details (fname, saddress, email, pNo, productName, cost)
                            SELECT o.fname, o.saddress, o.email, o.pNo, p.productName, p.cost
                            FROM orderdetails o
                            JOIN purchaseDetails p ON o.id = p.id
                        """)
        con.commit()
        con.close()
        return render_template('orderPlaced.html')


@app.route('/buy_now', methods=['POST'])
def buy_now():
    if request.method == 'POST':
        data = request.json
        product_name = data.get('productName')
        cost = data.get('cost')

        # Insert product details into the existing PurchaseDetails table
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO purchaseDetails (productName, cost) 
                          VALUES (?, ?)''', (product_name, cost))
        conn.commit()
        conn.close()

        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': 'Invalid request method'}), 405


if __name__ == '__main__':
    app.run(debug=True)
