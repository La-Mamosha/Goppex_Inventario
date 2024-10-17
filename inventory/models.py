from django.db import models

# Create your models here.

#########################################################################################################################################################
# Modelo de Rol
class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

#########################################################################################################################################################
# Modelo de Usuario
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_usuario

#########################################################################################################################################################
# Modelo de Registro de Actividades
class RegistroActividad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    actividad = models.TextField()
    fecha_actividad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Actividad {self.id} - {self.usuario.nombre_usuario}'

#########################################################################################################################################################
# Modelo de Cliente
class Cliente(models.Model):
    rut = models.CharField(max_length=15, unique=True)
    razon_social = models.CharField(max_length=255)
    giro = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateTimeField(auto_now=True)
    oculto = models.BooleanField(default=False)  # Agregado para ocultar clientes

    def __str__(self):
        return self.razon_social

#########################################################################################################################################################
# Modelo de Categoría de Producto
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    oculto = models.BooleanField(default=False) 

    def __str__(self):
        return self.nombre

#########################################################################################################################################################
# Modelo de Producto
class Producto(models.Model):
    id = models.AutoField(primary_key=True)  # Campo ID automático
    codigo = models.CharField(max_length=50, unique=True)  # Código ingresado manualmente
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    oculto = models.BooleanField(default=False)  # Campo para ocultar productos
    visible = models.BooleanField(default=True)  # Este campo indica si el producto está visible o no

    def __str__(self):
        return self.nombre

#########################################################################################################################################################
# Modelo de Ventas
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()
    fecha_venta = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=15, decimal_places=2)
    iva = models.DecimalField(max_digits=15, decimal_places=2)
    descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'Venta {self.id} - {self.cliente.razon_social}'

#########################################################################################################################################################
# Modelo de Factura
class Factura(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=15, decimal_places=2)
    estado_pago = models.CharField(max_length=50)  # Ejemplo: 'Pagado', 'Pendiente'
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Factura {self.id} - {self.venta.cliente.razon_social}'

#########################################################################################################################################################
# Modelo de Pago
class Pago(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    monto_pago = models.DecimalField(max_digits=15, decimal_places=2)
    metodo_pago = models.CharField(max_length=100)  # Ejemplo: 'Tarjeta de crédito', 'Efectivo'
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=50)  # Ejemplo: 'Completado', 'Pendiente'

    def __str__(self):
        return f'Pago {self.id} - Factura {self.factura.id}'

#########################################################################################################################################################
# Modelo de Guía de Despacho
class GuiaDespacho(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f'Guía {self.id} - {self.venta.cliente.razon_social}'

#########################################################################################################################################################
# Modelo de Historial de Inventario
class HistorialInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)  # 'Ingreso', 'Salida'
    cantidad = models.IntegerField()
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f'Historial {self.id} - {self.producto.nombre}'


