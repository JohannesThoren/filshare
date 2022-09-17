# Copyright 2022 Johannes Thorén. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from flask import Flask, render_template, request, flash
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html", upload="https://"+os.environ.get("HOSTNAME")+"/upload")


@app.post("/upload")
def upload():
    # TODO: well we can save file, but it should not be saved as a something dot something file.
    # it should have a UID as file name. then the file path should sent to the db together with
    # the password and email address.

    file = request.files['file']
    open(os.environ.get("FILE_STORAGE_LOCATION")+file.filename,"w+").close()
    file.save(os.environ.get("FILE_STORAGE_LOCATION")+"/"+file.filename)

    return render_template("file-details.html", password=request.form.get("Password"), filename=file.filename, )



if __name__ == "__main__":
    app.run(port=os.environ.get("PORT"), host=os.environ["HOSTNAME"], debug=True)