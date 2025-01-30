from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

movies_db = {}

class MovieRating(BaseModel):
    title: str
    rating: int

@app.post("/rate_movie/")
def rate_movie(movie: MovieRating):
    if movie.rating < 1 or movie.rating > 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10.")

    if movie.title not in movies_db:
        movies_db[movie.title] = []

    movies_db[movie.title].append(movie.rating)  # add rating to the movie
    return {"message": f"Rating for movie {movie.title} added successfully!"}

@app.get("/get_average_rating/{movie_title}")
def get_average_rating(movie_title: str):
    if movie_title not in movies_db or not movies_db[movie_title]:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    avg_rating = sum(movies_db[movie_title]) / len(movies_db[movie_title])
    return {"title": movie_title, "average_rating": round(avg_rating, 2)}

@app.get("/get_all_movies")
def get_all_movies():
    return {"movies": list(movies_db.keys())}

@app.get("/get_movie_ratings/{movie_title}")
def get_movie_ratings(movie_title: str):
    if movie_title not in movies_db:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return {"title": movie_title, "ratings": movies_db[movie_title]}
