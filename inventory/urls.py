from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Productos
    path('inventario/', views.inventario, name='inventario'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('ocultar-producto/<int:producto_id>/', views.ocultar_producto, name='ocultar_producto'),
    path('activar-producto/<int:producto_id>/', views.activar_producto, name='activar_producto'),
    path('productos-ocultos/', views.productos_ocultos, name='productos_ocultos'), 
    path('exportar-csv/', views.exportar_csv, name='exportar_csv'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
    
    # Categorias
    path('categorias/', views.categorias, name='categorias'),
    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('editar-categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('ocultar-categoria/<int:categoria_id>/', views.ocultar_categoria, name='ocultar_categoria'),
    path('categorias-ocultas/', views.categorias_ocultas, name='categorias_ocultas'),
    path('activar-categoria/<int:categoria_id>/', views.activar_categoria, name='activar_categoria'),
    
    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes-ocultos/', views.clientes_ocultos, name='ver_clientes_ocultos'),
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('ocultar-cliente/<int:cliente_id>/', views.ocultar_cliente, name='ocultar_cliente'),  
    path('activar-cliente/<int:cliente_id>/', views.activar_cliente, name='activar_cliente'),
    path('exportar_csv_clientes/', views.exportar_csv_clientes, name='exportar_csv_clientes'),
    path('exportar_pdf_clientes/', views.exportar_pdf_clientes, name='exportar_pdf_clientes'),

    # Ventas
    path('ventas/', views.ventas, name='ventas'),
    path('agregar-venta/', views.agregar_venta, name='agregar_venta'),
    path('eliminar-venta/<int:venta_id>/', views.eliminar_venta, name='eliminar_venta'),

    # Facturas
    path('facturas/', views.facturas, name='facturas'),
    path('agregar-factura/', views.agregar_factura, name='agregar_factura'),
    path('eliminar-factura/<int:factura_id>/', views.eliminar_factura, name='eliminar_factura'),

    # Guías de despacho
    path('guias-despacho/', views.guias_despacho, name='guias_despacho'),
    path('agregar-guia-despacho/', views.agregar_guia_despacho, name='agregar_guia_despacho'),
    path('eliminar-guia-despacho/<int:guia_id>/', views.eliminar_guia_despacho, name='eliminar_guia_despacho'),

    # Historial de Inventario
    path('historial-inventario/', views.historial_inventario, name='historial_inventario'),
    path('agregar-historial-inventario/', views.agregar_historial_inventario, name='agregar_historial_inventario'),
    path('eliminar-historial-inventario/<int:historial_id>/', views.eliminar_historial_inventario, name='eliminar_historial_inventario'),
    
    # Usuario
    path('usuario/', views.usuario, name='usuario'),

    
    
]
