# from odoo.addons.product_sale_history.scripts.sale_excel_import import import_excel,eraseDataImported,checkIfUserCreated
# import_excel(self, '/tmp/books_test.xlsx', 5)
# import_excel(self, '/home/arxisd/Downloads/books.xlsx', 5)
# checkIfUserCreated(self, '/home/arxisd/Downloads/books.xlsx')
import math
import os
import pandas as pd
from odoo import _
from odoo.exceptions import ValidationError
from odoo.tests import Form
import logging
_logger = logging.getLogger(__name__)


# NOS ALIVE 2023
nos_alive_2023 = {
    'product_06_julho' : 4246,
    'product_07_julho' : 4247,
    'product_08_julho' : 4248
}

# NOS ALIVE 2024
nos_alive_2024 = {
    'Dia 11 Julho' : 4322,
    'Dia 12 Julho' : 4323,
    'Dia 13 Julho' : 4324
}

# NOS ALIVE 2025
nos_alive_2025 = {
    'Dia 10 Julho' : 4405,
    'Dia 11 Julho' : 4406,
    'Dia 12 Julho' : 4407
}

# NOS ALIVE 2024 2ºbatch TODO Update after importing pdf's
nos_alive_2024_2batch = {
    '11-Jul-2024 2Vaga' : 4329,
    '12-Jul-2024 2Vaga' : 4330,
}


def eraseDataImported(self):  # TODO Delete before commit

    for p in self.env['res.partner'].search([('email', 'like', '%@heiway.net')]):
        for s in self.env['sale.order'].browse(p.sale_order_ids.ids):
            s.unlink()

        try:
            name = p.name
            p.unlink()
            self.env.cr.commit()
            _logger.info(f'Contact [{name}]')
        except Exception as e:
            raise ValidationError(f"Not able to erase contact {p.name}: {e}")
    _logger.info('All demo contacts erased')

def customer_domain_NOS_ALIVE_2023(sale, company_id):
    return [
            '|',
            ('email', '=', sale.get('Email')),
            ('vat', '=', sale.get('NIF')),
            ('company_id', '=', company_id.id)
            ]

def customer_domain_NOS_ALIVE_2024(sale, company_id):
    return [
            '|',
            ('email', '=', sale.get('Email')),
            ('vat', '=', str(sale.get('NIF'))),
            ('company_id', '=', company_id.id)
        ]

# from odoo.addons.product_sale_history.scripts.sale_excel_import import getCustomerInfo
# getCustomerInfo(self, e[0], company_id)
def getCustomerInfo(self, sale, company_id):
    customer = self.env['res.partner'].search(customer_domain_NOS_ALIVE_2024(sale, company_id))
    if len(customer) > 1:
        temp_customer = self.env['res.partner']
        for i in range(len(customer)):
            if not temp_customer or customer[i].create_date < temp_customer.create_date:
                temp_customer = customer[i]
        customer = temp_customer

    if not customer:
        new_customer = {
            'company_id'    : company_id.id,
            'name'          : sale['Name'],
            'email'         : sale['Email'],
            'mobile'        : sale['Telemóvel'],
            'category_id'   : self.env.ref('product_sale_history.res_partner_category_exclusive_sale').ids + [3]
        }
        try:
            customer = self.env['res.partner'].create(new_customer)
            # _logger.info(f"New customer created: {customer.name}")
            customer.update({
                'vat': 'PT' + str(int(round(sale['NIF'], 0))) if not math.isnan(sale['NIF']) else False
            })
        except Exception as e:
            _logger.info(f'Error creating customer {new_customer}:\n {e}')
    elif customer.mobile == False:
        customer.update({
            'mobile': sale['Telemóvel'],
        })
    return customer

def get_product_nos_alive_2023():
    return ['Dia 6 Julho', 'Dia 7 Julho', 'Dia 8 Julho']

