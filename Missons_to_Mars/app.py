from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# import scrape_mars

from scrape_mars import scrape

# Create an instance of Flask
app = Flask(__name__)

# connection variable
conn = 'mongodb://localhost:27017'


#app name
an="mars_ap"


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri=f"{conn}/{an}")





@app.route("/")
def home():




    ##psuedo
    ### if database exists, display the scrape button less prominently and render the template with the data. if the database doesn't exist, make the scrape buttom more prominent and use a simpler hteml template

    if mongo.db.collection.count()==0:
            home_data={
                "blue":"database is empty, run the scrape",
                "green":"ya nerd"
                }
    else:
        home_data=mongo.db.find("Hemispheres")
        


    return render_template("index.html", data=home_data)




# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_page():

    # Run the scrape function
    # data = scrape_mars.scrape()
    data = scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
