# Generated by Django 4.1.2 on 2023-04-18 10:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentUid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('status', models.CharField(max_length=10)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
