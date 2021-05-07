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
    Field('Title', 'text'),
    Field('x_coordinate', 'integer'),
    Field('y_coordinate', 'integer'),
    Field('date_location_found', 'datetime'),
    Field('overall_rating', 'integer'),
)


db.define_table(
    'weep_reviews',
    Field('review_id', 'reference location_catalog', ondelete="CASCADE"),
    Field('noise_rating', 'integer'),
    Field('people_rating', 'integer'),
    Field('atmosphere_rating', 'integer'),
    Field('cry_rating', 'integer'),
    Field('additional_comments', 'text'),
    Field('images', Field('image', 'upload', default='path/to/file')), #******
    Field('helpful_count', 'integer'),
)

db.define_table(
    'student_reviews',
    Field('date_review_posted', 'reference user_profiles', 'reference weep_reviews', 'datetime', ondelete="CASCADE"),
    Field('number_of_reviews', 'integer'),
)

db.define_table(
    'user_profiles',
    Field('Name', 'text', ondelete = "CASCADE"),
    Field('Email', 'text', default=get_user_email),
    Field('user_id', 'text'),
)
db.user_profiles.Name.requires = IS_NOT_EMPTY()
db.user_profiles.Email.requires = IS_NOT_EMPTY()
db.user_profiles.user_id.requires = IS_NOT_EMPTY()
db.user_profiles.Name.readable = db.user_profiles.Name.writable = False
db.user_profiles.Email.readable = db.user_profiles.Email.writable = False
db.user_profiles.Email.readable = db.user_profiles.Email.writable = True


db.commit()
