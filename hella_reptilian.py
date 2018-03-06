import os
from flask import Flask, render_template, request, abort, redirect, url_for
from flask.views import MethodView
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://frwarqgpoagzfk:1739020739f0fabf22d558773024fbf2ea9738941d8082fe216bc5cf030971fd@ec2-54-204-46-60.compute-1.amazonaws.com:5432/d7igmaohp1q70m'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#sECRET_KEY = os.environ['flask-secret-key']
app.config.from_object(__name__)
db = SQLAlchemy(app)


from models import Merch, Sales, Show


@app.route('/')
def home():
    return render_template('home.html', active='home')


@app.route('/merch_table/<int:merch_id>')
def merch_info(merch_id):
    target_merch = Merch.query.get_or_404(merch_id)
    return render_template('merch_table.html', merch=target_merch, active='merch_table')


@app.route('/merch_table', methods=['GET', 'POST'])
def merch_table():

    if request.method == 'GET':

        items = db.session.query(Merch.merch_name, Merch.merch_cost, Merch.merch_descr).order_by(Merch.merch_name)
        return render_template('merch_table.html', items=items, active='merch_table')

    if request.method == 'POST':

        action_type = request.form['actions']  # https://stackoverflow.com/a/31663422

        f_merch_name = request.form['merch_name']
        f_merch_cost = request.form['merch_cost']
        f_merch_descr = request.form['merch_descr']

        orig_merch_name = request.form['merch_orig_name']
        orig_merch_cost = request.form['merch_orig_cost']
        orig_merch_descr = request.form['merch_orig_descr']

        if not f_merch_name or not f_merch_cost or not f_merch_descr or not action_type:

            app.logger.error('Attempt to create merch without name, cost, and/or description.')
            return redirect(url_for('merch_table'))

        if action_type == 'upd':

            if 'merch_name' not in request.form \
            or 'merch_cost' not in request.form \
            or 'merch_descr' not in request.form\
            or 'merch_orig_name' not in request.form \
            or 'merch_orig_cost' not in request.form \
            or 'merch_orig_descr' not in request.form :

                app.logger.error('update to merch_table missing name, cost, and/or dscr')
                abort(500)

            record = get_post_merch_record(orig_merch_name, orig_merch_cost, orig_merch_descr)
            sales = get_merch_sale_records(orig_merch_name)

            for sale in sales:
                sale.merch_name = f_merch_name

            record.merch_name = f_merch_name
            record.merch_cost = f_merch_cost
            record.merch_descr = f_merch_descr

            db.session.commit()

        if action_type == 'del':

            if 'merch_orig_name' not in request.form \
            or 'merch_orig_cost' not in request.form \
            or 'merch_orig_descr' not in request.form:

                app.logger.error('del merch_table POST missing orig name, cost, and/or descr')
                abort(500)

            record = get_post_merch_record(orig_merch_name, orig_merch_cost, orig_merch_descr)

            db.session.delete(record)
            db.session.commit()

        if action_type == 'add':

            if 'merch_name' not in request.form \
            or 'merch_cost' not in request.form \
            or 'merch_descr' not in request.form:

                app.logger.error('add merch_table POST missing name, cost, and/or descr')
                abort(500)

            new_merch = Merch(f_merch_name, f_merch_cost, f_merch_descr)

            db.session.add(new_merch)
            db.session.commit()

        items = db.session.query(Merch.merch_name, Merch.merch_cost, Merch.merch_descr).order_by(Merch.merch_name)

        return render_template('merch_table.html', items=items, active='merch_table')


@app.route('/tour_dates/<int:show_id>')
def show_info(show_id):
    target_show = Show.query.get_or_404(show_id)
    return render_template('tour_dates.html', show=target_show, active='tour_dates')


class TourDatesView(MethodView):

    def __init__(self, template_name):
        self.template_name=template_name

    def render(self):
        shows = db.session.query(Show.show_id, Show.show_date, Show.show_venue).order_by(Show.show_date)
        return render_template(self.template_name, shows=shows, active='tour_dates')

    def get(self):
        return self.render()

    def post(self):

        rf = request.form
        import showManager
        show_mgr = showManager.ShowManager(db, rf)

        if not rf['show_date'] or not rf['show_venue'] or not rf['actions']:
            app.logger.error('post to tour_dates missing data, venue, and/or action')
            return redirect(url_for('tour_dates'))

        if rf['actions'] == 'upd':
            show_mgr.update_show()

        if rf['actions'] == 'del':
            show_mgr.delete_show()

        if rf['actions'] == 'add':
            show_mgr.add_show()

        return self.render()


