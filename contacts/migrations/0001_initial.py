# Generated by Django 3.1.5 on 2021-01-09 11:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('email', models.CharField(blank=True, max_length=255)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contacts.category')),
            ],
        ),
    ]
