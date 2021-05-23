"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_username

from py4web.utils.form import Form, FormStyleBulma
from .common import Field

url_signer = URLSigner(session)

# SERVING PAGES ----------------------------------------------------------

@action('index')
@action.uses(url_signer, auth, 'home.html')
def index():
    if get_user_email() is None:
        redirect(URL('auth/login'))
    if get_username() is None:
        redirect(URL('signup'))
    return dict(
        username=get_username(),
    )

@action('signup')
@action.uses(db, auth, 'signup.html')
def signup():
    return dict()

# API FUNCTIONS ----------------------------------------------------------

# USER AUTH

@action('add_user')
@action.uses(url_signer.verify(), db, auth)
def add_user():
    # called when user signs up
    # add the username to user_profiles
    return dict()

# LOCATION

# @action('add_location', method=["GET", "POST"])
# @action.uses(db, session, auth.user, 'add_location.html')
# def add():
#     form = Form(db.location, csrf_session=session, formstyle=FormStyleBulma)
#     if form.accepted:
#         redirect(URL('index'))
#     return dict(form=form)


# @action('edit/<location_id:int>', method=["GET", "POST"])
# @action.uses(db, session, auth.user, url_signer.verify(), 'edit.html')
# def edit(location_id=None):
#     assert location_id is not None
#     p = db.location[location_id]
#     if p is None:
#         redirect(URL('index'))
#     form = Form(db.location, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
#     if form.accepted:
#         redirect(URL('index'))
#     return dict(form=form)

# REVIEWS

# @action('add_review/<location_title:int>', method=["GET", "POST"])
# @action.uses(db, session, auth.user, 'add_review.html')
# def add_review(title=None):
#     assert title is not None
#     name = db.location[title]
#     data = db(db.Location.title == title)
#     assert data is not None
#     form = Form([Field('Noise Rating'), Field('People Rating'), Field('Atmosphere Rating'),
#     Field('Cry Rating'), Field('Comments'),],
#                 csrf_session=session,
#                 formstyle=FormStyleBulma                
#                 )
#     if form.accepted:
#         db.weep_reviews.insert(
#             title = title,
#             review_id = db.user_profiles.user_id,
#             noise_rating = form.vars['Noise Rating'],
#             people_rating = form.vars['People Rating'],
#             atmosphere_rating = form.vars['Atmosphere Rating'],
#             cry_rating = form.vars['Cry Rating'],
#             additional_comments = form.vars['Comments'],
#         )
#         redirect(URL('index'))
#     return dict(form=form, name=name)


# @action('edit_review/<location_title:int>/<review_id:int>', method=["GET", "POST"])
# @action.uses(db, session, auth.user, url_signer.verify(), 'edit_review.html')
# def edit_review(location_title=None, review_id=None, title=None):
#     assert location_title is not None
#     assert review_id is not None
#     assert title is not None
#     p = db(
#         (db.review.id == review_id) &
#         (db.location.title == location_title) &
#         (db.weep_review.review_id == db.user_profiles.user_id)
#         ).select().first()
#     if p is None:
#         redirect(URL('index'))
#     name = db.location[title]
#     form = Form([Field('Noise Rating'), Field('People Rating'), Field('Atmosphere Rating'),
#     Field('Cry Rating'), Field('Comments'),],
#             record=dict(noise=p.weep_reviews.noise_rating, people=p.weep_reviews.people_rating,
#             atmosphere=p.weep_reviews.atmosphere_rating, cry=p.weep_reviews.cry_rating,
#             acomments=p.weep_reviews.additional_comments,), 
#             deletable=False, 
#             csrf_session=session, 
#             formstyle=FormStyleBulma)
#     if form.accepted:
#         p.weep_reviews.update_record(
#         noise_rating = form.vars['Noise Rating'], 
#         people_rating = form.vars['People Rating'],
#         atmosphere_rating = form.vars['Atmosphere Rating'], 
#         cry_rating = form.vars['Cry Rating'],
#         additional_comments = form.vars['Comments'],)
#         redirect(URL('index'))
#     return dict(form=form, name=name)

# @action('delete_review/<location_title:int>/<review_id:int>', method=["GET", "POST"])
# @action.uses(db, session, auth.user, url_signer.verify())
# def edit_phone(title=None, review_id=None):
#     assert title is not None
#     assert review_id is not None
#     p = db(
#         (db.review.id == review_id) &
#         (db.title.id == title) &
#         (db.weep_reviews.review_id == title)
#         ).select().first()
#     if p is None:
#         redirect(URL('index'))
#     p.weep_reviews.delete_record()
#     redirect(URL('index'))
