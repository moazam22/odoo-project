# -*- coding: utf-8 -*-
# from odoo import fields, models
# class Partner(models.Model):
#     _inherit="res.partner"
# #    instructor= fields.Boolean('Instructor', Default=False)
#     instructor = fields.Boolean("Instructor", default=False)
#     session_ids= fields.Many2many('openacademy.session', string='Attended Sessions', readonly=True)

from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)
