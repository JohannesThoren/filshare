from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html", upload="https://"+os.environ.get("HOSTNAME")+"/upload")


@app.post("/upload")
def upload():
    # TODO: handle file upload and mail confirmation
    return "poof"



if __name__ == "__main__":
    app.run(port=os.environ.get("PORT"), host=os.environ["HOSTNAME"])