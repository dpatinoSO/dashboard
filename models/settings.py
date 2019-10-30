from openerp import models, fields, api

class DashboardSettings(models.Model):
    _name = 'dashboard.settings'

    @api.one
    def create_fields_dashboard(self):
        partner_id=self.env['ir.model'].search([("name","=","Partner")]).id
        line_id_1={
            'name': 'Numero Clientes',
            'model_id': partner_id,
            'type':'qty',
            'field_id':self.env['ir.model.fields'].search([("model_id","=",partner_id),("name","=","id")]).id,
            'filter':'customer',
            'color':'red',
            'icon':'fa-address-book',
            'display':True,
            'dashboard_id':self.id,
        }
        self.env['dashboard.settings.line'].create(line_id_1)


        invoice_id=self.env['ir.model'].search([("name","=","Invoice")]).id
        line_id_2={
            'name': 'Ventas Totales',
            'model_id': invoice_id,
            'type':'money',
            'field_id':self.env['ir.model.fields'].search([("model_id","=",invoice_id),("name","=","amount_total")]).id,
            'filter':"type='out_invoice'",
            'color':'green',
            'icon':'fa-money',
            'display':True,
            'dashboard_id':self.id,
        }
        self.env['dashboard.settings.line'].create(line_id_2)

        line_id_3={
            'name': 'Compras Totales',
            'model_id': invoice_id,
            'type':'money',
            'field_id':self.env['ir.model.fields'].search([("model_id","=",invoice_id),("name","=","amount_total")]).id,
            'filter':"type='in_invoice'",
            'color':'red',
            'icon':'fa-credit-card-alt',
            'display':True,
            'dashboard_id':self.id,
        }
        self.env['dashboard.settings.line'].create(line_id_3)

        sales_id=self.env['ir.model'].search([("name","=","Sales Order")]).id
        chart_line_1={
            'sequence': 1,
            'display_type':'area',
            'name': 'Ordenes de Compra',
            'chart_model_id': sales_id,
            'type':'money',
            'chart_measure_field_id':self.env['ir.model.fields'].search([("model_id","=",sales_id),("name","=","amount_total")]).id,
            'chart_date_field_id':self.env['ir.model.fields'].search([("model_id","=",sales_id),("name","=","date_order")]).id,
            'filter':'' ,
            'display':True,
            'dashboard_id':self.id,
        }
        self.env['dashboard.settings.chart'].create(chart_line_1)

        invoice_id=self.env['ir.model'].search([("name","=","Invoice")]).id
        chart_line_2={
            'sequence': 2,
            'display_type':'bar',
            'name': 'Facturacion',
            'chart_model_id': invoice_id,
            'type':'money',
            'chart_measure_field_id':self.env['ir.model.fields'].search([("model_id","=",invoice_id),("name","=","amount_total")]).id,
            'chart_date_field_id':self.env['ir.model.fields'].search([("model_id","=",invoice_id),("name","=","date_invoice")]).id,
            'filter':"type='out_invoice'" ,
            'display':True,
            'dashboard_id':self.id,
        }
        self.env['dashboard.settings.chart'].create(chart_line_2)
        

        return True
    
    
    def get_default_chart_model(self):
        return self.search([],limit=1,order='id desc').chart_model_id.id
    def get_default_chart_measure_field(self):
        return self.search([],limit=1,order='id desc').chart_measure_field_id.id
    def get_default_chart_date_field(self):
        return self.search([],limit=1,order='id desc').chart_date_field_id.id
    
    def get_default_lines(self):
        return self.search([],limit=1,order='id desc').line_ids.ids
    
    def get_default_chart(self):
        return self.search([],limit=1,order='id desc').chart_ids.ids
    
    name=fields.Char('Name',default="Setting")
    provider_latitude=fields.Char('latitude')
    provider_longitude=fields.Char('ongitude')
    map=fields.Char('ongitude')
    line_ids=fields.One2many('dashboard.settings.line','dashboard_id','Fields',default=get_default_lines)
    chart_ids=fields.One2many('dashboard.settings.chart','dashboard_id','Charts',default=get_default_chart)
    

class DashboardSettingsLine(models.Model):
    _name = 'dashboard.settings.line'
    
    name=fields.Char('Name')
    model_id = fields.Many2one('ir.model','Model')
    field_id = fields.Many2one('ir.model.fields','Field')
    color=fields.Selection([('red','Red'),('green','Green'),('primary','Primary'),('yellow','Yellow')],string='Color')
    icon=fields.Char('Icon')
    filter=fields.Char('Filter')
    type=fields.Selection([('money','Money'),('qty','Quantity')],string='Type')
    dashboard_id = fields.Many2one('dashboard.settings','Setting')
    display=fields.Boolean('Show/hide',default=True)
    

class DashboardSettingschart(models.Model):
    _name = 'dashboard.settings.chart'
    
    name=fields.Char('Name')
    sequence=fields.Integer('Sequence',default=1)
    display_type=fields.Selection([('area','Area'),('bar','Bar')],string='Display Type')
    chart_model_id = fields.Many2one('ir.model','Chart Model')
    chart_measure_field_id = fields.Many2one('ir.model.fields','Chart measure Field')
    chart_date_field_id = fields.Many2one('ir.model.fields','Chart date Field')
    filter=fields.Char('Filter')
    type=fields.Selection([('money','Money'),('qty','Quantity')],string='Type')
    dashboard_id = fields.Many2one('dashboard.settings','Setting')
    display=fields.Boolean('Show/hide',default=True)
    

