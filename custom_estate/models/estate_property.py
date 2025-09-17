# Imports
from odoo import api, fields, models

# Create the model
class EstateProperty(models.Model):
    # Define model metadata
    _name = 'estate.property'
    _description = 'Estate Property'

    # Define fields for the model
    name = fields.Char('Title', required=True)
    description = fields.Text()
    active = fields.Boolean(default=True, required=True)
    postcode = fields.Char()
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)) # We do "lambda self:" to convert it into a function (if we don't do this, we'll always get the same day)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    facades = fields.Integer()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    garden_area = fields.Integer('Garden Area (sqm)')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], copy=False, required=True, default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    # Method for calculating the total area
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self: # Loop through every record where one of the dependent fields changed
            record.total_area = record.living_area + record.garden_area

    # Method for calculating the best price
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        # Alternative (better performance)
        #records_with_offer = self.filtered('offer_ids.price') # Create a list with only the records containing a offer_ids.price
        #for record in records_with_offer:
        #    record.best_price = max(record.offer_ids.mapped('price'))
        #(self - records_with_offer).best_price = 0 # For all the other records, put the amount to 0
        for record in self:
            record.best_price = max([0, *record.offer_ids.mapped('price')])

    # Automatically fill in/remove data when the garden field is (un)checked
    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 0 if not self.garden else 10
        self.garden_orientation = '' if not self.garden else 'north'