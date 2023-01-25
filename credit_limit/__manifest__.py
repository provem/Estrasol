{
    'name': 'Credit Limits',
    'version': '1.0',
    'description': 'Credit Limits for partners',
    'summary': '',
    'author': 'Estrasol - Santiago Ramos Morales',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'base', 'sale', 'contacts', 'sale_stock'
    ],
    'data': [
        'views/inherit_partner_views.xml',
        'views/inherit_sale_order_views.xml',
        'security/groups.xml'
    ],
    'demo': [
        ''
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}