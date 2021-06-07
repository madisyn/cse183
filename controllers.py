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

import datetime
import json
import os
import traceback
import uuid

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_username, get_user, get_time

from nqgcs import NQGCS
from .settings import APP_FOLDER
from .gcs_url import gcs_url

url_signer = URLSigner(session)

BUCKET = '/weep-project'
# GCS keys.  You have to create them for this to work.  See README.md
GCS_KEY_PATH = os.path.join(APP_FOLDER, 'private/gcs_keys.json')
with open(GCS_KEY_PATH) as gcs_key_f:
    GCS_KEYS = json.load(gcs_key_f)

# I create a handle to gcs, to perform the various operations.
gcs = NQGCS(json_key_path=GCS_KEY_PATH)

# SERVING PAGES ----------------------------------------------------------

@action('index')
@action.uses(url_signer, auth, 'home.html')
def index():
    if get_user_email() is None:
        redirect(URL('auth/login'))
    if get_username() is None:
        redirect(URL('signup'))
    return dict(
        signer=url_signer,
        get_email_url = URL('get_email', signer=url_signer),
        add_location_url = URL('add_location', signer=url_signer),
        get_locations_url = URL('get_locations', signer=url_signer),
        delete_location_url = URL('delete_location', signer=url_signer),
        location_url = URL('location'),
        add_username_url = URL('add_username', signer=url_signer),
        add_review_url = URL('add_review', signer=url_signer),
        file_upload_url = URL('file_upload', signer=url_signer),
        obtain_gcs_url = URL('obtain_gcs', signer=url_signer),
        notify_upload_url = URL('notify_upload', signer=url_signer),
        notify_delete_url = URL('notify_delete', signer=url_signer),
    )

@action('signup')
@action.uses(db, auth, 'signup.html')
def signup():
    return dict(
        index_url = URL('index'),
        add_username_url = URL('add_username', signer=url_signer),
    )

@action('location/<loc_id:int>')
@action.uses(url_signer, db, auth, 'location.html')
def location(loc_id=None):
    assert loc_id is not None
    return dict(
        loc_id=loc_id,
        get_email_url = URL('get_email', signer=url_signer),
        get_location_url = URL('get_location', signer=url_signer),
        get_reviews_url =URL('get_reviews', signer=url_signer),
        add_review_url = URL('add_review', signer=url_signer),
        delete_review_url = URL('delete_review', signer=url_signer),
        get_user_helpful_url = URL('get_user_helpful', signer=url_signer),
        add_helpful_url = URL('add_helpful', signer=url_signer),
        delete_helpful_url = URL('delete_helpful', signer=url_signer),
    )

# API FUNCTIONS ----------------------------------------------------------

# USER AUTH

@action('add_username', method="POST")
@action.uses(url_signer.verify(), db, auth)
def add_username():
    user = get_user()
    id = db.user_profiles.insert(
        user = user,
        username=request.json.get('username'),
    )
    return dict(id=id, username=request.json.get('username'))

@action('get_email')
@action.uses(url_signer.verify(), db, auth)
def get_email():
    return dict(email=get_user_email())

# IMAGES

@action('obtain_gcs', method="POST")
@action.uses(url_signer.verify(), db)
def obtain_gcs():
    # Returns the URL to do download / upload / delete for GCS.
    verb = request.json.get("action")
    if verb == "PUT":
        mimetype = request.json.get("mimetype", "")
        file_name = request.json.get("file_name")
        location = request.json.get("location")
        extension = os.path.splitext(file_name)[1]
        # Use + and not join for Windows, thanks Blayke Larue
        file_path = BUCKET + "/" + str(uuid.uuid1()) + extension
        # marks that the path may be used to upload a file.
        mark_possible_upload(file_path, location)
        upload_url = gcs_url(GCS_KEYS, file_path, verb='PUT',
                             content_type=mimetype)
        return dict(
            signed_url=upload_url,
            file_path=file_path
        )
    elif verb in ["GET", "DELETE"]:
        file_path = request.json.get("file_path")
        location = request.json.get("location")
        if file_path is not None:
            # check file_path
            r = db(db.image.file_path == file_path).select().first()
            if r is not None and r.location == location:
                # let deletion happening
                delete_url = gcs_url(GCS_KEYS, file_path, verb='DELETE')
                return dict(signed_url=delete_url)
        # return no url (deletion not authorized)
        return dict(signer_url=None)

@action('notify_upload', method="POST")
@action.uses(url_signer.verify(), db)
def notify_upload():
    # file has been uploaded
    file_path = request.json.get("file_path")
    location = request.json.get("location")
    print("File was uploaded:", file_path, file_name, file_type)
    # confirms update
    d = datetime.datetime.utcnow()
    db.image.update_or_insert(
        (db.image.location == location),
        location=location,
        file_path=file_path,
        confirmed=True,
    )
    # returns the file information.
    return dict(
        download_url=gcs_url(GCS_KEYS, file_path, verb='GET'),
    )

@action('notify_delete', method="POST")
@action.uses(url_signer.verify(), db)
def notify_delete():
    file_path = request.json.get("file_path")
    location = request.json.get("location")
    # prevent DDOS
    db((db.image.location == location) &
       (db.image.file_path == file_path)).delete()
    return dict()

