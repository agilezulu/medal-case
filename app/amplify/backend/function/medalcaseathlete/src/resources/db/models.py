from pony.orm import Database, Required, Optional, PrimaryKey, Set, LongUnicode
from datetime import datetime

db = Database()


class GetMixin:
    @classmethod
    def update_and_get_or_create(cls, params):
        o = cls.get(**params)
        if o:
            o.set(**params)
            return o
        return cls(**params)


class Athlete(db.Entity):
    _table_ = 'athlete'

    id = PrimaryKey(int, auto=True)
    uuid = Required(str, unique=True)
    strava_id = Required(int, size=64, sql_type='BIGINT', unique=True)
    slug = Required(str, unique=True)
    firstname = Optional(str)
    lastname = Optional(str)
    units = Optional(str)
    country = Optional(str)
    country_code = Optional(str)
    city = Optional(str)
    sex = Optional(str)
    date_fmt = Optional(str)
    photo_m = Optional(str)
    photo_l = Optional(str)
    access_token = Optional(str)
    refresh_token = Optional(str)
    expires_at = Optional(int)
    total_runs = Optional(int, sql_default=0)
    total_distance = Optional(int, sql_default=0)
    total_medals = Optional(int, sql_default=0)
    c_marathon = Optional(int, sql_default=0)
    c_marathon_race = Optional(int, sql_default=0)
    c_50k = Optional(int, sql_default=0)
    c_50k_race = Optional(int, sql_default=0)
    c_50mi = Optional(int, sql_default=0)
    c_50mi_race = Optional(int, sql_default=0)
    c_100k = Optional(int, sql_default=0)
    c_100k_race = Optional(int, sql_default=0)
    c_100k_plus = Optional(int, sql_default=0)
    c_100k_plus_race = Optional(int, sql_default=0)
    c_100mi = Optional(int, sql_default=0)
    c_100mi_race = Optional(int, sql_default=0)
    c_xtreme = Optional(int, sql_default=0)
    c_xtreme_race = Optional(int, sql_default=0)

    created_at = Optional(datetime)
    last_run_date = Optional(datetime)
    processing = Optional(int, sql_default=0)
    runs = Set('Run')


class Run(db.Entity):
    _table_ = 'run'
    strava_id = PrimaryKey(int, size=64, sql_type='BIGINT')
    name = Required(LongUnicode)
    distance = Required(float)
    moving_time = Required(int)
    elapsed_time = Required(int)
    total_elevation_gain = Required(float)
    start_date = Required(datetime, optimistic=False)
    start_date_local = Required(datetime)
    utc_offset = Required(float)
    timezone = Required(str)
    start_latlng = Optional(str)
    location_country = Required(str)
    location_city = Required(str)
    average_heartrate = Optional(float)
    average_cadence = Optional(float)
    race = Required(int)

    athlete = Required('Athlete', cascade_delete=False, column='user_id')
    run_class = Required('RunClass', cascade_delete=False, column='run_class_id')


class RunClass(db.Entity):
    _table_ = 'run_class'
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    key = Required(str)
    min = Required(int)
    max = Required(int)
    parent = Required(str)
    run = Set('Run')
