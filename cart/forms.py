from django import forms


class AddForm(forms.Form):
	choices = [
		('1', 1),
		('2', 2),
		('3', 3),
		('4', 4),
		('5', 5),
	]
	qty = forms.ChoiceField(choices=choices)


class QuantityForm(forms.Form):
	qty = forms.IntegerField()
	
	qty.widget.attrs.update({'min': 0, 'class': 'w-25'})
	