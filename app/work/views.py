import os

from app import *
from app.work import work
from db_utils import ModelUtil
from workload import f_workload
from flask_login import login_required

db_name = 'Work'
table_name = 'work_list'
time_name = 'update_request_time'


def timestamp():
    import time
    return int(time.time())


@work.route('/', methods=['POST'])
@login_required
def get_work_list():
    form = request.get_json()
    start_time = int(form['start_time']) if 'start_time' in form else 180000000
    end_time = int(form['end_time']) if 'end_time' in form else 1800000000
    marker = form['marker']
    now_time = timestamp()
    last_update_time = ModelUtil.query_one(db_name, time_name, {}, False)['updated_time']
    mark_list = ModelUtil.query_one('User', 'user', {"username": marker})['mark_list']
    result = []
    if mark_list is not None:
        if now_time - last_update_time >= 2000:
            lists = load_work_list()
        else:
            lists = ModelUtil.query_many(db_name, table_name, {"update_time": {"$gte": start_time, "$lte": end_time}})
        for item in lists:
            if (marker != '' and item['bag_name'] in mark_list) or marker == '':
                item.pop('_id')
                item.pop('deleted')
                result.append(item)
        return json_response_ok(result)
    else:
        return json_response_error(401, 'The user is not exist.'), 200


@work.route('/', methods=['PATCH'])
@login_required
def update_work_list():
    load_work_list()
    return json_response_ok('success')


def load_work_list():
    anno_dir = './nfs/lidar_data/labeled_data/'
    if not ModelUtil.exists(db_name, table_name, {}):
        ModelUtil.add(db_name, table_name, {})
    for path in os.listdir(anno_dir):
        subdir = os.path.join(anno_dir, path)
        if not os.path.exists(subdir) or path.find('lijie') > -1 or path.find('2018-01') > -1:
            continue
        box_num = f_workload(subdir, ['0', '0', '0', '0', '0', '150'])
        box_num = round(box_num / 3.0, 2)
        bag_name = "bag-" + path.replace('.json', '')
        find_bag_name = ModelUtil.query_one(db_name, table_name, {"bag_name": bag_name})
        item = dict(
            bag_name=bag_name,
            box_num=str(int(box_num)),
            update_time=int(os.stat(subdir).st_mtime),
            create_time=int(os.stat(subdir).st_ctime)
        )
        if find_bag_name is None:
            ModelUtil.add(db_name, table_name, item)
            ModelUtil.create_index(db_name, table_name, ['bag_name', 'box_num'])
        elif find_bag_name is not None and find_bag_name['box_num'] != str(int(box_num)):
            find_bag_name['box_num'] = str(int(box_num))
            find_bag_name['update_time'] = int(os.stat(subdir).st_mtime)
            ModelUtil.update(db_name, table_name, find_bag_name)
            print(find_bag_name)
    update_request_work_time()
    return ModelUtil.query_many(db_name, table_name)


def update_request_work_time():
    if not ModelUtil.exists(db_name, time_name, {}):
        ModelUtil.add(db_name, time_name, {})
    else:
        time = ModelUtil.query_one(db_name, time_name, {}, False)
        ModelUtil.update(db_name, time_name, time)


# load_work_list()