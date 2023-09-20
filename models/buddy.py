from odoo import models, fields, api, _
from datetime import datetime, timedelta


class BringBuddy(models.Model):
    _name = 'bring.your.buddy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bring Your Buddy'
    _rec_name = 'name'

    # name = fields.Char(string='Name')
    marketing_staff_id = fields.Many2many('hr.employee', string='Marketing Staff', required=True)
    batch_id = fields.Many2one('logic.base.batch', string='Batch', required=True)
    batch_start_date = fields.Date(string='Batch Start Date', related='batch_id.from_date')
    batch_end_date = fields.Date(string='Batch End Date', related='batch_id.to_date')
    state = fields.Selection([
        ('draft', 'Draft'), ('done', 'Done'),
    ], string='Status', default='draft')
    batch_students_ids = fields.One2many('bring.your.buddy.attendance', 'bring_ids', string='Students')
    buddy_photo = fields.Binary(string='Buddy Photo')
    remarks = fields.Text(string='Remarks', help='if any remarks')
    date = fields.Date(string='Date', required=True)
    branch = fields.Selection([('corporate_office', 'Corporate Office'), ('cochin_campus', 'Cochin Campus'),
                               ('kottayam_campus', 'Kottayam Campus'), ('calicut_campus', 'Calicut Campus'),
                               ('malappuram_campus', 'Malappuram Campus'), ('trivandrum_campus', 'Trivandrum Campus'),
                               ('palakkad_campus', 'Palakkad Campus'), ('dubai_campus', 'Dubai Campus')],
                              string='Branch')

    @api.depends('batch_students_ids')
    def _compute_child_count(self):
        for record in self:
            record.child_count = len(record.batch_students_ids)

    child_count = fields.Integer(string='Attended Students', compute='_compute_child_count', store=True)

    @api.onchange('batch_id')
    def _compute_batch_name(self):
        students = self.env['logic.students'].search([('batch_id', '=', self.batch_id.id)])
        stud = []
        unlink_commands = [(3, child.id) for child in self.batch_students_ids]
        self.write({'batch_students_ids': unlink_commands})
        for record in students:
            student_data = {
                'name': record.name,
                'std_id': record.id
            }
            stud.append((0, 0, student_data))
        self.batch_students_ids = stud

    def action_done(self):
        students = []
        student = self.env['logic.students'].search([('id', 'in', [stud.std_id for stud in self.batch_students_ids])])
        for i in student:
            for jk in self.batch_students_ids:
                print(i.name, 'uiddisfh')
                if i.id == jk.std_id:
                    res_list_std = {
                        'name': jk.name,
                        'attendance': jk.day_attendance,
                        'date': self.date,
                        'stud_id': jk.std_id
                    }
                    students.append((0, 0, res_list_std))
                    i.bring_buddy_attendance_ids = students
                else:
                    print('noo')
                std = self.env['logic.students'].search([])
                for jk in std:
                    for jkm in jk.bring_buddy_attendance_ids:

                        if jkm.stud_id != jk.id:
                            jkm.unlink()

        batches_feedback = self.env['mail.activity'].search([('res_id', '=', self.batch_id.id), (
            'activity_type_id', '=', self.env.ref('bring_your_buddy.mail_activity_bring_your_buddy').id)])
        batches_feedback.action_feedback(feedback='Bring Your Buddy Done')
        batches = self.env['mail.activity'].search([('res_id', '=', self.batch_id.id), (
            'activity_type_id', '=', self.env.ref('bring_your_buddy.mail_activity_bring_your_buddy').id)])
        batches.unlink()

        self.state = 'done'

    name = fields.Char(
        string='Custom Name',
        compute='_compute_custom_name',
        store=True,
    )

    @api.depends('batch_id')
    def _compute_custom_name(self):
        for record in self:
            print('jhsdgffy')
            # Customize the custom_name based on other fields
            record.name = f'Bring Your Buddy Batch {record.batch_id.name} '

    def activity_batch_coordinator_bring_buddy(self):
        records = self.env['logic.base.batch'].sudo().search([])
        current_date = datetime.now().date()
        print(current_date)
        activity_type = self.env.ref('bring_your_buddy.mail_activity_bring_your_buddy')
        for record in records:
            date_14_days_later = record.from_date + timedelta(days=14)
            if current_date == date_14_days_later:
                if record.class_teacher_id:
                    user_id = record.class_teacher_id.user_id.id
                    record.activity_schedule('bring_your_buddy.mail_activity_bring_your_buddy', user_id=user_id,
                                             note=f'{record.name} This Batch commenced two weeks ago from today.')
                    print(date_14_days_later, 'day')
                    print(record.name, 'its after 14 days')
                    print(record.from_date, 'rec from date')
                    # activity = self.env['mail.activity'].create({
                    #     'activity_type_id': self.env.ref('bring_your_buddy.mail_activity_bring_your_buddy').id,
                    #     'res_id': self.id,
                    #     'res_model_id': self.env.ref('bring_your_buddy.model_bring_your_buddy').id,  # Replace with your model's ID
                    #     'user_id': user_id,
                    #     # 'date_deadline': fields.Date.today(),  # Set the due date of the activity (you can change this)
                    #     'note': f"{record.name} + This Batch commenced two weeks ago from today. ",  # Add any notes or description for the activity
                    # })
                    # return True
            else:
                print(record.name, 'rec not 14 days')
