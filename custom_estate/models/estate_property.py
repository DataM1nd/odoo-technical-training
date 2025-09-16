# Imports
from odoo import fields, models

# Create the model
class EstateProperty(models.Model):
    # Define model metadata
    _name = 'estate.property'
    _description = 'Estate Property'

    # Define fields for the model
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postal Code')
    date_availability = fields.Date('Availbility Date', copy=False, default=fields.Date.add(fields.Date.today(), month=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Number of Bedrooms', default=2)
    living_area = fields.Integer('Number of Living Areas')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Has Garage?')
    garden = fields.Boolean('Has Garden?')
    garden_area = fields.Integer('Garden Surface')
    garden_orientation = fields.Selection(string="Garden's Orientation", selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])