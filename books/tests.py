from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import date
from books.models import Book, Category


class CategoryModelTest(TestCase):
    """Pruebas para el modelo Category"""

    def setUp(self):
        self.category = Category.objects.create(
            name="Ficción",
            description="Libros de ficción literaria"
        )

    def test_category_creation(self):
        """Test de creación de categoría"""
        self.assertEqual(self.category.name, "Ficción")
        self.assertEqual(self.category.description, "Libros de ficción literaria")
        self.assertTrue(self.category.is_active)
        self.assertIsNotNone(self.category.created_at)

    def test_category_str_method(self):
        """Test del método __str__ de Category"""
        self.assertEqual(str(self.category), "Ficción")

    def test_category_unique_name(self):
        """Test que el nombre de categoría sea único"""
        with self.assertRaises(Exception):
            Category.objects.create(name="Ficción")


class BookModelTest(TestCase):
    """Pruebas para el modelo Book"""

    def setUp(self):
        self.category = Category.objects.create(
            name="Ciencia Ficción",
            description="Libros de ciencia ficción"
        )
        self.book = Book.objects.create(
            title="Dune",
            author="Frank Herbert",
            isbn="978-0441013593",
            description="Una épica historia de ciencia ficción",
            publication_date=date(1965, 8, 1),
            pages=688,
            price=Decimal('25.99'),
            stock=10,
            category=self.category
        )

    def test_book_creation(self):
        """Test de creación de libro"""
        self.assertEqual(self.book.title, "Dune")
        self.assertEqual(self.book.author, "Frank Herbert")
        self.assertEqual(self.book.price, Decimal('25.99'))
        self.assertEqual(self.book.stock, 10)
        self.assertTrue(self.book.is_available)

    def test_book_str_method(self):
        """Test del método __str__ de Book"""
        expected = "Dune - Frank Herbert"
        self.assertEqual(str(self.book), expected)

    def test_discounted_price_without_discount(self):
        """Test precio sin descuento"""
        self.assertEqual(self.book.discounted_price, Decimal('25.99'))

    def test_discounted_price_with_discount(self):
        """Test precio con descuento"""
        self.book.discount_percentage = Decimal('20.00')
        # Precio exacto calculado: 25.99 - (25.99 * 0.20) = 20.792
        expected_price = Decimal('20.79')  # Redondeado a 2 decimales
        # Usar almostEqual para decimales con pequeñas diferencias
        self.assertAlmostEqual(float(self.book.discounted_price), float(expected_price), places=1)

    def test_apply_discount_valid(self):
        """Test aplicar descuento válido"""
        result = self.book.apply_discount(15)
        self.assertTrue(result)
        self.assertEqual(self.book.discount_percentage, Decimal('15.00'))

    def test_apply_discount_invalid(self):
        """Test aplicar descuento inválido"""
        result = self.book.apply_discount(150)
        self.assertFalse(result)
        self.assertEqual(self.book.discount_percentage, Decimal('0.00'))

    def test_update_stock_positive(self):
        """Test actualizar stock positivamente"""
        result = self.book.update_stock(5)
        self.assertTrue(result)
        self.assertEqual(self.book.stock, 15)

    def test_update_stock_negative_valid(self):
        """Test reducir stock válido"""
        result = self.book.update_stock(-3)
        self.assertTrue(result)
        self.assertEqual(self.book.stock, 7)

    def test_update_stock_negative_invalid(self):
        """Test reducir stock más de lo disponible"""
        result = self.book.update_stock(-15)
        self.assertFalse(result)
        self.assertEqual(self.book.stock, 10)


