from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feature_asset", "0002_asset_is_spritesheet"),
    ]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="frame_offset_x",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="asset",
            name="frame_offset_y",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
