from ISP_warehouse.models import *
from django import forms


class SearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"myfield"}))


class InvFilterForm(forms.Form):
    loc_choices = [(loc.pk, loc.name) for loc in LocType.objects.all()]
    loc_choices.insert(0, (-1, "---"))
    cat_choices = [(cat.pk, cat.name) for cat in Category.objects.all()]
    cat_choices.insert(0, (-1, "---"))
    select_location = forms.ChoiceField(choices=loc_choices)
    select_category = forms.ChoiceField(choices=cat_choices)


class OperationsFilterForm(forms.Form):
    worker_type = LocType.objects.get(name="Співробітник")

    loc_choices = [(loc.pk, loc.name) for loc in Location.objects.all()]
    loc_choices.insert(0, (-1, "---"))
    select_location_from = forms.ChoiceField(choices=loc_choices)
    select_location_to = forms.ChoiceField(choices=loc_choices)
    types_choices = [(type.pk, type.name) for type in Type.objects.all()]
    types_choices.insert(0, (-1, "---"))
    select_type = forms.ChoiceField(choices=types_choices)
    num = forms.IntegerField(min_value=1, required=False)
    who_choices = [(loc.pk, loc.name) for loc in Location.objects.filter(loc_type=worker_type)]
    who_choices.insert(0, (-1, "---"))
    select_author = forms.ChoiceField(choices=who_choices)


class LocFilterForm(forms.Form):
    loc_choices = [(loc.pk, loc.name) for loc in LocType.objects.all()]
    loc_choices.insert(0, (-1, "---"))
    select_location = forms.ChoiceField(choices=loc_choices)


class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class AddInvForm(forms.Form):
    serial_num = forms.CharField()
    cost = forms.IntegerField()
    loc_choices = [(loc.pk, loc.name) for loc in Location.objects.all()]
    location = forms.ChoiceField(choices=loc_choices)
    comment = forms.CharField(required=False)
    sup_choices = [(sup.pk, sup.name) for sup in Supplier.objects.all()]
    supplier = forms.ChoiceField(choices=sup_choices)


class EditInvForm(forms.Form):
    type_choices = [(type.pk, type.name) for type in Type.objects.all()]
    type = forms.ChoiceField(choices=type_choices)
    serial_num = forms.CharField()
    cost = forms.IntegerField()
    loc_choices = [(loc.pk, loc.name) for loc in Location.objects.all()]
    location = forms.ChoiceField(choices=loc_choices)
    comment = forms.CharField(required=False)
    sup_choices = [(sup.pk, sup.name) for sup in Supplier.objects.all()]
    supplier = forms.ChoiceField(choices=sup_choices)


class AddTypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ('name',)


class AddSupForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'address', 'phone', 'director', 'email', 'web', 'notes')
    name = forms.CharField()
    address = forms.CharField()
    phone = forms.CharField()
    director = forms.CharField()
    email = forms.EmailField()
    web = forms.CharField()
    notes = forms.CharField()


class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ('notes',)

    worker_type = LocType.objects.get(name="Співробітник")

    loc_choices = [(loc.pk, loc.name) for loc in Location.objects.all()]
    from_place = forms.ChoiceField(choices=loc_choices)
    destination = forms.ChoiceField(choices=loc_choices)
    inventory_choices = [(inv.pk, ((inv.inv_type.name)+' - '+str(inv.serial_num))) for inv in Inventory.objects.all()]
    inventory = forms.ChoiceField(choices=inventory_choices)
    who_choices = [(loc.pk, loc.name) for loc in Location.objects.filter(loc_type=worker_type)]
    who_choices.insert(0, (-1, "---"))
    author = forms.ChoiceField(choices=who_choices)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=120,
                               widget=forms.PasswordInput)
