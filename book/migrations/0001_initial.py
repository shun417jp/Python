# Generated by Django 4.2 on 2025-02-03 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('category', models.CharField(choices=[('business', 'ビジネス'), ('life', '生活'), ('hobby', '趣味'), ('other', 'その他')], max_length=100)),
            ],
        ),
    ]
