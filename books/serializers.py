from rest_framework import serializers
from decimal import Decimal
from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para el modelo Category"""
    
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'books_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'books_count']
    
    def get_books_count(self, obj):
        """Retorna el número de libros en esta categoría"""
        return obj.books.filter(is_available=True).count()


class BookListSerializer(serializers.ModelSerializer):
    """Serializer para listado de libros (campos básicos)"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'discounted_price', 'discount_percentage', 
                 'stock', 'category_name', 'is_available', 'created_at']


class BookDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle completo de libros"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'description', 'publication_date', 
                 'pages', 'price', 'discounted_price', 'discount_percentage', 'stock', 
                 'category', 'category_name', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'discounted_price', 'created_at', 'updated_at']
    
    def validate_isbn(self, value):
        """Validar formato ISBN"""
        # Eliminar espacios y guiones
        isbn = value.replace('-', '').replace(' ', '')
        
        # Verificar longitud (ISBN-10 o ISBN-13)
        if len(isbn) not in [10, 13]:
            raise serializers.ValidationError("ISBN debe tener 10 o 13 dígitos")
        
        # Verificar que contenga solo dígitos y X (para ISBN-10)
        if not isbn[:-1].isdigit() or (len(isbn) == 10 and isbn[-1] not in '0123456789X'):
            raise serializers.ValidationError("ISBN contiene caracteres inválidos")
        
        return value
    
    def validate_discount_percentage(self, value):
        """Validar porcentaje de descuento"""
        if value < 0 or value > 100:
            raise serializers.ValidationError("El descuento debe estar entre 0 y 100%")
        return value
    
    def validate_price(self, value):
        """Validar que el precio sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0")
        return value


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear y actualizar libros"""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'description', 'publication_date', 
                 'pages', 'price', 'stock', 'category', 'discount_percentage', 'is_available']
    
    def validate_isbn(self, value):
        """Validar ISBN único"""
        instance = getattr(self, 'instance', None)
        if Book.objects.filter(isbn=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("Ya existe un libro con este ISBN")
        return value


class DiscountSerializer(serializers.Serializer):
    """Serializer para aplicar descuentos"""
    
    discount_percentage = serializers.DecimalField(
        max_digits=5, 
        decimal_places=2,
        min_value=Decimal('0.00'),
        max_value=Decimal('100.00')
    )
    
    def validate_discount_percentage(self, value):
        """Validar porcentaje de descuento"""
        if value < 0 or value > 100:
            raise serializers.ValidationError("El descuento debe estar entre 0% y 100%")
        return value


class StockUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar stock"""
    
    quantity = serializers.IntegerField()
    
    def validate_quantity(self, value):
        """Validar que la cantidad resulte en stock positivo"""
        book = self.context.get('book')
        if book and (book.stock + value) < 0:
            raise serializers.ValidationError(
                f"No se puede reducir el stock por debajo de 0. Stock actual: {book.stock}"
            )
        return value


class BookFilterSerializer(serializers.Serializer):
    """Serializer para filtros de búsqueda de libros"""
    
    title = serializers.CharField(required=False, max_length=200)
    author = serializers.CharField(required=False, max_length=150)
    category = serializers.IntegerField(required=False)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    is_available = serializers.BooleanField(required=False)
    has_discount = serializers.BooleanField(required=False)
    
    def validate(self, data):
        """Validaciones cruzadas"""
        min_price = data.get('min_price')
        max_price = data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise serializers.ValidationError("El precio mínimo no puede ser mayor al precio máximo")
        
        return data 