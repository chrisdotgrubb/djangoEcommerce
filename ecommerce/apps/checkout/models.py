from django.db import models
from django.utils.translation import gettext_lazy as _

class DeliveryOptions(models.Model):
	DELIVERY_CHOICES = [('IS', 'In Store'), ('PA', 'Physical Address'), ('DD', 'Digital Delivery')]
	
	delivery_name = models.CharField(verbose_name=_('Delivery Name'), help_text=_('Required'), max_length=255)
	delivery_price = models.DecimalField(
		verbose_name=_('Delivery Price'),
		help_text=_('Maximum 999.99'),
		error_messages={'name': {'max_length':_('The price must be between 0 and 999.99')}},
		max_digits=5,
		decimal_places=2
	)
	delivery_method = models.CharField(
		choices=DELIVERY_CHOICES,
		verbose_name=_('Delivery Method'),
		help_text=_('Required'),
		max_length=255
	)
	delivery_timeframe = models.CharField(verbose_name=_('Delivery Timeframe'), help_text=_('Required'), max_length=255)
	delivery_window = models.CharField(verbose_name=_('Delivery Window'), help_text=_('Required'), max_length=255)
	order = models.IntegerField(verbose_name=_('List order'), help_text=_('Required'), default=0)
	is_active = models.BooleanField(default=True)
	
	class Meta:
		verbose_name = _('Delivery Option')
		verbose_name_plural = _('Delivery Options')
		
	def __str__(self):
		return self.delivery_name
		