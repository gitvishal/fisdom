from django.db import models

class MutualFund(models.Model):
	isin = models.CharField('ISIN', max_length=15, primary_key=True)
	name = models.CharField('Mutual Fund name', max_length=100, blank=True, null=True)

	def __str__(self):
		return f'{self.name}({self.isin})'

class MutualFundPrice(models.Model):
	date = models.DateTimeField()
	price = models.DecimalField(max_digits=15, decimal_places=2)
	mutual_fund = models.ForeignKey(MutualFund, related_name='%(class)s_mf', on_delete=models.PROTECT)

	class Meta:
		unique_together = ('price', 'date', 'mutual_fund')
		ordering = ('date',)
			

	def __str__(self):
		return f'{self.price}-{self.date}-{self.mutual_fund.isin}'

