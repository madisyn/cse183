# Feature: Image Upload w/ GCS

We didn't have enough time to fully implement allowing users to upload images of their locations. This document details what we needed to do to get there.

### Database
- image
    - location
    - file_path (link to GCS)
    - confirmed

### Server
- upload_gcs (serves link to upload, takes in location, filename, and mimetype)
- get_gcs (serves links, takes in file_path and location)
- get_images (sends image rows)
- get_image (sends image of location_id)

### Client

##### index.js

- app.init
    - call get_images and stores file_path in post.image
- app.upload_image
    - called in add_post
    - calls upload_gcs
    - calls GCS to upload image
    - after successful upload, calls get_gcs
    - stores url in post.image
- app.delete_image
    - called in delete_post
    - calls get_gcs
    - calls GCS to delete image

##### location.js
- app.init
    - call get_image and store in app.vue.image
