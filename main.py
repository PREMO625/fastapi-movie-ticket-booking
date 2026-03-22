from math import ceil
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, Field

app = FastAPI(title="CineStar Movie Ticket Booking API")


movies = [
    {
        "id": 1,
        "title": "Skyline Chase",
        "genre": "Action",
        "language": "English",
        "duration_mins": 138,
        "ticket_price": 280,
        "seats_available": 42,
    },
    {
        "id": 2,
        "title": "Hearts in Monsoon",
        "genre": "Drama",
        "language": "Hindi",
        "duration_mins": 124,
        "ticket_price": 220,
        "seats_available": 36,
    },
    {
        "id": 3,
        "title": "Laugh Riot 2",
        "genre": "Comedy",
        "language": "English",
        "duration_mins": 112,
        "ticket_price": 180,
        "seats_available": 55,
    },
    {
        "id": 4,
        "title": "The Last Corridor",
        "genre": "Horror",
        "language": "Telugu",
        "duration_mins": 105,
        "ticket_price": 200,
        "seats_available": 30,
    },
    {
        "id": 5,
        "title": "Code of Valor",
        "genre": "Action",
        "language": "Hindi",
        "duration_mins": 146,
        "ticket_price": 300,
        "seats_available": 25,
    },
    {
        "id": 6,
        "title": "Midnight Memoir",
        "genre": "Drama",
        "language": "Tamil",
        "duration_mins": 132,
        "ticket_price": 240,
        "seats_available": 40,
    },
]

bookings = []
booking_counter = 1

holds = []
hold_counter = 1


class BookingRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=10)
    phone: str = Field(..., min_length=10)
    seat_type: str = Field(default="standard", min_length=3)
    promo_code: str = Field(default="")


class NewMovie(BaseModel):
    title: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    language: str = Field(..., min_length=2)
    duration_mins: int = Field(..., gt=0)
    ticket_price: int = Field(..., gt=0)
    seats_available: int = Field(..., gt=0)


class SeatHoldRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=10)


def find_movie(movie_id: int) -> Optional[dict]:
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return None


def calculate_ticket_cost(
    base_price: int, seats: int, seat_type: str, promo_code: str = ""
) -> dict:
    seat_type_key = seat_type.strip().lower()
    promo_code_key = promo_code.strip().upper()

    seat_multiplier = {
        "standard": 1.0,
        "premium": 1.5,
        "recliner": 2.0,
    }.get(seat_type_key)

    if seat_multiplier is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid seat_type. Use one of: standard, premium, recliner.",
        )

    original_cost = int(base_price * seat_multiplier * seats)

    discount_percent = {
        "SAVE10": 10,
        "SAVE20": 20,
    }.get(promo_code_key, 0)

    discount_amount = int(original_cost * (discount_percent / 100))
    discounted_cost = original_cost - discount_amount

    return {
        "seat_type": seat_type_key,
        "promo_code": promo_code_key,
        "original_cost": original_cost,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "discounted_cost": discounted_cost,
    }


def filter_movies_logic(
    movie_list: list,
    genre: Optional[str] = None,
    language: Optional[str] = None,
    max_price: Optional[int] = None,
    min_seats: Optional[int] = None,
) -> list:
    filtered = []

    for movie in movie_list:
        if genre is not None and movie["genre"].lower() != genre.lower():
            continue
        if language is not None and movie["language"].lower() != language.lower():
            continue
        if max_price is not None and movie["ticket_price"] > max_price:
            continue
        if min_seats is not None and movie["seats_available"] < min_seats:
            continue
        filtered.append(movie)

    return filtered


def validate_sorting(sort_by: str, order: str, allowed_fields: list) -> tuple:
    sort_key = sort_by.strip()
    order_key = order.strip().lower()

    if sort_key not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by. Allowed values: {allowed_fields}.",
        )

    if order_key not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'.")

    return sort_key, order_key


def paginate_items(items: list, page: int, limit: int) -> dict:
    total = len(items)
    total_pages = ceil(total / limit) if total > 0 else 0
    start = (page - 1) * limit
    page_items = items[start : start + limit]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "items": page_items,
    }


@app.get("/")
def home():
    return {"message": "Welcome to CineStar Booking"}


@app.get("/movies")
def get_movies():
    return {
        "movies": movies,
        "total": len(movies),
        "total_seats_available": sum(movie["seats_available"] for movie in movies),
    }


@app.get("/bookings")
def get_bookings():
    return {
        "bookings": bookings,
        "total": len(bookings),
        "total_revenue": sum(booking["total_cost"] for booking in bookings),
    }


@app.get("/movies/summary")
def movies_summary():
    if not movies:
        return {
            "total_movies": 0,
            "message": "No movies available in the system.",
        }

    prices = [movie["ticket_price"] for movie in movies]
    genre_count = {}
    for movie in movies:
        genre_count[movie["genre"]] = genre_count.get(movie["genre"], 0) + 1

    return {
        "total_movies": len(movies),
        "most_expensive_ticket": max(prices),
        "cheapest_ticket": min(prices),
        "total_seats_across_movies": sum(movie["seats_available"] for movie in movies),
        "movies_by_genre": genre_count,
    }


