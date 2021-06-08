# Weep
Created by: Colina Guan and Madisyn Maldonado

## Table of Contents

- [Client](#client)
- [Server](#server)
- [Database](#database-tables)
- [Known Issues](#known-issues)

## Client

#### Overview

The first page users see is the landing page. This details the goals and purpose of our website. From there, users can login through Google, create a username, and access the home page where all Weep locations are displayed. Users can then click on "See Reviews" on the bottom of a location, which will show them more detailed information about the location, and all the reviews that other users have posted.

#### Landing Page (Index)

This page shows Weep's landing page and has a button that redirects to the home page.

#### Signup

This page uses Vue.js (static/js/signup.js).

The user can input a username. If successful, it will redirect to the home page.

signup.js handles the form input and API call to the server to store the username.

#### Home

This page uses Vue.js (static/js/index.js).

The user can browse through existing posts, sort them by three filters (top, new, my posts), and create a new post. Users can also delete posts that were created by them. For each location, users can see the average rating of the location, the number of reviews, and the tags associated with the post.

index.js handles all the API calls to get locations, add locations, and delete locations. It also deals with the form input, resetting the form, and applying filters.

#### Location

This page uses Vue.js (static/js/location.js).

The user can browse through the info of a location, the reviews of a location, sort them by three filters (top, new, my posts), and create a new review. Users can also delete reviews that were created by them, and mark reviews as "helpful". The information about the location (average ratings and the number of reviews) should update automatically after the user posts a new review, or deletes a review.

location.js handles all the API calls to get the location information, get reviews, add reviews, delete reviews, mark a post as helpful, and unmark a post as helpful. It also deals with the add review form, input validation, and applying filters.

#### Layout

We made very minimal changes to the layout of the navbar and footer. The navbar will show a button to sign in if no user is detected. If a user is logged in, it will show their email and a sign out button.

## Server

Note: All API calls require signed urls.

#### Served Pages

- **index:** serves the landing page
- **home:** serves the home page (user must be logged into a Google account and have a username)
- **signup:** serves the signup page where users will enter a username
- **location/loc_id:** serves the location page

#### API: User Authentication

- **add_username:** adds entry to user_profiles database
- **get_email:** gets current user's email

#### API: Locations

- **get_locations:** returns a list of all locations
- **get_location:** returns information for requested location
- **add_location:** adds a location
- **delete_location:** deletes a location
  
#### API: Reviews

- **get_reviews:** gets reviews for requested location
- **add_review:** adds a review
- **delete_review:** deletes a review

#### API: Helpful

- **get_user_helpful:** gets all helpful entries belonging to a user
- **add_helpful:** adds helpful entry
- **delete_helpful:** removes helpful entry

#### Helper Functions

- **update_reviews:** updates the average ratings and tags in a location (called when reviews are added or deleted)
  - tags are based off of the average noise ratings (peaceful, mild noise, vibrant) and the average people ratings (uncrowded, somewhat crowded, crowded)
  - the average rating is based off of the average atmosphere and cry ratings

## Database Tables

#### user_profiles

This table stores users and their respective usernames. We are using the built-in auth_user database table for emails and passwords.

#### location

This table stores all data needed for a location:
- name
- description
- the date posted
- the number of reviews
- average rating (avg of atmosphere + cry)
- average noise
- average people
- average atmosphere
- average cry
- tags

It also references the user who posted the location.

#### review

This table stores reviews for a location:
- noise rating
- people rating
- atmosphere rating
- cry rating
- common
- number of people that marked the review as helpful
- the date posted

It references the reviewed location and the user who posted the review.

#### helpful

This table stores which users have marked which reviews as helpful. It references the review that was marked helpful and the user who marked it.

## Known Issues

- image upload is not fully implemented
  - full documentation of the necessary implementation and attempted code is in the feature/gcs branch
