from django.urls import path

from purchase_orders.views.productView import ProductView
from purchase_orders.views.purchase_order_item import (
    PurchaseOrderItemCreateView,
    PurchaseOrderItemDetailView,
    PurchaseOrderItemListView,
)
from purchase_orders.views.purchase_order_view import PurchaseOrderCreateView
from purchase_orders.views.vendor import (
    VendorCreateView,
    VendorDetailView,
    VendorListView,
)

urlpatterns = [

    #vendors
    path('vendors/', VendorListView.as_view(), name='vendor-list'),  
    path('vendors/create/', VendorCreateView.as_view(), name='vendor-create'),  
    path('vendors/<uuid:uuid>/', VendorDetailView.as_view(), name='vendor-detail'),  

    # Purchase Orders
    path('purchase-orders/', PurchaseOrderCreateView.as_view(), name='create_purchase_order'),  
    path('purchase-orders/<int:pk>/', PurchaseOrderCreateView.as_view(), name='purchase_order_detail'),  
    path('purchase-orders/<int:pk>/confirm/', PurchaseOrderCreateView.as_view(), name='confirm_purchase_order'),  
    path('purchase-orders/<int:pk>/approve/', PurchaseOrderCreateView.as_view(), name='approve_purchase_order'),  

     # Purchase Orders_items
    path('purchase-order-items/', PurchaseOrderItemListView.as_view(), name='purchase-order-item-list'),  
    path('purchase-order-items/create/', PurchaseOrderItemCreateView.as_view(), name='purchase-order-item-create'),  
    path('purchase-order-items/<uuid:uuid>/', PurchaseOrderItemDetailView.as_view(), name='purchase-order-item-detail'),  

    #Products
    path('products/', ProductView.as_view(), name='product_list_create'),  
    path('products/<uuid:uuid>/', ProductView.as_view(), name='product_detail'),  

]