def mark_possible_upload(file_path, location):
    # file might be uploaded
    delete_previous_uploads()
    db.upload.insert(
        location=location,
        file_path=file_path,
        confirmed=False,
    )

# LOCATION

@action('get_locations', method="GET")
@action.uses(url_signer.verify(), db, auth)
def get_locations():
    posts = db(db.location).select().as_list()
    return dict(posts=posts)

@action('get_location', method="GET")
@action.uses(url_signer.verify(), db, auth)
def get_location():
    loc_id = request.params.get("loc_id")
    location = db(db.location.id == loc_id).select().as_list()[0]
    return dict(location=location)

@action('add_location', method="POST")
@action.uses(url_signer.verify(), db, auth)
def add_location():
    # TODO: adding an author to posts isn't working (foreign key bug)
    id = db.location.insert(
        name=request.json.get('name'),
        description=request.json.get('description'),
        email=get_user_email(),
    )
    return dict(id=id)

@action('delete_location')
@action.uses(url_signer.verify(), db, auth)
def delete_location():
    id = request.params.get('id')
    assert id is not None
    db(db.location.id == id).delete()
    return "ok"

def update_reviews(loc_id):
    reviews = db(db.review.location == loc_id).select().as_list()
    num_reviews = len(reviews)

    if num_reviews == 0:
        updated = dict(
            review_count=0,
            avg_rating=0,
            avg_noise=0,
            avg_people=0,
            avg_atmosphere=0,
            avg_cry=0,
            tags=[],
        )
    else:
        # get average reviews
        avg_noise = sum(review['noise_rating'] for review in reviews) / num_reviews
        avg_people = sum(review['people_rating'] for review in reviews) / num_reviews
        avg_atmosphere = sum(review['atmosphere_rating'] for review in reviews) / num_reviews
        avg_cry = sum(review['cry_rating'] for review in reviews) / num_reviews
        avg_rating = (avg_atmosphere + avg_cry) / 2

        tags = []
        # generate noise tags
        if (avg_noise < 2):
            tags.append("peaceful")
        elif (avg_noise < 4):
            tags.append("mild noise")
        else:
            tags.append("vibrant")
        # generate people tags
        if (avg_people < 2):
            tags.append("uncrowded")
        elif(avg_people < 4):
            tags.append("somewhat crowded")
        else:
            tags.append("crowded")

        updated = dict(
            review_count=num_reviews,
            avg_rating=round(avg_rating),
            avg_noise=round(avg_noise),
            avg_people=round(avg_people),
            avg_atmosphere=round(avg_atmosphere),
            avg_cry=round(avg_cry),
            tags=tags,
        )
    
    # update
    db.location[loc_id] = updated
    return updated

# REVIEWS

@action('get_reviews', method="GET")
@action.uses(url_signer.verify(), db, auth)
def get_reviews():
    loc_id = request.params.get("loc_id")
    reviews = db(db.review.location == loc_id).select().as_list()
    return dict(reviews=reviews)

@action('add_review', method="POST")
@action.uses(url_signer.verify(), db, auth)
def add_review():
    username = get_username()
    user = get_user()
    date = get_time()
    id = db.review.insert(
        location=request.json.get('location'),
        cry_rating=request.json.get('cry'),
        atmosphere_rating=request.json.get('atmosphere'),
        noise_rating=request.json.get('noise'),
        people_rating=request.json.get('people'),
        comment=request.json.get('comment'),
        date_posted=date,
        username=username,
        user=user,
    )
    updated = update_reviews(request.json.get('location'))
    return dict(id=id, date_posted=date, username=username, updated=updated)

@action('delete_review')
@action.uses(url_signer.verify(), db, auth)
def delete_review():
    id = request.params.get('id')
    assert id is not None
    db(db.review.id == id).delete()
    updated = update_reviews(request.params.get('location'))
    return dict(updated=updated)

# IMAGES

@action('file_upload', method="POST")
@action.uses(url_signer.verify(), db)
def file_upload():
    uploaded_file = request.body # This is a file, you can read it.
    print(request.body)
    # Diagnostics
    return dict(image=uploaded_file)

# HELPFUL

@action('get_user_helpful')
@action.uses(url_signer.verify(), db, auth)
def get_user_helpful():
    rows = db(db.helpful.user == get_user()).select().as_list()
    return dict(helpful=rows)

@action('add_helpful', method="POST")
@action.uses(url_signer.verify(), db, auth)
def add_helpful():
    review_id = request.json.get('id')
    user = get_user()
    email = get_user_email()
    id = db.helpful.insert(
        review=review_id,
        email=email,
        user=user,
    )
    new_count = db.review[review_id].helpful_count + 1
    db.review[review_id] = dict(
        helpful_count=new_count,
    )
    return dict(count=new_count)

@action('delete_helpful')
@action.uses(url_signer.verify(), db, auth)
def delete_helpful():
    review_id = request.params.get('id')
    email = request.params.get('email')
    assert review_id is not None
    db((db.helpful.review == review_id) & (db.helpful.email == email)).delete()
    new_count = db.review[review_id].helpful_count - 1
    db.review[review_id] = dict(
        helpful_count=new_count,
    )
    return dict(count=new_count)