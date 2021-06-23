#  Nikulin Vasily (c) 2021

from flask import render_template, Blueprint, abort
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from data import db_session
from data.companies import Company
from data.db_functions import get_game_roles
from data.news import News
from data.users import User

news_page = Blueprint('news-page', __name__)
app = news_page


@app.route('/news')
@mobile_template('{mobile/}news.html')
@login_required
def news(template):
    if not get_game_roles():
        abort(404)

    db_sess = db_session.create_session()

    data = list(db_sess.query(News.title, News.message, News.user_id, News.company_id,
                              News.date, News.author, News.id, News.picture))
    news_list = []
    days_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа',
                 'сентября', 'октября', 'ноября', 'декабря']

    for i in range(len(data)):
        user = ' '.join(db_sess.query(User.surname, User.name).filter(
            User.id == data[i][2]
        ).first())
        if data[i][5] == 'от себя':
            company = 0
        else:
            company = db_sess.query(Company.title).filter(
                Company.id == data[i][3]
            ).first()[0]
        date = str(data[i][4]).split()
        time = date[1].split(':')
        time = ':'.join((time[0], time[1]))
        date = date[0].split('-')
        date = f'{date[2]} {days_list[int(date[1]) - 1]}'
        date = f'{date} в {time}'
        news_list.append([data[i][6], data[i][0], data[i][1], user, company, date, data[i][5],
                          data[i][7]])

    news_list.reverse()
    return render_template(template,
                           game_role=get_game_roles(),
                           title='Новости',
                           news=news_list)
