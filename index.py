import requests
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask,render_template,request
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

@app.route("/")
def index():
	homepage = "<h1>簡宏宥Python網頁(時間+8)</h1>"
	homepage += "<a href=/mis>MIS</a><br>"
	homepage += "<a href=/today>顯示日期時間</a><br>"
	homepage += "<a href=/welcome?nick=hongyu>傳送使用者暱稱</a><br>"
	homepage += "<a href=/account>網頁表單傳值</a><br>"
	homepage += "<a href=/account>宏宥簡介網頁</a><br>"
	homepage += "<br><a href=/read>讀取Firestore資料</a><br>"
	homepage += "<br><a href=/spider>爬取開眼即將上映電影,存到資料庫</a><br>"
	return homepage


@app.route("/mis")
def course():
	return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
	tz = timezone(timedelta(hours=+8))
	now = datetime.now(tz)
	return render_template("today.html",datetime = str(now))

@app.route("/about")
def me():
	return render_template("about.html")

@app.route("/welcome", methods=["GET"])
def welcome():
	user = request.values.get("nick")
	w = request.values.get("work")
	return render_template("welcome.html", name= user, work = w)


@app.route("/account", methods=["GET", "POST"])
def account():
	if request.method == "POST":
		user = request.form["user"]
		pwd = request.form["pwd"]
		result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd
		return result
	else:
		return render_template("account.html")


@app.route("/read")
def read():
	Result = ""
	db = firestore.client()
	collection_ref = db.collection("靜宜資管")
	docs = collection_ref.get()
	for doc in docs:
		Result += "文件內容 : {}".format(doc.to_dict()) + "<br>"
	return Result

@app.route("/spider")
def read():
	db = firestore.client()

	url = "http://www.atmovies.com.tw/movie/next/"
	Data = requests.get(url)
	Data.encoding = "utf-8"

	sp = BeautifulSoup(Data.text, "html.parser")
	result=sp.select(".filmListAllX li")

	for item in result:
		img = item. find("img")
		#print("片名:", img.get("alt"))
		#print("海報:", img.get("src"))
		a = item.find("a")
		#print("介紹.", "https://www.atmovies.com.tw/" + a.get("href"))
		#print("編號.", a.get("href")[7:19])
		div = item.find(class_="runtime")
		#print("日期.", div.text[5:15])

		if div.text.find("片長:")>0:
			FilmLen = div.text[21:]
			print("片長:", div.text[21:])
		else:
			FilmLen = "無"
			#print("目前無片長資訊")

			doc = {
				"title": img.get("alt"),
				"hyperlink":"https://www.atmovies.com.tw" +　ａ.get("href"),
				"picture": img.get("src"),
				"showDate": div.text[5:15],
				"showLength": FilmLen
			}

			doc_ref = db.collection("簡宏宥").document(a.get("href")[7:19])
			doc_ref.set(doc)
		return "資料庫更新"
	if __name__ =="__main__":
	app.run()



@app.route("DispMovie", methods=["GET", "POST"])
def DispMovie():
	if request.method == "POST":
		keyword = request.form["MovieKeyword"]
		
	else:
		return render_template("account.html")


	db = firestore.client()
	docs = db.collection("簡宏宥").order_by("showDate").get()
	info = ""
	keyword = "人"

	for item in docs:
			if keyword in item. to_dict()["title"]
			info += "片名:<a href=" + item.to_dict()["hyperlink"] + ">" + item.to_dict()["title"]
			info += "介紹" + item.to_dict()["hyperlink"] + "<br>"
			info += "海報:<img src=" + item.to_dict()["picture"] + ">  </img> <br>"
			info += "片長" + item.to_dict()["showLength"] + "<br>"
			info += "上映日期" + item.to_dict()["showLength"] + "<br><br>"
	return info

else:
	return render_template("movie.html")



if __name__ == "__main__":
	app.run()