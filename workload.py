import json


def f_workload(filename, loc):
    with open(filename) as f:
        data_list = f.readline()
    json_list = json.loads(data_list[:])
    box_num = 0
    if int(loc[2]) == int(loc[4]):
        for j in range(len(json_list[loc[2]]['obstacles'])):
            real_start = max(json_list[loc[2]]['obstacles'][j]['start'], int(loc[3]))
            if 'end' not in json_list[loc[2]]['obstacles'][j]:
                json_list[loc[2]]['obstacles'][j]['end'] = min(len(json_list[loc[2]]['obstacles'][j]['boxes']) - 1, 224)
                real_end = json_list[loc[2]]['obstacles'][j]['end']
            else:
                real_end = json_list[loc[2]]['obstacles'][j]['end']
            for k in range(real_start, real_end + 1):
                if json_list[loc[2]]['obstacles'][j]['boxes'][k]['injected']:
                    box_num = box_num + 0.8
                else:
                    box_num = box_num + 0.2
            if json_list[loc[2]]['obstacles'][j]['start'] <= int(loc[3]) <= \
                    json_list[loc[2]]['obstacles'][j]['end']:
                box_num = box_num + 1
            elif json_list[loc[2]]['obstacles'][j]['start'] > int(loc[5]) >= \
                    json_list[loc[2]]['obstacles'][j]['start']:
                box_num = box_num + 1
            else:
                box_num = box_num
        box_num = box_num + 6 * len(json_list[loc[2]]['obstacles'])
    return box_num
