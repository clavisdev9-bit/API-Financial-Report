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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

