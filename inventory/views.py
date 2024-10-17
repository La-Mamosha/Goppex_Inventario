from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Producto, Venta, Factura, GuiaDespacho, Pago, HistorialInventario, Categoria, Usuario, Rol
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db import IntegrityError
from reportlab.lib.pagesizes import letter


# Create your views here.

#########################################################################################################################################################
# Vista del Dashboard
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_productos = Producto.objects.count()
    total_ventas = Venta.objects.count()
    total_facturas = Factura.objects.count()
    total_guias = GuiaDespacho.objects.count()

    context = {
        'total_clientes': total_clientes,
        'total_productos': total_productos,
        'total_ventas': total_ventas,
        'total_facturas': total_facturas,
        'total_guias': total_guias
    }
    return render(request, 'inventory/dashboard.html', context)

#########################################################################################################################################################
'''# Vista para listar las categorías
def categorias(request):
    categorias = Categoria.objects.filter(oculto=False)  # Solo categorías que no están ocultas
    return render(request, 'inventory/categorias.html', {'categorias': categorias})'''

# Vista para listar las categorías
def categorias(request):
    query = request.GET.get('q')  # Obtén el término de búsqueda
    if query:
        categorias = Categoria.objects.filter(oculto=False, nombre__icontains=query)  # Filtrar por nombre
    else:
        categorias = Categoria.objects.filter(oculto=False)  # Solo categorías que no están ocultas
    return render(request, 'inventory/categorias.html', {'categorias': categorias})

# Vista para agregar una nueva categoría
def agregar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria = Categoria(nombre=nombre)
        categoria.save()
        return redirect('categorias')  # Redirigir a la vista de categorías
    return render(request, 'inventory/agregar_categoria.html')

# Vista para editar una categoría
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.save()
        return redirect('categorias')
    return render(request, 'inventory/editar_categoria.html', {'categoria': categoria})

def ocultar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    # Aquí cambiamos el estado a oculto sin solicitar confirmación
    categoria.oculto = True  
    categoria.save()  # Guarda los cambios
    return redirect('categorias')  # Redirige a la vista de categorías

# Vista para listar las categorías ocultas
def categorias_ocultas(request):
    categorias = Categoria.objects.filter(oculto=True)  # Solo categorías que están ocultas
    return render(request, 'inventory/categorias_ocultas.html', {'categorias': categorias})

# Vista para activar una categoría
def activar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        # Cambia el estado a visible
        categoria.oculto = False  # Asegúrate de que tu modelo tenga este campo
        categoria.save()
        return redirect('categorias_ocultas')  # Redirigir a la vista de categorías ocultas

#########################################################################################################################################################
# Vistas para productos
def inventario(request):
    query = request.GET.get('q')
    if query:
        # Filtrar los productos visibles que coinciden con la búsqueda
        productos = Producto.objects.filter(nombre__icontains=query, visible=True)
    else:
        # Mostrar solo los productos visibles
        productos = Producto.objects.filter(visible=True)
    return render(request, 'inventory/inventario.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')  # Obtener el código
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio_unitario = request.POST.get('precio_unitario')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        categoria_id = request.POST.get('categoria')
        cantidad = request.POST.get('cantidad')

        # Crear el producto, pero manejar errores si el código ya existe
        try:
            producto = Producto(
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                precio_unitario=precio_unitario,
                fecha_vencimiento=fecha_vencimiento,
                categoria_id=categoria_id,
                cantidad=cantidad
            )
            producto.save()
            return redirect('inventario')
        except IntegrityError:
            # Si el código es duplicado, capturar el error y devolver el formulario con un mensaje
            error_message = "El código ya está en uso. Por favor, elige otro código."

            categorias = Categoria.objects.all()
            return render(request, 'inventory/agregar_producto.html', {
                'categorias': categorias,
                'error_message': error_message
            })

    categorias = Categoria.objects.all()
    return render(request, 'inventory/agregar_producto.html', {'categorias': categorias})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio_unitario = request.POST.get('precio_unitario')
        producto.fecha_vencimiento = request.POST.get('fecha_vencimiento')
        producto.cantidad = request.POST.get('cantidad')
        producto.save()
        return redirect('inventario')
    categorias = Categoria.objects.all()
    return render(request, 'inventory/editar_producto.html', {'producto': producto, 'categorias': categorias})

def ocultar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.visible = False  # Cambia el estado del producto a oculto
        producto.save()
        return redirect('inventario')
    return render(request, 'inventory/ocultar_producto.html', {'producto': producto})

def activar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.visible = True  # Cambiar el estado a visible
    producto.save()
    return redirect('productos_ocultos')

