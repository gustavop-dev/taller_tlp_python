from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear router para los ViewSets
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'categories', views.CategoryViewSet, basename='category')

# URLs de la aplicación (solo API REST)
urlpatterns = [
    # API endpoints usando Django REST Framework router
    path('', include(router.urls)),
    
    # Ejemplos de rutas generadas automáticamente por el router:
    # GET /api/books/ - Listar libros
    # POST /api/books/ - Crear libro
    # GET /api/books/{id}/ - Detalle de libro
    # PUT /api/books/{id}/ - Actualizar libro
    # DELETE /api/books/{id}/ - Eliminar libro
    # POST /api/books/{id}/apply_discount/ - Aplicar descuento
    # POST /api/books/{id}/update_stock/ - Actualizar stock
    # POST /api/books/{id}/remove_discount/ - Remover descuento
    # GET /api/books/discounted_books/ - Libros con descuento
    # GET /api/books/low_stock/ - Libros con stock bajo
    # GET /api/books/by_category/ - Libros por categoría
    # GET /api/books/search_advanced/ - Búsqueda avanzada
    
    # GET /api/categories/ - Listar categorías
    # POST /api/categories/ - Crear categoría
    # GET /api/categories/{id}/ - Detalle de categoría
    # PUT /api/categories/{id}/ - Actualizar categoría
    # DELETE /api/categories/{id}/ - Eliminar categoría
    # GET /api/categories/{id}/books/ - Libros de una categoría
] 