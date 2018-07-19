# coding:utf-8
from flask import Blueprint

work = Blueprint('work', __name__)

from app.work import views
