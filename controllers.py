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
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma
from .common import Field
url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth, 'index.html')
def index():
    if get_user_email() is None:
        redirect(URL('auth/login'))
        return dict()

@action('add_location', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add_location.html')
def add():
    form = Form(db.location, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)


@action('edit/<location_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify(), 'edit.html')
def edit(location_id=None):
    assert location_id is not None
    p = db.location[location_id]
    if p is None:
        redirect(URL('index'))
    form = Form(db.location, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('add_review/<location_Title:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add_review.html')
def add_review(Title=None):
    assert Title is not None
    name = db.location[Title]
    data = db(db.Location.Title == Title)
    assert data is not None
    form = Form([Field('Noise Rating'), Field('People Rating'), Field('Atmosphere Rating'),
    Field('Cry Rating'), Field('Comments'), Field('Images'),],
                csrf_session=session,
                formstyle=FormStyleBulma                
                )
    if form.accepted:
        db.weep_reviews.insert(
            Title = Title,
            review_id = db.user_profiles.user_id,
            noise_rating = form.vars['Noise Rating'],
            people_rating = form.vars['People Rating'],
            atmosphere_rating = form.vars['Atmosphere Rating'],
            cry_rating = form.vars['phone'],
            additional_comments = form.vars['Comments'],
            images = form.vars['Images']
        )
        redirect(URL('index'))
    return dict(form=form, name=name)


@action('edit_review/<location_Title:int>/<review_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify(), 'edit_review.html')
def edit_review(location_Title=None, review_id=None, Title=None):
    assert location_Title is not None
    assert review_id is not None
    assert Title is not None
    p = db(
        (db.review.id == review_id) &
        (db.location.Title == location_Title) &
        (db.weep_review.review_id == db.user_profiles.user_id)
        ).select().first()
    if p is None:
        redirect(URL('index'))
    name = db.location[Title]
    form = Form([Field('Noise Rating'), Field('People Rating'), Field('Atmosphere Rating'),
    Field('Cry Rating'), Field('Comments'), Field('Images'),],
            record=dict(noise=p.weep_reviews.noise_rating, people=p.weep_reviews.people_rating,
            atmosphere=p.weep_reviews.atmosphere_rating, cry=p.weep_reviews.cry_rating,
            acomments=p.weep_reviews.additional_comments, image=p.weep_reviews.images), 
            deletable=False, 
            csrf_session=session, 
            formstyle=FormStyleBulma)
    if form.accepted:
        p.weep_reviews.update_record(noise_rating = form.vars['Noise Rating'], people_rating = form.vars['People Rating'],
        atmosphere_rating = form.vars['Atmosphere Rating'], cry_rating = form.vars['Cry Rating'],
        additional_comments = form.vars['Comments'], images = form.vars['Images'],)
        redirect(URL('index'))
    return dict(form=form, name=name)

@action('delete_review/<location_Title:int>/<review_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify())
def edit_phone(Title=None, review_id=None):
    assert Title is not None
    assert review_id is not None
    p = db(
        (db.review.id == review_id) &
        (db.Title.id == Title) &
        (db.weep_reviews.review_id == Title)
        ).select().first()
    if p is None:
        redirect(URL('index'))
    p.weep_reviews.delete_record()
    redirect(URL('index'))


@action('back')
@action.uses(db, session)
def back():
    redirect(URL('index'))