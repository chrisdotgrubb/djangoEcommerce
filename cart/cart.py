class Cart:
	"""
	A base Cart class, providing some default behaviors
	that can be inherited or overridden as necessary.
	"""
	
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get('skey')
		if 'skey' not in self.session:
			cart = self.session['skey'] = {}
		self.cart = cart
	
	def add(self, product):
		product_id = product.id
		
		if product_id not in self.cart:
			self.cart[product_id] = {'price': float(product.price)}
			
		self.session.modified = True
			
			
			