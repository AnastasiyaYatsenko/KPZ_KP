import csv
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView
from ISP_warehouse.models import *
from ISP_warehouse.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


class InventoryListView(LoginRequiredMixin, DetailView):
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = {'inventory_list': Inventory.objects.all().order_by('inv_type__category__name', 'inv_type__name',
                                                                      'serial_num')}
        return context

    def get(self, request, **kwargs):
        search_form = SearchForm(request.POST)
        filter_form = InvFilterForm(request.POST)
        context = self.get_context_data(**kwargs)
        context['search_form'] = search_form
        context['filter_form'] = filter_form
        return render(request, 'inventory.html', context=context)

    def post(self, request, **kwargs):
        search_form = SearchForm(request.POST)
        filter_form = InvFilterForm(request.POST)
        if "type_submit" in request.POST:
            name = request.POST['name']
            type_pk = Type.objects.get(name=name)
            inv_list = Inventory.objects.filter(inv_type=type_pk).order_by('inv_type__category__name', 'inv_type__name',
                                                                           'serial_num')
            context = {'inventory_list': inv_list, 'search_form': search_form, 'filter_form': filter_form}
            return render(request, 'inventory.html', context=context)
        if "filter_submit" in request.POST:
            loctype_id = int(request.POST['select_location'])
            category_id = int(request.POST['select_category'])
            print(loctype_id)
            print(category_id)
            if loctype_id == -1 and category_id != -1:
                types = Type.objects.filter(category=category_id)
                inv_list = Inventory.objects.filter(inv_type__in=types).order_by('inv_type__category__name',
                                                                               'inv_type__name', 'serial_num')
                context = {'inventory_list': inv_list, 'search_form': search_form, 'filter_form': filter_form}
                return render(request, 'inventory.html', context=context)
            if loctype_id != -1 and category_id == -1:
                locations = Location.objects.filter(loc_type=loctype_id)
                inv_list = Inventory.objects.filter(location__in=locations).order_by('inv_type__category__name',
                                                                                 'inv_type__name', 'serial_num')
                context = {'inventory_list': inv_list,
                           'search_form': search_form, 'filter_form': filter_form}
                return render(request, 'inventory.html', context=context)
            if loctype_id != -1 and category_id != -1:
                locations = Location.objects.filter(loc_type=loctype_id)
                types = Type.objects.filter(category=category_id)
                inv_list = Inventory.objects.filter(location__in=locations,
                                                    inv_type__in=types).order_by('inv_type__category__name',
                                                                                 'inv_type__name', 'serial_num')
                context = {'inventory_list': inv_list,
                           'search_form': search_form, 'filter_form': filter_form}
                return render(request, 'inventory.html', context=context)
        context = self.get_context_data(**kwargs)
        context['search_form'] = search_form
        context['filter_form'] = filter_form
        return render(request, 'inventory.html', context=context)


class InventoryView(LoginRequiredMixin, DetailView):
    login_url = '/login'

    def get_context_data(self, **kwargs):
        inv_id = self.kwargs['inv_id']
        inv = Inventory.objects.get(pk=inv_id)
        context = {
            'inv': inv,
            'operations': Operation.objects.filter(inventory=inv_id)
        }
        return context

    def get(self, request, **kwargs):
        form = UploadFileForm()
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, 'inventory_card.html', context=context)

    def post(self, request, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            inv_id = self.kwargs['inv_id']
            inv = Inventory.objects.get(pk=inv_id)
            inv.document = request.FILES['docfile']
            inv.save()
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, 'inventory_card.html', context=context)


class TransactionListView(LoginRequiredMixin, DetailView):
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = {'operations': Operation.objects.all().order_by('-date')}
        return context

    def get(self, request, **kwargs):
        form = OperationsFilterForm(request.POST)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, 'transaction_log.html', context=context)

    def post(self, request, **kwargs):
        form = OperationsFilterForm(request.POST)
        if form.is_valid():
            from_id = int(request.POST['select_location_from'])
            to_id = int(request.POST['select_location_to'])
            type_id = int(request.POST['select_type'])
            author_id = int(request.POST['select_author'])
            if request.POST['num'] != '':
                num = int(request.POST['num'])
                context = {'operations': Operation.objects.filter(pk=num), 'form': form}
                return render(request, 'transaction_log.html', context=context)
            from_loc = Location.objects.all()
            to_loc = Location.objects.all()
            types = Type.objects.all()
            inventory = Inventory.objects.filter(inv_type__in=types)
            if from_id != -1:
                from_loc = Location.objects.filter(pk=from_id)
            if to_id != -1:
                to_loc = Location.objects.filter(pk=to_id)
            if author_id != -1:
                author = Location.objects.get(pk=author_id)
                operations = Operation.objects.filter(from_place__in=from_loc, destination__in=to_loc,
                                                      inventory__in=inventory, author=author).order_by('-date')
            else:
                operations = Operation.objects.filter(from_place__in=from_loc, destination__in=to_loc,
                                                      inventory__in=inventory).order_by('-date')
            context = {'operations': operations, 'form': form}
            return render(request, 'transaction_log.html', context=context)


