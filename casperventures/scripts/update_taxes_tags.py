# from odoo.addons.casperventures.scripts.update_taxes_tags import _update_taxes_tags;
# _update_taxes_tags(self, self.env['res.company'].browse(1), self.env['res.company'].browse(8));

def _update_taxes_tags(self, company_id, company_dest_id):
    from odoo import fields

    mapping = {
        'VEXMN-IVA23': 'IVA 23% (Bens)',
        'VEXMN-IVA13': 'IVA 13% (Bens)',
        'VEXMC-IVA6': 'IVA 6% (Bens)',
        'VOBSMN-IVA23': 'IVA 23% (Serviços)',
        'VOBSMN-IVA13': 'IVA 13% (Serviços)',
        'VOBSMN-IVA6': 'IVA 6% (Serviços)',
        'CIMOMN-IVA23': 'IVA 23% (Imobilizado)',
        'CIMOMN-IVA13': 'IVA 13% (Imobilizado)',
        'CIMOMN-IVA6': 'IVA 6% (Imobilizado)',
        'CEXMN-IVA23': 'IVA 23% (Bens)',
        'CEXMN-IVA13': 'IVA 13% (Bens)',
        'CEXMN-IVA6': 'IVA 6% (Bens)',
        'COBSMN-IVA23': 'IVA 23% (Serviços)',
        'COBSMN-IVA13': 'IVA 13% (Serviços)',
        'COBSMN-IVA6': 'IVA 6% (Serviços)',
        'CIMOMC-IVA23 ISP': 'IVA 23% (Imobilizado intracomunitários com ISP)',
        'CIMOMC-IVA13 ISP': 'IVA 13% (Imobilizado intracomunitários com ISP)',
        'CIMOMC-IVA6 ISP': 'IVA 6% (Imobilizado intracomunitários com ISP)',
        'COBSMC-IVA23 ISP': 'IVA 23% (Serviços intracomunitários com ISP)',
        'COBSMC-IVA13 ISP': 'IVA 13% (Serviços intracomunitários com ISP)',
        'COBSMC-IVA6 ISP': 'IVA 6% (Serviços intracomunitários com ISP)',
        'CEXMC-IVA23 ISP': 'IVA 23% (Bens intracomunitários com ISP)',
        'CEXMC-IVA13 ISP': 'IVA 13% (Bens intracomunitários com ISP)',
        'CEXMC-IVA6 ISP': 'IVA 6% (Bens intracomunitários com ISP)',
        'IMPORTIMOMC-IVA23 ISP': 'IVA 23% (Importação de Imobilizado com ISP)',
        'IMPORTIMOMC-IVA13 ISP': 'IVA 13% (Importação de Imobilizado com ISP)',
        'IMPORTIMOMC-IVA6 ISP': 'IVA 6% (Importação de Imobilizado com ISP)',
        'IMPORTEXMC-IVA23 ISP': 'IVA 23% (Importação de bens com ISP)',
        'IMPORTEXMC-IVA13 ISP': 'IVA 13% (Importação de bens com ISP)',
        'IMPORTEXMC-IVA6 ISP': 'IVA 6% (Importação de Bens com ISP)',
        '50%GASÓLEO(IVA23)': 'IVA 23% (Gasóleo Outros)',
        'COBSME-IVA23 ISP': 'IVA 23% (Serviços extracomunitários com ISP)',
        'COBSME-IVA13 ISP': 'IVA 13% (Serviços extracomunitários com ISP)',
        'COBSME-IVA6 ISP': 'IVA 6% (Serviços extracomunitários com ISP)'
    }

    def _write_values_repartition_lines(line_ids, company_tax_id, tax_dest_id, mode):
        already_done = []
        if mode == 'invoice':
            lines_to_see = tax_dest_id.invoice_repartition_line_ids
        else:
            lines_to_see = tax_dest_id.refund_repartition_line_ids
        if not self.env['account.move.line'].search([('tax_repartition_line_id', 'in', lines_to_see.ids)]):
            try:
                if mode == 'invoice':
                    tax_dest_id.write({
                        'invoice_repartition_line_ids': [fields.Command.clear()] + [fields.Command.create(vals) for vals in _prepare_vals_repartition_lines(
                            line_ids, company_tax_id
                        )],
                    })
                else:
                    tax_dest_id.write({
                        'refund_repartition_line_ids': [fields.Command.clear()] + [fields.Command.create(vals) for vals in _prepare_vals_repartition_lines(
                            line_ids, company_tax_id
                        )],
                    })
            except Exception as e:
                print(e)
        else:
            for line in line_ids.sudo():
                account_id = self.env['account.account'].sudo().search([('company_id', '=', company_tax_id.id), ('code', '=', line.account_id.code)], limit=1)
                if mode == 'invoice':
                    line_tax_invoice = tax_dest_id.invoice_repartition_line_ids.sudo().filtered(
                        lambda l: l.factor_percent == line.factor_percent and l.repartition_type == line.repartition_type and l not in already_done
                    )
                    line_tax_invoice.write({
                        'tag_ids': line.tag_ids,
                        'account_id': account_id.id
                    })
                    already_done.append(line_tax_invoice)
                else:
                    line_tax_refund = tax_dest_id.refund_repartition_line_ids.sudo().filtered(
                        lambda l: l.factor_percent == line.factor_percent and l.repartition_type == line.repartition_type and l not in already_done
                    )[0]
                    line_tax_refund.write({
                        'tag_ids': line.tag_ids,
                        'account_id': account_id.id
                    })
                    already_done.append(line_tax_refund)

    def _prepare_vals_repartition_lines(line_ids, company_tax_id):
        res = []
        for line_id in line_ids:
            account_id = self.env['account.account'].search([
                ('company_id', '=', company_tax_id.id), ('code', '=', line_id.account_id.code)
            ], limit=1)
            res.append({
                'factor_percent': line_id.factor_percent,
                'repartition_type': line_id.repartition_type,
                'account_id': account_id.id,
                'tag_ids': line_id.tag_ids,
            })
        return res

    def _copy_tax_record(tax_rec_id, dest_company_id):
        new_tax_id = tax_rec_id.copy()
        vals = {
            'company_id': dest_company_id.id,
            'name': tax_rec_id.name,
            'invoice_repartition_line_ids': [fields.Command.clear()] + [fields.Command.create(vals) for vals in _prepare_vals_repartition_lines(
                tax_rec_id.invoice_repartition_line_ids, dest_company_id
            )],
            'refund_repartition_line_ids': [fields.Command.clear()] + [fields.Command.create(vals) for vals in _prepare_vals_repartition_lines(
                tax_rec_id.refund_repartition_line_ids, dest_company_id
            )],
        }
        new_tax_id.write(vals)

    for tax_id in self.env['account.tax'].search([('company_id', '=', company_id.id)]):
        if tax_id.name in mapping:
            if dest_tax_id := self.env['account.tax'].search([
                ('name', '=', mapping.get(tax_id.name, False)), ('company_id', '=', company_dest_id.id), ('type_tax_use', '=', tax_id.type_tax_use)
            ], limit=1):
                _write_values_repartition_lines(tax_id.invoice_repartition_line_ids, company_dest_id, dest_tax_id, 'invoice')
                _write_values_repartition_lines(tax_id.refund_repartition_line_ids, company_dest_id, dest_tax_id, 'refund')
                try:
                    dest_tax_id.write({
                        'name': tax_id.name,
                        'tax_scope': tax_id.tax_scope,
                    })
                except Exception as e:
                    print(e)
                    print('Write failure', dest_tax_id.name)
            elif dest_tax_id := self.env['account.tax'].search([
                ('name', '=', tax_id.name), ('company_id', '=', company_dest_id.id), ('type_tax_use', '=', tax_id.type_tax_use)
            ], limit=1):
                _write_values_repartition_lines(tax_id.invoice_repartition_line_ids, company_dest_id, dest_tax_id, 'invoice')
                _write_values_repartition_lines(tax_id.refund_repartition_line_ids, company_dest_id, dest_tax_id, 'refund')
                try:
                    dest_tax_id.write({
                        'name': tax_id.name,
                        'tax_scope': tax_id.tax_scope,
                        'active': tax_id.active,
                    })
                except Exception as e:
                    print(e)
                    print('Write failure', dest_tax_id.name)
            else:
                if external_id := self.env['ir.model.data'].search(
                        [('model', '=', 'account.tax'), ('res_id', '=', tax_id.id)]):
                    external_name = f"l10n_pt_certificate.{company_dest_id.id}_{external_id.name.split('_', 1)[1]}"
                    # Encontrei uma taxa mapeada na empresa destino
                    try:
                        dest_tax_id = self.env.ref(str(external_name))
                    # Não econtrei uma taxa mapeada na empresa destino
                    except Exception as e:
                        print(e)
                        _copy_tax_record(tax_id, company_dest_id)
                    else:
                        _write_values_repartition_lines(tax_id.invoice_repartition_line_ids, company_dest_id, dest_tax_id, 'invoice')
                        _write_values_repartition_lines(tax_id.refund_repartition_line_ids, company_dest_id, dest_tax_id, 'refund')
                        try:
                            dest_tax_id.write({
                                'name': tax_id.name,
                                'tax_scope': tax_id.tax_scope,
                            })
                        except Exception as e:
                            print(e)
                            print('Write failure', dest_tax_id.name)
                else:
                    print('Mapping not found - Creating tax in destiny company')
                    _copy_tax_record(tax_id, company_dest_id)
        else:
            if external_id := self.env['ir.model.data'].search([('model', '=', 'account.tax'), ('res_id', '=', tax_id.id)]):
                external_name = f"l10n_pt_certificate.{company_dest_id.id}_{external_id.name.split('_', 1)[1]}"
                # Encontrei uma taxa mapeada na empresa destino
                try:
                    dest_tax_id = self.env.ref(str(external_name))
                # Não econtrei uma taxa mapeada na empresa destino
                except Exception as e:
                    print(e)
                    _copy_tax_record(tax_id, company_dest_id)
                else:
                    _write_values_repartition_lines(tax_id.invoice_repartition_line_ids, company_dest_id, dest_tax_id, 'invoice')
                    _write_values_repartition_lines(tax_id.refund_repartition_line_ids, company_dest_id, dest_tax_id, 'refund')
                    try:
                        dest_tax_id.write({
                            'name': tax_id.name,
                            'tax_scope': tax_id.tax_scope,
                        })
                    except Exception as e:
                        print(e)
                        print('Write failure', dest_tax_id.name)
            else:
                print('Mapping not found - Creating tax in destiny company')
                _copy_tax_record(tax_id, company_dest_id)
