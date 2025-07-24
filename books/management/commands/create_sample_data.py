from django.core.management.base import BaseCommand
from django.db import transaction
from books.models import Category, Book
from decimal import Decimal
from datetime import date


class Command(BaseCommand):
    help = 'Crea datos de ejemplo para la aplicación de libros'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(
                self.style.WARNING('🗑️  Eliminando datos existentes...')
            )
            Book.objects.all().delete()
            Category.objects.all().delete()

        with transaction.atomic():
            self.stdout.write(
                self.style.SUCCESS('🚀 Creando datos de ejemplo...')
            )
            
            # Crear categorías
            categories_data = [
                ('Ficción', 'Novelas y cuentos de ficción literaria'),
                ('Tecnología', 'Libros sobre programación y tecnología'),
                ('Ciencia', 'Libros científicos y de divulgación'),
                ('Historia', 'Libros de historia mundial y biografías'),
                ('Filosofía', 'Obras filosóficas y pensamiento'),
                ('Arte', 'Libros sobre arte, música y cultura'),
                ('Biografías', 'Historias de vida de personajes importantes'),
                ('Negocios', 'Libros sobre emprendimiento y finanzas'),
            ]
            
            created_categories = {}
            for name, description in categories_data:
                category, created = Category.objects.get_or_create(
                    name=name,
                    defaults={'description': description}
                )
                created_categories[name] = category
                if created:
                    self.stdout.write(f"📂 Categoría creada: {name}")

            # Crear libros de ejemplo
            books_data = [
                {
                    'title': 'Cien años de soledad',
                    'author': 'Gabriel García Márquez',
                    'isbn': '978-0060883287',
                    'description': 'Una obra maestra del realismo mágico que narra la historia de la familia Buendía a lo largo de varias generaciones.',
                    'publication_date': date(1967, 6, 5),
                    'pages': 417,
                    'price': Decimal('15.99'),
                    'stock': 25,
                    'category': created_categories['Ficción'],
                    'discount_percentage': Decimal('10.00')
                },
                {
                    'title': 'Clean Code: A Handbook of Agile Software Craftsmanship',
                    'author': 'Robert C. Martin',
                    'isbn': '978-0132350884',
                    'description': 'Manual de estilo para el desarrollo ágil de software. Principios y técnicas para escribir código limpio y mantenible.',
                    'publication_date': date(2008, 8, 1),
                    'pages': 464,
                    'price': Decimal('42.99'),
                    'stock': 8,
                    'category': created_categories['Tecnología']
                },
                {
                    'title': 'Sapiens: De animales a dioses',
                    'author': 'Yuval Noah Harari',
                    'isbn': '978-0062316097',
                    'description': 'Breve historia de la humanidad desde la aparición del Homo sapiens hasta la actualidad. Una reflexión fascinante sobre nuestro pasado, presente y futuro.',
                    'publication_date': date(2014, 2, 10),
                    'pages': 443,
                    'price': Decimal('18.99'),
                    'stock': 15,
                    'category': created_categories['Historia'],
                    'discount_percentage': Decimal('15.00')
                },
                {
                    'title': 'Python Crash Course',
                    'author': 'Eric Matthes',
                    'isbn': '978-1593279288',
                    'description': 'Una introducción práctica a la programación en Python. Perfecto para principiantes que quieren aprender rápidamente.',
                    'publication_date': date(2019, 5, 3),
                    'pages': 544,
                    'price': Decimal('35.99'),
                    'stock': 3,  # Stock bajo para testing
                    'category': created_categories['Tecnología'],
                    'discount_percentage': Decimal('20.00')
                },
                {
                    'title': 'El origen de las especies',
                    'author': 'Charles Darwin',
                    'isbn': '978-0451529060',
                    'description': 'La teoría de la evolución que cambió para siempre nuestra comprensión de la vida en la Tierra.',
                    'publication_date': date(1859, 11, 24),
                    'pages': 502,
                    'price': Decimal('12.99'),
                    'stock': 12,
                    'category': created_categories['Ciencia']
                },
                {
                    'title': 'Don Quijote de la Mancha',
                    'author': 'Miguel de Cervantes',
                    'isbn': '978-0142437230',
                    'description': 'La obra cumbre de la literatura española y una de las novelas más importantes e influyentes de la historia universal.',
                    'publication_date': date(1605, 1, 16),
                    'pages': 863,
                    'price': Decimal('14.99'),
                    'stock': 20,
                    'category': created_categories['Ficción'],
                    'discount_percentage': Decimal('5.00')
                },
                {
                    'title': 'Django for Professionals',
                    'author': 'William S. Vincent',
                    'isbn': '978-1735467200',
                    'description': 'Desarrollo web profesional con Django. Desde conceptos básicos hasta despliegue en producción.',
                    'publication_date': date(2022, 1, 15),
                    'pages': 385,
                    'price': Decimal('39.99'),
                    'stock': 2,  # Stock bajo
                    'category': created_categories['Tecnología']
                },
                {
                    'title': 'Una breve historia del tiempo',
                    'author': 'Stephen Hawking',
                    'isbn': '978-0553380163',
                    'description': 'Del Big Bang a los agujeros negros. Física teórica explicada de manera accesible para el público general.',
                    'publication_date': date(1988, 4, 1),
                    'pages': 256,
                    'price': Decimal('16.99'),
                    'stock': 18,
                    'category': created_categories['Ciencia'],
                    'discount_percentage': Decimal('25.00')
                },
                {
                    'title': 'Así habló Zaratustra',
                    'author': 'Friedrich Nietzsche',
                    'isbn': '978-0140441185',
                    'description': 'Una obra filosófica fundamental que explora temas de moral, religión y el significado de la existencia.',
                    'publication_date': date(1883, 8, 24),
                    'pages': 352,
                    'price': Decimal('13.99'),
                    'stock': 10,
                    'category': created_categories['Filosofía']
                },
                {
                    'title': 'JavaScript: The Good Parts',
                    'author': 'Douglas Crockford',
                    'isbn': '978-0596517748',
                    'description': 'Guía esencial para dominar las mejores características de JavaScript y evitar sus partes problemáticas.',
                    'publication_date': date(2008, 5, 1),
                    'pages': 176,
                    'price': Decimal('29.99'),
                    'stock': 1,  # Stock muy bajo
                    'category': created_categories['Tecnología'],
                    'discount_percentage': Decimal('30.00')
                },
                {
                    'title': 'Steve Jobs',
                    'author': 'Walter Isaacson',
                    'isbn': '978-1451648539',
                    'description': 'La biografía definitiva del co-fundador de Apple, basada en más de cuarenta entrevistas exclusivas.',
                    'publication_date': date(2011, 10, 24),
                    'pages': 656,
                    'price': Decimal('22.99'),
                    'stock': 7,
                    'category': created_categories['Biografías'],
                    'discount_percentage': Decimal('12.00')
                },
                {
                    'title': 'El arte de la guerra',
                    'author': 'Sun Tzu',
                    'isbn': '978-1599869773',
                    'description': 'Tratado militar clásico chino que ha influido tanto en el pensamiento militar como en la filosofía empresarial moderna.',
                    'publication_date': date(1910, 1, 1),  # Edición moderna del texto clásico
                    'pages': 273,
                    'price': Decimal('9.99'),
                    'stock': 30,
                    'category': created_categories['Filosofía']
                },
            ]

            # Crear libros
            created_books = 0
            for book_data in books_data:
                book, created = Book.objects.get_or_create(
                    isbn=book_data['isbn'],
                    defaults=book_data
                )
                if created:
                    created_books += 1
                    status = "📚"
                    if book_data.get('discount_percentage', 0) > 0:
                        status += " 💰"
                    if book_data['stock'] < 5:
                        status += " ⚠️"
                    self.stdout.write(f"{status} Libro creado: {book_data['title']} - {book_data['author']}")

            # Mostrar estadísticas
            self.stdout.write(
                self.style.SUCCESS('\n📊 Resumen de datos creados:')
            )
            self.stdout.write(f"📂 Categorías: {Category.objects.count()}")
            self.stdout.write(f"📚 Libros totales: {Book.objects.count()}")
            self.stdout.write(f"💰 Libros con descuento: {Book.objects.filter(discount_percentage__gt=0).count()}")
            self.stdout.write(f"⚠️  Libros con stock bajo (<5): {Book.objects.filter(stock__lt=5).count()}")
            self.stdout.write(f"✅ Libros disponibles: {Book.objects.filter(is_available=True).count()}")
            
            self.stdout.write(
                self.style.SUCCESS('\n🎉 ¡Datos de ejemplo creados exitosamente!')
            )
            self.stdout.write(
                self.style.HTTP_INFO('💡 Ahora puedes visitar http://localhost:8000/books/ para ver la aplicación en acción')
            ) 