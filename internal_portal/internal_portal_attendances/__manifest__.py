# noinspection PyStatementEffect
{
	'name': "Internal Portal Attendances",
	'summary': """Internal Portal Attendances""",
	'author': "Arxi",
	'website': "https://www.arxi.pt",
	'license': 'OPL-1',
	'category': 'Uncategorized',
	'version': '19.0.0.0.6',
	'depends': [
		'base_internal_portal',
		'hr_attendance'
	],
	'data': [
		# Security
		'security/groups.xml',
		# Portal Views
		'views/hr_attendances_portal_templates.xml',
		'views/internal_portal_check_in_out.xml'
	],
	'assets': {
		'web.assets_frontend': [
			'internal_portal_attendances/static/src/styles/check_in_out.scss'
		]
	},
}
