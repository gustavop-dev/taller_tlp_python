from django.contrib import admin
from .models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configuración del admin para Category"""
    list_display = ['name', 'is_active', 'books_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def books_count(self, obj):
        """Mostrar cantidad de libros en la categoría"""
        return obj.books.filter(is_available=True).count()
    books_count.short_description = 'Libros Activos'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Configuración del admin para Book"""
    list_display = ['title', 'author', 'category', 'price', 'discounted_price', 
                   'discount_percentage', 'stock', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'publication_date', 'created_at']
    search_fields = ['title', 'author', 'isbn', 'description']
    readonly_fields = ['created_at', 'updated_at', 'discounted_price']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'author', 'isbn', 'description', 'category')
        }),
        ('Detalles de Publicación', {
            'fields': ('publication_date', 'pages')
        }),
        ('Precio y Stock', {
            'fields': ('price', 'discount_percentage', 'discounted_price', 'stock')
        }),
        ('Estado', {
            'fields': ('is_available',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def discounted_price(self, obj):
        """Mostrar precio con descuento"""
        return f"${obj.discounted_price:.2f}"
    discounted_price.short_description = 'Precio con Descuento'
