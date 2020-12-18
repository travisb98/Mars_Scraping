from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# import scrape_mars

from scrape_mars import scrape

# Create an instance of Flask
app = Flask(__name__)

# connection variable
conn = 'mongodb://localhost:27017'


#app name
an="mars_db"


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri=f"{conn}/{an}")




@app.route("/")
def home():


    ##psuedo
    ### if database exists, display the scrape button less prominently and render the template with the data. if the database doesn't exist, make the scrape buttom more prominent and use a simpler hteml template
    print("------------------------")
    print("------------------------")
    if mongo.db.mars_coll.count()==0:
        print("db is empty")
        print(mongo.db.mars_coll.count())
        home_data={
            "Hemispheres":"database is empty ",
            "Articles":"you need to",
            "FeaturedImage":"run the",
            "Facts":"scrape"
            }
        

    else:
        print("full")
        print(mongo.db.mars_coll.count())

        home_data=mongo.db.mars_coll.find_one()


    print("------------------------")
    print("------------------------")

    # if mongo.db.mars.count()==0:
    #         home_data={
    #             "blue":"database is empty, run the scrape",
    #             "green":"ya nerd"
    #             }
    # else:
    #     home_data=mongo.db.collection.find_one()
    # home_data=mongo.db.collection.Facts

    # home_data=mongo.db.mars.find("Hemispheres")
    # home_data=mongo.db.mars.Hemispheres
    


    return render_template("index.html", data=home_data)




# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_page():



    mars_coll=mongo.db.mars_coll

    if mars_coll.count()==0:
        # Run the scrape function
        data = scrape()
        mars_coll.update({}, data, upsert=True)
    else:
        mars_coll.drop()
        data = scrape()
        mars_coll.update({}, data, upsert=True)

    



    # # Run the scrape function
    # data = scrape()


    ###psuedo code
    ##### if mars_db contains and collections, delete all collections and create new collection and update it with new scraped data

    ## Update the Mongo database using update and upsert=True
    # mars_coll.update({}, data, upsert=True)

 


    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
