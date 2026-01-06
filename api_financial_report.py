import xmlrpc.client
from flask import Flask, request, jsonify


url = 'https://edu-student4.odoo.com'
db = 'edu-student4'
username = 'usamah@clavis.co.id'
password = '1'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

app = Flask(__name__)

def odoo_search_read(model, domain, fields, limit=50, offset=0):
    return models.execute_kw(
        db,
        uid,
        password,
        model,
        'search_read',
        [domain],
        {
            'fields': fields,
            'limit': limit,
            'offset': offset,
            'order': 'create_date desc',
        }
    )

# phase 1
@app.route('/clavis_connect/sales/GetSalesOrder', methods=['GET'])
def get_sale_orders():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'access_url',
        'amount_invoiced',
        'amount_paid',
        'amount_tax',
        'amount_to_invoice',
        'amount_total',
        'amount_undiscounted',
        'amount_unpaid',
        'amount_untaxed',
        'company_price_include',
        'create_date',
        'create_uid',
        'currency_id',
        'customizable_pdf_form_fields',
        'date_order',
        'delivery_count',
        'delivery_status',
        'display_name',
        'duplicated_order_ids',
        'effective_date',
        'expected_date',
        'expense_count',
        'margin',
        'margin_percent',
        'medium_id',
        'name',
        'order_line',
        'partner_id',
        'partner_invoice_id',
        'partner_shipping_id',
        'picking_ids',
        'planning_initial_date',
        'pricelist_id',
        'procurement_group_id',
        'tax_calculation_rounding_method',
        'tax_country_id',
        'team_id',
        'transaction_ids',
        'type_name',
        'user_id',
        'validity_date',
        'warehouse_id',
        'write_date',
        'write_uid',
        'x_studio_email',
        'company_id',
        'country_code',
    ]

    data = odoo_search_read(
        model='sale.order',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/clavis_connect/purchase/GetPurchaseOrder', methods=['GET'])
def get_purchase_orders():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'access_url',
        'amount_tax',
        'amount_total',
        'amount_total_cc',
        'amount_untaxed',
        'company_currency_id',
        'company_id',
        'company_price_include',
        'country_code',
        'create_date',
        'create_uid',
        'currency_id',
        'currency_rate',
        'date_approve',
        'date_calendar_start',
        'date_order',
        'date_planned',
        'default_location_dest_id_usage',
        'display_name',
        'name',
        'order_line',
        'partner_id',
        'partner_ref',
        'payment_term_id',
        'picking_type_id',
        'product_id',
        'tax_country_id',
        'user_id',
        'write_date',
        'write_uid',
        'invoice_status'
    ]

    data = odoo_search_read(
        model='purchase.order',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/clavis_connect/inventory/GetMasterData', methods=['GET'])
def get_product():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'avg_cost',
        'bom_count',
        'categ_id',
        'code',
        'company_currency_id',
        'company_id',
        'cost_currency_id',
        'cost_method',
        'country_of_origin',
        'create_date',
        'create_uid',
        'currency_id',
        'date_from',
        'date_to',
        'default_code',
        'display_name',
        'expected_margin',
        'expected_margin_rate',
        'free_qty',
        'id',
        'incoming_qty',
        'l10n_id_product_code',
        'list_price',
        'location_id',
        'lst_price',
        'name',
        'product_variant_id',
        'property_stock_inventory',
        'property_stock_production',
        'responsible_id',
        'sale_avg_price',
        'sale_delay',
        'sale_expected',
        'standard_price',
        'total_cost',
        'total_margin',
        'total_margin_rate',
        'total_value',
        'uom_id',
        'virtual_available',
        'volume',
        'volume_uom_name',
        'warehouse_id',
        'weight',
        'weight_uom_name',
        'write_date'
    ]

    data = odoo_search_read(
        model='product.product',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/clavis_connect/partner/GetPartner', methods=['GET'])
def get_partner():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'calendar_last_notif_ack',
        'color',
        'commercial_company_name',
        'commercial_partner_id',
        'company_name',
        'company_registry_label',
        'company_type',
        'complete_name',
        'contact_address',
        'contact_address_complete',
        'contact_address_inline',
        'contract_ids',
        'country_code',
        'country_id',
        'create_date',
        'create_uid',
        'credit',
        'currency_id',
        'days_sales_outstanding',
        'display_name',
        'email',
        'email_formatted',
        'email_normalized',
        'id',
        'im_status',
        'mobile',
        'name',
        'partner_latitude',
        'partner_longitude',
        'partner_vat_placeholder',
        'phone',
        'property_product_pricelist',
    ]

    data = odoo_search_read(
        model='res.partner',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/clavis_connect/partner/GetVendor', methods=['GET'])
def get_vendor():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'calendar_last_notif_ack',
        'city',
        'commercial_company_name',
        'commercial_partner_id',
        'company_registry_label',
        'company_type',
        'complete_name',
        'contact_address',
        'contact_address_complete',
        'contact_address_inline',
        'country_code',
        'country_id',
        'create_date',
        'create_uid',
        'credit',
        'currency_id',
        'date_localization',
        'days_sales_outstanding',
        'debit',
        'display_name',
        'email',
        'email_formatted',
        'email_normalized',
        'im_status',
        'invoice_ids',
        'mobile',
        'name',
        'on_time_rate',
        'partner_vat_placeholder',
        'phone',
        'phone_sanitized',
        'purchase_line_ids',
        'street',
        'total_all_due',
        'total_all_overdue',
        'total_due',
        'total_invoiced',
        'total_overdue',
        'type',
        'tz',
        'website_url',
        'write_date',
        'zip'
    ]

    data = odoo_search_read(
        model='res.partner',
        domain=[['supplier_rank', '>', 0]],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/clavis_connect/sales/GetSalesAnalyst', methods=['GET'])
def get_sale_orders_analyst():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'access_url',
        'amount_invoiced',
        'amount_paid',
        'amount_tax',
        'amount_to_invoice',
        'amount_total',
        'amount_undiscounted',
        'amount_unpaid',
        'amount_untaxed',
        'company_id',
        'country_code',
        'create_date',
        'create_uid',
        'currency_id',
        'date_order',
        'effective_date',
        'expected_date',
        'name',
        'order_line',
        'partner_id',
        'partner_invoice_id',
        'partner_shipping_id',
        'planning_initial_date',
        'tax_country_id',
        'team_id',
        'type_name',
        'user_id',
        'validity_date',
        'warehouse_id',
        'write_date',
        'write_uid',
        'x_studio_email',
        'display_name',
        'invoice_status'
    ]

    data = odoo_search_read(
        model='sale.order',
        domain=[['invoice_status','=','invoiced']],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/clavis_connect/purchase/GetPurchaseReport', methods=['GET'])
def get_purchase_orders_analyst():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'access_url',
        'amount_tax',
        'amount_total',
        'amount_total_cc',
        'amount_untaxed',
        'company_currency_id',
        'company_id',
        'company_price_include',
        'country_code',
        'create_date',
        'create_uid',
        'currency_id',
        'date_approve',
        'date_calendar_start',
        'date_order',
        'date_planned',
        'default_location_dest_id_usage',
        'display_name',
        'effective_date',
        'group_id',
        'invoice_status',
        'name',
        'on_time_rate',
        'partner_id',
        'picking_ids',
        'picking_type_id',
        'product_id',
        'state',
        'tax_country_id',
        'user_id',
        'write_uid',
        'write_date'
    ]

    data = odoo_search_read(
        model='purchase.order',
        domain=[['invoice_status','=','invoiced']],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

# phase 2
@app.route('/api/account/move', methods=['GET'])
def get_account_move():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'display_name',
        'move_type',
        'state',
        'date',
        'invoice_date',
        'invoice_date_due',
        'partner_id',
        'commercial_partner_id',
        'partner_shipping_id',
        'bank_partner_id',
        'company_id',
        'currency_id',
        'company_currency_id',
        'amount_total',
        'amount_untaxed',
        'amount_tax',
        'amount_residual',
        'amount_paid',
        'payment_state',
        'payment_reference',
        'journal_id',
        'line_ids',
        'invoice_line_ids',
        'user_id',
        'create_uid',
        'create_date',
        'write_uid',
        'write_date',
        'team_id',
        'country_code',
        'tax_country_id',
        'l10n_id_kode_transaksi',
        'sequence_number',
        'sequence_prefix'
    ]

    data = odoo_search_read(
        model='account.move',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/account/invoice', methods=['GET'])
def get_account_invoice():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'move_type',
        'state',
        'partner_id',
        'commercial_partner_id',
        'company_id',
        'currency_id',
        'amount_total',
        'amount_untaxed',
        'amount_tax',
        'amount_residual',
        'amount_paid',
        'payment_state',
        'payment_reference',
        'invoice_date',
        'invoice_date_due',
        'next_payment_date',
        'journal_id',
        'invoice_origin',
        'invoice_line_ids',
        'line_ids',
        'payment_ids',
        'matched_payment_ids',
        'partner_bank_id',
        'bank_partner_id',
        'team_id',
        'user_id',
        'create_date',
        'write_date',
        'create_uid',
        'write_uid',
        'country_code',
        'tax_country_id',
        'l10n_id_kode_transaksi',
        'message_ids',
        'message_follower_ids',
        'audit_trail_message_ids'
    ]

    data = odoo_search_read(
        model='account.move',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/account/cust_get_payment', methods=['GET'])
def get_customer_payment():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'company_currency_id',
        'available_payment_method_line_ids',
        'date',
        'name',
        'journal_id',
        'company_id',
        'payment_method_line_id',
        'partner_id',
        'amount_signed',
        'currency_id',
        'activity_ids',
        'amount_company_currency_signed',
        'state'
    ]

    data = odoo_search_read(
        model='account.payment',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/account/vendor_get_bill', methods=['GET'])
def get_vendor_bill():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'ref',
        'display_name',
        'move_type',
        'type_name',
        'state',
        'payment_state',
        'status_in_payment',
        'amount_total',
        'amount_untaxed',
        'amount_tax',
        'amount_residual',
        'currency_id',
        'company_id',
        'company_currency_id',
        'partner_id',
        'commercial_partner_id',
        'journal_id',
        'invoice_date',
        'invoice_date_due',
        'date',
        'create_date',
        'write_date',
        'create_uid',
        'write_uid',
        'sequence_number',
        'sequence_prefix',
        'highest_name',
        'partner_shipping_id',
        'partner_credit',
        'extract_partner_name',
        'extract_attachment_id',
        'message_main_attachment_id',
        'line_ids',
        'invoice_line_ids',
        'matched_payment_ids',
        'reconciled_payment_ids',
        'country_code',
        'tax_country_id',
        'l10n_id_kode_transaksi'
    ]

    data = odoo_search_read(
        model='account.move',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/account/vendor_get_payment', methods=['GET'])
def get_vendor_payment():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'state',
        'payment_type',
        'partner_id',
        'amount',
        'currency_id',
        'date',
        'memo',
        'journal_id',
        'payment_method_line_id',
        'partner_bank_id',
        'qr_code',
        'duplicate_payment_ids',
        'reconciled_invoices_count',
        'reconciled_bills_count',
        'reconciled_statement_lines_count',
        'move_id',
        'company_id',
        'partner_type',
        'is_sent',
        'need_cancel_request',
        'is_reconciled',
        'is_matched',
        'payment_method_code',
        'show_partner_bank_account',
        'require_partner_bank_account',
        'available_payment_method_line_ids',
        'available_partner_bank_ids',
        'available_journal_ids',
        'country_code',
        'paired_internal_transfer_payment_id',
        'reconciled_invoices_type'
    ]

    data = odoo_search_read(
        model='account.payment',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/account/vendor_get_journal_entry', methods=['GET'])
def get_vendor_journal_entry():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'move_type',
        'state',
        'date',
        'invoice_date',
        'invoice_date_due',
        'company_id',
        'company_currency_id',
        'currency_id',
        'partner_id',
        'commercial_partner_id',
        'partner_shipping_id',
        'bank_partner_id',
        'journal_id',
        'team_id',
        'user_id',
        'invoice_user_id',
        'create_uid',
        'write_uid',
        'create_date',
        'write_date',
        'amount_untaxed',
        'amount_tax',
        'amount_total',
        'amount_residual',
        'amount_paid',
        'amount_total_words',
        'payment_state',
        'payment_reference',
        'partner_credit',
        'invoice_origin',
        'sale_order_count',
        'line_ids',
        'invoice_line_ids',
        'message_ids',
        'message_follower_ids',
        'attachment_ids',
        'country_code',
        'tax_country_id',
        'l10n_id_kode_transaksi',
        'display_name',
        'type_name',
        'auto_post',
        'posted_before',
        'checked',
        'has_message',
        'show_reset_to_draft_button',
        'show_payment_term_details',
        'show_delivery_date',
        'show_discount_details',
        'show_signature_area',
        'narration',
        'ref',
        'sequence_number',
        'sequence_prefix',
        'secure_sequence_number',
        'inalterable_hash',
        'message_partner_ids',
        'audit_trail_message_ids'
    ]

    data = odoo_search_read(
        model='account.move',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/account/vendor_get_journal_items', methods=['GET'])
def get_vendor_journal_items():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'move_id',
        'invoice_date',
        'date',
        'company_id',
        'journal_id',
        'move_name',
        'account_id',
        'partner_id',
        'ref',
        'product_id',
        'name',
        'analytic_distribution',
        'tax_ids',
        'amount_currency',
        'currency_id',
        'debit',
        'credit',
        'tax_tag_ids',
        'discount_date',
        'discount_amount_currency',
        'tax_line_id',
        'date_maturity',
        'balance',
        'matching_number',
        'amount_residual',
        'amount_residual_currency',
        'move_type',
        'parent_state',
        'account_type',
        'statement_line_id',
        'company_currency_id',
        'is_same_currency',
        'is_account_reconcile',
        'sequence'
    ]

    data = odoo_search_read(
        model='account.move.line',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/account/get_analytic_items', methods=['GET'])
def get_analytic_items():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'display_name',
        'account_id',
        'amount',
        'analytic_distribution',
        'analytic_precision',
        'auto_account_id',
        'category',
        'code',
        'company_id',
        'currency_id',
        'date',
        'create_date',
        'create_uid',
        'write_date',
        'write_uid',
        'employee_id',
        'general_account_id',
        'journal_id',
        'move_line_id',
        'partner_id',
        'product_id',
        'product_uom_id',
        'product_uom_category_id',
        'ref',
        'so_line',
        'unit_amount',
        'user_id'
    ]

    data = odoo_search_read(
        model='account.analytic.line',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/account/get_asset_items', methods=['GET'])
def get_asset_items():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'move_id',
        'invoice_date',
        'date',
        'company_id',
        'journal_id',
        'move_name',
        'account_id',
        'partner_id',
        'ref',
        'product_id',
        'name',
        'analytic_distribution',
        'tax_ids',
        'amount_currency',
        'currency_id',
        'debit',
        'credit',
        'tax_tag_ids',
        'discount_date',
        'discount_amount_currency',
        'tax_line_id',
        'date_maturity',
        'balance',
        'matching_number',
        'amount_residual',
        'amount_residual_currency',
        'move_type',
        'parent_state',
        'account_type',
        'statement_line_id',
        'company_currency_id',
        'is_same_currency',
        'is_account_reconcile',
        'sequence'
    ]

    data = odoo_search_read(
        model='account.asset',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/inventory/get_receipt', methods=['GET'])
def get_receipt():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'move_id',
        'invoice_date',
        'date',
        'company_id',
        'name',
        'display_name',
        'origin',
        'state',
        'scheduled_date',
        'date',
        'date_deadline',
        'date_done',
        'create_date',
        'write_date',
        'create_uid',
        'write_uid',
        'company_id',
        'warehouse_address_id',
        'picking_type_id',
        'picking_type_code',
        'partner_id',
        'location_id',
        'location_dest_id',
        'move_ids',
        'move_line_ids',
        'move_type',
        'product_id',
        'purchase_id',
        'sale_id',
        'group_id',
        'backorder_id',
        'is_return_picking',
        'is_locked',
        'priority'
    ]

    data = odoo_search_read(
        model='stock.picking',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/inventory/get_delivery', methods=['GET'])
def get_delivery():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'origin',
        'state',
        'scheduled_date',
        'date',
        'date_deadline',
        'date_done',
        'is_locked',
        'picking_type_id',
        'picking_type_code',
        'picking_type_entire_packs',
        'company_id',
        'warehouse_address_id',
        'location_id',
        'location_dest_id',
        'partner_id',
        'product_id',
        'move_ids',
        'move_ids_without_package',
        'move_line_ids',
        'move_line_ids_without_package',
        'move_type',
        'backorder_id',
        'backorder_ids',
        'return_ids',
        'return_count',
        'sale_id',
        'group_id',
        'shopee_delivery_status',
        'shopee_label_status',
        'shopee_order_ref',
        'carrier_id',
        'carrier_price',
        'carrier_tracking_ref'
    ]

    data = odoo_search_read(
        model='product.product',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/inventory/get_product', methods=['GET'])
def get_product_2():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'origin',
        'state',
        'scheduled_date',
        'date',
        'date_deadline',
        'date_done',
        'is_locked',
        'picking_type_id',
        'picking_type_code',
        'picking_type_entire_packs',
        'company_id',
        'warehouse_address_id',
        'location_id',
        'location_dest_id',
        'partner_id',
        'product_id',
        'move_ids',
        'move_ids_without_package',
        'move_line_ids',
        'move_line_ids_without_package',
        'move_type',
        'backorder_id',
        'backorder_ids',
        'return_ids',
        'return_count',
        'sale_id',
        'group_id',
        'shopee_delivery_status',
        'shopee_label_status',
        'shopee_order_ref',
        'carrier_id',
        'carrier_price',
        'carrier_tracking_ref'
    ]

    data = odoo_search_read(
        model='stock.picking',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/api/inventory/get_move_history', methods=['GET'])
def get_move_history():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'display_name',
        'origin',
        'state',
        'move_type',
        'scheduled_date',
        'date',
        'date_done',
        'delay_pass',
        'days_to_arrive',
        'is_locked',
        'is_return_picking',
        'return_id',
        'sale_id',
        'group_id',
        'partner_id',
        'company_id',
        'warehouse_address_id',
        'location_id',
        'location_dest_id',
        'picking_type_id',
        'picking_type_code',
        'product_id',
        'move_ids',
        'move_line_ids',
        'package_level_ids',
        'has_packages',
        'has_tracking',
        'use_create_lots',
        'use_existing_lots',
        'lot_id',
        'weight',
        'weight_bulk',
        'shipping_weight',
        'shipping_volume',
        'carrier_id',
        'carrier_price',
        'carrier_tracking_ref',
        'carrier_tracking_url',
        'shopee_delivery_status',
        'shopee_label_status',
        'note',
        'priority',
        'printed',
        'is_signed'
    ]

    data = odoo_search_read(
        model='stock.picking',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/sales/get/so', methods=['GET'])
def get_so():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'id',
        'name',
        'display_name',
        'state',
        'date_order',
        'validity_date',
        'expected_date',
        'commitment_date',
        'company_id',
        'warehouse_id',
        'partner_id',
        'partner_invoice_id',
        'partner_shipping_id',
        'user_id',
        'team_id',
        'currency_id',
        'amount_total',
        'amount_untaxed',
        'amount_tax',
        'amount_unpaid',
        'amount_invoiced',
        'amount_paid',
        'invoice_status',
        'invoice_ids',
        'picking_ids',
        'delivery_status',
        'order_line',
        'margin',
        'margin_percent',
        'pricelist_id',
        'procurement_group_id',
        'payment_term_id',
        'require_signature',
        'require_payment',
        'create_date',
        'create_uid',
        'write_date',
        'write_uid',
        'x_studio_email'
    ]

    data = odoo_search_read(
        model='sale.order',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

@app.route('/purchase/get/po', methods=['GET'])
def get_po():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    fields = [
        'access_token',
        'access_url',
        'access_warning',
        'activity_calendar_event_id',
        'activity_date_deadline',
        'activity_exception_decoration',
        'activity_exception_icon',
        'activity_ids',
        'activity_state',
        'activity_summary',
        'activity_type_icon',
        'activity_type_id',
        'activity_user_id',
        'amount_tax',
        'amount_total',
        'amount_total_cc',
        'amount_untaxed',
        'company_currency_id',
        'company_id',
        'company_price_include',
        'country_code',
        'create_date',
        'create_uid',
        'currency_id',
        'currency_rate',
        'date_approve',
        'date_calendar_start',
        'date_order',
        'date_planned',
        'default_location_dest_id_usage',
        'dest_address_id',
        'display_name',
        'effective_date',
        'fiscal_position_id',
        'group_id',
        'has_message',
        'id',
        'incoming_picking_count',
        'incoterm_id',
        'incoterm_location',
        'invoice_count',
        'invoice_ids',
        'invoice_status',
        'is_above_budget',
        'is_analytic',
        'is_shipped',
        'mail_reception_confirmed',
        'mail_reception_declined'
    ]

    data = odoo_search_read(
        model='purchase.order',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

