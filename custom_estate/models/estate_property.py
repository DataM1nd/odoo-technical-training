# Imports
from odoo import fields, models

# Create the model
class EstateProperty(models.Model):
    # Define model metadata
    _name = 'estate.property'
    _description = 'Estate Property'

    # Define fields for the model
    name = fields.Char(required=True)
    active = fields.Boolean(default=True, required=True)
    description = fields.Text()
    postcode = fields.Char('Postal Code')
    date_availability = fields.Date('Availability date', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer('Number of bedrooms', default=2)
    living_area = fields.Integer('Living room surface area')
    garden_area = fields.Integer('Garden surface area')
    facades = fields.Integer('Number of facades')
    garage = fields.Boolean('Has garage?')
    garden = fields.Boolean('Has garden?')
    garden_orientation = fields.Selection(string="Garden's orientation", selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], copy=False, required=True, default='new')