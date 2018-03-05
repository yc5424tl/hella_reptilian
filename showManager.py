from datetime import datetime
from flask import redirect, url_for

from models import Show


class ShowManager(object):

    def __init__(self, database, request_form):

        self.db = database
        # self.app = app
        self.rf = request_form

    def update_show(self):

        self.check_for_reference_values()
        self.check_for_input_values()

        orig_date = self.rf['show_orig_date']
        sani_orig_date = self.sanitize_date(orig_date)
        new_date = self.rf['show_date']
        sani_new_date = self.sanitize_date(new_date)
        orig_venue = self.rf['show_orig_venue']
        new_venue = self.rf['show_venue']

        show = self.get_show(sani_orig_date, orig_venue)

        self.edit_show(show, sani_new_date, new_venue)

    def delete_show(self):

        self.check_for_reference_values()

        orig_date = self.rf['show_orig_date']
        sani_orig_date = self.sanitize_date(orig_date)
        orig_venue = self.rf['show_orig_venue']

        show = self.get_show(sani_orig_date, orig_venue)

        self.remove_show(show)

    def add_show(self):

        self.check_for_input_values()

        show_date = self.rf['show_date']
        sani_show_date = self.sanitize_date(show_date)
        new_venue = self.rf['show_venue']

        show = self.create_show(sani_show_date, new_venue)
        self.insert_show(show)

    def insert_show(self, show):
        self.db.session.add(show)
        self.db.session.commit()

    @staticmethod
    def create_show(show_date, venue):
        show = Show(show_date, venue)
        return show

    def edit_show(self, show, new_date, new_venue):
        show.show_date = new_date
        show.show_venue = new_venue
        self.db.session.commit()

    def remove_show(self, show):
        self.db.session.delete(show)
        self.db.session.commit()

    def check_for_reference_values(self):
        if 'show_orig_date' not in self.rf or 'show_orig_venue' not in self.rf:
            # self.app.logger.error('tour_dates post missing req(s)')
            return redirect(url_for('tour_dates'))

    def check_for_input_values(self):
        if 'show_date' not in self.rf or 'show_venue' not in self.rf:
            return redirect(url_for('tour_dates'))

    @staticmethod
    def get_show(show_date, venue):
        show = Show.query.filter_by(show_date=show_date, show_venue=venue).first()
        return show

    @staticmethod
    def sanitize_date(dirty_date):
        clean_date = datetime.strptime(dirty_date, '%Y-%m-%d').date()
        return clean_date