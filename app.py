from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flask_paginate import Pagination, get_page_args


app = Flask(__name__)
bootstrap = Bootstrap(app)

# change this to your own db config here
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = '3172lab5'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# separate result to fit paginate
def subset_res(res, offset=0, per_page=20):
    return res[offset: offset + per_page]







@app.route('/', methods=['POST','GET'])
def search():
    cur = mysql.connection.cursor()
    results = []
    if 'inst' in request.args or 'inst_course' in request.args or 'dal_course'in request.args or 'cre' in request.args or 'approve' in request.args or 'page' in request.args:
        # run the query
        inst = request.args.get('inst')
        inst_course = request.args.get('inst_course')
        dal_course = request.args.get('dal_course')
        credit = request.args.get('cre')
        approve = request.args.get('approve')
        keyword = "Your search result for " + inst + " "+ " "+ inst_course + " " + dal_course + " " + credit + " " + approve
        qry = ["%s LIKE '%%%s%%'" % (x, y) for x, y in
                   (('inst_name', inst), ('inst_course', inst_course), ('dal_course', dal_course), ('inst_credit', credit), ('dal_credit', credit), ('last_assess', approve))
                   if y is not None and y != '']
        if not qry:
            return render_template('search.html')
        cur.execute(
                'SELECT * FROM Course WHERE '
                    + ' AND '.join(qry) + ';')
        results = cur.fetchall()
        for result in results:
            print(result)
        # use get_page_args to get page and offset, as we define perpage below, set it to _
        page, _, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        page_results = subset_res(results, offset=offset, per_page=20)
        pagination = Pagination(page=page, total=len(results), bs_version=3, per_page=20)

        return render_template('search.html', results=page_results, pagination=pagination, keyword = keyword)

    else:
        return  render_template('search.html')












if __name__ == '__main__':
    app.run()