# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request, make_response, jsonify
from common.libs.Helper import ops_render,iPagination
from flask import Blueprint
import time
import json
import datetime
from application import app
from sqlalchemy import distinct
from application import app, db
from common.libs.Helper import ops_render
import csv

import json
import urllib.request



route_index = Blueprint('index_page', __name__)



@route_index.route("/", methods=["GET", "POST"])
def index():
    return ops_render('index/index.html')
