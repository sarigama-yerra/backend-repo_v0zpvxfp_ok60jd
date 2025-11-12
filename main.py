import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from database import db, create_document, get_documents

app = FastAPI(title="Cinema Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MovieIn(BaseModel):
    title: str
    description: Optional[str] = None
    duration_mins: int
    genre: Optional[str] = None
    rating: Optional[str] = None
    poster_url: Optional[str] = None


class ShowtimeIn(BaseModel):
    movie_id: str
    start_time: datetime
    auditorium: str
    rows: int = 8
    cols: int = 12
    price: float = 12.0


class BookingIn(BaseModel):
    showtime_id: str
    customer_name: str
    customer_email: EmailStr
    seats: List[str]


@app.get("/")
def read_root():
    return {"message": "Cinema Booking API is running"}


@app.get("/api/movies")
def list_movies():
    try:
        movies = get_documents("movie")
        for m in movies:
            m["_id"] = str(m["_id"])  # serialize
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/movies")
def create_movie(movie: MovieIn):
    try:
        new_id = create_document("movie", movie.dict())
        return {"_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/showtimes")
def list_showtimes(movie_id: Optional[str] = None):
    try:
        filt = {"movie_id": movie_id} if movie_id else {}
        sts = get_documents("showtime", filt)
        for s in sts:
            s["_id"] = str(s["_id"])  # serialize
        return sts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/showtimes")
def create_showtime(st: ShowtimeIn):
    try:
        new_id = create_document("showtime", st.dict())
        return {"_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/bookings")
def list_bookings(email: Optional[str] = None, showtime_id: Optional[str] = None):
    try:
        filt = {}
        if email:
            filt["customer_email"] = email
        if showtime_id:
            filt["showtime_id"] = showtime_id
        bks = get_documents("booking", filt)
        for b in bks:
            b["_id"] = str(b["_id"])  # serialize
        return bks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/bookings")
def create_booking(b: BookingIn):
    try:
        new_id = create_document("booking", {**b.dict(), "status": "confirmed"})
        return {"_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
                response["database_url"] = "✅ Set"
                response["database_name"] = db.name
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
