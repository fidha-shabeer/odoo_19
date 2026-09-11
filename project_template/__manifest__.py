# -*- coding: utf-8 -*-
{
    'name': "Project Template",
    'version': "19.0.1.0.0",
    'category': "project template",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base', 'project'],
    'data': ['security/ir.model.access.csv',
             'security/security_group.xml',
             'views/project_project.xml',
             'views/project_task.xml',
             'views/project_template.xml',
             'views/project_task_template.xml',
             'views/project_template_menu.xml',
             ]
}
