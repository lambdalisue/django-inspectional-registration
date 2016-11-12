from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_default_supplement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationprofile',
            name='_status',
            field=models.CharField(choices=[('untreated', 'Unprocessed'), ('accepted', 'Registration accepted'), ('rejected', 'Registration rejected')], db_column='status', default='untreated', editable=False, max_length=10, verbose_name='status'),
        ),
    ]
