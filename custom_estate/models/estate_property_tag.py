# Imports
from odoo import fields, models

# Create the model
class EstatePropertyType(models.Model):
    # Define model metadata
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraints = [('check_unique_name', 'UNIQUE(name)', "Another tag with this name already exists. The name must be unique across property tags.")]

    # Define fields for the model
    name = fields.Char(required=True)