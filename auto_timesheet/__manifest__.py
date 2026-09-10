{
    'name': 'Auto Timesheet',
    'version': "19.0.1.0.0",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','hr','project'],
    'data': [
        "views/hr_employee.xml",
        "views/project_task.xml",
        "views/project_project.xml",
    ]
}