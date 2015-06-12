from flask import Flask,  render_template, request
import requests
import random
from qaym import keyCode
app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app

@app.route("/")
def index():
    url = "http://api.qaym.com/0.1/countries/55/cities/key="+keyCode
    cities = requests.get(url).json()
    return render_template("index.html", cities=cities)
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        restuName = "http://api.qaym.com/0.1/cities/" + request.form["user_city"]+ "/items/key="+keyCode
        restu = requests.get(restuName).json()
        if restu==False:
            print("restu is False")
            return page_not_found(restu)
            # break;
        restuInt = random.randint(0,len(restu)-1)
	restuRand = restu[restuInt]
	print restuRand["item_id"]
	restuLocation = "http://api.qaym.com/0.1/items/"+ restuRand["item_id"] +"/locations/key="+keyCode
	restuLocation = requests.get(restuLocation).json()
    restuListInThisCity = []
    for resturant in restuLocation:
        print("jowiejfaoiwej")
        if(resturant["city_id"]!=request.form["user_city"]):
            print("deleted resturant:")
            del resturant
	print restuLocation
	return render_template("search.html", restuRand = restuRand,restuLocation=restuLocation)
    else:
        return render_template("search.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    

if __name__ == "__main__":
    app.run()
    #host="0.0.0.0"
