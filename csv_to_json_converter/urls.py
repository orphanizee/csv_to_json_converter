from django.contrib import admin
from django.urls import path
from csvtojson.views import csv_to_json

urlpatterns = [
    path('csv-to-json/', csv_to_json, name='csv_to_json'),
]
