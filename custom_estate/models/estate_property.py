# Imports
from odoo import fields, models

# Create the model
class EstateProperty(models.Model):
    # Define model metadata
    _name = 'estate.property'
    _description = 'Estate Property'

    # Define fields for the model
    name = fields.Char('Title', required=True)
    active = fields.Boolean(default=True, required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)) # We do "lambda self:" to convert it into a function (if we don't do this, we'll always get the same day)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    garden_area = fields.Integer('Garden surface area')
    facades = fields.Integer()
    garage = fields.Boolean('Has garage?')
    garden = fields.Boolean('Has garden?')
    garden_orientation = fields.Selection(string="Garden's orientation", selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], copy=False, required=True, default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')