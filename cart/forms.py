from django import forms


class QuantityForm(forms.Form):
	choices = [
		('1', 1),
		('2', 2),
		('3', 3),
		('4', 4),
		('5', 5),
	]
	qty = forms.ChoiceField(choices=choices)
