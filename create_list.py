#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urllib import urlencode
import json
from musician import musician
import hashlib

cookies = {"os": "osx"}
header = {
    "Host": "music.163.com", "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "orpheus://orpheus",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko)"
}


def get_user_id_by_name(name):
    url = "http://music.163.com/api/search/pc"

    params = {"type": "1002", "s": name, "offset": "0", "total": "true", "limit": "1"}
    print(urlencode(params))
    resp = requests.post(url, urlencode(params), cookies=cookies, headers=header)
    musician_r = resp.json()
    m = musician()
    print(json.dumps(musician_r, ensure_ascii=False))
    profile = musician_r["result"]["userprofiles"][0]
    m.userId = profile["userId"]
    m.avatarUrl = profile["avatarUrl"]
    m.detailDescription = profile["detailDescription"]
    m.description = profile["description"]
    m.signature = profile["signature"]
    m.nickname = profile["nickname"]
    m.gender = profile["gender"]
    m.result = resp.text

    print(m.userId)
    return (m.userId)


# 需要登录.
def delete_list(listId,m):
    url = "http://music.163.com/api/playlist/delete"
    params = {"id": listId, "pid": listId}
    resp = requests.post(url, params, cookies=cookies, headers=header)
    if resp.status_code == 200:
        print("歌单删除成功...")


# 需要登录.
def create_list(name, m):
    url = "http://music.163.com/api/playlist/create"
    params = {"name": name, "uid": m.userId}
    resp = requests.post(url, urlencode(params), cookies=cookies, headers=header)
    result = resp.json()
    if result["code"] == 200:
        print("创建成功..")
        return result["id"]
    else:
        print(resp.text)
        print("啥也没干")


# 登录(密码MD5)
# emember=true&https=true&username=zhourongfaith%40163.com
def login(name, password):
    url = "https://music.163.com/api/login"
    m2 = hashlib.md5()
    m2.update(password)
    encodePass = m2.hexdigest()
    m = musician()
    params = {
        "username": name,
        "password": encodePass,
        "type": "0",
        "remember": "true",
        "https": "true"
    }
    resp = requests.post(url, urlencode(params), cookies=cookies, headers=header)
    account = resp.json()['account']
    m.userId = account['id']
    m.cookie = resp.cookies
    cookies['MUSIC_U'] = resp.cookies['MUSIC_U']
    print json.dumps(resp.json(), ensure_ascii=False)
    print resp.cookies['MUSIC_U']
    return m

def add_song_to_list(listid,songs):
    url="http://music.163.com/api/playlist/manipulate/tracks"
    params={
        "trackIds":songs,
        "pid":listid,
        "op":"add"
    }



if __name__ == '__main__':
    create_list("23333", login("clay169@163.com", "p111111"))

