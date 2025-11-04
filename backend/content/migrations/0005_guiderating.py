from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0004_alter_guide_is_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='content.guide')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guide_ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'guide')},
            },
        ),
    ]
