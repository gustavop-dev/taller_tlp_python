from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from decimal import Decimal

from .models import Book, Category
from .serializers import (
    BookListSerializer, BookDetailSerializer, BookCreateUpdateSerializer,
    CategorySerializer, DiscountSerializer, StockUpdateSerializer,
    BookFilterSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de categorías de libros
    Casos de uso:
    - Listar categorías
    - Crear nueva categoría
    - Actualizar categoría existente
    - Eliminar categoría
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """Filtrar categorías activas por defecto"""
        queryset = Category.objects.all()
        
        # Filtro para incluir categorías inactivas si se especifica
        include_inactive = self.request.query_params.get('include_inactive', False)
        if not include_inactive:
            queryset = queryset.filter(is_active=True)
        
        return queryset

    def perform_destroy(self, instance):
        """Soft delete: marcar como inactivo en lugar de eliminar"""
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Obtener todos los libros de una categoría específica"""
        category = self.get_object()
        books = category.books.filter(is_available=True)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión completa de libros
    Casos de uso:
    - Listar libros con filtros
    - Crear nuevo libro
    - Obtener detalle de libro
    - Actualizar libro existente
    - Eliminar libro
    - Aplicar descuentos
    - Actualizar stock
    """
    queryset = Book.objects.filter(is_available=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['title', 'author', 'isbn', 'description']
    ordering_fields = ['title', 'author', 'price', 'publication_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action == 'list':
            return BookListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        else:
            return BookDetailSerializer

    def get_queryset(self):
        """Aplicar filtros personalizados"""
        queryset = Book.objects.all()
        
        # Filtros básicos
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        category = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        is_available = self.request.query_params.get('is_available', None)
        has_discount = self.request.query_params.get('has_discount', None)

        # Aplicar filtros
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        if author:
            queryset = queryset.filter(author__icontains=author)
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        if is_available is not None:
            is_available_bool = is_available.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(is_available=is_available_bool)
        
        if has_discount is not None:
            has_discount_bool = has_discount.lower() in ['true', '1', 'yes']
            if has_discount_bool:
                queryset = queryset.filter(discount_percentage__gt=0)
            else:
                queryset = queryset.filter(discount_percentage=0)

        return queryset

    def perform_destroy(self, instance):
        """Soft delete: marcar como no disponible"""
        instance.is_available = False
        instance.save()

    @action(detail=True, methods=['post'])
    def apply_discount(self, request, pk=None):
        """
        Aplicar descuento a un libro específico
        Caso de uso: Transformación (aplicar descuento)
        """
        book = self.get_object()
        serializer = DiscountSerializer(data=request.data)
        
        if serializer.is_valid():
            discount_percentage = serializer.validated_data['discount_percentage']
            success = book.apply_discount(float(discount_percentage))
            
            if success:
                # Retornar datos actualizados del libro
                book_serializer = BookDetailSerializer(book)
                return Response({
                    'message': f'Descuento del {discount_percentage}% aplicado exitosamente',
                    'book': book_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'No se pudo aplicar el descuento'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """
        Actualizar stock de un libro
        Caso de uso: Transformación (modificar stock)
        """
        book = self.get_object()
        serializer = StockUpdateSerializer(
            data=request.data, 
            context={'book': book}
        )
        
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            success = book.update_stock(quantity)
            
            if success:
                book_serializer = BookDetailSerializer(book)
                return Response({
                    'message': f'Stock actualizado. Nuevo stock: {book.stock}',
                    'book': book_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'No se pudo actualizar el stock'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_discount(self, request, pk=None):
        """
        Remover descuento de un libro
        Caso de uso: Transformación (quitar descuento)
        """
        book = self.get_object()
        book.discount_percentage = Decimal('0.00')
        book.save()
        
        book_serializer = BookDetailSerializer(book)
        return Response({
            'message': 'Descuento removido exitosamente',
            'book': book_serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def discounted_books(self, request):
        """
        Listar todos los libros con descuento
        Caso de uso: Listado filtrado
        """
        books = self.get_queryset().filter(discount_percentage__gt=0)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Listar libros con stock bajo (menos de 5 unidades)
        Caso de uso: Listado filtrado por stock
        """
        threshold = int(request.query_params.get('threshold', 5))
        books = self.get_queryset().filter(stock__lt=threshold, is_available=True)
        serializer = BookListSerializer(books, many=True)
        return Response({
            'threshold': threshold,
            'count': books.count(),
            'books': serializer.data
        })

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Agrupar libros por categoría
        Caso de uso: Listado agrupado
        """
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({
                'error': 'Se requiere el parámetro category_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = Category.objects.get(id=category_id, is_active=True)
            books = self.get_queryset().filter(category=category)
            
            return Response({
                'category': CategorySerializer(category).data,
                'books_count': books.count(),
                'books': BookListSerializer(books, many=True).data
            })
        except Category.DoesNotExist:
            return Response({
                'error': 'Categoría no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def search_advanced(self, request):
        """
        Búsqueda avanzada de libros
        Caso de uso: Búsqueda compleja con múltiples criterios
        """
        # Validar parámetros de búsqueda
        filter_serializer = BookFilterSerializer(data=request.query_params)
        if not filter_serializer.is_valid():
            return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Construir query
        queryset = self.get_queryset()
        validated_data = filter_serializer.validated_data
        
        # Aplicar filtros
        if 'title' in validated_data:
            queryset = queryset.filter(title__icontains=validated_data['title'])
        
        if 'author' in validated_data:
            queryset = queryset.filter(author__icontains=validated_data['author'])
        
        if 'category' in validated_data:
            queryset = queryset.filter(category_id=validated_data['category'])
        
        if 'min_price' in validated_data:
            queryset = queryset.filter(price__gte=validated_data['min_price'])
        
        if 'max_price' in validated_data:
            queryset = queryset.filter(price__lte=validated_data['max_price'])
        
        if 'is_available' in validated_data:
            queryset = queryset.filter(is_available=validated_data['is_available'])
        
        if 'has_discount' in validated_data:
            if validated_data['has_discount']:
                queryset = queryset.filter(discount_percentage__gt=0)
            else:
                queryset = queryset.filter(discount_percentage=0)
        
        # Serializar resultados
        serializer = BookListSerializer(queryset, many=True)
        
        return Response({
            'filters_applied': validated_data,
            'total_results': queryset.count(),
            'books': serializer.data
        })


# ========== VISTAS PARA TEMPLATES ==========

from django.shortcuts import render

def book_list_view(request):
    """Vista para mostrar la lista de libros en template"""
    return render(request, 'books/book_list.html')

def category_list_view(request):
    """Vista para mostrar la lista de categorías en template"""
    return render(request, 'books/category_list.html')
