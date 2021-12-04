from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


db = pymysql.connect(host='localhost', user='root', password='password', database='demodb1')


@app.route("/", methods=['GET'])
def index():
   return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
   data = request.form
   email = data["email"]
   password = data["password"]

   cursor = db.cursor()

   authenticated_user = authenticate_user(email, password, cursor)

   if authenticated_user:
       return render_template("index.html", login="success", name=authenticated_user)

   return render_template("index.html", login="failed")


def authenticate_user(email, password, cursor):
   sql = "select password, name from users where email='{}'".format(email)
   cursor.execute(sql)
   result = cursor.fetchone()

   if not result:
       return False

   if result[0] == password:
       return result[1]

   return False


if __name__ == "__main__":
   app.run(debug=True)
