# Generated by Django 4.0.3 on 2025-02-22 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_pod_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Failed', 'Failed'), ('Success', 'Success'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('pod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pod')),
            ],
        ),
    ]
