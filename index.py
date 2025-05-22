import requests
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask,render_template,request,make_response, jsonify
from datetime import datetime, timezone, timedelta

import google.generativeai as genai
import os
import google.generativeai as genai

app = Flask(__name__)

@app.route("/")
def index():
	homepage = "<h1>簡宏宥Python網頁(firestore) AI5 webhook6</h1>"
	homepage += "<a href=/mis>MIS</a><br>"
	homepage += "<a href=/today>顯示日期時間</a><br>"
	homepage += "<a href=/welcome?nick=hongyu>傳送使用者暱稱</a><br>"
	homepage += "<a href=/account>網頁表單傳值</a><br>"
	homepage += "<a href=/account>宏宥簡介網頁</a><br>"
	homepage += "<br><a href=/read>讀取Firestore資料</a><br>"
	homepage += "<a href=/movie_read>讀取開眼即將上映影片, 寫入Firestore</a><br>"
	homepage += "<a href=/delete>刪除Firestore資料</a><br>"
	homepage += "<a href=/searchQ>查詢Firestore資料</a><br>"
	homepage += "<a href=/searchtraffic>查詢交通</a><br>"
	homepage += "<a href=/movie_rate>讀取開眼即將上映影片(含分級及最新更新日期)存到資料庫</a><br>"
	
	homepage += '<script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>'
	homepage += '<df-messenger'
	homepage += 'intent="WELCOME"'
	homepage += 'chat-title= "簡宏宥的聊天機器人"'
	homepage += '</script><df-messenger intent="WELCOME" chat-title="MISagent簡宏宥"'
	homepage += 'agent-id="752b836d-e6ed-40ca-9b5c-053384196fd5"'
	homepage += 'language-code="zh-tw" ></df-messenger>'
	homepage += '></df-messenger>'

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


@app.route("/rate")
def rate():
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".filmListAllX li")
    lastUpdate = sp.find(class_="smaller09").text[5:]

    for x in result:
        picture = x.find("img").get("src").replace(" ", "")
        title = x.find("img").get("alt")    
        movie_id = x.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
        hyperlink = "http://www.atmovies.com.tw" + x.find("a").get("href")

        t = x.find(class_="runtime").text
        showDate = t[5:15]

        showLength = ""
        if "片長" in t:
            t1 = t.find("片長")
            t2 = t.find("分")
            showLength = t[t1+3:t2]

        r = x.find(class_="runtime").find("img")
        rate = ""
        if r != None:
             rr = r.get("src").replace("/images/cer_", "").replace(".gif", "")
            if rr == "G":
                rate = "普遍級"
            elif rr == "P":
                rate = "保護級"
            elif rr == "F2":
                rate = "輔12級"
            elif rr == "F5":
                rate = "輔15級"
            else:
                rate = "限制級"

        doc = {
            "title": title,
            "picture": picture,
            "hyperlink": hyperlink,
            "showDate": showDate,
            "showLength": showLength,
            "rate": rate,
            "lastUpdate": lastUpdate
        }

        db = firestore.client()
        doc_ref = db.collection("電影含分級").document(movie_id)
        doc_ref.set(doc)
    return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate





@app.route("/webhook6", methods=["POST"])
def webhook6():
	# build a request object
	req = request.get_json(force=True)
	# fetch queryResult from json
	action =  req.get("queryResult").get("action")
	#msg =  req.get("queryResult").get("queryText")
	#info = "動作：" + action + "； 查詢內容：" + msg

	if (action == "rateChoice"):
		rate = req.get("queryResult").get("parameters").get("rate")
		info = "您選擇的電影分級是:" +　rate

		db = firestore.client()
		collection_ref = db.collection("電影含分級")
		docs = collection_ref.get()
		result = ""
		for doc in docs:
			dict = doc.to_dict()
			if rate in dict["rate"]:
				result += "片名:" + dict["title"] + "\n"
				result += "介紹:" + dict["hyperlink"] + "\n\n"

		if result == "":
			result = ", 抱歉料庫目前無此分級電影"
		else:
			result = ", 相關電影:" + result
		info == result

	elif (action == "MovieDetail"):
			filmq =  req.get("queryResult").get("parameters").get("filmq")
			keyword =  req.get("queryResult").get("parameters").get("any")
			info = "我是簡宏宥開發的電影聊天機器人，您要查詢電影的" + filmq + "問題，關鍵字是：" + any 

			if (question == "片名"):
            db = firestore.client()
            collection_ref = db.collection("電影含分級")
            docs = collection_ref.get()
            found = False
            info = ""
            for doc in docs:
                dict = doc.to_dict()
                if keyword in dict["title"]:
                    found = True 
                    info += "片名：" + dict["title"] + "\n"
                    info += "海報：" + dict["picture"] + "\n"
                    info += "影片介紹：" + dict["hyperlink"] + "\n"
                    info += "片長：" + dict["showLength"] + " 分鐘\n"
                    info += "分級：" + dict["rate"] + "\n" 
                    info += "上映日期：" + dict["showDate"] + "\n\n"
            if not found:
                info += "很抱歉，目前無符合這個關鍵字的相關電影喔"
			elif (action == "CityWeather"):
				city =  req.get("queryResult").get("parameters").get("city")
				token = "rdec-key-123-45678-011121314"
				url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + token + "&format=JSON&locationName=" + str(city)
				Data = requests.get(url)
				Weather = json.loads(Data.text)["records"]["location"][0]["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
				Rain = json.loads(Data.text)["records"]["location"][0]["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
				MinT = json.loads(Data.text)["records"]["location"][0]["weatherElement"][2]["time"][0]["parameter"]["parameterName"]
				MaxT = json.loads(Data.text)["records"]["location"][0]["weatherElement"][4]["time"][0]["parameter"]["parameterName"]
				info = city + "的天氣是" + Weather + "，降雨機率：" + Rain + "%"
				info += "，溫度：" + MinT + "-" + MaxT + "度"


	return make_response(jsonify({"fulfillmentText": "我是簡宏宥聊天機器人"}))


elif (action == "input.unknown"):
		q =  req["queryResult"]["queryText"]
		api_key = os.getenv("API_KEY")
		genai.configure(api_key = api_key)
		model = genai.GenerativeModel('gemini-2.0-flash', generation_config = {"max_output_tokens": 128})
		response = model.generate_content(info)
		info =  response.text

@app.route("/AI")
def AI():
	api_key = 'API_KEY'
	genai.configure(api_key = api_key)
	model = genai.GenerativeModel('gemini-2.0-flash')
	response = model.generate_content('我想查詢靜宜大學資管系的評價？')
	return response.text

@app.route("/webhook7", methods=["POST"])
def webhook7():
	 # build a request object
	req = request.get_json(force=True)
	# fetch queryResult from json
	action =  req.get("queryResult").get("action")
	#msg =  req.get("queryResult").get("queryText")
	#info = "動作：" + action + "； 查詢內容：" + msg
	if (action == "rateChoice"):
…
	elif (action == "MovieDetail"): 
…
	elif (action == "CityWeather"):
…
	elif (action == "input.unknown"):
		info =  req["queryResult"]["queryText"]

	return make_response(jsonify({"fulfillmentText": info}))



if __name__ == "__main__":
    app.run(debug=True)

