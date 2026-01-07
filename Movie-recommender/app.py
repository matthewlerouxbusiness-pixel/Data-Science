from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

#load model artifacts
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def Recommendation_system(movie_title):
    if movie_title not in movies['title'].values:
        return []

    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])),
                       reverse=True, key=lambda x: x[1])

    recommended_titles = [movies.iloc[i[0]].title for i in distances[1:20]]
    return recommended_titles

@app.route('/')
def home():
    return "Movie Recommender is running. Use /recommend?title=MovieName"

@app.route('/recommend')
def recommend():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "No title provided"}), 400

    recs = Recommendation_system(title)
    if not recs:
        return jsonify({"error": "Movie not in dataset"}), 404
    
    return jsonify({"recommendations": recs})

if __name__ == '__main__':
    app.run(debug=True)
