# Copyright 2022 Johannes Thorén. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from crypt import methods
from sqlite3 import dbapi2
from flask import Flask, render_template, request, flash, send_file
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from hashlib import md5
import os
import uuid
import db
import datetime

load_dotenv()

app = Flask(__name__)

db.create_table()


@app.get("/")
def index():
    return render_template("index.html", upload="https://"+os.environ.get("HOSTNAME")+"/upload")


@app.post("/upload")
def upload():

    # TODO: well we can save file, but it should not be saved as a something dot something file.
    # it should have a UID as file name. then the file path should sent to the db together with
    # the password and email address.

    uid = str(uuid.uuid4())[:8]

    file = request.files['file']

    open(os.path.join(os.environ.get("FILE_STORAGE_LOCATION"), uid), "w+").close()
    file.save(os.path.join(os.environ.get("FILE_STORAGE_LOCATION"), uid))

    file_password = request.form.get("Password")
    email = request.form.get("Email")
    url = f"http://{os.environ.get('HOSTNAME')}:{os.environ.get('PORT')}/f/{uid}"
    date = datetime.datetime.now()

    if(file_password != ""):
        db.add_file(uid, file.filename, email, md5(file_password.encode("UTF-8")).hexdigest(), date=date)
    else:
        db.add_file(uid, file.filename, email, "", date=date)

    return render_template("file-details.html", password=file_password, filename=file.filename, url=url)


@app.route('/f/<uid>', methods=["GET", "POST"])
def download(uid):
    fd = db.get_file_information(uid)
    passwd = request.form.get("Password")

    if request.method == "POST":
        if md5(passwd.encode("UTF-8")).hexdigest() == fd[2]:
            file_path = os.environ.get("FILE_STORAGE_LOCATION")
            return send_file(f"{file_path}/{uid}", download_name=fd[1], )


    if request.method == "GET":          
        if fd[2] and not passwd:
            url = f"http://{os.environ.get('HOSTNAME')}:{os.environ.get('PORT')}/f/{fd[0]}"
            return render_template("enter-password.html", url=url)
        else:
            file_path = os.environ.get("FILE_STORAGE_LOCATION")
            return send_file(f"{file_path}/{uid}", download_name=fd[1],)


if __name__ == "__main__":
    app.run(port=os.environ.get("PORT"),
            host=os.environ["HOSTNAME"], debug=True)