@app.get("/movies/filter")
def filter_movies(
    genre: Optional[str] = Query(default=None),
    language: Optional[str] = Query(default=None),
    max_price: Optional[int] = Query(default=None, gt=0),
    min_seats: Optional[int] = Query(default=None, ge=0),
):
    filtered = filter_movies_logic(
        movie_list=movies,
        genre=genre,
        language=language,
        max_price=max_price,
        min_seats=min_seats,
    )

    return {
        "filters": {
            "genre": genre,
            "language": language,
            "max_price": max_price,
            "min_seats": min_seats,
        },
        "count": len(filtered),
        "movies": filtered,
    }


@app.get("/movies/search")
def search_movies(keyword: str = Query(..., min_length=1)):
    key = keyword.lower()
    matched = [
        movie
        for movie in movies
        if key in movie["title"].lower()
        or key in movie["genre"].lower()
        or key in movie["language"].lower()
    ]

    if not matched:
        return {
            "message": "No movies matched your search keyword.",
            "total_found": 0,
            "movies": [],
        }

    return {
        "keyword": keyword,
        "total_found": len(matched),
        "movies": matched,
    }


@app.get("/movies/sort")
def sort_movies(
    sort_by: str = Query(default="ticket_price"),
    order: str = Query(default="asc"),
):
    allowed_fields = ["ticket_price", "title", "duration_mins", "seats_available"]
    sort_key, order_key = validate_sorting(sort_by, order, allowed_fields)

    sorted_movies = sorted(
        movies,
        key=lambda movie: movie[sort_key],
        reverse=(order_key == "desc"),
    )

    return {
        "sort_by": sort_key,
        "order": order_key,
        "movies": sorted_movies,
    }


@app.get("/movies/page")
def paginate_movies(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=3, ge=1, le=10),
):
    paging = paginate_items(movies, page, limit)
    return {
        "page": paging["page"],
        "limit": paging["limit"],
        "total": paging["total"],
        "total_pages": paging["total_pages"],
        "movies": paging["items"],
    }


@app.get("/movies/browse")
def browse_movies(
    keyword: Optional[str] = Query(default=None),
    genre: Optional[str] = Query(default=None),
    language: Optional[str] = Query(default=None),
    sort_by: str = Query(default="ticket_price"),
    order: str = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=3, ge=1, le=10),
):
    browsed = movies

    if keyword is not None:
        key = keyword.lower()
        browsed = [
            movie
            for movie in browsed
            if key in movie["title"].lower()
            or key in movie["genre"].lower()
            or key in movie["language"].lower()
        ]

    browsed = filter_movies_logic(
        movie_list=browsed,
        genre=genre,
        language=language,
        max_price=None,
        min_seats=None,
    )

    allowed_fields = ["ticket_price", "title", "duration_mins", "seats_available"]
    sort_key, order_key = validate_sorting(sort_by, order, allowed_fields)
    browsed = sorted(
        browsed,
        key=lambda movie: movie[sort_key],
        reverse=(order_key == "desc"),
    )

    paging = paginate_items(browsed, page, limit)
    return {
        "keyword": keyword,
        "genre": genre,
        "language": language,
        "sort_by": sort_key,
        "order": order_key,
        "page": paging["page"],
        "limit": paging["limit"],
        "total": paging["total"],
        "total_pages": paging["total_pages"],
        "movies": paging["items"],
    }