def productos_ocultos(request):
    productos = Producto.objects.filter(visible=False)  # Mostrar solo los productos ocultos
    return render(request, 'inventory/productos_ocultos.html', {'productos': productos})

def exportar_csv(request):
    productos = Producto.objects.filter(oculto=False)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Código', 'Nombre', 'Descripción', 'Precio Unitario', 'Cantidad'])
    for producto in productos:
        writer.writerow([producto.codigo, producto.nombre, producto.descripcion, producto.precio_unitario, producto.cantidad])

    return response

# Vista para exportar inventario a PDF
def exportar_pdf(request):
    # Configura el tipo de respuesta como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'

    # Crea el objeto canvas para el PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('Listado de Productos')

    # Añadir título al documento
    pdf.setFont('Helvetica-Bold', 18)
    pdf.drawString(100, 750, "Listado de Productos")

    # Configura la posición inicial
    y = 720
    productos = Producto.objects.filter(oculto=False)

    # Añade el encabezado de la tabla
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(30, y, "Código")
    pdf.drawString(120, y, "Nombre")
    pdf.drawString(250, y, "Descripción")
    pdf.drawString(400, y, "Precio Unitario")
    pdf.drawString(500, y, "Cantidad")

    y -= 30

    # Añade los productos al PDF
    pdf.setFont('Helvetica', 10)
    for producto in productos:
        pdf.drawString(30, y, str(producto.codigo))
        pdf.drawString(120, y, producto.nombre)
        pdf.drawString(250, y, producto.descripcion[:30])  # Limitar la descripción a 30 caracteres
        pdf.drawString(400, y, f"${producto.precio_unitario:.2f}")
        pdf.drawString(500, y, str(producto.cantidad))
        y -= 20

        # Si la página está llena, agrega una nueva página
        if y < 50:
            pdf.showPage()  # Nueva página
            pdf.setFont('Helvetica', 10)  # Restablecer la fuente
            y = 720

    # Finaliza y guarda el PDF
    pdf.showPage()
    pdf.save()

    return response

#########################################################################################################################################################
# Vista para mostrar todos los clientes (solo visibles)
def clientes(request):
    clientes = Cliente.objects.filter(oculto=False)
    return render(request, 'inventory/clientes.html', {'clientes': clientes})

# Agregar cliente
def agregar_cliente(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        razon_social = request.POST.get('razon_social')
        giro = request.POST.get('giro')
        direccion = request.POST.get('direccion')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')

        try:
            cliente = Cliente(
                rut=rut,
                razon_social=razon_social,
                giro=giro,
                direccion=direccion,
                correo=correo,
                telefono=telefono
            )
            cliente.save()
            return redirect('clientes')
        except IntegrityError:
            # Manejar el caso de rut duplicado
            error_message = "El RUT ya está en uso."
            return render(request, 'inventory/agregar_cliente.html', {'error_message': error_message})

    return render(request, 'inventory/agregar_cliente.html')

# Editar cliente
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.rut = request.POST.get('rut')
        cliente.razon_social = request.POST.get('razon_social')
        cliente.giro = request.POST.get('giro')
        cliente.direccion = request.POST.get('direccion')
        cliente.correo = request.POST.get('correo')
        cliente.telefono = request.POST.get('telefono')
        cliente.save()
        return redirect('clientes')
    return render(request, 'inventory/editar_cliente.html', {'cliente': cliente})

# Ocultar cliente
def ocultar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.oculto = True  # Cambiar el estado a oculto
        cliente.save()
        return redirect('clientes')
    return render(request, 'inventory/ocultar_cliente.html', {'cliente': cliente})

# Activar cliente
def activar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.oculto = False  # Cambiar el estado a visible
    cliente.save()
    return redirect('ver_clientes_ocultos')  

def clientes_ocultos(request):
    clientes = Cliente.objects.filter(oculto=True)
    return render(request, 'inventory/clientes_ocultos.html', {'clientes': clientes})

# Exportar clientes a CSV
def exportar_csv_clientes(request):
    clientes = Cliente.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'

    writer = csv.writer(response)
    writer.writerow(['RUT', 'Razón Social', 'Giro', 'Dirección', 'Correo', 'Teléfono'])
    for cliente in clientes:
        writer.writerow([cliente.rut, cliente.razon_social, cliente.giro, cliente.direccion, cliente.correo, cliente.telefono])

    return response

# Exportar clientes a PDF
def exportar_pdf_clientes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clientes.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('Listado de Clientes')

    # Títulos
    pdf.setFont('Helvetica-Bold', 18)
    pdf.drawString(100, 750, "Listado de Clientes")

    # Encabezado
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(30, 720, "RUT")
    pdf.drawString(120, 720, "Razón Social")
    pdf.drawString(300, 720, "Giro")
    pdf.drawString(400, 720, "Dirección")
    pdf.drawString(500, 720, "Correo")
    pdf.drawString(600, 720, "Teléfono")

    y = 700
    pdf.setFont('Helvetica', 10)
    for cliente in Cliente.objects.all():
        pdf.drawString(30, y, cliente.rut)
        pdf.drawString(120, y, cliente.razon_social)
        pdf.drawString(300, y, cliente.giro)
        pdf.drawString(400, y, cliente.direccion)
        pdf.drawString(500, y, cliente.correo)
        pdf.drawString(600, y, cliente.telefono)
        y -= 20  # Salto de línea

        if y < 50:  # Nueva página si es necesario
            pdf.showPage()
            pdf.setFont('Helvetica', 10)
            y = 750  # Reiniciar posición

    pdf.save()
    return response

#########################################################################################################################################################
# Vistas para ventas
def ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'inventory/ventas.html', {'ventas': ventas})

