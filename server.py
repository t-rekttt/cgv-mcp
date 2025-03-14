import httpx
from typing import List, Optional
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("CGV")

# Constants
USER_AGENT = 'CGV Cinema/2.9.4 (iPhone; iOS 18.3.1; Scale/3.00)'
BASE_API_URL = 'https://www.cgv.vn/default'

class CineItem(BaseModel):
    cine_id: str
    cine_title: str 
    cine_image: str
    cine_url: str

class CineListResponse(BaseModel):
    data: List[CineItem]

class MovieItem(BaseModel):
    id: str
    sku: str
    category_id: int
    category: str
    name: str
    thumbnail: str
    movie_trailer: str | None
    movie_event: str
    rating_code: str
    rating_icon: str
    codes: str
    is_booking: bool
    is_sneakshow: bool
    is_new: bool
    position: int
    movie_endtime: int
    release_date: str | None
    is_gerp: bool
    showing_date: str

class MovieListResponse(BaseModel):
    data: List[MovieItem]

class Session(BaseModel):
    id: int
    cinema_id: str
    time: str
    cinox_endtime: str
    room: str
    theater: str
    is_booking: bool
    code: str
    remaining_seats: int
    sub_type: str
    showing_date_time: str
    showing_type: str

class Language(BaseModel):
    name: str
    name_color: str
    code: str
    cinema_type: str
    service_link: str
    sessions: List[Session]

class Cinema(BaseModel):
    id: str
    name: str
    latitude: str
    longitude: str
    languages: List[Language]

class Location(BaseModel):
    city_id: str
    name: str
    cinemas: List[Cinema]

class Schedule(BaseModel):
    date: str
    locations: List[Location]

class MovieScheduleResponse(BaseModel):
    data: List[Schedule]

class Seat(BaseModel):
    id: Optional[str] = None
    col: Optional[str] = ""
    row: Optional[str] = ""
    seat_type_name: Optional[str] = None
    seat_type_color: Optional[str] = None
    areacode: Optional[str] = None
    areanumber: Optional[str] = None
    areacat_code: Optional[str] = None
    status: Optional[str] = None
    ticket_type_code: Optional[str] = None
    ttype_code: Optional[str] = None
    price: Optional[int] = None
    areacat_intseq: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    combo: Optional[int] = None
    couple_code: Optional[str] = None
    real_price: Optional[int] = None
    price_u22: Optional[int] = None

class SeatRow(BaseModel):
    label: str
    seats: List[Seat]

class SeatMapResponse(BaseModel):
    data: List[SeatRow]

class Session(BaseModel):
    id: int
    cinema_id: str
    time: str
    cinox_endtime: str
    room: str
    theater: str
    is_booking: bool
    code: str
    remaining_seats: int
    sub_type: str
    showing_date_time: str
    showing_type: str

class Language(BaseModel):
    name: str
    name_color: str
    code: str
    cinema_type: str
    service_link: str
    sessions: List[Session]

class Movie(BaseModel):
    id: str
    thumbnail: str
    sku: str
    name: str
    movie_endtime: int
    rating_code: str
    rating_icon: str
    languages: List[Language]

class Schedule(BaseModel):
    date: str
    movies: List[Movie]

class CinemaScheduleResponse(BaseModel):
    data: List[Schedule]

@mcp.tool()
def get_cine_list() -> CineListResponse:
    """Get list of CGV cinemas.
    
    Returns:
        CineListResponse: List of cinema locations with details
    """
    response = httpx.get(BASE_API_URL + '/api/common/getcine', headers={'User-Agent': USER_AGENT})
    return CineListResponse(**response.json())

@mcp.tool()
def get_movie_list() -> MovieListResponse:
    """Get list of movies currently showing at CGV.
    
    Returns:
        MovieListResponse: List of movies with details
    """
    response = httpx.get(BASE_API_URL + '/api/movie/listSneakShow', headers={'User-Agent': USER_AGENT})
    return MovieListResponse(**response.json())

@mcp.tool()
def get_movie_schedules(sku: str, date: str) -> MovieScheduleResponse:
    """Get movie schedules for a specific movie on a given date.
    
    Args:
        sku: Movie SKU identifier
        date: Date to get schedules for (format: DDMMYYYY, e.g. 14032025 for March 14, 2025)
        
    Returns:
        MovieScheduleResponse: Movie schedules with showtimes
    """
    response = httpx.get(BASE_API_URL + f'/cinemas/catalog_mobile/movieSchedules/sku/{sku}/date/{date}', headers={'User-Agent': USER_AGENT})
    return MovieScheduleResponse(**response.json())

@mcp.tool()
def get_cinema_schedules(cinema_id: str, date: str) -> CinemaScheduleResponse:
    """Get all movie schedules for a specific cinema on a given date.
    
    Args:
        cinema_id: Cinema location identifier
        date: Date to get schedules for (format: DDMMYYYY, e.g. 14032025 for March 14, 2025)
        
    Returns:
        CinemaScheduleResponse: Cinema schedules with movies and showtimes
    """
    response = httpx.get(BASE_API_URL + f'/cinemas/catalog_mobile/siteschedules/id/{cinema_id}/date/{date}', headers={'User-Agent': USER_AGENT})
    return CinemaScheduleResponse(**response.json())

def get_seatmap(cinema_id, customer_id, u_token, date, session_id, signature) -> SeatMapResponse:
    url = "https://www.cgv.vn/default/api/ticket/seatmap"
    
    headers = {
        "User-Agent": USER_AGENT,
        "U-Token": u_token,
        "X-Device": "iOS_18.3_2.9.4",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    data = {
        "cinema_id": cinema_id,
        "customer_id": customer_id,
        "date": date,
        "session_id": session_id,
        "signature": signature
    }
    
    return SeatMapResponse(**httpx.post(url, headers=headers, data=data).json())

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')