@app.post("/bookings")
def create_booking(payload: BookingRequest, response: Response):
    global booking_counter

    movie = find_movie(payload.movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")

    if movie["seats_available"] < payload.seats:
        raise HTTPException(status_code=400, detail="Not enough seats available.")

    pricing = calculate_ticket_cost(
        base_price=movie["ticket_price"],
        seats=payload.seats,
        seat_type=payload.seat_type,
        promo_code=payload.promo_code,
    )

    movie["seats_available"] -= payload.seats

    booking = {
        "booking_id": booking_counter,
        "customer_name": payload.customer_name,
        "phone": payload.phone,
        "movie_id": movie["id"],
        "movie_title": movie["title"],
        "seats": payload.seats,
        "seat_type": pricing["seat_type"],
        "promo_code": pricing["promo_code"],
        "original_cost": pricing["original_cost"],
        "discount_percent": pricing["discount_percent"],
        "discount_amount": pricing["discount_amount"],
        "total_cost": pricing["discounted_cost"],
        "status": "confirmed",
        "source": "direct_booking",
    }

    bookings.append(booking)
    booking_counter += 1
    response.status_code = 201

    return {
        "message": "Booking confirmed.",
        "booking": booking,
    }


@app.post("/movies")
def add_movie(payload: NewMovie, response: Response):
    duplicate = next(
        (movie for movie in movies if movie["title"].lower() == payload.title.lower()),
        None,
    )

    if duplicate is not None:
        raise HTTPException(status_code=400, detail="Movie title already exists.")

    new_movie = {
        "id": max([movie["id"] for movie in movies], default=0) + 1,
        "title": payload.title,
        "genre": payload.genre,
        "language": payload.language,
        "duration_mins": payload.duration_mins,
        "ticket_price": payload.ticket_price,
        "seats_available": payload.seats_available,
    }
    movies.append(new_movie)
    response.status_code = 201

    return {
        "message": "Movie created successfully.",
        "movie": new_movie,
    }


@app.post("/seat-hold")
def create_seat_hold(payload: SeatHoldRequest, response: Response):
    global hold_counter

    movie = find_movie(payload.movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")

    if movie["seats_available"] < payload.seats:
        raise HTTPException(status_code=400, detail="Not enough seats available for hold.")

    movie["seats_available"] -= payload.seats

    hold = {
        "hold_id": hold_counter,
        "customer_name": payload.customer_name,
        "movie_id": movie["id"],
        "movie_title": movie["title"],
        "seats": payload.seats,
        "status": "held",
    }
    holds.append(hold)
    hold_counter += 1
    response.status_code = 201

    return {
        "message": "Seat hold created.",
        "hold": hold,
    }


@app.get("/seat-hold")
def get_holds():
    return {
        "holds": holds,
        "total": len(holds),
    }


@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id: int, response: Response):
    global booking_counter

    hold = next((item for item in holds if item["hold_id"] == hold_id), None)
    if hold is None:
        raise HTTPException(status_code=404, detail="Hold not found.")

    movie = find_movie(hold["movie_id"])
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found for this hold.")

    pricing = calculate_ticket_cost(
        base_price=movie["ticket_price"],
        seats=hold["seats"],
        seat_type="standard",
        promo_code="",
    )

    booking = {
        "booking_id": booking_counter,
        "customer_name": hold["customer_name"],
        "phone": "N/A",
        "movie_id": movie["id"],
        "movie_title": movie["title"],
        "seats": hold["seats"],
        "seat_type": "standard",
        "promo_code": "",
        "original_cost": pricing["original_cost"],
        "discount_percent": pricing["discount_percent"],
        "discount_amount": pricing["discount_amount"],
        "total_cost": pricing["discounted_cost"],
        "status": "confirmed",
        "source": "hold_confirmation",
    }

    bookings.append(booking)
    booking_counter += 1
    holds.remove(hold)
    response.status_code = 201

    return {
        "message": "Hold converted to confirmed booking.",
        "booking": booking,
    }


@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id: int):
    hold = next((item for item in holds if item["hold_id"] == hold_id), None)
    if hold is None:
        raise HTTPException(status_code=404, detail="Hold not found.")

    movie = find_movie(hold["movie_id"])
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found for this hold.")

    movie["seats_available"] += hold["seats"]
    holds.remove(hold)

    return {
        "message": "Hold released and seats restored.",
        "released_hold_id": hold_id,
    }


@app.get("/bookings/search")
def search_bookings(customer_name: str = Query(..., min_length=1)):
    key = customer_name.lower()
    matched = [booking for booking in bookings if key in booking["customer_name"].lower()]

    return {
        "customer_name": customer_name,
        "total_found": len(matched),
        "bookings": matched,
    }


@app.get("/bookings/sort")
def sort_bookings(
    sort_by: str = Query(default="total_cost"),
    order: str = Query(default="asc"),
):
    allowed_fields = ["total_cost", "seats"]
    sort_key, order_key = validate_sorting(sort_by, order, allowed_fields)

    sorted_bookings = sorted(
        bookings,
        key=lambda booking: booking[sort_key],
        reverse=(order_key == "desc"),
    )

    return {
        "sort_by": sort_key,
        "order": order_key,
        "bookings": sorted_bookings,
    }


@app.get("/bookings/page")
def paginate_bookings(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=3, ge=1, le=20),
):
    paging = paginate_items(bookings, page, limit)
    return {
        "page": paging["page"],
        "limit": paging["limit"],
        "total": paging["total"],
        "total_pages": paging["total_pages"],
        "bookings": paging["items"],
    }


@app.get("/movies/{movie_id}")
def get_movie_by_id(movie_id: int):
    movie = find_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return movie


@app.put("/movies/{movie_id}")
def update_movie(
    movie_id: int,
    ticket_price: Optional[int] = Query(default=None, gt=0),
    seats_available: Optional[int] = Query(default=None, ge=0),
):
    movie = find_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")

    if ticket_price is not None:
        movie["ticket_price"] = ticket_price
    if seats_available is not None:
        movie["seats_available"] = seats_available

    return {
        "message": "Movie updated successfully.",
        "movie": movie,
    }


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")

    has_bookings = any(booking["movie_id"] == movie_id for booking in bookings)
    if has_bookings:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete movie with existing bookings.",
        )

    movies.remove(movie)
    return {
        "message": "Movie deleted successfully.",
        "deleted_movie": movie["title"],
    }