def agregar_venta(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        producto_id = request.POST.get('producto')
        cantidad_producto = request.POST.get('cantidad_producto')
        cliente = Cliente.objects.get(id=cliente_id)
        producto = Producto.objects.get(id=producto_id)
        sub_total = producto.precio_unitario * int(cantidad_producto)
        iva = sub_total * 0.19
        total = sub_total + iva

        venta = Venta(
            cliente=cliente,
            producto=producto,
            cantidad_producto=cantidad_producto,
            sub_total=sub_total,
            iva=iva,
            total=total
        )
        venta.save()
        return redirect('ventas')
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, 'inventory/agregar_venta.html', {'clientes': clientes, 'productos': productos})

def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        venta.delete()
        return redirect('ventas')
    return render(request, 'inventory/eliminar_venta.html', {'venta': venta})

#########################################################################################################################################################
# Vistas para facturas
def facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'inventory/facturas.html', {'facturas': facturas})

def agregar_factura(request):
    if request.method == 'POST':
        venta_id = request.POST.get('venta')
        estado_pago = request.POST.get('estado_pago')
        venta = Venta.objects.get(id=venta_id)
        factura = Factura(
            venta=venta,
            monto_total=venta.total,
            estado_pago=estado_pago
        )
        factura.save()
        return redirect('facturas')
    ventas = Venta.objects.all()
    return render(request, 'inventory/agregar_factura.html', {'ventas': ventas})

def eliminar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        factura.delete()
        return redirect('facturas')
    return render(request, 'inventory/eliminar_factura.html', {'factura': factura})

#########################################################################################################################################################
# Vistas para guías de despacho
def guias_despacho(request):
    guias = GuiaDespacho.objects.all()
    return render(request, 'inventory/guias_despacho.html', {'guias': guias})

def agregar_guia_despacho(request):
    if request.method == 'POST':
        venta_id = request.POST.get('venta')
        direccion = request.POST.get('direccion')
        venta = Venta.objects.get(id=venta_id)
        guia = GuiaDespacho(
            venta=venta,
            direccion=direccion
        )
        guia.save()
        return redirect('guias_despacho')
    ventas = Venta.objects.all()
    return render(request, 'inventory/agregar_guia_despacho.html', {'ventas': ventas})

def eliminar_guia_despacho(request, guia_id):
    guia = get_object_or_404(GuiaDespacho, id=guia_id)
    if request.method == 'POST':
        guia.delete()
        return redirect('guias_despacho')
    return render(request, 'inventory/eliminar_guia_despacho.html', {'guia': guia})

#########################################################################################################################################################
# Vistas para historial de inventario
def historial_inventario(request):
    historial = HistorialInventario.objects.all()
    return render(request, 'inventory/historial_inventario.html', {'historial': historial})

def agregar_historial_inventario(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        tipo = request.POST.get('tipo')
        cantidad = request.POST.get('cantidad')
        descripcion = request.POST.get('descripcion')
        producto = Producto.objects.get(id=producto_id)

        historial = HistorialInventario(
            producto=producto,
            tipo=tipo,
            cantidad=cantidad,
            descripcion=descripcion
        )
        historial.save()
        return redirect('historial_inventario')
    productos = Producto.objects.all()
    return render(request, 'inventory/agregar_historial_inventario.html', {'productos': productos})

def eliminar_historial_inventario(request, historial_id):
    historial = get_object_or_404(HistorialInventario, id=historial_id)
    if request.method == 'POST':
        historial.delete()
        return redirect('historial_inventario')
    return render(request, 'inventory/eliminar_historial_inventario.html', {'historial': historial})

# Vista para la página de usuario
def usuario(request):
    usuarios = Usuario.objects.all()  # Asumiendo que deseas listar los usuarios
    return render(request, 'inventory/usuario.html', {'usuarios': usuarios})
