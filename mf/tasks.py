# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.schedules import crontab
from celery.decorators import periodic_task
from celery import group
from .models import MutualFund, MutualFundPrice
from .mutual_funds import mutual_funds_price_update
from django.utils import timezone
import requests
import tablib

@shared_task
def get_or_create_mf(isin):
	return MutualFund.objects.get_or_create(isin=isin)

@shared_task
def update_or_create_mfprice(mf, mutual_data=None):
	try:
		mutual_funds_price_update(mf, mutual_data=None)
	except Exception as e:
		pass

@shared_task
def mf():
	csv = requests.get('https://amberja.in/wp-content/uploads/2020/01/isin_list.csv').text
	isins = tablib.Dataset().load(csv, format='csv', headers=False).get_col(0)
	group(get_or_create_mf.s(isin) for isin in isins)()
	return MutualFund.objects.all()

@shared_task
def mutual_price_all(mutual_fund):
	return group(update_or_create_mfprice.s(mf) for mf in mutual_fund.iterator())()

@periodic_task(run_every=crontab())
def schedule_task():
	return (mf.s() | mutual_price_all.s())()

# (mf.s() | group(update_or_create_mfprice.s(mf) for mf in MutualFund.objects.iterator()))()
