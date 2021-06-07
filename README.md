# Weep Implementation

## Overview

- [Client](#client)
- [Server](#server)
- [Database](#database-tables)
- [Known Issues](#known-issues)

## Client

#### Index

#### Signup

#### Home

#### Location

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
  - full documentation of the necessary implementation and attempted code is in the feature/image_upload branch
- the google sign-in page does not automatically redirect to the home page