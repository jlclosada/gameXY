from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from community.models import Group, GroupMembership, Forum, Topic, Post
from games.models import Game

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate community with default forums, groups and sample content'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating community data...')
        
        # Get or create admin user
        admin_user = User.objects.filter(role='admin').first()
        if not admin_user:
            admin_user = User.objects.filter(role='goat').first()
        
        if not admin_user:
            self.stdout.write(self.style.WARNING('No admin or GOAT user found. Creating default admin...'))
            admin_user = User.objects.create_superuser(
                email='admin@gamexy.com',
                username='admin',
                password='admin123'
            )
            admin_user.role = 'admin'
            admin_user.save()
        
        self.stdout.write(f'Using user: {admin_user.username}')
        
        # Create Forums
        forums_data = [
            {
                'name': 'General',
                'slug': 'general',
                'description': 'Charla general sobre videojuegos y gaming',
                'icon': '💬',
                'category': 'general',
                'order': 1
            },
            {
                'name': 'Noticias de Gaming',
                'slug': 'noticias-gaming',
                'description': 'Últimas noticias y novedades del mundo gaming',
                'icon': '📰',
                'category': 'news',
                'order': 2
            },
            {
                'name': 'Guías y Tutoriales',
                'slug': 'guias-tutoriales',
                'description': 'Comparte y encuentra guías para tus juegos favoritos',
                'icon': '📚',
                'category': 'guides',
                'order': 3
            },
            {
                'name': 'Ayuda y Soporte',
                'slug': 'ayuda-soporte',
                'description': '¿Necesitas ayuda? Pregunta aquí',
                'icon': '🆘',
                'category': 'support',
                'order': 4
            },
            {
                'name': 'Discusión de Juegos',
                'slug': 'discusion-juegos',
                'description': 'Debate sobre tus juegos favoritos',
                'icon': '🎮',
                'category': 'games',
                'order': 5
            },
            {
                'name': 'Off Topic',
                'slug': 'off-topic',
                'description': 'Cualquier cosa que no tenga que ver con gaming',
                'icon': '🗨️',
                'category': 'off_topic',
                'order': 6
            },
        ]
        
        forums_created = 0
        for forum_data in forums_data:
            forum, created = Forum.objects.get_or_create(
                slug=forum_data['slug'],
                defaults=forum_data
            )
            if created:
                forums_created += 1
                self.stdout.write(f'  ✓ Created forum: {forum.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {forums_created} forums'))
        
        # Create Groups
        groups_data = [
            {
                'name': 'Competitivo Español',
                'slug': 'competitivo-espanol',
                'description': 'Grupo para jugadores competitivos de habla hispana. Organizamos torneos y scrims regularmente.',
                'is_public': True
            },
            {
                'name': 'Gamers Casuales',
                'slug': 'gamers-casuales',
                'description': 'Para quienes juegan por diversión sin presión competitiva. Ambiente relajado y amistoso.',
                'is_public': True
            },
            {
                'name': 'Retro Gaming',
                'slug': 'retro-gaming',
                'description': 'Amantes de los clásicos. Comparte tus recuerdos y descubre joyas olvidadas.',
                'is_public': True
            },
            {
                'name': 'Speedrunners',
                'slug': 'speedrunners',
                'description': 'Comunidad de speedrunning. Comparte tus récords y estrategias.',
                'is_public': True
            },
        ]
        
        groups_created = 0
        for group_data in groups_data:
            group, created = Group.objects.get_or_create(
                slug=group_data['slug'],
                defaults={
                    **group_data,
                    'creator': admin_user
                }
            )
            if created:
                groups_created += 1
                # Auto-join creator as admin
                GroupMembership.objects.get_or_create(
                    group=group,
                    user=admin_user,
                    defaults={'role': 'admin'}
                )
                self.stdout.write(f'  ✓ Created group: {group.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {groups_created} groups'))
        
        # Create sample topics in General forum
        general_forum = Forum.objects.get(slug='general')
        
        topics_data = [
            {
                'title': '¡Bienvenidos a GameXY!',
                'slug': 'bienvenidos-gamexy',
                'content': 'Bienvenidos a la comunidad de GameXY. Este es un espacio para compartir, aprender y conectar con otros gamers. ¡Preséntate y cuéntanos qué juegos te gustan!',
                'is_pinned': True
            },
            {
                'title': '¿Qué juego estáis jugando ahora?',
                'slug': 'que-juego-estais-jugando',
                'content': 'Abro este hilo para que compartamos qué estamos jugando actualmente. Yo acabo de empezar con un RPG increíble, ¿y vosotros?',
                'is_pinned': False
            },
            {
                'title': 'Consejos para nuevos jugadores',
                'slug': 'consejos-nuevos-jugadores',
                'content': '¿Qué consejos le darías a alguien que está empezando en el mundo gaming? Comparte tu sabiduría.',
                'is_pinned': False
            },
        ]
        
        topics_created = 0
        for topic_data in topics_data:
            topic, created = Topic.objects.get_or_create(
                forum=general_forum,
                slug=topic_data['slug'],
                defaults={
                    **topic_data,
                    'author': admin_user
                }
            )
            if created:
                topics_created += 1
                
                # Create sample replies
                if topic_data['slug'] == 'que-juego-estais-jugando':
                    Post.objects.get_or_create(
                        topic=topic,
                        author=admin_user,
                        defaults={
                            'content': 'Yo estoy enganchado a los roguelikes últimamente. No puedo parar de jugar.'
                        }
                    )
                
                self.stdout.write(f'  ✓ Created topic: {topic.title}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {topics_created} topics'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Community data populated successfully!'))
        self.stdout.write(f'   - {forums_created} forums')
        self.stdout.write(f'   - {groups_created} groups')
        self.stdout.write(f'   - {topics_created} topics')
