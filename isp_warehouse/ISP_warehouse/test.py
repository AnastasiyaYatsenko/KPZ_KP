from django.test import TestCase, Client
import unittest
from ISP_warehouse.models import *
from ISP_warehouse.forms import *
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


class ISPTestCase(unittest.TestCase):

    def test_1_success_index(self):
        c = Client()
        response = c.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_2_db(self):
        c = Category.objects.get(name='category')
        self.assertEqual(c.name, 'category')

    def test_3_login(self):
        c = Client()
        response = c.post('/login', {'username': 'storekeeper', 'password': 'qwerty'},
                          follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_4_add_sup(self):
        c = Client()
        c.login(username='storekeeper', password='qwerty')
        c.post('/add_sup', {'name': 'test_name', 'address': 'test_address', 'phone': '+1111',
                            'director': 'Director T.T.', 'email': 'test@test.com', 'web': 'test.com', 'notes': 'test'})

        s = Supplier.objects.get(name='test_name')
        s_id = s.pk
        self.assertEqual(model_to_dict(s), {'id': s.pk, 'name': 'test_name', 'address': 'test_address',
                                            'phone': '+1111', 'director': 'Director T.T.', 'email': 'test@test.com',
                                            'web': 'test.com', 'notes': 'test'})

    def test_5_add_type(self):
        c = Client()
        c.login(username='storekeeper', password='qwerty')
        cat = Category.objects.get(name='category')
        c.post('/add_type_category', {'name': 'test_type', 'category': cat})

        t = Type.objects.get(name='test_type')
        t_id = t.pk
        self.assertEqual(model_to_dict(t), {'id': t.pk, 'name': 'test_type', 'category': cat.pk})

    def test_6_add_inv(self):
        c = Client()
        c.login(username='storekeeper', password='qwerty')
        inv_type = Type.objects.get(name='type1')
        loc = Location.objects.get(name='location2')
        sup = Supplier.objects.get(name='supplier')
        c.post('/add_inv_'+str(inv_type.pk), {'serial_num': '123456', 'cost': 12, 'location': loc.pk,
                                              'comment': 'test_comment', 'supplier': sup.pk})

        inv = Inventory.objects.get(serial_num=123456)
        inv_dict = {'id': inv.pk,
                    'inv_type': inv.inv_type.pk,
                    'serial_num': inv.serial_num,
                    'cost': inv.cost,
                    'location': inv.location.pk,
                    'comment': inv.comment,
                    'supplier': inv.supplier.pk}
        self.assertEqual(inv_dict, {'id': inv.pk, 'inv_type': inv_type.pk, 'serial_num': '123456', 'cost': 12,
                                    'location': loc.pk, 'comment': 'test_comment', 'supplier': sup.pk})

    def test_7_edit_inv(self):
        c = Client()
        c.login(username='storekeeper', password='qwerty')

        inv = Inventory.objects.get(serial_num='1')

        inv_type = Type.objects.get(name='type1')
        loc = Location.objects.get(name='location2')
        sup = Supplier.objects.get(name='supplier')
        c.post('/edit_inv_'+str(inv.pk), {'type': inv.inv_type.pk, 'serial_num': 'EDIT1', 'cost': 12,
                                          'location': loc.pk, 'comment': 'comment_EDIT', 'supplier': sup.pk})

        inv_edit = Inventory.objects.get(pk=inv.pk)
        inv_dict = {'id': inv_edit.pk,
                    'inv_type': inv_edit.inv_type.pk,
                    'serial_num': inv_edit.serial_num,
                    'cost': inv_edit.cost,
                    'location': inv_edit.location.pk,
                    'comment': inv_edit.comment,
                    'supplier': inv_edit.supplier.pk}
        self.assertEqual(inv_dict, {'id': inv_edit.pk, 'inv_type': inv_type.pk, 'serial_num': 'EDIT1', 'cost': 12,
                                    'location': loc.pk, 'comment': 'comment_EDIT', 'supplier': sup.pk})

    def test_8_add_op(self):
        c = Client()
        c.login(username='storekeeper', password='qwerty')

        inv = Inventory.objects.get(serial_num='2')
        from_loc = Location.objects.get(name='location2')
        to_loc = Location.objects.get(name='location1')
        author = Location.objects.get(name='cowork')
        notes = 'test'

        c.post('/add_tr', {'from_place': from_loc.pk, 'destination': to_loc.pk, 'inventory': inv.pk,
                           'author': author.pk, 'notes': notes})

        inv = Inventory.objects.get(serial_num='2')
        op = Operation.objects.get(inventory=inv.pk, author=author.pk)
        test_dict = {'inv_loc': inv.location.pk,
                    'op_from': op.from_place.pk,
                    'op_destination': op.destination.pk,
                    'op_inv': op.inventory.pk,
                    'op_author': op.author.pk,
                    'op_notes': op.notes}
        self.assertEqual(test_dict, {'inv_loc': to_loc.pk, 'op_from': from_loc.pk, 'op_destination': to_loc.pk,
                    'op_inv': inv.pk, 'op_author': author.pk, 'op_notes': notes})
