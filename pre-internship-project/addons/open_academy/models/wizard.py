from odoo import models, fields, api
class Wizard(models.TransientModel):
    _name="openacademy.wizard"

    def _default_sessions(self):
        return self.env["openacademy.session"].browse(self._context.get("active_ids"))

    session_ids = fields.Many2one("openacademy.session", string = "Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2one("res.partner", string = "Attendees")

    #To save the list of attendees added by the wizard into the session'attendee_id's
    @api.multi
    def subscribe(self):
        # s1 |= s2
        # s1 = s1 Union s2
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}
