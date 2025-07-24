from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Category(models.Model):
    """Modelo para categorías de libros"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Modelo para libros"""
    title = models.CharField(max_length=200, verbose_name="Título")
    author = models.CharField(max_length=150, verbose_name="Autor")
    isbn = models.CharField(max_length=17, unique=True, verbose_name="ISBN")
    description = models.TextField(verbose_name="Descripción")
    publication_date = models.DateField(verbose_name="Fecha de publicación")
    pages = models.PositiveIntegerField(verbose_name="Número de páginas")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='books',
        verbose_name="Categoría"
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        verbose_name="Porcentaje de descuento"
    )
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.author}"

    @property
    def discounted_price(self):
        """Calcula el precio con descuento aplicado"""
        if self.discount_percentage > 0:
            discount_amount = self.price * (self.discount_percentage / 100)
            return self.price - discount_amount
        return self.price

    def apply_discount(self, percentage):
        """Aplica un descuento al libro"""
        if 0 <= percentage <= 100:
            self.discount_percentage = Decimal(str(percentage))
            self.save()
            return True
        return False

    def update_stock(self, quantity):
        """Actualiza el stock del libro"""
        if self.stock + quantity >= 0:
            self.stock += quantity
            self.save()
            return True
        return False
