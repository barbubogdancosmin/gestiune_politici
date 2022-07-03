import jwt
from flask import Blueprint, request
import peewee as pw

myDB = pw.MySQLDatabase("heroku_1526160c5506bb4", host="eu-cdbr-west-02.cleardb.net", port=3306, user="b553007ab680ac",
                        passwd="7e350aca")


class MySQLModel(pw.Model):
    class Meta:
        database = myDB


class Admin(MySQLModel):
    admin_user = pw.CharField(primary_key=True)
    admin_pass = pw.CharField()


myDB.create_tables([Admin])

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                       "message": "Please provide user details",
                       "data": None,
                       "error": "Bad request"
                   }, 400
        existing_user = Admin.get(Admin.admin_user == data["admin_user"])
        is_validated = existing_user.admin_pass == data["admin_pass"]
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        if existing_user:
            try:
                # token should expire after 24 hrs
                token = jwt.encode(
                    {"admin_user": data["admin_user"]},
                    "SecretString",
                    algorithm="HS256"
                )
                return token
            except Exception as e:
                return {
                           "error": "Something went wrong",
                           "message": str(e)
                       }, 500
        return {
                   "message": "Error fetching auth token!, invalid email or password",
                   "data": None,
                   "error": "Unauthorized"
               }, 404
    except Exception as e:
        return {
                   "message": "Something went wrong!",
                   "error": str(e),
                   "data": None
               }, 500
