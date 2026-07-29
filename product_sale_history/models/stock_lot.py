import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = 'stock.lot'

    file_name = fields.Char('File Name')
    file_data = fields.Binary('File', attachment=False)
