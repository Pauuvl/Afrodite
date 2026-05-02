from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0002_cartitem_product_alter_cartitem_product_name_and_more'),
        ('catalogo', '0004_producto_stock_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[('pending', 'Pendiente'), ('paid', 'Pagado'), ('cancelled', 'Cancelado')],
                default='pending',
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carrito.order')),
                ('product', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='catalogo.producto'
                )),
            ],
        ),
    ]
