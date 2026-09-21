from django.db import migrations, models


def mark_existing_sheets(apps, schema_editor):
    """Carry existing assets over to the new static-sprite / spritesheet split.

    Until now every asset was treated as a sheet, with a 32x32 default frame
    size.  Assets whose frame size was changed from that default were clearly
    set up as animated sheets, so they stay sheets.  Everything else becomes a
    plain static sprite (and loses the meaningless default frame size).
    """
    Asset = apps.get_model("feature_asset", "Asset")
    Asset.objects.exclude(frame_width=32, frame_height=32).update(is_spritesheet=True)
    Asset.objects.filter(is_spritesheet=False).update(frame_width=None, frame_height=None)


def restore_default_frame_sizes(apps, schema_editor):
    Asset = apps.get_model("feature_asset", "Asset")
    Asset.objects.filter(frame_width__isnull=True).update(frame_width=32)
    Asset.objects.filter(frame_height__isnull=True).update(frame_height=32)


class Migration(migrations.Migration):

    dependencies = [
        ("feature_asset", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="is_spritesheet",
            field=models.BooleanField(
                default=False,
                help_text="Tick if this image is a sheet of animation frames rather than a single sprite.",
            ),
        ),
        migrations.AlterField(
            model_name="asset",
            name="frame_width",
            field=models.PositiveIntegerField(
                blank=True, null=True, help_text="Width of a single animation frame, in pixels."
            ),
        ),
        migrations.AlterField(
            model_name="asset",
            name="frame_height",
            field=models.PositiveIntegerField(
                blank=True, null=True, help_text="Height of a single animation frame, in pixels."
            ),
        ),
        migrations.RunPython(mark_existing_sheets, restore_default_frame_sizes),
    ]
