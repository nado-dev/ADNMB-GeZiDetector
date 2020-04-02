# coding=utf-8
import json
import codecs

import switch as switch

global JSON_READ


def load_json():
    global JSON_READ
    with codecs.open('Adnmb.json', 'r', encoding='utf-8') as f:
        config = f.read()
    JSON_READ = json.loads(config)


def add():
    global JSON_READ
    new_THREAD_ID = raw_input("thread id")
    new_PO_ID = raw_input("PO")
    JSON_READ[str(new_THREAD_ID)] = {
        "LAST_MODIFIED_TIME": 0,
        "THREAD_ID": int(new_THREAD_ID),
        "PO_ID": new_PO_ID
    }


def delete():
    global JSON_READ
    to_delete = raw_input("to delete thread id")
    try:
        JSON_READ.pop(str(to_delete))
        print "删除成功"
    except KeyError:
        print "删除失败"


def save():
    global JSON_READ
    str_to_load = json.dumps(JSON_READ)
    with codecs.open('Adnmb.json', 'w', encoding='utf-8') as f:
        f.write(str_to_load)


if __name__ == '__main__':
    load_json()
    while True:
        print "当前跟踪列表"
        for (k, v) in JSON_READ.items():
            print "串号"+str(k)
            print "上次回复串号 :" + str(v["LAST_MODIFIED_TIME"])
            print "Po :" + str(v["PO_ID"])

        print "选择功能"
        print "1:删除一条记录"
        print "2:增加一条记录"
        print "其他:退出"
        _input = raw_input()
        if _input == "2":
            add()
        elif _input == "1":
            delete()
        else:
            break
    save()
