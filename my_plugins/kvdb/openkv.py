# -*- coding: utf-8 -*-
"""
---------OpenKV-----------

Description: A extreme light-weight online KV database based on html parsing.

Version: 0.1


---------Concact----------
Welcome to contact me via Email: 307977586@qq.com

Author: Ray Williams (Songlin Hou)



**NOTE**

(1)It is NOT recommended to use this library for realtime transmission or in
high-concurrent environments.

(2)Stability is NOT guaranteed.

"""
import requests
import datetime
import base64
import pytz
from openkvCore import OpenKVCore


class OpenKV(object):
    def __init__(self, root=None, pwd=None, webbase_id=None):
        if root is not None and pwd is not None:
            self.root = root
            self.pwd = pwd
        else:
            self.root = 'openkv'
            self.pwd = 'openkv'
        if webbase_id is None:
            self.webbase_id = 'W7EWD8rb'
        else:
            self.webbase_id = webbase_id
        self.data = {'code': None, 'lang': "Plain Text", 'submit': 'Submit'}
        self.comment_url = 'http://codepad.org/' + self.webbase_id + '/post'
        self.session = requests.session()
        self.kvcore = OpenKVCore()
        self.kvcore.login(self.root, self.pwd, self.session)

    def createDB(self, description):
        self.data['code'] = description.strip()
        r = requests.post("http://codepad.org/", data=self.data)
        if r.ok:
            print('webkv database is successfully created.')
            base_id = r.url.split('/')[-1]
            base_url = r.url
            print('BASE_ID:', base_id)
            print('BASE_URL:', base_url)
            return base_id
        else:
            raise ("Server Error")
        return None

    def setDB(self, webbase_id):
        if webbase_id is None or type(webbase_id) is not str:
            raise ("WebBaseIdFormatError", "webbase_id must be an non-empty string")
        else:
            self.webbase_id = webbase_id.strip()
            self.__init__()

    def setValue(self, username, password, key, value):
        upload_raw = ''
        tz = pytz.timezone('Asia/Shanghai')
        stamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now(tz))
        content_filtered = base64.b64encode(value)
        upload_raw = '#SEP#'.join([stamp, username, password, key, content_filtered])
        upload_raw = "$HEAD$" + upload_raw + "$TAIL$"
        return self.kvcore.postComment(self.session, upload_raw, self.comment_url)

    def val(self, records):
        if type(records) is not dict:
            raise Exception("RecordTypeError", "records must be of dict type")
        else:
            if len(records.keys()) == 0:
                return None
            if len(records.keys()) == 1:
                return records.values()[0]
            else:
                return records.values()

    def latest(self, records):
        latestRecords = {}
        keys = records.keys()
        keys.sort()
        if type(records) is not dict:
            raise Exception("RecordTypeError", "records must be of dict type")
        else:
            latestRecords[keys[-1]] = records[keys[-1]]
        return latestRecords

    def earlest(self, records, key=None):
        earlestRecords = {}
        keys = records.keys()
        keys.sort()
        if type(records) is not dict:
            raise Exception("RecordTypeError", "records must be of dict type")
        else:
            earlestRecords[keys[0]] = records[keys[0]]
        return earlestRecords

    def getValue(self, username, password, key=None):
        raw = self.kvcore.getHtml(self.session, self.webbase_id)
        s = raw
        head = '$HEAD$'
        tail = '$TAIL$'
        headlen, taillen = len(head), len(tail)
        search_pos = 0
        records = {}
        if s != 'ERROR':
            while (s.find(head, search_pos) >= 0):
                start = s.find(head, search_pos) + headlen
                end = s.find(tail, start)
                record_raw = s[start:end]
                search_pos = end + taillen
                try:
                    if self.kvcore.fastVerify(record_raw, username, password, key):
                        k, v, t = self.kvcore.filteredContent(record_raw, username, password, key)
                        if not records.has_key(k):
                            records[k] = {}
                        records[k][t] = v
                except:
                    pass
        return records