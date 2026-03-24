from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

FILE = "ratings.json"

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump({}, f)

def get_data():
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

movies = [
    {"id": "the bloodworm", "title": "", the bloodworm"pdf": "the bloodworm.pdf", "poster": "posters/leo.jpg"},
    {"id": "vikram", "title": "Vikram", "pdf": "vikram.pdf", "poster": "posters/vikram.jpg"}
]

@app.route("/")
def home():
    return render_template("index.html", movies=movies)

@app.route("/movie/<movie_id>")
def movie_page(movie_id):
    movie = next((m for m in movies if m["id"] == movie_id), None)
    return render_template("movie.html", movie=movie)

@app.route("/rate/<movie_id>", methods=["POST"])
def rate(movie_id):
    data = request.json
    user = data.get("user")
    rating = data.get("rating")

    all_data = get_data()

    if movie_id not in all_data:
        all_data[movie_id] = []

    # remove old rating
    all_data[movie_id] = [r for r in all_data[movie_id] if r["user"] != user]

    # add new
    all_data[movie_id].append({"user": user, "rating": rating})

    save_data(all_data)

    avg = sum(r["rating"] for r in all_data[movie_id]) / len(all_data[movie_id])

    return jsonify({"average": round(avg, 2)})

if __name__ == "__main__":
    app.run(debug=True)
