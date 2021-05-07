"""
This file defines cache, session, and translator T object for the app
These are fixtures that every app needs so probably you will not be editing this file
"""
import copy
import os
import sys
import logging
from py4web import Session, Cache, Translator, Flash, DAL, Field, action
from py4web.utils.mailer import Mailer
from py4web.utils.auth import Auth
from py4web.utils.downloader import downloader
from py4web.utils.tags import Tags
from py4web.utils.factories import ActionFactory
from py4web.utils.form import FormStyleBulma
from . import settings