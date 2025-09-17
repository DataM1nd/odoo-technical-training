# Imports
from odoo import fields, models

# Create the model
class EstatePropertyType(models.Model):
    # Define model metadata
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints = [('check_unique_name', 'UNIQUE(name)', "Another type with this name already exists. The name must be unique across property types.")]

    # Define fields for the model
    name = fields.Char(required=True)