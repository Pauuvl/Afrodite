from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0003_producto_tipo_piel'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
    ]
