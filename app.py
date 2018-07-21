from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape

app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route("/")
def index():
    dict = db.mars.find_one()
    return render_template("index.html", dict=dict)

@app.route("/scrape")
def scrape_():
    db.mars.update(
        {},
        scrape(),
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
