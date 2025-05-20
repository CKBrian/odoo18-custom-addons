# -*- coding: utf-8 -*-
{
    'name': "Estate Accounting Integration",

    'summary': "Generates invoices for sold properties in the Estate module.e",

    'description': """
		This module extends the Estate module by integrating it with Odoo Accounting.
		When a property is marked as sold, a customer invoice is automatically created
		for the buyer based on the selling price of the property.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['estate', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
         'views/views.xml',
         'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

