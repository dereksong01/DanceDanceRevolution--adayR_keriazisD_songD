from flask import Flask, render_template, request, session, redirect, url_for, flash


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    '''Index takes current user and their posts '''
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
