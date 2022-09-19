# Copyright 2022 Johannes Thorén. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from crypt import methods
from sqlite3 import dbapi2
from flask import Flask, render_template, request, flash, send_file
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
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


    db.add_file(uid, file.filename, email, file_password, date)
    return render_template("file-details.html", password=file_password, filename=file.filename, url=url)


@app.get('/f/<uid>')
def download(uid):
    fd = db.get_file_information(uid)
    file_path = os.environ.get("FILE_STORAGE_LOCATION")

    return send_file(f"{file_path}/{uid}", download_name=fd[1], )


if __name__ == "__main__":
    app.run(port=os.environ.get("PORT"),
            host=os.environ["HOSTNAME"], debug=True)