class ReportLocationsListView(LoginRequiredMixin, DetailView):
    login_url = '/login'

    def get_context_data(self, **kwargs):
        loc_type_id = self.kwargs['select_location']
        locations = Location.objects.filter(loc_type=loc_type_id)
        location_list = {}
        for loc in locations:
            loc_inv = Inventory.objects.filter(location=loc)
            location_list[loc.name] = loc_inv
        context = {"loc_list": location_list,
                   "loc_name": LocType.objects.get(pk=loc_type_id)}
        return context

    def get(self, request, **kwargs):
        form = LocFilterForm(request.POST)
        context = {'form': form, "loc_name": "none"}
        return render(request, 'reports.html', context=context)

    def post(self, request, **kwargs):
        form = LocFilterForm(request.POST)
        if form.is_valid():
            loc_type_id = int(request.POST['select_location'])
            locations = Location.objects.filter(loc_type=loc_type_id).order_by('name')
            location_list = {}
            for loc in locations:
                sum_queryset = Inventory.objects.filter(location=loc.pk)
                sum = sum_queryset.aggregate(Sum('cost'))['cost__sum']
                if sum is None:
                    sum = 0
                loc_inv = Inventory.objects.filter(location=loc)
                location_list[(loc.name, sum)] = loc_inv
            context = {"loc_list": location_list,
                       "loc_name": LocType.objects.get(pk=loc_type_id).name,
                       "form": form}
            return render(request, 'reports.html', context=context)


class TransactionView(LoginRequiredMixin, DetailView):
    login_url = '/login'

    def get_context_data(self, **kwargs):
        op_id = self.kwargs['op_id']
        op = Operation.objects.get(pk=op_id)
        context = {
            'op': op
        }
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'operation_card.html', context=context)


class CatalogView(LoginRequiredMixin, DetailView):
    login_url = '/login'

    def get_context_data(self, **kwargs):
        categorys = Category.objects.all().order_by('name')
        category_dict = {}
        for c in categorys:
            category_dict[c.name] = Type.objects.filter(category=c).order_by('name')
        context = {
            'keys': category_dict.keys(),
            'catalog': category_dict,
        }
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'catalog.html', context=context)


class SuppliersListView(LoginRequiredMixin, ListView):
    login_url = '/login'

    model = Supplier
    template_name = 'suppliers.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        return Supplier.objects.all().order_by('name')


class SupplierView(LoginRequiredMixin, DetailView):
    login_url = '/login'

    def get_context_data(self, **kwargs):
        sup_id = self.kwargs['sup_id']
        sup = Supplier.objects.get(pk=sup_id)
        context = {
            'sup': sup
        }
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'supplier_card.html', context=context)


# views for adding
class AddInvView(LoginRequiredMixin, CreateView):
    login_url = '/login'

    def get(self, request, **kwargs):
        form = AddInvForm()
        type_id = self.kwargs['type_id']
        name = Type.objects.get(pk=type_id).name
        context = {
            'form': form,
            'name': name
        }
        return render(request, 'add_inv.html', context)

    def post(self, request, **kwargs):
        form = AddInvForm(request.POST, request.FILES)
        if form.is_valid():
            type_id = self.kwargs['type_id']
            loc = Location.objects.get(pk=form.cleaned_data['location'])
            sup = Supplier.objects.get(pk=form.cleaned_data['supplier'])
            inv_type = Type.objects.get(pk=type_id)

            inv = Inventory(inv_type=inv_type, document=None, serial_num=form.cleaned_data['serial_num'],
                            cost=form.cleaned_data['cost'], location=loc, comment=form.cleaned_data['comment'],
                            supplier=sup)
            inv.save()
            return redirect('/')
        context = {
            'form': form
        }
        return render(request, 'add_inv.html', context)