class SalesReportView(MethodView):

    def __init__(self, template_name):
        self.template_name = template_name


    def render(self):

        shows_data = db.session.query(Show).all()
        items_data = db.session.query(Merch).all()
        sales_data = db.session.query(Sales.show_id, Sales.merch_id, Sales.merch_name, Sales.num_sold).order_by(Sales.show_id)

        return render_template(self.template_name, sales=sales_data, shows=shows_data, items=items_data,  active='sales')

    def get(self):

        return self.render()

    def post(self):

        rf = request.form

        f_data = dict((key, rf.getlist(key) if len(rf.getlist(key)) > 1 else rf.getlist(key)[0]) for key in rf.keys())
                                                                    # https://stackoverflow.com/a/18422573
        action = f_data['actions']

        import salesManager
        sales_mgr = salesManager.SalesManager(db, rf)

        if action == 'add':
            sales_mgr.add_sale(rf, f_data)

        if action == 'del':
            pass

        if action == 'upd':
            pass

        return self.render()


# def get_post_merch_record(m_name, m_cost, m_descr):
#
#     record = Merch.query.filter_by(merch_name=m_name, merch_cost=m_cost, merch_descr=m_descr).first()
#     return record


# def update_show(rf):
#
#     check_for_reference_values(rf)
#     check_for_input_values(rf)
#
#     orig_date = rf['show_orig_date']
#     sani_orig_date = sanitize_date(orig_date)
#     new_date = rf['show_date']
#     sani_new_date = sanitize_date(new_date)
#     orig_venue = rf['show_orig_venue']
#     new_venue = rf['show_venue']
#
#     show = get_show(sani_orig_date, orig_venue)
#     # show_table = Show.query.all()
#     edit_show(show, sani_new_date, new_venue)
#
#
#
# def delete_show( rf):
#     check_for_reference_values(rf)
#
#     orig_date = rf['show_orig_date']
#     sani_orig_date = sanitize_date(orig_date)
#     orig_venue = rf['show_orig_venue']
#
#     show = get_show(sani_orig_date, orig_venue)
#     remove_show(show)
#
#
#
# def add_show(rf):
#     check_for_input_values(rf)
#     show_date = rf['show_date']
#     sani_show_date = sanitize_date(show_date)
#     new_venue = rf['show_venue']
#
#     show = create_show(sani_show_date, new_venue)
#     insert_show(show)
#
# def insert_show(show):
#     db.session.add(show)
#     db.session.commit()
#
#
# def create_show(show_date, venue):
#     show = Show(show_date, venue)
#     return show
#
#
# def edit_show(show, new_date, new_venue):
#     show.show_date = new_date
#     show.show_venue = new_venue
#     db.session.commit()
#
#
# def remove_show(show):
#     db.session.delete(show)
#     db.session.commit()
#
#
# def check_for_reference_values(rf):
#     if 'show_orig_date' not in rf or 'show_orig_venue' not in rf:
#         app.logger.error('tour_dates post missing req(s)')
#         return redirect(url_for('tour_dates'))
#
#
# def check_for_input_values(rf):
#     if 'show_date' not in rf or 'show_venue' not in rf:
#         app.logger('tour_dates post missing req(s)')
#         return redirect(url_for('tour_dates'))
#
#
#
#
# def get_show(show_date, venue):
#
#     show = Show.query.filter_by(show_date=show_date, show_venue=venue).first()
#     return show


# def sanitize_date(dirty_date):
#
#     clean_date = datetime.strptime(dirty_date, '%Y-%m-%d').date()
#     return clean_date


# def add_sale(req_f, data):
#
#     target_show = req_f['select_show_id']
#     # str_date = target_show[0:10]
#     # date = datetime.strptime(str_date, '%Y-%m-%d').date()
#     # venue = target_show[13:]
#     #
#     # show = get_show_record(date, venue) #could either include this in a hidden column, use its attributes to replace the usage of data/venue above
#
#     items_id_data = db.session.query(Merch.merch_id).all()
#     items_name_data = db.session.query(Merch.merch_name).all()
#     item_tuples = [(item_id, item_name) for item_id, item_name in zip(items_id_data, items_name_data)]
#
#     for item in item_tuples:
#
#         merch_id = item[0][0]
#         merch_name = item[1][0]
#         amount = data[merch_name]
#         sold = int(amount)
#
#         new_sale = Sales(target_show, merch_id, merch_name, sold)
#         db.session.add(new_sale)
#
#     db.session.commit()


# def get_show_record(s_date, s_venue):
#     show = Show.query.filter_by(show_date=s_date, show_venue=s_venue).first()
#     return show


#class view routes
app.add_url_rule('/tour_dates', view_func=TourDatesView.as_view('tour_dates', 'tour_dates.html'), methods=['GET', 'POST'])
app.add_url_rule('/sales', view_func=SalesReportView.as_view('sales', 'sales.html'), methods=['GET', 'POST'])


def get_post_merch_record(m_name, m_cost, m_descr):

    record = Merch.query.filter_by(merch_name=m_name, merch_cost=m_cost, merch_descr=m_descr).first()
    return record


def get_merch_sale_records(m_name):
    sales = Sales.query.filter_by(merch_name=m_name)
    return sales

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)