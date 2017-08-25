# -*- coding: utf-8 -*-
"""
Created on Sun May  7 07:50:10 2017

@author: Ray
"""
import base64
import urllib2
import datetime

class OpenKVCore:
    def postComment(self, session, content, comment_url):
        comment_data = {'parent': "", 'text': content, 'submit': "Post Comment"}
        r = session.post(comment_url, data=comment_data)
        if r.ok:
            s = r.url
            if s.find("comment") == -1:
                raise ("failed to upload")
                return False
            else:
                return True
        raise ("server error")
        return False

    def getHtml(self, session, webbase_id):
        info_url = 'http://codepad.org/' + webbase_id
        r = session.get(info_url)
        if r.ok:
            return r.text
        raise ("server error")

    def filteredContent(self, record, username, password, key):
        items = record.split('#SEP#')
        time, user, pwd, key, value = tuple(items)
        if user == username.strip() and pwd == password.strip():
            return key, base64.b64decode(value), time
        return None

    def login(self, root, pwd, session):
        login_url = 'http://codepad.org/login'
        login_data = {'username': root, 'password': pwd, 'submit': 'Login'}
        r = session.post(login_url, data=login_data)
        if r.ok:
            ret = r.text
            if ret.find("logout") == -1:
                raise ("failed to init")
                return False
            return True
        else:
            print ("server error")
            return False

    def fastVerify(self, record, username, password, key=None):
        if key is None:
            s = '#SEP#' + username + '#SEP#' + password + '#SEP#'
        else:
            s = '#SEP#' + username + '#SEP#' + password + '#SEP#' + key + '#SEP#'
        return record.find(s) >= 0

    def getOnlineUTCTime(self):
        webpage = urllib2.urlopen("http://just-the-time.appspot.com/")
        internettime = webpage.read()
        OnlineUTCTime = datetime.datetime.strptime(internettime.strip(), '%Y-%m-%d %H:%M:%S')
        return OnlineUTCTime