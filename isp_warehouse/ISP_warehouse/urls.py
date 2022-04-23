from django.urls import path

from . import views

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='index'),
    path('transactions', views.TransactionListView.as_view(), name='transaction'),
    path('suppliers', views.SuppliersListView.as_view(), name='supplier'),
    path('detail_op_<op_id>', views.TransactionView.as_view(), name='op'),
    path('detail_sup_<sup_id>', views.SupplierView.as_view(), name='sup'),
    path('detail_<inv_id>', views.InventoryView.as_view(), name='inv'),
    path('reports', views.ReportLocationsListView.as_view(), name='rep'),
    path('add_inv_<type_id>', views.AddInvView.as_view(), name='add_inv'),
    path('add_type_<cat_name>', views.AddTypeView.as_view(), name='add_type'),
    path('add_sup', views.AddSupView.as_view(), name='add_sup'),
    path('add_tr', views.AddTransactionView.as_view(), name='add_tr'),
    path('edit_inv_<inv_id>', views.EditInvView.as_view(), name='edit_inv'),
    path('catalog', views.CatalogView.as_view(), name='catalog'),
    path('csv_<loc_name>', views.export_csv, name='csv'),
    path('pdf_<loc_name>', views.export_pdf, name='pdf'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]
