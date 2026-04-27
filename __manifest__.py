{
    'name': 'Sale Margin without Delivery',
    'version': '19.0.1.0.0',
    'summary': 'Excluye el costo de envío del cálculo del margen en órdenes de venta',
    'description': """
        Cuando se activa la función "Márgenes" en órdenes de venta, este módulo
        recalcula el margen total de la orden excluyendo las líneas de envío,
        ya que el cliente paga el costo de envío.

        El margen total y el porcentaje de margen mostrados en la orden
        reflejan únicamente los productos vendidos, sin incluir el envío.
    """,
    'category': 'Sales/Sales',
    'author': 'Custom',
    'depends': ['sale_margin', 'delivery'],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
