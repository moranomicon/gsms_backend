# Generated by Django 3.2 on 2021-05-24 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gsms', '0005_auto_20210520_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packinglistchangehistory',
            name='transfer_to',
        ),
        migrations.AddField(
            model_name='materialchangehistory',
            name='transfer_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='gsms.transferlocation'),
        ),
    ]
