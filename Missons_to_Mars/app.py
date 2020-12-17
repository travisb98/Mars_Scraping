from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# import scrape_mars

from scrape_mars import scrape

# Create an instance of Flask
app = Flask(__name__)

#connection variable
# conn = 'mongodb://localhost:27017'



# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri=conn)

@app.route("/")
def home():

    # data = scrape()
    # return render_template("index.html", data=data)

    testy={
        "blue":1,
        "green":2
    }

    return render_template("index.html", data=testy)




# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_page():

    # Run the scrape function
    # data = scrape_mars.scrape()
    data = scrape()

    # Update the Mongo database using update and upsert=True
    # mongo.db.collection.update({}, data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
