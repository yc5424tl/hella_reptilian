

from models import Sales, Merch


class SalesManager(object):

    def __init__(self, database, request_form):

        self.db = database
        self.rf = request_form

    def add_sale(self, req_f, data):

        db = self.db
        target_show = req_f['select_show_id']

        # str_date = target_show[0:10]
        # date = datetime.strptime(str_date, '%Y-%m-%d').date()
        # venue = target_show[13:]
        #
        # show = get_show_record(date, venue) #could either include this in a hidden column, use its attributes to replace the usage of data/venue above

        items_id_data = db.session.query(Merch.merch_id).all()
        items_name_data = db.session.query(Merch.merch_name).all()
        item_tuples = [(item_id, item_name) for item_id, item_name in zip(items_id_data, items_name_data)]

        for item in item_tuples:

            merch_id = item[0][0]
            merch_name = item[1][0]
            amount = data[merch_name]
            sold = int(amount)

            new_sale = Sales(target_show, merch_id, merch_name, sold)
            db.session.add(new_sale)

        db.session.commit()



    @staticmethod
    def get_post_merch_record(m_name, m_cost, m_descr):

        record = Merch.query.filter_by(merch_name=m_name, merch_cost=m_cost, merch_descr=m_descr).first()
        return record
