import httpx
from typing import List
from mcp.server.fastmcp import FastMCP
import hmac
import base64
import hashlib
from models import *

# Initialize FastMCP server
mcp = FastMCP("CGV")

# Constants
USER_AGENT = 'CGV Cinema/2.9.4 (iPhone; iOS 18.3.1; Scale/3.00)'
BASE_API_URL = 'https://www.cgv.vn/en'
SIGNATURE_SECRET_KEY = 'juBDKUIb9C8vfbV171hdMHwSzxo='
X_DEVICE = 'iOS_18.3_2.9.4'

def server_lifespan():
    pass

@mcp.tool()
def get_cinema_list() -> CinemaListResponse:
    """Get list of all CGV cinema locations grouped by city.
    
    Returns:
        CinemaListResponse: List of cities containing cinema locations with details like name,
                           address, coordinates and special features
    """
    response = httpx.get(BASE_API_URL + '/api/cinema/list', headers={'User-Agent': USER_AGENT})
    return CinemaListResponse(**response.json())

@mcp.tool()
def get_movie_list() -> MovieListResponse:
    """Get list of movies currently showing at CGV.
    
    Returns:
        MovieListResponse: List of movies with details
    """
    response = httpx.get(BASE_API_URL + '/api/movie/listSneakShow', headers={'User-Agent': USER_AGENT})
    return MovieListResponse(**response.json())

@mcp.tool()
def get_movie_schedules(sku: str | int, date: str | int) -> MovieScheduleResponse:
    """Get movie schedules for a specific movie on a given date.
    
    Args:
        sku: Movie SKU identifier (example: 25002900)
        date: Date to get schedules for (format: DDMMYYYY, e.g. 14032025 for March 14, 2025)
        
    Returns:
        MovieScheduleResponse: Movie schedules with showtimes
    """
    response = httpx.get(BASE_API_URL + f'/cinemas/catalog_mobile/movieSchedules/sku/{sku}/date/{date}', headers={'User-Agent': USER_AGENT})
    return MovieScheduleResponse(**response.json())

@mcp.tool()
def get_cinema_schedules(cinema_id: str | int, date: str | int) -> CinemaScheduleResponse:
    """Get all movie schedules for a specific cinema on a given date.
    
    Args:
        cinema_id: Cinema location identifier (Cinema.id)
        date: Date to get schedules for (format: DDMMYYYY, e.g. 14032025 for March 14, 2025)
        
    Returns:
        CinemaScheduleResponse: Cinema schedules with movies and showtimes
    """
    response = httpx.get(BASE_API_URL + f'/cinemas/catalog_mobile/siteschedules/id/{cinema_id}/date/{date}', headers={'User-Agent': USER_AGENT})
    return CinemaScheduleResponse(**response.json())

def generate_signature(message: str, secret_key: str = SIGNATURE_SECRET_KEY) -> str:
    """Generate HMAC-SHA256 signature for API requests.
    
    Args:
        message: Message to sign
        secret_key: Secret key for signing (defaults to SIGNATURE_SECRET_KEY)
        
    Returns:
        str: Base64 encoded HMAC signature
    """
    
    key = secret_key.encode('utf-8')
    message = (X_DEVICE + message).encode('utf-8')
    
    hmac_obj = hmac.new(key, message, hashlib.sha256)
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')
    return signature

@mcp.tool()
def login(email: str, password: str) -> LoginResponse:
    url = BASE_API_URL + "/api/customer/login"
    signature = generate_signature(f"{email}{password}")

    data = {
        "password": password,
        "auto": 0,
        "signature": signature,
        "email": email
    }

    response = httpx.post(url, data=data, headers={
        "User-Agent": USER_AGENT,
        "X-Device": X_DEVICE,
        "Content-Type": "application/x-www-form-urlencoded",
    })
    print(response.json())
    return LoginResponse(**response.json())

