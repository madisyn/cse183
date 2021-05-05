"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'location_catalog',
    Field('Title'),
    Field('x_coordinate'),
    Field('y_coordinate'),
    Field('date_location_found'),
    Field('overall_rating'),
)


db.define_table(
    'weep_reviews',
    Field('review_id', 'reference location_catalog', ondelete="CASCADE"),
    Field('noise_rating'),
    Field('people_rating'),
    Field('atmosphere_rating'),
    Field('cry_rating'),
    Field('additional_comments'),
    Field('images'),
    Field('helpful_count'),
)

db.define_table(
    'student_reviews',
    Field('date_review_posted', 'reference user_profiles', 'reference weep_reviews', ondelete="CASCADE"),
    Field('number_of_reviews'),

)

db.define_table(
    'user_profiles',
    Field('Name'),
    Field('Email'),
    Field('user_id'),
)


db.commit()
