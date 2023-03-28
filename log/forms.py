from django import forms
from django.forms import *
from equipamentos.models import *
from django.forms import modelform_factory
from django.forms import BaseModelFormSet

from cadastro_equipamentos.settings import TIME_ZONE
import datetime
import pytz


