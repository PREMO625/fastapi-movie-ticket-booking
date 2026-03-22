# CineStar Movie Ticket Booking API

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-222222?style=for-the-badge&logo=uvicorn&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger%20UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

A complete FastAPI backend built for the internship final project requirement using the Movie Ticket Booking domain.

## Linkedln Post Link

- LinkedIn post: https://www.linkedin.com/posts/geet-jamdal-6824b7316_github-premo625fastapi-movie-ticket-booking-activity-7441535098325196800-Ud6H?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFAp_gIBGXslOmEQLFltxJy5tVLPPptJ-c4

## Project Summary

- Selected project: Movie Ticket Booking
- Coverage: All 20 required tasks (Day 1 to Day 6)
- Data store: In-memory lists (resets after server restart)
- API docs/testing: Swagger at http://127.0.0.1:8000/docs

## Folder Structure

```text
.
|- main.py
|- requirements.txt
|- README.md
`- screenshots/
```

## Quick Start

### 1) Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Run server

```powershell
uvicorn main:app --reload
```

### 4) Open Swagger

```text
http://127.0.0.1:8000/docs
```

## Tech Features Implemented

### Day 1 - Core GET APIs

- `GET /`
- `GET /movies`
- `GET /movies/{movie_id}`
- `GET /bookings`
- `GET /movies/summary`

### Day 2 - Pydantic Validation + POST APIs

- `BookingRequest` model with field constraints
- Validation errors for invalid body payloads
- `POST /bookings` booking flow

### Day 3 - Helper Functions + Query Logic

- `find_movie(movie_id)`
- `calculate_ticket_cost(base_price, seats, seat_type, promo_code)`
- `filter_movies_logic(...)` using `is not None`
- Reusable pagination helper

### Day 4 - CRUD

- `POST /movies` (201 created + duplicate title check)
- `PUT /movies/{movie_id}`
- `DELETE /movies/{movie_id}` with booking protection

### Day 5 - Multi-step Workflow

- `POST /seat-hold`
- `GET /seat-hold`
- `POST /seat-confirm/{hold_id}`
- `DELETE /seat-release/{hold_id}`

### Day 6 - Search, Sort, Pagination, Combined Browse

- `GET /movies/search`
- `GET /movies/sort`
- `GET /movies/page`
- `GET /bookings/search`
- `GET /bookings/sort`
- `GET /bookings/page`
- `GET /movies/browse`

## Route Ordering Compliance

Fixed routes are declared before variable routes to avoid path conflicts.

Example order used:

1. `/movies/summary`
2. `/movies/filter`
3. `/movies/search`
4. `/movies/sort`
5. `/movies/page`
6. `/movies/browse`
7. `/movies/{movie_id}`

## Screenshot Evidence

All question-wise screenshots are saved in the `screenshots/` folder using proper names.

Primary files include:

- `Q1_home_route.png`
- `Q2_get_all_movies.png`
- `Q3_get_movie_by_id_valid.png`
- `Q3_get_movie_by_id_invalid.png`
- `Q4_get_bookings_initial.png`
- `Q5_movies_summary.png`
- `Q6_validation_error_seats_0.png`
- `Q7_helpers_in_code.png`
- `Q8_create_booking_success.png`
- `Q9_booking_with_promo_save10.png`
- `Q10_movies_filter.png`
- `Q11_create_movie_201.png`
- `Q12_update_movie.png`
- `Q13_delete_movie_blocked_400.png`
- `Q14_seat_hold_create_201.png`
- `Q14_seat_hold_list_200.png`
- `Q15_seat_confirm_hold_201.png`
- `Q15_seat_release_hold_200.png`
- `Q16_movies_search_keyword_action.png`
- `Q17_movies_sort_ticket_price_desc.png`
- `Q18_movies_page_1_limit_3.png`
- `Q18_movies_page_2_limit_3.png`
- `Q19_bookings_search_customer_prem.png`
- `Q19_bookings_sort_total_cost_desc.png`
- `Q19_bookings_page_1_limit_2.png`
- `Q20_movies_browse_combined_filters.png`

## Final Submission Checklist

- Project selected and completed: Movie Ticket Booking
- All 20 tasks implemented and tested in Swagger
- Screenshots captured and organized in `screenshots/`
- Code pushed to GitHub
- LinkedIn post published
- Tagged Innomatics Research Labs in post
- Submitted GitHub and LinkedIn links in Google Form

## Notes

- Since this project uses in-memory lists, restarting the server resets data.
- For final verification screenshots, run all mutation endpoints in one session.
