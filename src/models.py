from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class Error(BaseModel):
    code: int | None = None
    detail: str | bool

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
    id: str | int
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
    data: List[SeatRow] | None = None
    errors: List[Error] | None = None

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

class Special(BaseModel):
    title: str
    id: int
    code: str
    small_image: str
    main_image: str

class Cinema(BaseModel):
    id: str
    code: str
    name: str
    latitude: str
    longitude: str
    address: str
    is_gerp: bool
    specials: List[Special]

class CityGroup(BaseModel):
    name: str
    cinemas: List[Cinema]

class CinemaListResponse(BaseModel):
    data: List[CityGroup]

class MemberCard(BaseModel):
    card_name: str
    card_number: str 
    card_type: str
    card_info: str
    is_clicked: int
    remaining_ticket: int

class LoginData(BaseModel):
    access_token: str
    entity_id: str
    member_id: str
    member_card_number: str
    member_level: str
    total_spend_in_year: int
    total_spend_last_year: str
    current_year: str
    reference_site: str | None
    fav_region_id: str
    info_available_point: int
    info_expiring_point: int
    info_expected_point: int
    info_total_saving_point: int
    info_total_spend_point: int
    usersessionid: str
    fullname: str
    telephone: str
    email: str
    referral_code: str
    gender: str
    info_grades: list
    avatar: str
    is_u22: int
    remain_refund: int
    u22_url: str
    info_member_cards: List[MemberCard]
    partnercard_goto: str
    partnercard_title: str
    partnercard_icon: str

class LoginResponse(BaseModel):
    data: LoginData | None = None
    errors: List[Error] | None = None

class SeatInfo(BaseModel):
    label: str
    number: str
    col: int
    row: int
    id: int

class TicketRequest(BaseModel):
    TicketTypeCode: str
    Qty: int
    PriceInCents: str
    OptionalAreaCatSequence: str
    OptionalAreaCatCode: int
    Title: str
    TTypeCode: str
    total: int
    combo: int
    Seat: List[SeatInfo]

class PartnerPaymentMethod(BaseModel):
    code: str
    payment_method: str
    name: str
    require_input_code: bool
    icon: str

class PartnerItem(BaseModel):
    id: str
    name: str
    description: str
    partner_code: str
    allow_card: str
    require_input_code: bool
    payment_method: List[PartnerPaymentMethod]

class PartnerShip(BaseModel):
    id: str
    name: str
    items: List[PartnerItem]

class PaymentMethod(BaseModel):
    name: str
    icon: str
    sort: str
    payment_method: str

class ExtraDataTicket(BaseModel):
    price: str
    qty: int
    type: str

class ExtraDataConcession(BaseModel):
    type: str
    price: int
    qty: int

class ExtraData(BaseModel):
    is_discounted: bool
    site_code: str
    site_name: str
    screen_name: str
    screen_code: str
    session_time: str
    session_date: str
    movie_name: str
    movie_format: str
    ticket: Dict[str, ExtraDataTicket]
    concession: Dict[str, ExtraDataConcession]

class InfoPayment(BaseModel):
    marketing_promo: List[Any]
    info_partner_ship: List[PartnerShip]
    info_payment_gateway: Dict[str, str]

class AddTicketResponse(BaseModel):
    data: Dict[str, Any]
    cart_id: str
    billing: List[Any]
    info_payment: InfoPayment
    extra_data: ExtraData
    payment_methods: List[PaymentMethod]
    zalopay: str
    airpay: str
    max_percent_point: int

class InfoCompound(BaseModel):
    info_admission_cards: str = ""
    info_discounts: dict = {}
    info_vouchers: list = []
    info_points: str = ""
    info_gift_cards: str = ""
    info_gift_cards_new: str = ""
    info_combo: dict = {}
    info_partner_ship: str = ""

class VNPayInfo(BaseModel):
    url: str
    Tmn_code: str

class BookOrderResponse(BaseModel):
    data: dict[str, Any]
    order_id: str
    payment_method: str
    info_vnpay: VNPayInfo | None = None
    is_gerp: bool

class ExtraDataConcessionResponse(BaseModel):
    id: str
    name: str
    short_desc: str
    desc: str
    icon: str
    background: str
    price: int
    qty: int
    o_price: int
    ticket: int
    tprice: int
    type: int
    remaining_concession: int

class ConcessionResponse(BaseModel):
    data: dict[str, Any] = {
        "banner": str | None,
        "concession": List[ExtraDataConcessionResponse]
    } 