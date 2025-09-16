from odoo import fields, models

# Create a new model
class EstateProperty(models.Model):
    # Define model metadata
    _name = 'estate.property'
    _description = 'Estate Property'

    # Define fields
    name = fields.Char(required=True)
    description = fields.Text()
    date_availability = fields.Date()
    expected_price = fields.Float()
    bedrooms = fields.Integer()
    garden = fields.Boolean()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'Sout'), ('east', 'East'), ('west', 'West')])