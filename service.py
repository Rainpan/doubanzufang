# -*- coding: utf-8 -*-

import requests
import sqlite3
from flask_cors import *
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, supports_credentials=True)

conn = sqlite3.connect('/home/panda/Downloads/test.db', check_same_thread=False)
c = conn.cursor()


@app.route('/get', methods=['POST'])
def select():
    response = {}
    rows = []
    limit = int(request.values.get('pageSize', 10))
    page_number = int(request.values.get('pageNumber', 1))
    offset = (page_number - 1) * limit
    type = request.values.get('type', None)
    collection = request.values.get('collection', None)
    status = request.values.get('status',1)

    sql = ("select id,title,href,update_time from douban where 1=1 " + (
        " and status={status}") + (
        " and type={type}" if type else "") + (
        " and collection={collection}" if collection else "") + \
        " limit {limit} offset {offset}").format(limit=limit, offset=offset, type=type, collection=collection,status=status)

    sqlCount = ("select count(*) from douban where status=1 " + (
        " and status={status}") + (
        " and type={type}" if type else "") + (
        " and collection={collection}" if collection else "")).format(type=type, collection=collection,status=status)

    count = c.execute(sqlCount).fetchone()[0]

    results = c.execute(sql)
    for res in results:
        data = {'id': res[0], 'title': res[1], 'href': res[2], 'update_time': res[3]}
        rows.append(data)
    response['rows'] = rows
    response['total'] = count

    return jsonify(response)


@app.route('/delete')
def delete():
    ids = request.values.get('ids', '')
    sql = "update douban set status = 0 where id in ({ids})".format(ids=ids)
    c.execute(sql)
    return 'delete'


@app.route('/collection')
def collection():
    ids = request.values.get('ids', '')
    sql = "update douban set collection = 1 where id in ({ids})".format(ids=ids)
    c.execute(sql)
    return 'collection'


if __name__ == "__main__":
    app.run()
