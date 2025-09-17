{
    'name': 'Estate',  # Name (app list)
    'author': 'DataMind (aka. Rune Van den Heuvel)', # Author
    'version': '18.0.1.0.14',  # Version
    'application': True,  # Indicate the module is an application, not a module
    'depends': ['base'],  # Define dependencies
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml'
    ],
    'installable': True,
    'license': 'LGPL-3',
}