# from DB_Admin import AdminDBHndler
# from DB_TransactionDetail import TransactionDetail
import imp
from flask import Flask, render_template, request, make_response, session, redirect, url_for
from Login import Login
from flask import request
from flask_restful import Api, Resource
from resources import initialize_routes

app = Flask(__name__)
app.config.from_object("config")

api = Api(app)
initialize_routes(api)

@app.route('/', methods=["POST", "GET"])
def landingPage():  # put application's code here

    if request.method == "GET":
        if session.get('adminUserName'):
            return redirect(url_for('admin'))
        elif session.get('pharmUserName'):
            return redirect(url_for('pharmacist'))
        else:
            # return render_template("login.html", error=None)
            return redirect(url_for('login_page'))


    # return render_template("login.html", error=None)
    # return redirect(url_for('landingPage'))

@app.route('/login', methods=["POST", "GET"])
def login_page():

    if request.method == "POST":
        userName = request.form["userId"]
        password = request.form["password"]
        loginObj = Login()
        accType = loginObj.getAccType(userName)

        if not accType:
            # return render_template('login.html', error=True)
            return redirect(url_for('login_page'))
        elif accType == 'pharmacist':
            if not loginObj.validatePharmacistPassword(userName, password):
                # return render_template('login.html', error=True)
                return redirect(url_for('login_page', error=True))
            else:
                # res = make_response(render_template("pharmDashboard.html"))
                # res.set_cookie("userPharmName", userName)
                # res.set_cookie("password", password)
                # return res
                session["pharmUserName"] = userName
                session["password"] = password
                return redirect(url_for('landingPage'))
                # return redirect(url_for('pharmacist'))
        else:
            if not loginObj.validateAdminPassword(userName, password):
                # return render_template('login.html', error=True)
                return redirect(url_for('login_page', error=True))
            else:
                # return admin dashbaord
                # res = make_response(render_template("adminDashboard.html"))
                # res.set_cookie("userAdminName", userName)
                # res.set_cookie("password", password)
                # return res
                session["adminUserName"] = userName
                session["password"] = password
                return redirect(url_for('landingPage'))
                # return redirect(url_for('admin'))
    else:
        return render_template("login.html", error=None)


@app.route('/pharmacist')
def pharmacist():
    return render_template('pharmDashboard.html')
    
@app.route('/admin')
def admin():  
    return render_template('adminDashboard.html')


@app.route('/logout', methods=["POST"])
def logout_page():
    res = make_response(render_template("login.html", error=None))
    # if "userAdminName" in request.cookies:
    #     res.set_cookie('userAdminName', expires=0)
    #     res.set_cookie('password', expires=0)
    # else:
    #     res.set_cookie('userPharmName', expires=0)
    #     res.set_cookie('password', expires=0)
    # return res
    session.clear()
    # return render_template("login.html", error=None)
    return redirect(url_for('landingPage'))

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
    return response

if __name__ == '__main__':
    app.run(debug=True)
