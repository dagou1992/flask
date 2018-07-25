import os

from app import *
from app.task import task
from db_utils import ModelUtil
from flask_login import login_required

db_name = "Task"
table_name = "task_list"


def list_set(a, b):
    return list(set(a + b))


def update_user_data(item):
    ModelUtil.update("User", "user", item)


@task.route('/', methods=['POST'])
@login_required
def get_task_list():
    result = []
    conditions = {}
    args = request.get_json()
    if args.get('start_time'):
        conditions["updated_time"] = {"$gte": int(args.get('start_time'))}
    if args.get('end_time'):
        conditions["updated_time"] = {"$lte": int(args.get('end_time'))}
    if args.get('start_time') and args.get('end_time'):
        conditions["updated_time"] = {"$gte": int(args.get('start_time')), "$lte": int(args.get('end_time'))}
    if args.get('bag_name'):
        conditions["bag_name"] = args.get('bag_name')
    if args.get('marker'):
        conditions["marker"] = args.get('marker')
    if args.get('reviewer'):
        conditions["reviewer"] = args.get('reviewer')
    lists = ModelUtil.query_many(db_name, table_name, conditions)
    for item in lists:
        item.pop('_id')
        result.append(item)
    return json_response_ok(result)


@task.route('/', methods=['PATCH'])
@login_required
def update_task():
    form = request.get_json()
    bag_list = form['bag_name']
    marker = form['marker']
    reviewer = form['reviewer']
    mark_search = ModelUtil.query_one("User", "user", {'username': marker})
    review_search = ModelUtil.query_one("User", "user", {'username': reviewer})
    if mark_search is not None and review_search is not None:
        for bag in bag_list:
            message = ModelUtil.query_one(db_name, table_name, {'bag_name': bag})
            message['marker'] = marker
            message['reviewer'] = reviewer
            message['status'] = 1
            ModelUtil.update(db_name, table_name, message)
        mark_search['mark_list'] = list_set(mark_search['mark_list'], bag_list)
        update_user_data(mark_search)
        if marker == reviewer:
            review_search = mark_search
        review_search['review_list'] = list_set(review_search['review_list'], bag_list)
        update_user_data(review_search)
        return json_response_ok('success')
    else:
        return json_response_error(401, 'The user is not exist.'), 200


def load_task_list():
    anno_dir = './nfs/lidar_data/raw_data/'
    for path in os.listdir(anno_dir):
        item = {
            "marker": '',
            "reviewer": '',
            "bag_name": "bag-" + path.replace('.bag', ''),
            "status": 0
        }
        if ModelUtil.exists(db_name, table_name, {"bag_name": "bag-" + path.replace('.bag', '')}):
            continue
        ModelUtil.add(db_name, table_name, item)
        ModelUtil.create_index(db_name, table_name, ['bag_name'])
    print('update done')
