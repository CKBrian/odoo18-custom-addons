from odoo import api, models, fields
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'
    _sql_constraints = [
        ('positive_price', 'CHECK(expected_price >= 0)', 'Property expected price must be strictly positive'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Property selling price must be strictly positive')
    ]
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price == 0.0:
                continue
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError('The selling price must be at least 90% of the expected price')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garden = fields.Boolean()
    garage = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')],
        help='Direction of the garden'
    )
    state = fields.Selection(
        string='Status',
        required=True,
        default='new',
        selection=[('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold')],
        help='Status of the property'
    )
    property_type_id = fields.Many2one(
            'estate.property.type',
            string="Property Type")
    salesperson_id = fields.Many2one('res.users',
            string='Salesperson',
            default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offers')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    def unlink(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError('You can only delete properties that are New or Cancelled.')
        return super().unlink()

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be sold')
            record.state = 'sold'
        return True

    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be cancelled.')
            record.state = 'cancelled'
        return True



class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique')
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help='Used to order stages')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Property Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_view_offers(self):
        return True


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Property tag name must be unique')
        ]

    name = fields.Char(required=True)
    color = fields.Integer('Color Index')


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'
    _sql_constraints = [
        ('positive_price', 'CHECK(price > 0)', 'Offer price must be strictly positive'),
    ]

    price = fields.Float()
    status = fields.Selection(
            string='Status',
            selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
            copy=False)
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True, string='Property')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
            compute='_compute_date_deadline',
            inverse='_inverse_date_deadline'
            )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        string='Property Type',
        store=True
    )
    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if 'property_id' in values:
                property = self.env['estate.property'].browse(values['property_id'])
                property.state = 'offer_received'
                offers = property.offer_ids.mapped('price')
                if offers and float_compare(min(offers), values['price'],2) > 0:
                    raise UserError('The offer price must be higher than the current best offer.')
        return super().create(vals_list)
    
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = (record.create_date + timedelta(days=record.validity)).date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
    def action_accepted(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True
    def action_refused(self):
        for record in self:
            record.status = 'refused'
        return True