class EditInvView(LoginRequiredMixin, CreateView):
    login_url = '/login'

    def get(self, request, **kwargs):
        inv_id = self.kwargs['inv_id']
        inv = Inventory.objects.get(pk=inv_id)
        form = EditInvForm(initial={'type': inv.inv_type.pk,
                                    'serial_num': inv.serial_num,
                                    'cost': inv.cost,
                                    'location': inv.location.pk,
                                    'comment': inv.comment,
                                    'supplier': inv.supplier.pk})
        context = {
            'form': form,
        }
        return render(request, 'edit_inv.html', context)

    def post(self, request, **kwargs):
        form = EditInvForm(request.POST)
        if form.is_valid():
            inv_id = self.kwargs['inv_id']
            inv = Inventory.objects.get(pk=inv_id)
            inv.inv_type = Type.objects.get(pk=form.cleaned_data['type'])
            inv.serial_num = form.cleaned_data['serial_num']
            inv.cost = form.cleaned_data['cost']
            inv.location = Location.objects.get(pk=form.cleaned_data['location'])
            inv.comment = form.cleaned_data['comment']
            inv.supplier = Supplier.objects.get(pk=form.cleaned_data['supplier'])
            inv.save()
            return redirect('/detail_'+inv_id)
        context = {
            'form': form
        }
        return render(request, 'edit_inv.html', context)


class AddTypeView(LoginRequiredMixin, CreateView):
    login_url = '/login'

    def get(self, request, **kwargs):
        form = AddTypeForm()
        context = {
            'form': form
        }
        return render(request, 'add.html', context)

    def post(self, request, **kwargs):
        form = AddTypeForm(request.POST)
        if form.is_valid():
            cat_name = self.kwargs['cat_name']
            category = Category.objects.get(name=cat_name)
            new_type = Type(category=category, name=form.cleaned_data['name'])
            new_type.save()
            return redirect('/catalog')
        context = {
            'form': form
        }
        return render(request, 'add.html', context)


class AddTransactionView(LoginRequiredMixin, CreateView):
    login_url = '/login'

    def get(self, request, **kwargs):
        form = AddTransactionForm()
        context = {
            'form': form
        }
        return render(request, 'add_operation.html', context)

    def post(self, request, **kwargs):
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            from_place = Location.objects.get(pk=form.cleaned_data['from_place'])
            destination = Location.objects.get(pk=form.cleaned_data['destination'])
            inv = Inventory.objects.get(pk=form.cleaned_data['inventory'])
            author = Location.objects.get(pk=form.cleaned_data['author'])
            notes = form.cleaned_data['notes']
            op = Operation(from_place=from_place, destination=destination, inventory=inv, author=author, notes=notes)
            op.save()
            inv.location = destination
            inv.save()

            return redirect('/transactions')
        context = {
            'form': form
        }
        return render(request, 'add_operation.html', context)


class AddSupView(LoginRequiredMixin, CreateView):
    login_url = '/login'

    def get(self, request, **kwargs):
        form = AddSupForm()
        context = {
            'form': form
        }
        return render(request, 'add_sup.html', context)

    def post(self, request, **kwargs):
        form = AddSupForm(request.POST)
        if form.is_valid():
            new_sup = Supplier(name=form.cleaned_data['name'], address=form.cleaned_data['address'],
                               phone=form.cleaned_data['phone'], director=form.cleaned_data['director'],
                               email=form.cleaned_data['email'], web=form.cleaned_data['web'],
                               notes=form.cleaned_data['notes'])
            new_sup.save()
            return redirect('/suppliers')
        context = {
            'form': form
        }
        return render(request, 'add_sup.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login')


def export_csv(request, **kwargs):
    loc_name = (kwargs['loc_name'])
    loc_type = LocType.objects.get(name=loc_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+loc_type.name+str(datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow([loc_type.name, '', '', ''])
    writer.writerow(['Місцезнаходження', 'ТМЦ', 'Серійний номер', 'Вартість'])

    locations = Location.objects.filter(loc_type=loc_type.pk).order_by('name')
    for loc in locations:
        sum_queryset = Inventory.objects.filter(location=loc.pk)
        sum = sum_queryset.aggregate(Sum('cost'))['cost__sum']
        if sum is None:
            sum = 0
        loc_inv = Inventory.objects.filter(location=loc)
        writer.writerow([loc.name, '', '', str(sum)+' грн.'])
        for inv in Inventory.objects.filter(location=loc.pk):
            writer.writerow(['', inv.inv_type.name, str(inv.serial_num), str(inv.cost)+' грн.'])
    return response


def export_pdf(request, **kwargs):
    loc_name = (kwargs['loc_name'])
    loc_type = LocType.objects.get(name=loc_name)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename='+loc_type.name+str(datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    locations = Location.objects.filter(loc_type=loc_type.pk).order_by('name')
    location_list = {}
    for loc in locations:
        sum_queryset = Inventory.objects.filter(location=loc.pk)
        sum = sum_queryset.aggregate(Sum('cost'))['cost__sum']
        if sum is None:
            sum = 0
        loc_inv = Inventory.objects.filter(location=loc)
        location_list[(loc.name, sum)] = loc_inv
    context = {"loc_list": location_list,
               "loc_name": loc_type.name,
               "date": datetime.now()}

    html_string = render_to_string('pdf_output.html', context)
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output=open(output.name, 'rb')
        response.write(output.read())

    return response
