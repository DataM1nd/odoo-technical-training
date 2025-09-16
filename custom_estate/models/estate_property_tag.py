# Imports
from odoo import fields, models

# Create the model
class EstatePropertyType(models.Model):
    # Define model metadata
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    # Define fields for the model
    name = fields.Char(required=True)