from flask import Flask,render_template
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def index():
	return"Hello 簡宏宥!"

@app.route("/mis")
def course():
	return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
	now = datetime.now()
	return render_template("today.html",datetime = str(now))

if __name__ =="__main__":
	app.run()