# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import timedelta

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users',
        ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")


    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)



    _sql_constraints = [
        ('Name_check_Description',
         'CHECK(name != description)',
         'Title and Description should not be same.'),
        ('Unique Title',
         'UNIQUE(name)',
         'Title of Course must be Unique.')
    ]


class Session(models.Model):
    _name="openacademy.session"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help="Duration in Days.")
    seats = fields.Integer(string="Number of Seats")
    instructor_id = fields.Many2one(
        'res.partner', string="Instructor",
        domain=['|', ('instructor', '=', True),
                ('category_id.name', 'ilike', "Teacher")
                ]
    )
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string='Taken Seats', compute='_taken_seats')
    active = fields.Boolean(default=True)
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string='Duration in hours', compute='_get_hours', inverse='_set_hours' )
    attendees_count = fields.Integer(string="Attendees Count", compute="_get_attendees_count", store=True)
    color = fields.Integer()


    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count=len(record.attendee_ids)

    @api.depends('duration')
    def _get_hours(self):
        for record in self:
            record.hours = record.duration * 24
    def _set_hours(self):
        for record in self:
            record.duration = record.hours / 24


    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for a in self:
            if not a.seats:
                a.taken_seats = 0.00
            else:
                a.taken_seats = (len(a.attendee_ids)/a.seats)*100

    #Caledar View
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration
    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1






    #onchange function is giving erorr while adding -ve seats number and increasing the number of attendee's than the seats
    #but it is not raising the warning
    # except warning it is working fine!
    @api.onchange('seats','attendee_ids')
    def _validate_verify_seats(self):
        if self.seats < 0:
            return {
                'warning':{
                    'title':_('Invalid value of Seats'),
                    'msg':_('Seats cannot be Negative'),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning':{
                    'title':_('Too many Attendees.'),
                    'msg':_('Ether Increase Seats or reduce Attendees.'),
                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_constraints(self):
        for record in self:
            if record.instructor_id:
                if record.instructor_id in record.attendee_ids:
                    raise exceptions.ValidationError(_('An instructor cannot be  an attendee in his/her own Session.'))












































# class open_academy(models.Model):
#     _name = 'open_academy.open_academy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100