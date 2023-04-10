from decimal import Decimal
from pony.orm import Database, Required, Optional, PrimaryKey, Set
from datetime import datetime

db = Database()


class Athlete(db.Entity):
    _table_ = 'athlete'

    id = PrimaryKey(int, auto=True)
    uuid = Required(str, unique=True)
    strava_id = Required(int, unique=True)
    slug = Required(str, unique=True)
    firstname = Optional(str)
    lastname = Optional(str)
    units = Optional(str)
    country = Optional(str)
    city = Optional(str)
    sex = Optional(str)
    date_fmt = Optional(str)
    photo_m = Optional(str)
    photo_l = Optional(str)
    access_token = Optional(str)
    refresh_token = Optional(str)
    expires_at = Optional(int)
    total_runs = Optional(int)
    c_marathon = Optional(int)
    c_marathon_race = Optional(int)
    c_50k = Optional(int)
    c_50k_race = Optional(int)
    c_50mi = Optional(int)
    c_50mi_race = Optional(int)
    c_100k = Optional(int)
    c_100k_race = Optional(int)
    c_100mi = Optional(int)
    c_100mi_race = Optional(int)
    c_extreme = Optional(int)
    c_extreme_race = Optional(int)

    created_at = Optional(datetime)
    last_run_date = Optional(datetime)
    runs = Set('Run')


class Run(db.Entity):
    _table_ = 'run'

    id = PrimaryKey(int, auto=True)
    user_id = Required(int)
    strava_id = Required(int, unique=True)
    name = Required(str)
    distance = Required(Decimal)
    moving_time = Required(int)
    elapsed_time = Required(int)
    total_elevation_gain = Required(Decimal)
    start_date = Required(datetime)
    start_date_local = Required(datetime)
    utc_offset = Required(Decimal)
    timezone = Required(str)
    location_country = Required(str)
    average_heartrate = Optional(Decimal)
    average_cadence = Optional(Decimal)
    race = Required(int)
    summary_polyline = Optional(str)

    athlete = Required('Athlete')
