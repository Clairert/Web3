from flask import Flask, request, render_template
from mongoengine import *
import os
import csv

app = Flask(__name__)
connect('web3DB')

app.config.from_object('config')



#Country class
class Country(Document):
	name = StringField()
	data = DictField()

#Home route
@app.route('/')
@app.route('/index')
@app.route('/home')
def hello_world():
    pageName = "Information"

    for file in os.listdir(app.config['FILES_FOLDER']):
        filename = os.fsdecode(file)
        path = os.path.join(app.config['FILES_FOLDER'],filename)
        f = open(path)
        r = csv.DictReader(f) 
        d = list(r)
        for data in d:
            county = Country()
            dict = {}
            for key in data: 
                if key == "country":
                    # check if this country already exists in the db
                    if Country.objects(name=data[key]).count() > 0:
                        county = Country.objects(name=data[key])[0]
                        dict = county.data
                    else:
                        county.name = data[key]
                else:
                    #saving data to the database from files
                    f = filename.replace(".csv","")
                    if f in dict: # check if this filename is already a field in the dict
                        dict[f][key] = data[key] # if it is, just add a new subfield
                    else:
                        dict[f] = {key:data[key]} # if it is not, create a new object and assign it to the dict
            county["data"] = dict
            Country.save(county)
            #saving country
    
    return render_template("index.html", title=pageName), 200


#route to inspiration page
@app.route('/inspiration')
def inspiration():
    pageName = "Inspiration"
    newcountry = Country(name="motivationLand")
    newcountry.save()
    return render_template("inspiration.html", title=pageName)


@app.route('/loadData')
def loadData():
    return "Success"


@app.route('/countries', methods=['GET'])
@app.route('/countries/<country_id>', methods=['GET'])
def getCountries(country_id=None):
    Countries = Country.objects
    return Countries.to_json(), 200



@app.route('/delete/<country_id>', methods=['DELETE'])
def deleteCountry(country_id):
    #codeGOESHERE
    return "Success"


@app.route('/newCountry', methods=['PUT'])
def addCountry():
    #CODECODEY
    return "Success"


if __name__=="__main__":
    app.run(debug=True, port=8080)

