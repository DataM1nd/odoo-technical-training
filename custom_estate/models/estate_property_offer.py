# Imports
from odoo import api, fields, models, exceptions

# Create the model
class EstatePropertyOffer(models.Model):
    # Define model metadata
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _sql_constraints = [('check_strictly_positive_price', 'CHECK(price >= 0)', "The offer's price must be strictly positive.")]

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
        for offer in self:
            offer.date_deadline = fields.Date.add(offer.create_date or fields.Date.today(), days=offer.validity)

    # Method for calculating the validity when the date_deadline field is changed
    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.to_date(offer.create_date)).days

    # Button function to accept an offer
    def action_accept_estate_property_offer(self):
        for offer in self:
            # Only do something if the current offer is not already accepted
            if not offer.status == 'accepted':
                # Make sure there is not already an accepted offer
                if not offer.property_id.offer_ids.filtered_domain([('status', '=', 'accepted')]):
                    offer.status = 'accepted'
                    offer.property_id.partner_id = offer.partner_id
                    offer.property_id.selling_price = offer.price
                else:
                    raise exceptions.UserError('Another offer was already accepted for this property.')
        return True

    # Button function to refuse an offer
    def action_refuse_estate_property_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True

    # Override the create function to update the state of the property when an offer is created
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            if property.offer_ids.filtered_domain([('price', '>', vals['price'])]):
                raise exceptions.UserError('You cannot create a lower offer than the ones already existing.')
            else:
                property.state = 'offer_received'
        return super().create(vals_list)