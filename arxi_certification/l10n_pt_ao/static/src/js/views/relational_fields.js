//odoo.define('invoice_refund_restrictions.relational_fields', function (require) {
//    "use strict";
//    var { relational_fields } = require('web.relational_fields');
//
//    return relational_fields.FieldX2Many.include({
//        _hasCreateLine: function () {
//            if (this.attrs.name === 'invoice_line_ids') {
//                if (this.recordData.is_rappel) {
//                    this.canCreate = false;
//                }
//            }
//            return this._super();
//        },
//        _hasTrashIcon: function () {
//            if (this.attrs.name === 'invoice_line_ids') {
//                if (this.recordData.is_rappel) {
//                    this.canDelete = false;
//                }
//            }
//            return this._super();
//        }
//    });
//});



