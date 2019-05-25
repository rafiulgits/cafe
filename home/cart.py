from home.models import BranchFood

CART_SEESION_ID = 'user_cart_session'
BRANCH_SESSION_ID = 'cart_branch'

class Cart:

	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(CART_SEESION_ID, None)
		branch_id = self.session.get(BRANCH_SESSION_ID, None)
		if not cart:
			cart = self.session[CART_SEESION_ID] = {}
		self.cart = cart
		self.branch_id = branch_id

	def add(self, branch_food_id):
		branch_food_id = str(branch_food_id)
		if branch_food_id not in self.cart:
			self.cart[branch_food_id] = 1
		else:
			self.cart[branch_food_id] +=1
		self.save()

	def remove(self, branch_food_id):
		if branch_food_id in self.cart:
			if self.cart[branch_food_id] == 1:
				del self.cart[branch_food_id]
			else:
				self.cart[branch_food_id] -= 1
			self.save()
		
	def set_branch_id(self, branch_id):
		self.branch_id = branch_id
		self.session[BRANCH_SESSION_ID] = self.branch_id
		self.session.modified = True

	def get_branch_id(self):
		try:
			return self.branch_id
		except Exception as e:
			return None

	def get_items(self):
		item_list = []
		total = 0
		branch_food = None

		for item_id in self.cart:
			branch_food = BranchFood.objects.get(id=item_id)
			sub_total = self.cart[item_id]*branch_food.food.price
			total += sub_total
			item_list.append(
				CartItem(
					branch_food=branch_food, 
					quantity=self.cart[item_id], 
					sub_total=sub_total		
				))
		return item_list, total

	def save(self):
		self.session[CART_SEESION_ID] = self.cart
		self.session.modified = True

	def clear(self):
		del self.session[BRANCH_SESSION_ID]
		del self.session[CART_SEESION_ID]
		self.session.modified = True


class CartItem:
	def __init__(self, branch_food, quantity, sub_total):
		self.branch_food = branch_food
		self.quantity = quantity
		self.sub_total = sub_total