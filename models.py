from sqlalchemy import UniqueConstraint, ForeignKeyConstraint

from manage import db




class Show(db.Model):

    __tablename__ = 'shows'

    show_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_date = db.Column(db.Date, nullable=False)
    show_venue = db.Column(db.String, nullable=False)
    sales = db.relationship('Sales', backref='shows', cascade='all, delete orphan', lazy='dynamic')

    # sales = db.relationship('sales', backref='shows', passive_deletes=True)
    # sales = db.relationship("Sales", cascade="save-update, merge, delete")
    def __init__(self, date, venue):
        self.show_date = date
        self.show_venue = venue

    def __repr__(self):
        template = 'id: {} date: {} venue: {}'
        return template.format(self.show_id, self.show_date, self.show_venue)


class Merch(db.Model):

    __tablename__ = 'merch'

    merch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merch_name = db.Column(db.String, nullable=False, unique=True)
    merch_cost = db.Column(db.Float, nullable=False)
    merch_descr = db.Column(db.VARCHAR, nullable=False)
    sales = db.relationship('Sales', backref='merch', cascade='all, delete-orphan', lazy='dynamic')
    #
    # sales = db.relationship('Sales', cascade="save-update, merge, delete")
    # sales = db.relationship('sales', backref='merch', passive_deletes=True)

    def __init__(self, name, cost, descr):
        self.merch_name = name
        self.merch_cost = cost
        self.merch_descr = descr

    def __repr__(self):
        template = 'id: {} name: {} cost: {} description: {}'
        return template.format(self.merch_id, self.merch_name, self.merch_cost, self.merch_descr)


class Sales(db.Model):

    # __tablename__ = 'sales'
    # __table_args__ = (UniqueConstraint('show_id', 'merch_id', 'merch_name', name='sales_table_unique_constraint_show-id_merch-id_merch-name'),)

    #sales_id = db.Column(db.Integer, primary_key=True)
    # show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id', onupdate="CASCADE", ondelete="CASCADE", nullable=False))
    # merch_id = db.Column(db.Integer, db.ForeignKey('merch.merch_id', onupdate="CASCADE", nullable=False))
    # merch_name = db.Column(db.String, db.ForeignKey('merch.merch_name', onupdate="CASCADE", nullable=False))
    #show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id'), nullable=False)
    # merch_id = db.Column(db.Integer, db.ForeignKey('merch.merch_id'), nullable=False)


    __tablename__ = 'sales'
    __table_args__ = (UniqueConstraint('show_id', 'merch_name', name='unique_show_merch'),)
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id'), nullable=False)
    merch_name = db.Column(db.String, db.ForeignKey('merch.merch_name'), nullable=False)
    num_sold = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, show_id, merch_name, num_sold):
        self.show_id = show_id
        self.merch_name = merch_name
        self.num_sold = num_sold

    def __repr__(self):
        template = 'show_id: {} merch_name: {} number_sold: {}'
        return template.format(self.show_id, self.merch_name, self.num_sold)
    # rel_show_id = db.relationship("Sales", foreign_keys=show_id, back_populates="rel_sales")
    # rel_merch_id = db.relationship("Merch", foreign_keys=merch_id, back_populates="rel_sales_id")
    # rel_merch_name = db.relationship("Merch", foreign_keys=merch_name, back_populates="rel_sales_name")

    # show = db.relationship(Show, foreign_keys=show_id)
    # item_id = db.relationship(Merch, foreign_keys=merch_id)
    # item_name = db.relationship(Merch, foreign_keys=merch_name)

    # def __init__(self, show_id, merch_id, merch_name, num_sold):
    #     self.show_id = show_id
    #     self.merch_id = merch_id
    #     self.merch_name = merch_name
    #     self.num_sold = num_sold
    #
    # def __repr__(self):
    #     template = 'show_id: {} merch_id: {} merch_name: {} number_sold: {}'
    #     return template.format(self.show_id, self.merch_id, self.merch_name, self.num_sold)