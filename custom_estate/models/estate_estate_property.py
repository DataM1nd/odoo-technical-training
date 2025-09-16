# Imports
from odoo import fields, models

# Create the new model
class EstateProperty(models.Model):
    # Define model metadata
    _name = 'estate.property'
    _description = 'Estate Property'

    # Define fields