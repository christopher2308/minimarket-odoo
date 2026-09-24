{
    'name': 'MiniMarket',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Gestión integral para un minimarket',
    'description': """
MiniMarket
==========

Aplicación para la gestión integral de un minimarket,
reutilizando y extendiendo la funcionalidad estándar de Odoo.
""",
    'author': 'Christian Bustamante',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'product',
        'purchase',
    ],

'data': [
    'security/minimarket_groups.xml',
    'security/ir.model.access.csv',
    'data/product_categories.xml',
    'views/product_template_views.xml',
    'views/purchase_order_views.xml',
    'views/purchase_price_change_views.xml',
],

    'installable': True,
    'application': True,
}