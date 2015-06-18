# -*- coding: utf-8 -*-
from flask import Flask,  render_template, request
import requests
import random
from qaym import keyCode
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app
GoogleMaps(app)

@app.route("/")
def index():
    countriesURL = "http://api.qaym.com/0.1/countries/key="+keyCode
    countries = requests.get(countriesURL).json()
    print("********************")
    print("countries")
    print countries
    print("********************")
    return render_template("index.html", countries = countries) 
    
@app.route('/user_country', methods=['POST'])
def user_country():
    ret = ''
    citiesURL = "http://api.qaym.com/0.1/countries/"+ request.form["user_country"]+"/cities/key="+keyCode
    cities = requests.get(citiesURL).json()
    if cities==False:
        print("cities is False")
        return page_not_found(cities)
    for entry in cities:
        ret += '<option value="{'+entry.city_id+'}">{}</option>'.format(entry)
        # <option value="{{ city.city_id }}"  required>{{city.name}} </option>
    return ret

@app.route("/city", methods=["GET", "POST"])
def city():
    if request.method == "POST":
        citiesURL = "http://api.qaym.com/0.1/countries/"+ request.form["user_country"]+"/cities/key="+keyCode
        cities = requests.get(citiesURL).json()
        if cities==False:
            print("cities is False")
            return page_not_found(cities)
        return render_template("city.html", cities = cities)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cityInfoAPIRequest = "http://api.qaym.com/0.1/cities/" + request.form["user_city"]+ "/key="+keyCode
        cityInfo = requests.get(cityInfoAPIRequest).json()
        resturantListInThisCityAPIRequest = "http://api.qaym.com/0.1/cities/" + request.form["user_city"]+ "/items/key="+keyCode
        restu = requests.get(resturantListInThisCityAPIRequest).json()
        if restu==False:
            print("restu is False")
            return page_not_found(restu)
            # break;
        restuInt = random.randint(0,len(restu)-1)
        print("restuInt: ")
        print(restuInt)
        restuRand = restu[restuInt]
        print restuRand["item_id"]
        restuLocation = "http://api.qaym.com/0.1/items/"+ restuRand["item_id"] +"/locations/key="+keyCode
        restuLocation = requests.get(restuLocation).json()
        restuListInThisCity = []
        listOfLocations = []
        for resturant in restuLocation:
            print("jowiejfaoiwej")
            print resturant
            print restuLocation
            if(resturant["city_id"]==request.form["user_city"]):
                print('request.form["user_city"]: %s, resturant["city_id"]: %s') % (request.form["user_city"] , resturant["city_id"])
                print("added resturant:")
                print resturant
                restuListInThisCity.append(resturant)
                location = (resturant["latitude"],resturant["longitude"])
                listOfLocations.append(location)
            else:
                print("deleted a resturant")
        print restuLocation
        # mymap = Map(
        #         identifier="view-side",
        #         lat=37.4419,
        #         lng=-122.1419,
        #         markers=[(37.4419, -122.1419)]
        #     )
        mapOfBranches = Map(identifier="resturantBranchesMap", lat=cityInfo["latitude"], lng=cityInfo["longitude"],markers=listOfLocations,zoom=cityInfo["zoom"])
        return render_template("search.html", restuRand = restuRand,restuLocation=restuListInThisCity, mapOfBranches=mapOfBranches)
    else:
        return render_template("search.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    

if __name__ == "__main__":
    app.run()
    #host="0.0.0.0"
