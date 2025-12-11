import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Servicio, Evento, Publicacion, Categoria
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from .cart import Cart
import urllib.parse
from django.conf import settings


def versioned_static(path):
    """Return static URL with a cache-busting timestamp query string when possible."""
    url = static(path)
    try:
        real_path = finders.find(path)
        if real_path:
            ts = int(os.path.getmtime(real_path))
            return f"{url}?v={ts}"
    except Exception:
        pass
    return url


def home(request):
    productos = Producto.objects.filter(activo=True)
    servicios = Servicio.objects.all()
    eventos = Evento.objects.filter(activo=True)[:3]
    articulos = Publicacion.objects.filter(activo=True)[:3]
    
    context = {
        'productos': productos,
        'servicios': servicios,
        'eventos': eventos,
        'articulos': articulos,
        'slide_images': [
            versioned_static('photos/index-menu-aceites.jpg'),
            versioned_static('photos/index-menu-aceites-tipo2.jpg'),
            versioned_static('photos/index-menu-aceites-tipo3.jpg'),
        ],
        'whatsapp_phone': settings.WHATSAPP_PHONE,
    }
    return render(request, 'core/index.html', context)

def productos(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(activo=True)
    
    categoria_seleccionada = request.GET.get('categoria')
    if categoria_seleccionada:
        productos = productos.filter(categoria_id=categoria_seleccionada)
    
    context = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'core/productos.html', context)

def servicios(request):
    servicios = Servicio.objects.all()

    message = "Hola AUKA Terapias, quiero más información sobre sus servicios."
    encoded_message = urllib.parse.quote_plus(message, safe="")
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_PHONE}?text={encoded_message}"

    context = {
        'servicios': servicios,
        'whatsapp_url': whatsapp_url,
    }
    return render(request, 'core/servicios.html', context)

def about(request):
    return render(request, 'core/about.html')

def blog(request):
    publicaciones = Publicacion.objects.all()[:6]
    eventos = Evento.objects.all()[:6]

    message = "Hola AUKA Terapias, me interesa saber más sobre los eventos publicados."
    encoded_message = urllib.parse.quote_plus(message, safe="")
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_PHONE}?text={encoded_message}"

    return render(request, "core/blog.html", {
        "publicaciones": publicaciones,
        "eventos": eventos,
        "whatsapp_url": whatsapp_url,
    })

def contacto(request):
    message = "Hola AUKA Terapias, tengo una consulta específica."
    encoded_message = urllib.parse.quote_plus(message, safe="")
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_PHONE}?text={encoded_message}"

    return render(request, "core/contacto.html", {
        "whatsapp_url": whatsapp_url,
    })


def producto_detalle(request, slug):
    producto = get_object_or_404(Producto, slug=slug, activo=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, 
        activo=True
    ).exclude(id=producto.id)[:4]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'core/producto_detalle.html', context)

# Todo esto es para el carrito de compras
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=product_id)
    cart.add(product)
    return redirect("core:cart_detail")

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=product_id)
    cart.remove(product)
    return redirect("core:cart_detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "core/cart_detail.html", {"cart": cart.cart, "total": cart.get_total()})

def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect("core:cart_detail")  # vuelve al carrito si está vacío

    message = "Buenas! quisiera comprar lo siguiente:\n"
    total = 0
    for item in cart.cart.values():
        subtotal = item['price'] * item['quantity']  # se quita si no hay precio
        message += f"- {item['quantity']}x {item['name']} (${subtotal})\n"
        total += subtotal  # se quita si no hay precio
    message += f"Total estimado: ${total}"

    phone = settings.WHATSAPP_PHONE  # número del vendedor en formato internacional
    encoded_message = urllib.parse.quote_plus(message, safe="")  # codifica correctamente
    url = f"https://wa.me/{phone}?text={encoded_message}"

    print(url)
    cart.clear()  # vacía el carrito después de generar el mensaje
    return redirect(url)

def increase_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=product_id)
    cart.add(product)  # reutilizamos el mismo método add, que suma cantidad
    return redirect("core:cart_detail")

def decrease_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=product_id)
    product_id_str = str(product.id)
    if product_id_str in cart.cart:
        if cart.cart[product_id_str]["quantity"] > 1:
            cart.cart[product_id_str]["quantity"] -= 1
        else:
            cart.remove(product)
        cart.save()
    return redirect("core:cart_detail")