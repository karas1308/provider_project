# Generated by Django 4.2.5 on 2023-11-06 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=255)),
                ('media', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.city')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.region'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.IntegerField()),
                ('apt', models.IntegerField(blank=True)),
                ('entrance', models.IntegerField(blank=True)),
                ('floor', models.IntegerField(blank=True)),
                ('street', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.street')),
            ],
        ),
    ]
