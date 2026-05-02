from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MensajeContacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField()),
                ('asunto', models.CharField(
                    choices=[
                        ('pedido', 'Consulta sobre pedido'),
                        ('producto', 'Información de producto'),
                        ('devolucion', 'Devolución o cambio'),
                        ('otro', 'Otro'),
                    ],
                    default='otro',
                    max_length=20,
                )),
                ('mensaje', models.TextField()),
                ('leido', models.BooleanField(default=False)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Mensaje de contacto',
                'verbose_name_plural': 'Mensajes de contacto',
                'ordering': ['-creado_en'],
            },
        ),
    ]
