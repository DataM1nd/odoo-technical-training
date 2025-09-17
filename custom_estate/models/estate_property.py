# Imports
from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero

# Create the model
class EstateProperty(models.Model):
    # Define model metadata
    _name = 'estate.property'
    _description = 'Estate Property'
    _sql_constraints = [
        ('check_strictly_positive_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_positive_selling_price', 'CHECK(expected_price >= 0)', 'The selling price must be positive.')
    ]

    # Define fields for the model
    name = fields.Char('Title', required=True)
    description = fields.Text()
    active = fields.Boolean(default=True, required=True)
    postcode = fields.Char()
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)) # We do "lambda self:" to convert it into a function (if we don't do this, we'll always get the same day)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    facades = fields.Integer()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    garden_area = fields.Integer('Garden Area (sqm)')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], copy=False, required=True, default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    # Method for calculating the total area
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self: # Loop through every record where one of the dependent fields changed
            property.total_area = property.living_area + property.garden_area

    # Method for calculating the best price
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        # Alternative (better performance)
        #records_with_offer = self.filtered('offer_ids.price') # Create a list with only the records containing a offer_ids.price
        #for record in records_with_offer:
        #    record.best_price = max(record.offer_ids.mapped('price'))
        #(self - records_with_offer).best_price = 0 # For all the other records, put the amount to 0
        for property in self:
            property.best_price = max([0, *property.offer_ids.mapped('price')])

    # Automatically fill in/remove data when the garden field is (un)checked
    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 0 if not self.garden else 10
        self.garden_orientation = '' if not self.garden else 'north'

    # Function for the button to mark a property as sold
    def action_mark_estate_property_as_sold(self):
        for property in self:
            # Make sure the property is not already cancelled
            if property.state != 'cancelled':
                property.state = 'sold'
            else:
                raise exceptions.UserError('Cancelled properties cannot be sold.')
        return True # We always have to return something in a public function

    # Function for the button to mark a property as sold
    def action_mark_estate_property_as_cancelled(self):
        for property in self:
            # Make sure the property is not already sold
            if property.state != 'sold':
                property.state = 'cancelled'
            else:
                raise exceptions.UserError('Sold properties cannot be cancelled.')
        return True

    # Check that the selling price is not lower than 90% of the expected price
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            # Only do something if the selling price is determined (it's 0 untill an offer is accepted)
            if not float_is_zero(property.selling_price, 2):
                if float_compare(property.selling_price, property.expected_price * 0.9, 2) == -1:
                    raise exceptions.ValidationError('The selling price should be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer.')

    # Prevent deletion if the state is not 'new' or 'cancelled'
    @api.ondelete(at_uninstall=False)
    def _prevent_property_deletion_based_on_state(self):
        if self.filtered_domain([('state', 'not in', ['new', 'cancelled'])]):
            raise exceptions.UserError('Only new and cancelled properties can be deleted.')