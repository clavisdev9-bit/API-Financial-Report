import xmlrpc.client
from flask import Flask, request, jsonify


url = 'https://demo-260818a.odoo.com/'
db = 'demo-260818a'
username = 'aristya.rahadiyan@clavis.co.id'
password = '5555'

# def get_models():
# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# uid = common.authenticate(db, username, password, {})
# models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
def get_odoo():
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common",allow_none=True)
    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy(
        f"{url}/xmlrpc/2/object",
        allow_none=True
    )

    return uid, models

app = Flask(__name__)

def odoo_search_read(model, domain, fields, limit=500, offset=0):
    uid, models = get_odoo()
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
            'order': 'create_date desc, id desc',
        }
    )

# phase 1
@app.route('/clavis_connect/sales/GetSalesOrder', methods=['GET'])
def get_sale_orders():

    limit = int(request.args.get('limit', 500))
    offset = int(request.args.get('offset', 0))

    limit = min(limit, 1000)

    domain = []

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
        # 'expense_count',
        # 'margin',
        # 'margin_percent',
        'medium_id',
        'name',
        'order_line',
        'partner_id',
        'partner_invoice_id',
        'partner_shipping_id',
        'picking_ids',
        'planning_initial_date',
        'pricelist_id',
        'tax_calculation_rounding_method',
        'tax_country_id',
        'team_id',
        'type_name',
        'user_id',
        'validity_date',
        'warehouse_id',
        'write_date',
        'write_uid',
        'company_id',
        'country_code',
    ]

    # Ambil total jumlah record
    uid, models = get_odoo()
    total = models.execute_kw(
        db,
        uid,
        password,
        'sale.order',
        'search_count',
        [domain]
    )

    # Ambil data berdasarkan pagination
    data = odoo_search_read(
        model='sale.order',
        domain=domain,
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',

        # Total seluruh record
        'total': total,

        # Jumlah record yang dikirim pada request ini
        'count': len(data),

        # Pagination
        'limit': limit,
        'offset': offset,

        # Apakah masih ada halaman berikutnya
        'has_more': offset + len(data) < total,

        'data': data,
    })