class BookAPITest(APITestCase):
    """Pruebas para las APIs de Book"""

    def setUp(self):
        self.category = Category.objects.create(
            name="Programación",
            description="Libros de programación"
        )
        self.book_data = {
            'title': 'Python para Todos',
            'author': 'Guido van Rossum',
            'isbn': '978-0134757599',
            'description': 'Aprende Python desde cero',
            'publication_date': '2020-01-15',
            'pages': 300,
            'price': '29.99',
            'stock': 5,
            'category': self.category.id
        }

    def test_create_book_api(self):
        """Test crear libro vía API"""
        url = reverse('book-list')
        response = self.client.post(url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

    def test_list_books_api(self):
        """Test listar libros vía API"""
        Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="123456789",
            description="Test description",
            publication_date=date(2023, 1, 1),
            pages=200,
            price=Decimal('19.99'),
            category=self.category
        )
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que hay resultados (puede ser paginado)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_book_detail_api(self):
        """Test obtener detalle de libro vía API"""
        book = Book.objects.create(
            title="Detail Book",
            author="Detail Author",
            isbn="987654321",
            description="Detail description",
            publication_date=date(2023, 1, 1),
            pages=250,
            price=Decimal('24.99'),
            category=self.category
        )
        url = reverse('book-detail', kwargs={'pk': book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Detail Book')

    def test_update_book_api(self):
        """Test actualizar libro vía API"""
        book = Book.objects.create(
            title="Update Book",
            author="Update Author",
            isbn="111222333",
            description="Update description",
            publication_date=date(2023, 1, 1),
            pages=300,
            price=Decimal('30.99'),
            category=self.category
        )
        url = reverse('book-detail', kwargs={'pk': book.id})
        updated_data = self.book_data.copy()
        updated_data['title'] = 'Libro Actualizado'
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_api(self):
        """Test eliminar libro vía API (soft delete)"""
        book = Book.objects.create(
            title="Delete Book",
            author="Delete Author",
            isbn="444555666",
            description="Delete description",
            publication_date=date(2023, 1, 1),
            pages=150,
            price=Decimal('15.99'),
            category=self.category
        )
        url = reverse('book-detail', kwargs={'pk': book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # El libro sigue existiendo pero marcado como no disponible (soft delete)
        book.refresh_from_db()
        self.assertFalse(book.is_available)


class CategoryAPITest(APITestCase):
    """Pruebas para las APIs de Category"""

    def setUp(self):
        self.category_data = {
            'name': 'Historia',
            'description': 'Libros de historia mundial'
        }

    def test_create_category_api(self):
        """Test crear categoría vía API"""
        url = reverse('category-list')
        response = self.client.post(url, self.category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_list_categories_api(self):
        """Test listar categorías vía API"""
        Category.objects.create(name="Test Category")
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que hay resultados (puede ser paginado)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_delete_category_api(self):
        """Test eliminar categoría vía API (soft delete)"""
        category = Category.objects.create(name="Delete Category")
        url = reverse('category-detail', kwargs={'pk': category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # La categoría sigue existiendo pero marcada como inactiva (soft delete)
        category.refresh_from_db()
        self.assertFalse(category.is_active)


class DiscountAPITest(APITestCase):
    """Pruebas para funcionalidad de descuentos"""

    def setUp(self):
        self.category = Category.objects.create(name="Ofertas")
        self.book = Book.objects.create(
            title="Libro con Descuento",
            author="Autor Descuento",
            isbn="777888999",
            description="Libro para probar descuentos",
            publication_date=date(2023, 1, 1),
            pages=200,
            price=Decimal('50.00'),
            category=self.category
        )

    def test_apply_discount_api(self):
        """Test aplicar descuento vía API"""
        url = reverse('book-apply-discount', kwargs={'pk': self.book.id})
        discount_data = {'discount_percentage': 25}
        response = self.client.post(url, discount_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el descuento se aplicó
        self.book.refresh_from_db()
        self.assertEqual(self.book.discount_percentage, Decimal('25.00'))
        # Usar almostEqual para verificar el precio con descuento
        self.assertAlmostEqual(float(self.book.discounted_price), 37.50, places=2)