@mcp.tool()
def get_seatmap(cinema_id: str | int, customer_id: str | int, u_token: str, date: str | int, session_id: str | int) -> SeatMapResponse:
    """Get seat map for a movie session.
    
    Args:
        cinema_id: Cinema location identifier (Cinema.id)
        customer_id: Customer ID from login response (LoginResponse.data.entity_id)
        u_token: Access token from login response (LoginResponse.data.access_token)
        date: Date of the session (format: YYYYMMDD)
        session_id: Session identifier (LoginResponse.data.sessions[0].id)
        
    Returns:
        SeatMapResponse: Seat map data including available seats and pricing
    """
    url = BASE_API_URL + "/api/ticket/seatmap"
    
    headers = { 
        "User-Agent": USER_AGENT,
        "U-Token": u_token,
        "X-Device": X_DEVICE,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    data = {
        "cinema_id": cinema_id,
        "customer_id": customer_id,
        "date": date,
        "session_id": session_id,
        "signature": generate_signature(f"{cinema_id}{session_id}{customer_id}")
    }
    
    return SeatMapResponse(**httpx.post(url, headers=headers, data=data).json())

@mcp.tool()
def get_info_concession(session_id: str | int, product: str | int, ticket: List[TicketRequest], customer_id: str | int, theater_id: str, session_date: str) -> dict:
    """Get concession information for a movie session.
    
    Args:
        session_id: Session identifier (LoginResponse.data.sessions[0].id)
        product: Product identifier (MovieItem.id)
        ticket: List of ticket details including seat information
        customer_id: Customer ID from login response (LoginResponse.data.entity_id)
        theater_id: Theater identifier (Cinema.id)
        session_date: Date of the session (format: DD/MM/YYYY)
        
    Returns:
        dict: Concession information including available combos and pricing
    """
    url = BASE_API_URL + "/api/ticket/getInfoConcession"
    
    data = {
        "session[id]": session_id,
        "product": product,
        "ticket": ticket,
        "customer_id": customer_id,
        "theater[id]": theater_id,
        "session[date]": session_date
    }
    
    headers = {
        "User-Agent": USER_AGENT,
        "X-Device": X_DEVICE,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    response = httpx.post(url, headers=headers, data=data)
    return ConcessionResponse(**response.json())

@mcp.tool()
def add_tickets(
    session_id: str | int,
    session_time: str,
    product: str | int,
    ticket: List[TicketRequest],
    session_showing_type: str,
    info_compound: dict,
    theater_name: str,
    is_u22: bool,
    session_date: str,
    movie_format: str,
    theater_cinema: str,
    customer_id: str | int,
    theater_id: str,
    u_token: str
) -> dict:
    f"""Add tickets to cart for a movie session.
    
    Args:
        session_id: Session identifier (LoginResponse.data.sessions[0].id)
        session_time: Session time in HH:MM format (e.g. "14:00")
        product: Product identifier (MovieItem.id)
        ticket: List of ticket details including seat information (TicketRequest schema). Keep the field names exactly as in the schema:
               {
                 "TicketTypeCode": str,  # Ticket type identifier (Seat.ticket_type_code)
                 "Qty": int,  # Number of tickets
                 "PriceInCents": str,  # Price in cents
                 "OptionalAreaCatSequence": str,  # Seat area sequence (Seat.areacode)
                 "OptionalAreaCatCode": int,  # Seat area code (Seat.areacat_code)
                 "Title": str,  # Ticket type name (Seat.name)
                 "TTypeCode": str,  # Ticket type code (Seat.ttype_code)
                 "total": int,  # Total number of tickets
                 "combo": int,  # Number of combos
                 "Seat": List[SeatInfo]  # List of seat details including:
                        # - label: Row label (e.g. "H") (SeatRow.label)
                        # - number: Seat number/sequence (e.g. "00900701") (Seat.areanumber)
                        # - col: Column index (Seat.col)
                        # - row: Row index (Seat.row)
                        # - id: Unique seat identifier (Seat.id)
               })
        session_showing_type: Type of showing (e.g. "03" for regular showing)
        info_compound: Compound information including:
                      - info_admission_cards: Admission card details (empty string if none)
                      - info_discounts: Discount information as JSON string (empty object if none)
                      - info_vouchers: List of vouchers as JSON string (empty array if none) 
                      - info_points: Points to redeem (0 if none)
                      - info_gift_cards: Gift card amount (0 if none)
                      - info_partner_ship: Partnership details (empty string if none)
                      - info_combo: Dictionary mapping combo IDs to quantities (e.g. {"103793": 1}) (ExtraDataConcessionResponse.id)
        theater_name: Full theater name (e.g. "CGV Vincom Royal City") (Cinema.name)
        is_u22: Whether customer is under 22 years old (bool: 0/1)
        session_date: Date of the session (format: DD/MM/YYYY)
        movie_format: Movie format description (e.g. "2D Phụ Đề Việt")
        theater_cinema: Cinema room name (e.g. "Cinema 5") (Session.room)
        customer_id: Customer ID from login response (LoginResponse.data.entity_id)
        theater_id: Theater identifier (Cinema.id)
        u_token: Access token from login response (LoginResponse.data.access_token)
        
    Returns:
        dict: Response containing cart information and payment details
    """
    url = BASE_API_URL + "/api/ticket/addTickets"
    
    headers = {
        "User-Agent": USER_AGENT,
        "U-Token": u_token,
        "X-Device": X_DEVICE,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "session[time]": session_time,
        "product": product,
        "ticket": ticket,
        "session[showing_type]": session_showing_type,
        "info_compound": info_compound,
        "theater[theatre]": theater_name,
        "is_u22": int(is_u22),
        "session[date]": session_date,
        "session[id]": session_id,
        "movie_format": movie_format,
        "theater[cinema]": theater_cinema,
        "customer_id": customer_id,
        "theater[id]": theater_id
    }
    
    response = httpx.post(url, headers=headers, data=data)
    return AddTicketResponse(**response.json())

@mcp.tool()
def book_order_by_compound(cart_id: str, payment_method: str, info_compound: InfoCompound, u_token: str) -> BookOrderResponse:
    """Book an order with compound information like discounts, vouchers, combos etc.
    
    Args:
        cart_id: Cart identifier from add_tickets response (AddTicketResponse.cart_id)
        payment_method: Payment method code (e.g. "vnpay")
        info_compound: Compound information including discounts, vouchers, combos etc.
        u_token: Access token from login response (LoginResponse.data.access_token)
        
    Returns:
        BookOrderResponse: Response containing order ID and payment details. For VNPay includes payment URL
                         with transaction details.
    """
    url = BASE_API_URL + "/api/ticket/bookOrderByCompound"
    
    headers = {
        "User-Agent": USER_AGENT,
        "U-Token": u_token,
        "X-Device": X_DEVICE,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Generate signature
    message = f"{cart_id}{payment_method}"
    signature = generate_signature(message)
    
    data = {
        "cart_id": cart_id,
        "payment[method]": payment_method,
        "signature": signature,
        "info_compound": info_compound.model_dump()
    }
    
    response = httpx.post(url, headers=headers, data=data)
    return BookOrderResponse(**response.json())

@mcp.tool()
def get_profile(profile_id: str, access_token: str) -> dict:
    """Get customer profile information.
    
    Args:
        profile_id: Customer profile ID (LoginResponse.data.entity_id)
        access_token: Access token from login response (LoginResponse.data.access_token)
        
    Returns:
        dict: Customer profile information
    """
    return httpx.get(BASE_API_URL + f'/api/customer/profile/id/{profile_id}', headers={
        "User-Agent": USER_AGENT,
        "U-Token": access_token,
        "X-Device": X_DEVICE
    }).json()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')