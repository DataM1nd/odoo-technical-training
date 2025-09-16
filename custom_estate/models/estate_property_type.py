# Imports
from odoo import fields, models

# Create the model
class EstatePropertyType(models.Model):
    # Define model metadata
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    # Define fields for the model
    name = fields.Char(required=True)