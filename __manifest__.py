{
    'name': "Bring Your Buddy",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail', 'hr', 'logic_base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/buddy.xml',
        'data/cron.xml',

    ],
    'demo': [],
    'summary': "bring_your_buddy",
    'description': "module_of_bring_your_buddy",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