@app.route('/clavis_connect/purchase/GetPurchaseOrder', methods=['GET'])
def get_purchase_orders():
    limit = int(request.args.get('limit', 500))
    offset = int(request.args.get('offset', 0))
    limit = min(limit, 1000)
    domain = []
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
    uid, models = get_odoo()
    total = models.execute_kw(
        db,
        uid,
        password,
        'purchase.order',
        'search_count',
        [domain]
    )

    data = odoo_search_read(
        model='purchase.order',
        domain=domain,
        fields=fields,
        limit=limit,
        offset=offset,
    )
    return jsonify({
        'status': 'success',
        'total': total,
        'count': len(data),
        'limit': limit,
        'offset': offset,
        'has_more': offset + len(data) < total,
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
        # 'country_of_origin', --unavailable di odoo 19--
        'create_date',
        'create_uid',
        'currency_id',
        # 'date_from', --context field, tidak bisa di-fetch via RPC--
        # 'date_to', --context field, tidak bisa di-fetch via RPC--
        'default_code',
        'display_name',
        # 'expected_margin', --unavailable di odoo 19--
        # 'expected_margin_rate', --unavailable di odoo 19--
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
        # 'sale_avg_price', --unavailable di odoo 19--
        'sale_delay',
        # 'sale_expected', --unavailable di odoo 19--
        'standard_price',
        # 'total_cost', --unavailable di odoo 19--
        # 'total_margin', --unavailable di odoo 19--
        # 'total_margin_rate', --unavailable di odoo 19--
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
        # 'credit', --unavailable di odoo 19--
        'currency_id',
        'days_sales_outstanding',
        'display_name',
        'email',
        'email_formatted',
        'email_normalized',
        'id',
        'im_status',
        # 'mobile', --unavailable di odoo 19--
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
        # 'credit', --unavailable di odoo 19--
        'currency_id',
        # 'date_localization', --unavailable di odoo 19--
        'days_sales_outstanding',
        # 'debit', --unavailable di odoo 19--
        'display_name',
        'email',
        'email_formatted',
        'email_normalized',
        'im_status',
        'invoice_ids',
        # 'mobile', --unavailable di odoo 19--
        'name',
        'on_time_rate',
        'partner_vat_placeholder',
        'phone',
        'phone_sanitized',
        'purchase_line_ids',
        'street',
        # 'total_all_due', --unavailable di odoo 19--
        # 'total_all_overdue', --unavailable di odoo 19--
        # 'total_due', --unavailable di odoo 19--
        # 'total_invoiced', --unavailable di odoo 19--
        # 'total_overdue', --unavailable di odoo 19--
        'type',
        'tz',
        # 'website_url', --unavailable di odoo 19--
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
        # 'x_studio_email', --field custom--
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
        # 'group_id', --unavailable di odoo 19--
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
    limit = int(request.args.get('limit', 500))
    offset = int(request.args.get('offset', 0))
    limit = min(limit, 1000)
    domain = []
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
    uid, models = get_odoo()
    total = models.execute_kw(
        db,
        uid,
        password,
        'account.move',
        'search_count',
        [domain]
    )
    data = odoo_search_read(
        model='account.move',
        domain=domain,
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'total': total,
        'count': len(data),
        'limit': limit,
        'offset': offset,
        'has_more': offset + len(data) < total,
        'data': data,
    })

@app.route('/api/account/cust_get_payment', methods=['GET'])
def get_customer_payment():
    limit = int(request.args.get('limit', 500))
    offset = int(request.args.get('offset', 0))
    limit = min(limit, 1000)
    domain = []

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
    uid, models = get_odoo()
    total = models.execute_kw(
        db,
        uid,
        password,
        'account.payment',
        'search_count',
        [domain]
    )
    data = odoo_search_read(
        model='account.payment',
        domain=[],
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'total': total,
        'count': len(data),
        'limit': limit,
        'offset': offset,
        'has_more': offset + len(data) < total,
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
        # 'partner_credit', --unavailable di odoo 19--
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
        # 'partner_credit', --unavailable di odoo 19--
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
        # 'group_id', --unavailable di odoo 19--
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
        # 'group_id', --unavailable di odoo 19--
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
        # 'group_id', --unavailable di odoo 19--
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
        # 'group_id', --unavailable di odoo 19--
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
    limit = int(request.args.get('limit', 500))
    offset = int(request.args.get('offset', 0))
    limit = min(limit, 1000)
    domain = []
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
        # 'procurement_group_id', --unavailable di odoo 19--
        'payment_term_id',
        'require_signature',
        'require_payment',
        'create_date',
        'create_uid',
        'write_date',
        'write_uid',
        # 'x_studio_email' --field custom--
    ]
    uid, models = get_odoo()
    total = models.execute_kw(
        db,
        uid,
        password,
        'sale.order',
        'search_count',
        [domain]
    )
    data = odoo_search_read(
        model='sale.order',
        domain=domain,
        fields=fields,
        limit=limit,
        offset=offset,
    )

    return jsonify({
        'status': 'success',
        'total': total,
        'count': len(data),
        'limit': limit,
        'offset': offset,
        'has_more': offset + len(data) < total,
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
        # 'group_id', --unavailable di odoo 19--
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

def get_purchase_order_lines(line_ids):
    uid, models = get_odoo()
    return models.execute_kw(
        db,
        uid,
        password,
        'purchase.order.line',
        'read',
        [line_ids],
        {
            'fields': [
                'order_id',
                'product_id',
                'name',
                'product_qty',
                'qty_received',
                'qty_invoiced',
                'analytic_distribution',
                'price_unit',
                'price_subtotal'
            ]
        }
    )

def get_analytic_accounts(analytic_ids):
    if not analytic_ids:
        return {}
    uid, models = get_odoo()
    records = models.execute_kw(
        db,
        uid,
        password,
        'account.analytic.account',
        'read',
        [analytic_ids],
        {'fields': ['name']}
    )

    return {rec['id']: rec['name'] for rec in records}

def build_po_with_lines(purchase_orders):
    all_line_ids = []
    for po in purchase_orders:
        all_line_ids.extend(po['order_line'])

    lines = get_purchase_order_lines(all_line_ids)

    analytic_ids = set()
    for line in lines:
        dist = line.get('analytic_distribution') or {}
        analytic_ids.update(int(k) for k in dist.keys())

    analytic_map = get_analytic_accounts(list(analytic_ids))

    line_map = {}
    for line in lines:
        order_id = line['order_id'][0]

        analytic_dist = []
        for analytic_id, percent in (line.get('analytic_distribution') or {}).items():
            analytic_dist.append({
                'id': int(analytic_id),
                'name': analytic_map.get(int(analytic_id)),
                'percentage': percent,
            })

        line_map.setdefault(order_id, []).append({
            'product_id': line['product_id'],
            'name': line['name'],
            'analytic_distribution': analytic_dist,
            'po_qty': line['product_qty'],
            'gr_qty': line['qty_received'],
            'qty_invoiced': line['qty_invoiced'],
            'price_unit': line['price_unit'],
            'subtotal': line['price_subtotal'],
        })

    for po in purchase_orders:
        po['lines'] = line_map.get(po['id'], [])
        po.pop('order_line')

    return purchase_orders

def get_product_templates2(template_ids):
    """Ambil detail product.template berdasarkan list ID."""
    if not template_ids:
        return []

    uid, models = get_odoo()

    return models.execute_kw(
        db,
        uid,
        password,
        'product.template',
        'read',
        [template_ids],
        {
            'fields': [
                'name',
                'default_code',
                'categ_id',
                'x_studio_brand',
                'list_price',
                'standard_price',
                'weight',
                'volume',
                'type'
            ]
        }
    )


def get_invoice_line_order(line_ids):
    """Ambil detail sale.order.line berdasarkan list ID."""
    if not line_ids:
        return []

    uid, models = get_odoo()

    return models.execute_kw(
        db,
        uid,
        password,
        'sale.order.line',
        'read',
        [line_ids],
        {
            'fields': [
                'order_id',
                'product_id',
                'product_type',
                'product_template_id',
                'product_uom_qty',
                'qty_delivered',
                'qty_invoiced',
                'product_uom_id',
                'price_unit',
                'tax_ids',
                'discount',
                'price_subtotal'
            ]
        }
    )


def get_sale_orders_by_name(names):
    """
    Cari sale.order berdasarkan nama (invoice_origin di account.move
    adalah Char, bukan relasi ID langsung, jadi harus dicocokkan lewat name).
    """
    if not names:
        return []

    uid, models = get_odoo()

    return models.execute_kw(
        db,
        uid,
        password,
        'sale.order',
        'search_read',
        [[('name', 'in', names)]],
        {
            'fields': [
                'id',
                'name',
                'order_line'
            ]
        }
    )


def build_si_with_lines(invoices):
    """
    Alur relasi (sesuai diagram):
    account.move.invoice_origin (name)
        -> sale.order (by name)
            -> sale.order.line (order_line, one to many)
                -> product.template (product_template_id, one to one)
    """

    # 1. Kumpulkan nama SO unik dari setiap invoice
    origin_names = list({
        inv['invoice_origin']
        for inv in invoices
        if inv.get('invoice_origin')
    })

    if not origin_names:
        for inv in invoices:
            inv['invoice_origin'] = []
        return invoices

    # 2. Ambil sale.order yang cocok
    sale_orders = get_sale_orders_by_name(origin_names)
    so_by_name = {so['name']: so for so in sale_orders}

    # 3. Kumpulkan semua ID sale.order.line dari seluruh sale order
    all_order_line_ids = []
    for so in sale_orders:
        all_order_line_ids.extend(so['order_line'])

    # 4. Ambil detail sale.order.line
    order_lines = get_invoice_line_order(all_order_line_ids)

    # 5. Kumpulkan ID product.template unik dari sale.order.line
    template_ids = list({
        line['product_template_id'][0]
        for line in order_lines
        if line.get('product_template_id')
    })

    # 6. Ambil detail product.template
    templates = get_product_templates2(template_ids)
    template_map = {t['id']: t for t in templates}

    # 7. Kelompokkan sale.order.line berdasarkan sale.order induknya
    lines_by_so_id = {}
    for line in order_lines:
        if not line.get('order_id'):
            continue
        so_id = line['order_id'][0]

        lines_by_so_id.setdefault(so_id, []).append({
            'product_id': line.get('product_id'),
            'product_template': (
                template_map.get(line['product_template_id'][0])
                if line.get('product_template_id') else None
            ),
            'product_type': line.get('product_type'),
            'po_qty': line.get('product_uom_qty'),
            'dl_qty': line.get('qty_delivered'),
            'qty_invoiced': line.get('qty_invoiced'),
            'unit': line.get('product_uom_id'),
            'price_unit': line.get('price_unit'),
            'tax': line.get('tax_ids'),
            'discount': line.get('discount'),
            'price_subtotal': line.get('price_subtotal'),
        })

    # 8. Sisipkan struktur invoice_origin -> [{name, lines}] ke tiap invoice
    for inv in invoices:
        origin_name = inv.get('invoice_origin')
        so = so_by_name.get(origin_name)

        if so:
            inv['invoice_origin'] = [{
                'name': so['name'],
                'lines': lines_by_so_id.get(so['id'], [])
            }]
        else:
            inv['invoice_origin'] = []

    return invoices


@app.route('/api/account/invoice_analytics', methods=['GET'])
def get_invoice_analytics():
    limit = int(request.args.get('limit', 500))
    offset = int(request.args.get('offset', 0))
    limit = min(limit, 1000)
    domain = []

    invoices = odoo_search_read(
        model='account.move',
        domain=domain,
        fields=[
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
        ],
        limit=limit,
        offset=offset
    )

    uid, models = get_odoo()
    total = models.execute_kw(
        db,
        uid,
        password,
        'account.move',
        'search_count',
        [domain]
    )

    data = build_si_with_lines(invoices)

    return jsonify({
        'status': 'success',
        'total': total,
        'count': len(data),
        'limit': limit,
        'offset': offset,
        'has_more': offset + len(data) < total,
        'data': data,
    })

@app.route('/purchase/get/po_analytic', methods=['GET'])
def get_po_analytic():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    purchase_orders = odoo_search_read(
        model='purchase.order',
        domain=[],
        fields=[
            'name',
            'partner_id',
            'partner_ref',
            # 'x_studio_delivery_address', --field custom--
            'currency_id',
            'date_order',
            'date_approve',
            'date_planned',
            'effective_date',
            'picking_type_id',
            'amount_total',
            'order_line',
            'company_id',
            'user_id',
            'origin',
            'state',
        ],
        limit=limit,
        offset=offset
    )

    data = build_po_with_lines(purchase_orders)

    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data,
    })
uid, models = get_odoo()
field_ids = models.execute_kw(
    db,
    uid,
    password,
    'ir.model.fields',
    'search_read',
    [[['model', '=', 'account.move']]],
    {
        'fields': ['name', 'field_description', 'ttype'],
        'order': 'name'
    }
)

for field in field_ids:
    print(field)

def get_product_templates(template_ids):
    uid, models = get_odoo()

    return models.execute_kw(
        db,
        uid,
        password,
        'product.template',
        'read',
        [template_ids],
        {
            'fields': [
                'name',
                'default_code',
                'categ_id',
                'x_studio_brand',
                'list_price',
                'standard_price',
                'weight',
                'volume',
                'type'
            ]
        }
    )
def get_sales_order_lines(line_ids):
    uid, models = get_odoo()
    
    return models.execute_kw(
        db,
        uid,
        password,
        'sale.order.line',
        'read',
        [line_ids],
        {
            'fields': [
                'order_id',
                'product_id',
                'product_type',
                'product_template_id',
                'product_uom_qty',
                'qty_delivered',
                'qty_invoiced',
                'product_uom_id',
                'price_unit',
                'tax_ids',
                'discount',
                'price_subtotal'
            ]
        }
    )

def build_so_with_lines(sales_orders):
    all_line_ids = []
    for so in sales_orders:
        all_line_ids.extend(so['order_line'])

    lines = get_sales_order_lines(all_line_ids)
    template_ids = []

    for line in lines:
        if line['product_template_id']:
            template_ids.append(line['product_template_id'][0])

    template_ids = list(set(template_ids))
    products = get_product_templates(template_ids)
    product_map = {
        p['id']: p
        for p in products
    }
    line_map = {}
    for line in lines:
        product_id = line['order_id'][0]
    
        line_map.setdefault(product_id, []).append({
            'product_id': line['product_id'],
            'product_template': product_map.get(
                line['product_template_id'][0]
            ) if line['product_template_id'] else None,
            'product_type': line['product_type'],
            'product_type': line['product_type'],
            'po_qty': line['product_uom_qty'],
            'dl_qty': line['qty_delivered'],
            'qty_invoiced': line['qty_invoiced'],
            'unit': line['product_uom_id'],
            'price_unit': line['price_unit'],
            'tax': line['tax_ids'],
            'discount': line['discount'],
            'price_subtotal': line['price_subtotal'],
        })

    for so in sales_orders:
        so['lines'] = line_map.get(so['id'], [])
        so.pop('order_line')

    return sales_orders

@app.route('/sales/get/so_analytic', methods=['GET'])
def get_so_analytic():
    limit = int(request.args.get('limit', 500))
    offset = int(request.args.get('offset', 0))
    limit = min(limit, 1000)
    domain = []
    sales_orders = odoo_search_read(
        model='sale.order',
        domain=domain,
        fields=[
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
            'commitment_date',
            'delivery_count',
            'delivery_status',
            'display_name',
            'duplicated_order_ids',
            'effective_date',
            'expected_date',
            # 'expense_count',
            # 'margin',
            # 'margin_percent',
            'medium_id',
            'name',
            'order_line',
            'partner_id',
            'partner_invoice_id',
            'partner_shipping_id',
            'picking_ids',
            'planning_initial_date',
            'pricelist_id',
            'tax_calculation_rounding_method',
            'tax_country_id',
            'team_id',
            'type_name',
            'user_id',
            'validity_date',
            'warehouse_id',
            'write_date',
            'write_uid',
            'company_id',
            'country_code',
            'invoice_status'
        ],
        limit=limit,
        offset=offset
    )

    uid, models = get_odoo()
    total = models.execute_kw(
        db,
        uid,
        password,
        'sale.order',
        'search_count',
        [domain]
    )
    data2 = build_so_with_lines(sales_orders)

    return jsonify({
        'status': 'success',
        'total': total,
        'count': len(data2),
        'limit': limit,
        'offset': offset,
        'has_more': offset + len(data2) < total,
        'data': data2,
    })
    
if __name__ == '__main__':
    # Make sure port 5000 isn't being used by another app (like macOS AirPlay Receiver)
    app.run(debug=True, host='0.0.0.0', port=5001)