def get_product_nos_alive_2024():
    return ['Dia 11 Julho', 'Dia 12 Julho', 'Dia 13 Julho']

def get_product_nos_alive_2025():
    return ['Dia 10 Julho', 'Dia 11 Julho', 'Dia 12 Julho']

def get_product_nos_alive_2024_2batch():
    return ['11-Jul-2024 2Vaga', '12-Jul-2024 2Vaga']

def get_sale_order_journal(self, sale):
    domain = [('sale_type_id', '=', self.env.ref('sale_journals.t_quotation').id)]

    if sale['id_journal'] != '':
        domain += [('id', '=', int(sale['id_journal']))]

    elif sale['sale_journal'] != '':
        domain += [('name', '=', sale['sale_journal'])]

    else:
        return False

    return self.env['sale.order.journal'].search(domain)

def getSaleOrderLines(self, sale, new_sale, company_id):
    sale_orders = self.env['sale.order.line']
    column_names = get_product_nos_alive_2025()
    for name in column_names:
        if sale[name] <= 0 or math.isnan(sale[name]):
            continue
        product_id = self.env['product.template'].with_company(company_id).browse(nos_alive_2025[name])
        if not product_id:
            raise ValidationError(_(f'Product {name} not found'))
        elif not product_id.taxes_id:
            raise ValidationError(_(f'Product {name} taxes not set'))

        new_sol = {
            'company_id'        : company_id.id,
            'order_id'          : new_sale.id,
            'product_id'        : product_id.product_variant_id.id,
            'price_unit'        : product_id.list_price,
            'name'              : product_id.name,
            'product_uom'       : product_id.uom_id.id,
            'product_uom_qty'   : sale[name],
            'tax_id'            : product_id.taxes_id.ids
        }
        try:
            sale_orders += self.env['sale.order.line'].create(new_sol)
            # _logger.info(f"New sale order line created for sale order ({new_sale.id}): {sale_orders[-1].id}")
        except Exception as e:
            raise ValidationError(_(f'Error creating sale.order.line {new_sol}:\n{e}'))
    return sale_orders

