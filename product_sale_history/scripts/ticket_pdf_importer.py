import base64
import textract
import os



from odoo import _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

# from odoo.addons.product_sale_history.scripts.ticket_pdf_importer import import_tickets
#
# Local
# import_tickets(self, '/home/adminarxi/Documents/funny/tickets', 5, 59.62)
# import_tickets(self, '/home/adminarxi/Documents/funny/tickets_test', 5, 59.62)
# import_tickets(self, '/home/adminarxi/Documents/funny/tickets_01_2024/test_pdfs', 5, 59.62, ' 2Vaga')
#
# SH
# import_tickets(self, '/tmp/tickets', 5, 59.62)
# import_tickets(self, '/tmp/pdfs', 5, 59.62, ' 2Vaga')
def import_tickets(self, folder, company_id, ticker_price, custom_name=''):
    if not ticker_price or ticker_price <= 0:
        raise ValidationError(_("No tickets price set"))

    if not os.path.isdir(folder):
        raise ValidationError(_("Path for import tickets is not a folder"))
    files = os.listdir(folder)

    if len(files) < 1:
        raise ValidationError(_(f"Folder {folder} is empty\nCheck path pass content"))

    for file in files:
        file_path = folder + "/" + file
        if os.path.isdir(file_path):
            continue
        text = textract.process(file_path)
        text_descrypted = text.decode('utf-8')
        text_array = text_descrypted.split('\n\n')
        text_array = [text.replace(' ', '') for text in text_array]
        _logger.info(_(f"Processing file: {file}"))

        code = ""
        date = ""
        for text in text_array:
            if len(text) == 13 and text.isdigit():
                code = text
            index = text.find('-')
            if index == 2:
                date = text.split('\n')[0]

            if code and date:
                break

        update_file_name(self, code, file, folder)
        new_file_path = file_system(self, date, folder)
        import_pdf(self, code, new_file_path, custom_name, company_id, ticker_price)

    logging.info(_(f"All files update and imported"))

def update_file_name(self, code, oldName, folder):
    if code:
        format = ".pdf"
        global current_file
        current_file = oldName
        if oldName != (code + format):
            try:
                os.rename(folder + "/" + oldName, folder + "/" + code + format)
                logging.info(_(f"New file name: {code + format}"))
                current_file = code + format
            except OSError as ex:
                raise ValidationError(_(f"Rename file error:\n{ex}"))


def file_system(self, ticket_date, folder):
    if ticket_date:
        try:
            path = folder + "/" + ticket_date
            if not os.path.isdir(path):
                os.mkdir(path)
                _logger.info(_(f"New folder created: {path}"))

            new_file_path = path + "/" + current_file

            if not os.path.isfile(new_file_path):
                try:
                    os.rename(folder + "/" + current_file, new_file_path)
                    _logger.info(_(f"File {current_file} move to: {path}"))
                except OSError as ex:
                    raise ValidationError(_(f"Error moving file {current_file}:\n{ex}"))

            return new_file_path

        except OSError as ex:
            raise ValidationError(_(f"Error Creating folder: \n{ex}"))


def import_pdf(self, code, file_path, custom_name, company_id, ticker_price):
    # Create and get the product from the ticket
    product_id = create_product_ticket(self, file_path, custom_name, company_id, ticker_price)

    with open(file_path, "rb") as imageFile:
        encodedString = base64.b64encode(imageFile.read())

    if not self.env['stock.lot'].search([('name', '=', code)], limit=1):

        lot_id = self.env['stock.lot'].create({
            "name"      : code,
            "product_id": product_id.sudo().product_variant_id.id,  # TODO Check if it's a specific product to client
            "company_id": company_id,
            "file_name" : code + '.pdf',
            "file_data" : encodedString,
        })
        warehouse_id = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1)
        self.env['stock.quant'].create({
            'product_id'        : product_id.sudo().product_variant_id.id,
            'lot_id'            : lot_id.id,
            'location_id'       : warehouse_id.lot_stock_id.id,
            'inventory_quantity': 1,
            'company_id'        : company_id,
        }).action_apply_inventory()
        self.env.cr.commit()
    else:
        logging.warning(_(f"Stock lot {code} already exists"))


def create_product_ticket(self, file_path, custom_name, company_id, ticker_price):
    product_name = file_path.split('/')[-2] + custom_name
    product_id = self.env['product.template'].search([('name', '=', product_name)], limit=1)

    if not product_id:
        product_id = self.env['product.template'].create({
            'name'         : f'{product_name}',
            'detailed_type': 'product',
            'tracking'     : 'serial',
            'categ_id'     : self.env.ref('product_sale_history.nos_tickets').id,
            'company_id'   : company_id,
            'list_price'   : ticker_price,
            'taxes_id'     : self.env.ref('account.5_iva6bens').ids
        })
    else:
        product_id.list_price = ticker_price

    return product_id