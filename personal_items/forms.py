from django.forms import ModelForm, HiddenInput, TextInput

from personal_items.models import PersonalThing


class PersonalThingForm(ModelForm):

    class Meta:
        model = PersonalThing
        fields = (
            'category',
            'nomenclature',
            'unit',
            'quantity',
            'cost',
        )
        widgets = {
            'nomenclature': HiddenInput(),
            'quantity': TextInput(attrs={
                'class': 'input input_quantity',
                'placeholder': 'количество',
            }),
            'cost': TextInput(attrs={
                'class': 'input input_cost',
                'placeholder': 'стоимость',
            }),
        }
