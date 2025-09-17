# Imports
from odoo import api, fields, models

# Create the model
class EstatePropertyOffer(models.Model):
    # Define model metadata
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    # Define fields for the model
    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    # Method for calculating the deadline when the validity field is changed
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)

    # Method for calculating the validity when the date_deadline field is changed
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = record.date_deadline.day - record.create_date.day