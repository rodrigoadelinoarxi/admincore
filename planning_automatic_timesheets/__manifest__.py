{
	'name': 'Planning Automatic Timesheets',
	'version': '19.0.1.0.5',
	'author': 'Casperventures',
	'summary': 'Creates timesheets automatically when a planning slot is published or sent.',
	'category': 'Human Resources/Planning',
	'depends': [
		'analytic', 'planning', 'hr_timesheet', 'project_timesheet_forecast'
	],
	'data': [
		'views/res_company_views.xml',
		'views/planning_slot_views.xml',
		'views/project_timesheet_forecast.xml'
	],
	'license': 'OPL-1',
}
