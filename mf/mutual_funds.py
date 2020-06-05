from django.db import transaction
from django.utils import timezone
from .models import MutualFundPrice
import requests

def get_mutual_data(isin):
	try:
		return requests.get(f'https://my.fisdom.com/api/funds/moreinfoonfund/{isin}').json()
	except Exception as e:
		return {'pfwresponse':{'status_code': 404, "result": {"error": str(e)}}}

def mutual_funds_price_update(mf, mutual_data=None):
	try:
		with transaction.atomic():
			data = mutual_data or get_mutual_data(mf.isin)
			if data['pfwresponse']['status_code'] == 200:
				graph_data_for_amfi = data['pfwresponse']['result']['fundinfo']['graph_data_for_amfi']
				name = data['pfwresponse']['result']['fundinfo']['legal_name']
				mf.name = name
				mf.save(update_fields=['name'])
				for epoch, price in graph_data_for_amfi:
					date = timezone.datetime.fromtimestamp(epoch/10)
					MutualFundPrice.objects.update_or_create(date=date, mutual_fund=mf, defaults={'price':price})
	except Exception as e:
		print(e)