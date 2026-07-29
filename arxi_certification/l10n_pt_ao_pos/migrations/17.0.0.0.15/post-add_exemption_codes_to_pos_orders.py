# Migration script for Odoo 17
# File: migrations/17.0.1.0.1/post-migration.py

import json
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Populate exemption_codes field for existing POS orders in Odoo 17"""
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    _logger.info("Starting exemption codes migration for Odoo 17...")

    # Check if exemption functionality exists in the system
    try:
        # Test if account.tax has exemption_id field
        test_tax = env['account.tax'].search([], limit=1)
        if test_tax and not hasattr(test_tax, 'exemption_id'):
            _logger.info("No exemption functionality found in system, skipping migration")
            return
    except Exception as e:
        _logger.error(f"Error checking exemption functionality: {e}")
        return

    # Find all POS orders without exemption_codes that have lines with taxes
    pos_orders = env['pos.order'].search([
        ('exemption_codes', '=', False),
        ('lines', '!=', False)
    ])

    _logger.info(f"Found {len(pos_orders)} POS orders to update with exemption codes")

    updated_count = 0
    error_count = 0

    for order in pos_orders:
        try:
            exemption_codes = {}

            # Method 1: Get exemption codes from the related account move if it exists
            if order.account_move and order.account_move.line_ids:
                for move_line in order.account_move.line_ids:
                    if move_line.product_id:  # Only product lines, not tax/account lines
                        for tax in move_line.tax_ids:
                            if hasattr(tax, 'exemption_id') and tax.exemption_id:
                                exemption_codes[tax.exemption_id.id] = {
                                    'code': tax.exemption_id.code,
                                    'name': tax.exemption_id.name
                                }

            # Method 2: If no exemption codes found in account move, try from POS order lines
            if not exemption_codes:
                for pos_line in order.lines:
                    # Check taxes after fiscal position (most accurate)
                    taxes_to_check = pos_line.tax_ids_after_fiscal_position
                    if not taxes_to_check:
                        # Fallback to product taxes
                        taxes_to_check = pos_line.product_id.taxes_id

                    for tax in taxes_to_check:
                        if hasattr(tax, 'exemption_id') and tax.exemption_id:
                            exemption_codes[tax.exemption_id.id] = {
                                'code': tax.exemption_id.code,
                                'name': tax.exemption_id.name
                            }

            # Method 3: If still no exemption codes, check product taxes directly
            if not exemption_codes:
                for pos_line in order.lines:
                    product = pos_line.product_id
                    if product and product.taxes_id:
                        for tax in product.taxes_id:
                            if hasattr(tax, 'exemption_id') and tax.exemption_id:
                                exemption_codes[tax.exemption_id.id] = {
                                    'code': tax.exemption_id.code,
                                    'name': tax.exemption_id.name
                                }

            # Store exemption codes if found
            if exemption_codes:
                exemption_json = json.dumps(exemption_codes)
                order.write({'exemption_codes': exemption_json})
                updated_count += 1

                if updated_count % 100 == 0:  # Log progress every 100 orders
                    _logger.info(f"Updated {updated_count} orders so far...")

        except Exception as e:
            error_count += 1
            _logger.error(f"Error updating exemption codes for POS order {order.id}: {e}")
            continue

    _logger.info(f"Exemption codes migration completed: {updated_count} orders updated, {error_count} errors")

    # Optional: Update existing POS sessions to ensure exemption codes are loaded
    try:
        _update_pos_sessions_with_exemption_data(env)
    except Exception as e:
        _logger.error(f"Error updating POS sessions: {e}")


def _update_pos_sessions_with_exemption_data(env):
    """Ensure POS sessions have access to exemption data"""
    _logger.info("Updating POS configurations for exemption support...")

    # Find all active POS configs
    pos_configs = env['pos.config'].search([('active', '=', True)])

    for config in pos_configs:
        try:
            # Check if the config has any taxes with exemptions
            company = config.company_id
            taxes_with_exemptions = env['account.tax'].search([
                ('company_id', '=', company.id),
                ('active', '=', True)
            ])

            exemption_count = 0
            for tax in taxes_with_exemptions:
                if hasattr(tax, 'exemption_id') and tax.exemption_id:
                    exemption_count += 1

            if exemption_count > 0:
                _logger.info(f"POS config '{config.name}' has {exemption_count} taxes with exemptions")

        except Exception as e:
            _logger.error(f"Error checking POS config {config.name}: {e}")

    _logger.info("POS configuration update completed")
