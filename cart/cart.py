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
		
		self.session.modified = True
			
			
			