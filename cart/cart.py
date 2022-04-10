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
		cart = self.session.get(self.session.session_key)
		if not cart:
			self.session.save()
			cart = self.session[self.session.session_key] = {}
		self.cart = cart
		self.shipping_cost = Decimal(9.99)
	
	def __len__(self):
		return sum(item['qty'] for item in self.cart.values())
	
	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()
		
		for product in products:
			cart[str(product.id)]['product'] = product
			cart[str(product.id)]['price'] = product.regular_price
		
		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['qty']
			yield item
	
	def as_dict(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()
		
		for product in products:
			cart[str(product.id)]['product'] = product
			cart[str(product.id)]['price'] = product.regular_price
		
		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['qty']
		
		return cart
	
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
		return sum(Decimal(item['price']) * item['qty'] for item in self.__iter__())
	
	def get_tax_price(self):
		return round(self.get_subtotal_price() * Decimal(0.06), 2)
	
	def get_shipping_price(self):
		return round(self.shipping_cost, 2)
	
	def get_total_price(self):
		subtotal = self.get_subtotal_price() + self.get_tax_price()
		
		if subtotal == 0:
			shipping = Decimal(0.00)
		else:
			shipping = self.shipping_cost
		
		total = subtotal + Decimal(shipping)
		return round(total, 2)
	
	def clear(self):
		try:
			del self.session[self.session.session_key]
		except KeyError:
			return
		self.save()
		
		