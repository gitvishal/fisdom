from django.shortcuts import render
from django.db import transaction
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from chartjs.views.lines import BaseLineChartView
from .models import MutualFund
from .mutual_funds import get_mutual_data
from .tasks import update_or_create_mfprice

class ISINCreate(CreateView):
    model = MutualFund
    fields = ['isin']

    def form_valid(self, form):
    	data = get_mutual_data(form.cleaned_data['isin'])
    	if data['pfwresponse']['status_code'] == 200:
    		self.object = form.save()
    		update_or_create_mfprice.s(self.object, mutual_data=data)
    	return self.render_to_response(self.get_context_data(form=form, isin_data=data['pfwresponse'])) 


class LineChartJSONView(BaseLineChartView):
	def get(self, *args, **kwargs):
		pk = kwargs.pop('pk')
		self.object = MutualFund.objects.get(pk=pk)
		return super().get(*args, **kwargs)

	def get_labels(self):
		return self.object.mutualfundprice_mf.values_list('date', flat=True)

	def get_providers(self):
		return [str(self.object,)]

	def get_data(self):
	    return [self.object.mutualfundprice_mf.values_list('price', flat=True),]

class LineChartView(DetailView):
	template_name = 'mf/graph.html'
	model = MutualFund


line_chart = LineChartView.as_view()
line_chart_json = LineChartJSONView.as_view()
