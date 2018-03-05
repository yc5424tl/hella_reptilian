from manage import db, app


class Show(db.Model):

    __tablename__ = 'shows'

    show_id = db.Column(db.Integer, primary_key=True)
    show_date = db.Column(db.Date, nullable=False)
    show_venue = db.Column(db.String, nullable=False)


    def __init__(self, date, venue):
        self.show_date = date
        self.show_venue = venue

    def __repr__(self):
        template = 'id: {} date: {} venue: {}'
        return template.format(self.show_id, self.show_date, self.show_venue)


class Merch(db.Model):

    __tablename__ = 'merch'

    merch_id = db.Column(db.Integer, primary_key=True)
    merch_name = db.Column(db.String, nullable=False)
    merch_cost = db.Column(db.Float, nullable=False)
    merch_descr = db.Column(db.VARCHAR, nullable=False)

    def __init__(self, name, cost, descr):
        self.merch_name = name
        self.merch_cost = cost
        self.merch_descr = descr

    def __repr__(self):
        template = 'id: {} name: {} cost: {} description: {}'
        return template.format(self.merch_id, self.merch_name, self.merch_cost, self.merch_descr)


class Sales(db.Model):

    __tablename__ = 'sales'

    sales_id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id'), nullable=False)
    merch_id = db.Column(db.Integer, db.ForeignKey('merch.merch_id'), nullable=False)
    merch_name = db.Column(db.String, db.ForeignKey('merch.merch_name'), nullable=False)
    num_sold = db.Column(db.Integer, default=0, nullable=False)

    # rel_sales_merch = db.relationship('Merch', backref='sales')

    def __init__(self, show_id, merch_id, merch_name, num_sold):
        self.show_id = show_id
        self.merch_id = merch_id
        self.merch_name = merch_name
        self.num_sold = num_sold

    def __repr__(self):
        template = 'show_id: {} merch_id: {} merch_name: {} number_sold: {}'
        return template.format(self.show_id, self.merch_id, self.merch_name, self.num_sold)