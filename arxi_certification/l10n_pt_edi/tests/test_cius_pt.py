import lxml
import markupsafe
from lxml import etree, isoschematron
from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from pathlib import Path
from io import StringIO


# Config for test this class
# -i l10n_pt_edi --test-tags cius_pt
from odoo.tools import file_open


@tagged('post_install', '-at_install', 'cius_pt')
class TestCiusPt(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Account move with 23% IVA
        cls.account_move_1 = cls.env.ref('l10n_pt_edi.account_move_1')

        # Account move with no IVA
        cls.account_move_2 = cls.env.ref('l10n_pt_edi.account_move_2')

        # Account move with different kinds of IVA (13%, 6%, 0%)
        cls.account_move_3 = cls.env.ref('l10n_pt_edi.account_move_3')

        # Account move with different kinds of IVA (13%, 6%, 0%)
        # Discounts on the lines
        cls.account_move_4 = cls.env.ref('l10n_pt_edi.account_move_4')

        # Account move with different kinds of IVA (13%, 6%, 0%)
        # Discounts on the lines
        # Fields compromisse and ref filled
        cls.account_move_5 = cls.env.ref('l10n_pt_edi.account_move_5')

        cls.AccountJournal = cls.env['account.journal']

    def _open_schema_file(self, path):
        with file_open(path, 'r') as f:
            schema_content = f.read()
        schema_etree = etree.parse(StringIO(schema_content))
        # schematron = etree.Schematron(schema_etree)
        schematron = isoschematron.Schematron(schema_etree)
        return schematron

    def _validate_datatype_xml(self, xml_content):
        # Datatye Schemas
        path = ''
        schematron = self._open_schema_file(path)

        # datatype_xml_validator = lxml.etree.XMLSchema(file="l10n_pt_edi/tests/cius_schema/datatype/urn_feap.gov.pt_CIUS-PT_2.1.1-UBL-datatype.sch")
        # is_valid = datatype_xml_validator.validate(xml_content)
        # print(schematron.validate(xml_content))

    def _validate_ubl_xml(self, xml_content):
        # UBL Schemas
        ubl_xml_validator_1 = lxml.etree.XMLSchema(file="cius_schema/UBL/urn_feap.gov.pt_CIUS-PT_2.1.1-UBL-condition.sch")
        ubl_xml_validator_2 = lxml.etree.XMLSchema(file="cius_schema/UBL/urn_feap.gov.pt_CIUS-PT_2.1.1-UBL-model.sch")
        ubl_xml_validator_3 = lxml.etree.XMLSchema(file="cius_schema/UBL/urn_feap.gov.pt_CIUS-PT_2.1.1-UBL-syntax.sch")

        is_valid_1 = ubl_xml_validator_1.validate(xml_content)
        is_valid_2 = ubl_xml_validator_2.validate(xml_content)
        is_valid_3 = ubl_xml_validator_3.validate(xml_content)

    def _validate_cius_pt_xml(self, xml_content):
        # CIUS PT Schemas
        cius_xml_validator_1 = lxml.etree.XMLSchema(file="cius_schema/abstract/urn_feap.gov.pt_CIUS-PT_2.1.1-condition.sch")
        cius_xml_validator_2 = lxml.etree.XMLSchema(file="cius_schema/abstract/urn_feap.gov.pt_CIUS-PT_2.1.1-model.sch")
        cius_xml_validator_3 = lxml.etree.XMLSchema(file="cius_schema/abstract/urn_feap.gov.pt_CIUS-PT_2.1.1-syntax.sch")

        is_valid_1 = cius_xml_validator_1.validate(xml_content)
        is_valid_2 = cius_xml_validator_2.validate(xml_content)
        is_valid_3 = cius_xml_validator_3.validate(xml_content)

    def test_cius_pt_xml_invoice(self):
        # Remove edi_format_ids for testing reasons
        self.account_move_1.journal_id.write({'edi_format_ids': [Command.clear()]})

        # Confirm account move
        self.account_move_1.action_post()

        # Get xml for Cius PT
        xml_content = markupsafe.Markup("<?xml version='1.0' encoding='UTF-8'?>")
        xml_content += self.env.ref('l10n_pt_certificate.export_cius_pt_invoice')._render(
            self.account_move_1._get_cius_pt_values())

        # xml_content = etree.parse(StringIO(xml_content))

        # Validate with eSPap provided schemas
        # self._validate_datatype_xml(xml_content)
        # self._validate_ubl_xml(xml_content)
        # self._validate_cius_pt_xml(xml_content)
