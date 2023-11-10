# Generated by Django 4.2.5 on 2023-11-06 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_date', models.DateField(default='2023-11-06T')),
                ('is_active', models.BooleanField(default=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
    ]
