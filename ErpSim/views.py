from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
import pandas as pd
from .models import MarketSalesData, GroupSalesData
import datetime

# Create your views here.


