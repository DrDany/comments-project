from flask import Flask, redirect, url_for, render_template, request, flash
import models as db_handler
import json
from flask import Response

# Flask
app = Flask(__name__)


@app.route("/")
def index():
    '''
    Home page
    '''
    return redirect(url_for('view'))


@app.route("/view")
def view():
    '''
    Show alls comments
    '''
    comments = db_handler.get_all_comments()
    return render_template('web/comments.html', comments=comments)


@app.route("/comment", methods=('GET', 'POST'))
def comment():
    '''
    Create new comment
    '''

    if request.method == 'GET':
        return render_template('web/new_comment.html', regions=db_handler.get_all_regions())
    else:
        surname = request.form["surname"]
        name = request.form["name"]
        patronymic = request.form["patronymic"]
        city = request.form["city"]
        phone = request.form["phone"]
        mail = request.form["email"]
        comment = request.form["comment"]
        db_handler.add_new_comment(surname, name, patronymic, city, phone, mail, comment)
        return redirect(url_for('view'))


@app.route("/city", methods=["POST"])
def city():
    region_id = request.form['id']
    city_by_region_id = db_handler.get_city_by_region_id(region_id)
    objects = [
        {
            'id': city['id'],
            'city': city['city'],
        } for city in city_by_region_id
    ]

    json_output = json.dumps(objects)
    return Response(json_output, content_type='application/json')


@app.route("/edit_comment/<id>", methods=('GET', 'POST'))
def edit_comment(id):
    if request.method == 'GET':
        comment = db_handler.get_comment_by_id(id)
        return render_template('web/edit_comment.html', comment=comment)
    else:
        surname = request.form["surname"]
        name = request.form["name"]
        patronymic = request.form["patronymic"]
        city = request.form["city"]
        phone = request.form["phone"]
        mail = request.form["email"]
        comment = request.form["comment"]
        db_handler.update_comment_by_id(surname, name, patronymic, city, phone, mail, comment, id)
        return redirect(url_for('view'))


@app.route("/comment_delete", methods=["POST"])
def comment_delete():
    id = request.form["id"]
    db_handler.delete_comment_by_id(id)
    return redirect(url_for('view'))


@app.route("/stat")
def stat():
    region_id = request.args.get("region_id")
    if region_id is None:
        count = 3
        regions = db_handler.get_regions_comment_count(count)
        comments_count_by_regions = db_handler.get_comment_count_by_regions()
        return render_template('web/stat.html', regions=regions, count=count,
                               comments_count_by_regions=comments_count_by_regions)
    else:
        region = db_handler.get_region_by_id(region_id)
        comment_count_by_region_id = db_handler.get_comment_count_by_region_id(region_id)
        return render_template('web/stat_by_region.html', region=region,
                               comment_count_by_region_id=comment_count_by_region_id)


if __name__ == "__main__":
    app.run()
