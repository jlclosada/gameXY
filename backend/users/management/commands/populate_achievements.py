from django.core.management.base import BaseCommand
from users.models import Achievement


class Command(BaseCommand):
    help = 'Poblar logros predefinidos en la base de datos'

    def handle(self, *args, **kwargs):
        achievements_data = [
            # Creación de Contenido
            {
                'code': 'first_guide',
                'name': 'Primera Guía',
                'description': 'Publica tu primera guía',
                'icon': '📖',
                'category': 'content',
                'points': 10,
                'requirement_value': 1
            },
            {
                'code': 'guide_master',
                'name': 'Maestro de Guías',
                'description': 'Publica 10 guías',
                'icon': '📚',
                'category': 'content',
                'points': 50,
                'requirement_value': 10
            },
            {
                'code': 'guide_legend',
                'name': 'Leyenda de Guías',
                'description': 'Publica 50 guías',
                'icon': '🏆',
                'category': 'content',
                'points': 200,
                'requirement_value': 50
            },
            # Engagement
            {
                'code': 'first_comment',
                'name': 'Primera Opinión',
                'description': 'Deja tu primer comentario',
                'icon': '💬',
                'category': 'engagement',
                'points': 5,
                'requirement_value': 1
            },
            {
                'code': 'social_butterfly',
                'name': 'Mariposa Social',
                'description': 'Deja 100 comentarios',
                'icon': '🦋',
                'category': 'engagement',
                'points': 50,
                'requirement_value': 100
            },
            {
                'code': 'popular_guide',
                'name': 'Guía Popular',
                'description': 'Una de tus guías recibe 50 likes',
                'icon': '⭐',
                'category': 'content',
                'points': 30,
                'requirement_value': 50
            },
            {
                'code': 'viral_guide',
                'name': 'Guía Viral',
                'description': 'Una de tus guías alcanza 1000 vistas',
                'icon': '🔥',
                'category': 'content',
                'points': 75,
                'requirement_value': 1000
            },
            # Social
            {
                'code': 'first_favorite',
                'name': 'Primer Favorito',
                'description': 'Marca tu primer juego como favorito',
                'icon': '❤️',
                'category': 'social',
                'points': 5,
                'requirement_value': 1
            },
            {
                'code': 'game_collector',
                'name': 'Coleccionista',
                'description': 'Marca 20 juegos como favoritos',
                'icon': '🎮',
                'category': 'social',
                'points': 25,
                'requirement_value': 20
            },
            {
                'code': 'guide_saver',
                'name': 'Curador',
                'description': 'Guarda 10 guías para leer después',
                'icon': '📑',
                'category': 'social',
                'points': 15,
                'requirement_value': 10
            },
            # Antigüedad
            {
                'code': 'veteran_30',
                'name': 'Veterano',
                'description': 'Miembro por 30 días',
                'icon': '🎖️',
                'category': 'time',
                'points': 20,
                'requirement_value': 30
            },
            {
                'code': 'veteran_365',
                'name': 'Veterano de Oro',
                'description': 'Miembro por 1 año',
                'icon': '👑',
                'category': 'time',
                'points': 100,
                'requirement_value': 365
            },
            # Especiales
            {
                'code': 'early_adopter',
                'name': 'Adoptante Temprano',
                'description': 'Uno de los primeros 100 usuarios',
                'icon': '🌟',
                'category': 'special',
                'points': 50,
                'requirement_value': 100
            },
            {
                'code': 'helpful',
                'name': 'Útil',
                'description': 'Tus guías reciben una valoración promedio de 4.5+',
                'icon': '✨',
                'category': 'content',
                'points': 40,
                'requirement_value': 45
            },
        ]

        created_count = 0
        updated_count = 0

        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.update_or_create(
                code=achievement_data['code'],
                defaults=achievement_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Creado: {achievement}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'⟳ Actualizado: {achievement}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Completado: {created_count} creados, {updated_count} actualizados'))
