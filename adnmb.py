# coding=utf-8
from time import sleep

import bs4
import requests
import codecs
import sys

# encoding=utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# 串号
THREAD_ID = ""
# 最后一页
LAST_PAGE = ""
# poID
PO_ID = ""
# 主URL
BASE_URL = "https://adnmb2.com/t/"
# 用于获取最后一页
A_NUMBER = 1
# 上次PO更新时间
LAST_MODIFIED_TIME = 0
# 要找的html class
target_class = ""
# SCKEY 用于server chan 推送服务 见http://sc.ftqq.com/3.version
SCKEY = ""


"""
    1、第一次执行 读配置文件，全为空，手动加载（只需要提供THREAD_ID）
    2、非第一次执行 读取配置文件，跳过init
"""


def set_thread_id():
    """
        设置串号
    """
    global THREAD_ID
    THREAD_ID = raw_input("输入串号")


def get_html(page, is_first_request=False, to_get_last_page=False):
    """
        请求指定页数的HTML
        :param 页数
        :return 该页所有post的 createdat, uid， thread_id, content [{},{}...{}]
    """
    global BASE_URL, THREAD_ID, target_class

    if is_first_request:
        target_class = "h-threads-item-main"
    else:
        target_class = "h-threads-item-reply"

    if to_get_last_page:
        target_class = "uk-active"

    print 'Loading page' + str(page)

    url = BASE_URL + str(THREAD_ID) + "?page=" + str(page)
    # url = 'https://adnmb2.com/t/49607?page=' + str(page)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return get_element(response.text, target_class)
    except requests.RequestException:
        return None


def get_element(html, targetClass="h-threads-item-reply"):
    """
        获取元素
        :param 传入的HTML
        :return 该页所有post的 createdat, uid， thread_id, content  [{},{}...{}]
    """
    soup = bs4.BeautifulSoup(html, 'lxml')
    post_list = soup.find_all(class_=targetClass)

    if targetClass == "uk-active":
        for i in post_list:
            return i.text

    post_info = []
    for item in post_list:
        title = item.find(class_='h-threads-info-title').string
        email = item.find(class_='h-threads-info-email').string
        createdat = item.find(class_='h-threads-info-createdat').string
        uid = item.find(class_='h-threads-info-uid').string
        thread_id = item.find(class_='h-threads-info-id').string
        contend = item.find(class_='h-threads-content').string

        thread_id = int(thread_id.split(".")[1])

        post_info_each = {
            "create_date": createdat,
            "uid": uid,
            "thread_id": thread_id,
            "content": contend
        }
        post_info.append(post_info_each)
        # print 'Title:{}\nEmail:{}\nCreatList:{}\nUid:{}\nThread_id:{}\nContend:{}\n'.format(title, email, createdat,
        #                                                                                     uid, thread_id, contend)
    print post_info
    return post_info


def init_info():
    """
    设置初始信息：获取po_id 以及 LAST_PAGE
    :return: null
    """
    global A_NUMBER, PO_ID, THREAD_ID

    load_config()
    print "loaded"
    print PO_ID
    if THREAD_ID == "":
        set_thread_id()
    if PO_ID == "":
        print "getting PO"
        PO_ID = get_html(A_NUMBER, True)[0]["uid"]
        print PO_ID

    # print get_html(A_NUMBER)


def set_thread_id():
    """
    设置串号
    :return: null
    """
    global THREAD_ID
    THREAD_ID = raw_input("输入串号")


def find_last_page():
    """
    找最后一页
    :return:
    """
    global LAST_PAGE
    LAST_PAGE = int(get_html(200, False, True))
    print "last page is" + str(LAST_PAGE)


def wechat_notify(update_date):
    global SCKEY
    url = "http://sc.ftqq.com/"+SCKEY+".send"
    text = "Po于"+str(update_date)+"更新了"
    try:
        response = requests.post(url + "?text=" + str(text))
        if response.status_code == 200:
            print "推送成功"
    except requests.RequestException:
        return None


def load_config():
    global LAST_MODIFIED_TIME, PO_ID, THREAD_ID
    with codecs.open('Adnmb.config', 'r', encoding='utf-8') as f:
        config = f.read()
    config_list = config.split(" ")
    try:
        LAST_MODIFIED_TIME = int(config_list[0])
    except ValueError:
        LAST_MODIFIED_TIME = 0
    finally:
        print config_list
        PO_ID = config_list[1]
        print "FU" + "now poid" + str(PO_ID == "\r")
        try:
            THREAD_ID = int(config_list[2])
        except ValueError:
            THREAD_ID = 0
        finally:
            return


def load_SCKEY():
    global SCKEY
    with codecs.open('SCKEY.config', 'r', encoding='utf-8') as f:
        SCKEY = f.read()
    print "SCKEY loaded"


def write_config():
    """
    写入配置，包括LAST_Modify POID, THREAD_ID
    :return:
    """
    content = str(LAST_MODIFIED_TIME) + " " + str(PO_ID) + " " + str(THREAD_ID)
    with codecs.open('Adnmb.config', 'w', encoding='utf-8') as f:
        f.write(content)


def find_last_modify():
    """
    找到最后一次修改的时间
    :return:
    """
    # 加载最后一页的内容
    global LAST_PAGE, LAST_MODIFIED_TIME, PO_ID

    '''
        遍历，是否有po记录
        Uid:ID:RAHQN2A
        由于是从最后一页找起的,情况可能有
        1、最后一页有比原来更新的记录，return
        2、最后一页没有更新的记录， page-1,循环
        
    '''
    i = 0
    while LAST_PAGE - i > 0:
        content_list = get_html(LAST_PAGE - i)
        content_list.reverse()
        sleep(1.5)
        for item in content_list:
            print "finding page " + str(LAST_PAGE - i) + " po" + "ID:" + PO_ID
            print item["uid"]
            print item
            print item["uid"] == PO_ID
            print "$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            print LAST_MODIFIED_TIME
            print "***************************"

            # 初始化
            if LAST_MODIFIED_TIME == 0 and item["uid"] == PO_ID:
                LAST_MODIFIED_TIME = item["thread_id"]
                write_config()
                return

            if item["thread_id"] > LAST_MODIFIED_TIME:
                if item["uid"] == PO_ID:
                    LAST_MODIFIED_TIME = item["thread_id"]
                    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                    print item
                    write_config()
                    print "更新了！"
                    wechat_notify(item["create_date"])
                    return

            if item["thread_id"] == LAST_MODIFIED_TIME:
                print "没有更新"
                return
        i = i + 1


if __name__ == '__main__':
    load_SCKEY()
    init_info()
    find_last_page()
    find_last_modify()
    # print PO_ID
