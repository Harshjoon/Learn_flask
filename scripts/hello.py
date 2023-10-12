from flask import Flask, render_template
from markupsafe import escape
from flask import send_from_directory
from flask import redirect, url_for


app = Flask(__name__)

@app.route("/")
def hello_world():
    #return "<p>Hello, World!</p>"
    #return send_from_directory('/','html/index.html')
    #return app.send_static_file("index.html")
    #return redirect(url_for(filename="index.html"))
    return render_template("./index.html")

