from odoo.tests.common import SavepointCase, tagged


@tagged('post_install', '-at_install')
class AccountTestPTInvoicingCommon(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(SavepointCase, cls).setUpClass()

        # Create user.
        user = cls.env['res.users'].create({
            'name': 'Because I am portuguese accountman!',
            'login': 'pt_accountman',
            'password': 'pt_accountman',
            'groups_id': [(6, 0, cls.env.user.groups_id.ids), (4, cls.env.ref('account.group_account_user').id)],
        })
        user.partner_id.email = 'accountman@test.com'

        # Shadow the current environment/cursor with one having the report user.
        # This is mandatory to test access rights.
        cls.env = cls.env(user=user)
        cls.cr = cls.env.cr
