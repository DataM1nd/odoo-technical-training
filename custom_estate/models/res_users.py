# Imports
from odoo import fields, models

# Create the model
class ResUsers(models.Model):
    # Define model metadata
    _inherit = 'res.users'

    # Define fields for the model
    property_ids = fields.One2many('estate.property', 'user_id', domain=[('state', 'not in', ['sold', 'cancelled'])])