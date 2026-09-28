from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_shelf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelf',
            name='is_public',
            field=models.BooleanField(default=False, help_text='Let other users view this shelf.'),
        ),
    ]