# from odoo.addons.product_sale_history.scripts.sale_excel_import import import_excel
# Local paths
# import_excel(self, '/home/adminarxi/Documentos/funny/nos_alive_2024.xlsx', 5)
# import_excel(self, '/home/adminarxi/Documents/funny/tickets_01_2024/NOS_Alive 2024_2_batch.xlsx' , 5)
# import_excel(self, '/home/adminarxi/Documents/funny/tickets_01_2024/NOS_Alive 2024_2_batch_copy.xlsx' , 5)
#
# Odoo.sh paths
# import_excel(self, '/tmp/nos_alive_2024.xlsx', 5)
# import_excel(self, '/tmp/NOS_Alive 2024_2_batch.xlsx', 5)
def import_excel(self, file_path, company_id):
    if not company_id:
        raise ValidationError(_("Not company_id set"))

    company_id = self.env['res.company'].browse(company_id)
    if not company_id:
        raise ValidationError(_(f'Company by id ({company_id} not found)'))
    excel_data = readExcel(self, file_path)
    counter = 0
    total_lines = len(excel_data)
    for sale in excel_data:

        counter += 1

        if counter % 50 == 0:
            _logger.info(f"*********************************************************************")
            _logger.info(f"{counter}/{total_lines} lines imported from {file_path.split('/')[-1]}")
            _logger.info(f"*********************************************************************")

        if sale['Email'] == '':
            continue

        contact = getCustomerInfo(self, sale, company_id)
        if not contact:
            continue

        if self.env.ref('product_sale_history.res_partner_category_exclusive_sale').id not in contact.category_id.ids:
            contact.write({
                'category_id': self.env.ref('product_sale_history.res_partner_category_exclusive_sale').ids + contact.category_id.ids
            })

        sale_order_journal_id = get_sale_order_journal(self, sale)

        if not sale_order_journal_id:
            _logger.info(f'Quotation journal {sale["sale_journal"]} or with Id.{sale["id_journal"]} not found')
            _logger.info(f'Sale for customer {sale["Name"]} not concluded')
            continue

        new_sale = {
            'company_id'        : company_id.id,
            'partner_id'        : contact.id,
            'require_payment'   : True,
            'require_signature' : False,
            'team_id'           : 16,
            'sale_journal'        : sale_order_journal_id.id
        }
        try:
            new_sale = self.env['sale.order'].create(new_sale)
            # _logger.info(f"New sale order created: {new_sale.id}")
        except Exception as e:
            raise ValidationError(_(f"Error creating {new_sale}:\n{e}"))

        new_sale.update({
            'order_line': getSaleOrderLines(self, sale, new_sale, company_id)
        })

        if new_sale.order_line:
            # self.env.cr.commit()
            new_sale.action_quotation_sent()
            mail_template = self.env.ref('product_sale_history.mail_template_sale_order_tickets')
            if mail_template and mail_template.lang:
                lang = mail_template._render_lang(new_sale.ids)[new_sale.id]
            ctx = {
                'default_model': 'sale.order',
                'default_res_ids': [new_sale.id],
                'default_use_template': bool(mail_template),
                'default_template_id': mail_template.id if mail_template else None,
                'default_composition_mode': 'comment',
                'mark_so_as_sent': True,
                'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
                'proforma': self.env.context.get('proforma', False),
                'force_email': True,
                'model_description': new_sale.with_context(lang=lang).type_name,
            }

            form = Form(self.env['mail.compose.message'].with_context(ctx))
            saved_form = form.save()
            saved_form._action_send_mail()
        self.env.cr.commit()


    _logger.info(f"*********************************************************************")
    _logger.info(f"Contacts and sale order from xmls {file_path.split('/')[-1]} imported")
    _logger.info(f"*********************************************************************")

# from odoo.addons.product_sale_history.scripts.sale_excel_import import readExcel
# readExcel(self, '/home/adminarxi/Documents/casper/Book4.xlsx')
# readExcel(self, '/home/adminarxi/Documents/casper/nos_alive_2024.xlsx')
def readExcel(self, file_path):
    if not os.path.isfile(file_path):
        raise ValidationError(_("File path it doesn't correspond to a file"))
    elif os.path.splitext(file_path)[-1].lower() != ".xlsx":
        raise ValidationError(_(f"File not Excel type: {file_path}"))

    data_frame = pd.read_excel(file_path)

    dict_keys = {}
    for column_name in data_frame.columns:
        dict_keys.update({column_name: ''})

    excel_dict = []
    try:
        for index, row in data_frame.iterrows():
            tmp_dict = {}
            for key in dict_keys.keys():
                tmp_dict.update({key: row[key]})
            excel_dict += [tmp_dict]
    except Exception as e:
        raise ValidationError(_(f"Error reading excel file:\n {e}"))

    return excel_dict

# from odoo.addons.product_sale_history.scripts.sale_excel_import import checkIfUserCreated
# checkIfUserCreated(self, '/home/adminarxi/Documents/casper/nos_alive_2024.xlsx')
def checkIfUserCreated(self, file_path):
    users_not_found = []
    users = 0
    missing = 0
    lines = len(readExcel(self, file_path))
    for line in readExcel(self, file_path):
        if not self.env['res.partner'].search([('email', '=', line.get('Email'))]):
            tmp_dict = {}
            for key in line.keys():
                tmp_dict.update({
                    key: line.get(key)
                })
            users_not_found += [tmp_dict]
            missing += 1
        else:
            users += 1
    _logger.info(f"\nExcel lines: {lines}\nFound: {users}\nMissing: {missing}")
    if users_not_found:
        _logger.info(f"Users not found:\n{users_not_found}")
    else:
        _logger.info("All users found")