# FastAPI Final Project - Movie Ticket Booking (CineStar)

This project is a complete FastAPI backend for a Movie Ticket Booking system, implemented to cover all Day 1 to Day 6 concepts from the internship assignment.

## Project Details

- Selected project: Movie Ticket Booking
- Framework: FastAPI
- Validation: Pydantic
- Data storage: In-memory lists (no database)
- API test interface: Swagger UI

## Folder Structure

- `main.py`
- `requirements.txt`
- `README.md`
- `screenshots/`

## Setup Instructions

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn main:app --reload
```

4. Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Implemented Features (Q1-Q20)

### Day 1 - Basic GET APIs

1. `GET /` home route.
2. `GET /movies` returns all movies, total count, total seats available.
3. `GET /movies/{movie_id}` returns movie by ID with not found handling.
4. `GET /bookings` returns all bookings, total, and total revenue.
5. `GET /movies/summary` returns overall movie analytics.

### Day 2 - POST + Pydantic Validation

6. `BookingRequest` model with constraints:
   - `customer_name` min length
   - `movie_id > 0`
   - `seats > 0 and <= 10`
   - `phone` min length
   - `seat_type` default `standard`
7. Helper functions and validation support used in booking flow.
8. `POST /bookings` with seat availability checks and booking creation.
9. Promo code support in booking (`SAVE10`, `SAVE20`) with original and discounted cost fields.
10. Filtering endpoint based on optional query params.

### Day 3 - Helper Functions + Query Logic

- `find_movie(movie_id)`
- `calculate_ticket_cost(base_price, seats, seat_type, promo_code)`
- `filter_movies_logic(...)` with `is not None` checks
- `paginate_items(...)`

### Day 4 - CRUD Operations

11. `POST /movies` adds a new movie with duplicate title check and `201 Created`.
12. `PUT /movies/{movie_id}` supports optional updates.
13. `DELETE /movies/{movie_id}` prevents deleting movies with existing bookings.

### Day 5 - Multi-step Workflow

14. Seat hold workflow:
   - `POST /seat-hold`
   - `GET /seat-hold`
15. Hold conversion/release workflow:
   - `POST /seat-confirm/{hold_id}` converts hold to booking
   - `DELETE /seat-release/{hold_id}` restores seats

### Day 6 - Search, Sort, Pagination, Combined Browse

16. `GET /movies/search` across title, genre, language.
17. `GET /movies/sort` with validated sort fields and order.
18. `GET /movies/page` with pagination metadata.
19. Booking utilities:
   - `GET /bookings/search`
   - `GET /bookings/sort`
   - `GET /bookings/page`
20. `GET /movies/browse` combines keyword search + filters + sorting + pagination.

## Route Ordering Note

Fixed routes are defined before variable routes to follow FastAPI routing rules. Example:

- `/movies/summary`, `/movies/filter`, `/movies/search`, `/movies/sort`, `/movies/page`, `/movies/browse`
- then `/movies/{movie_id}`

## Suggested Swagger Testing Order

1. Test all GET endpoints (Q1-Q5).
2. Test booking validation (Q6-Q9).
3. Test filters and helper-based logic (Q10).
4. Test CRUD on movies (Q11-Q13).
5. Test hold -> confirm/release workflow (Q14-Q15).
6. Test search/sort/page/browse endpoints (Q16-Q20).

## Screenshot Naming (Recommended)

Use PNG files in `screenshots/` such as:

- `Q1_home_route.png`
- `Q2_get_movies.png`
- `Q3_get_movie_by_id_valid.png`
- `Q3_get_movie_by_id_invalid.png`
- `Q8_create_booking.png`
- `Q9_promo_save10.png`
- `Q14_seat_hold.png`
- `Q15_hold_confirm.png`
- `Q20_movies_browse.png`

## Important Note

This project uses in-memory data structures. If you restart the server, data resets to initial seed values.
