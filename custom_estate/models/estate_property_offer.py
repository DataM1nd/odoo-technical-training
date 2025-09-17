# Imports
from odoo import api, fields, models, exceptions

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

    # Button function to accept an offer
    def action_accept_estate_property_offer(self):
        for record in self:
            # Make sure there is not already an accepted offer
            if not record.property_id.offer_ids.filtered_domain([('status', '=', 'accepted')]):
                record.status = 'accepted'
                record.property_id.partner_id = record.partner_id
                record.property_id.selling_price = record.price
            else:
                raise exceptions.UserError('Another offer was already accepted for this property.')
        return True

    # Button function to refuse an offer
    def action_refuse_estate_property_offer(self):
        for record in self:
            record.status = 'refused'
        return True