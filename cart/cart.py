import logging
from decimal import Decimal

from store.models import Product


class Cart:
	"""
	A base Cart class, providing some default behaviors
	that can be inherited or overridden as necessary.
	"""
	
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('cart')
		if not cart:
			self.session.save()
			cart = self.session['cart'] = {}
		self.cart = cart
	
	def __len__(self):
		return sum(item['qty'] for item in self.cart.values())
	
	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()
		
		for product in products:
			cart[str(product.id)]['price'] = product.regular_price
		
		for item in cart.values():
			item['price'] = f"{Decimal(item['price']):.2f}"
			item['total_price'] = F"{Decimal(item['price']) * item['qty']:2f}"
			yield item
	
	def add(self, product_id, product_qty):
		pid = str(product_id)
		obj = Product.objects.get(id=pid)
		pqt = int(product_qty)
		if pid not in self.cart:
			self.cart[pid] = {'name': obj.slug, 'qty': pqt}
		else:
			qty = int(self.cart[pid].get('qty'))
			qty += pqt
			self.cart[pid]['qty'] = qty
		
		self.save()
	
	def delete(self, product_id):
		pid = str(product_id)
		
		if pid in self.cart:
			del self.cart[pid]
			self.save()
			
	def set_quantity(self, product_id, product_qty):
		pid = str(product_id)
		obj = Product.objects.get(id=pid)
		pqt = int(product_qty)
		if pqt != 0:
			self.cart[pid]['qty'] = pqt
			self.save()
		else:
			self.delete(product_id)
	
	def save(self):
		self.session.modified = True
		
	def get_subtotal_price(self):
		return f"{sum(Decimal(item['price']) * item['qty'] for item in self.__iter__()):.2f}"
	
	def get_tax_price(self):
		return f"{round(Decimal(self.get_subtotal_price()) * Decimal(0.06), 2):.2f}"
	
	def get_subtotal_plus_tax_price(self):
		return f"{round(Decimal(self.get_subtotal_price()) + Decimal(self.get_tax_price()), 2):.2f}"
	
	def get_grand_total(self, delivery_price=0):
		return f"{Decimal(self.get_subtotal_price()) + Decimal(self.get_tax_price()) + Decimal(delivery_price):.2f}"
	
	def clear(self):
		try:
			del self.session['cart']
		except KeyError:
			return
		self.save()
		
		