"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_username():
    user = get_user()
    user_row = db(db.user_profiles.user == user).select().first()
    return user_row.username if user_row else None

def get_time():
    return datetime.datetime.utcnow()

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'user_profiles',
    Field('user', 'reference auth_user', default=get_user),
    Field('username', 'text'),
)

db.define_table(
    'location',
    Field('title', 'text'),
    #Field('location_decription', 'text'),
    Field('x_coordinate', 'integer'),
    Field('y_coordinate', 'integer'),
    Field('date_location_found', 'datetime'),
    Field('overall_rating', 'integer'),
)

db.define_table(
    'weep_reviews',
    Field('review_id', 'reference location', ondelete="CASCADE"),
    Field('noise_rating', 'integer'),
    Field('people_rating', 'integer'),
    Field('atmosphere_rating', 'integer'),
    Field('cry_rating', 'integer'),
    Field('additional_comments', 'text'),
    #Field('images', Field('image', 'upload', default='path/to/file')), Unit 18 storing files in google storage
    Field('helpful_count', 'integer'),
    Field('date_review_posted'),
)

#might keep
db.define_table(
    'student_reviews',
    Field('date_review_posted', 'reference user_profiles', 'reference weep_reviews', 'datetime', ondelete="CASCADE"),
    Field('number_of_reviews', 'integer'),
)

db.commit()
