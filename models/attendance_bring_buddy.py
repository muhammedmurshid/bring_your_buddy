from odoo import models, fields, api, _


class BringBuddyAttendance(models.Model):
    _name = 'bring.your.buddy.attendance'

    name = fields.Char(string='Name')
    bring_ids = fields.Many2one('bring.your.buddy')
    day_attendance = fields.Boolean(string='Day Attendance', default=True)
    std_id = fields.Integer()
