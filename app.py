#!/usr/bin/env python
"""Allows to dynamically manipulate a file in a given link and stores its content in a formatted way."""
from flask import Flask, jsonify
import io
import requests
import pandas as pd
import ast

app = Flask(__name__)

@app.route('/')
def get_data_csv():
    """Get data from a specific file in a given URL, read in memory and pass data converted to JSON."""
    url = 'http://falconi-test.coupahost.com/api/attachments/2416'
    headers = {'X-COUPA-API-KEY': '5f9aa3ecacae35a33305ee036e178194e402bf21', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    decoded_file = r.content.decode('utf-8')
    col_list = ["id"]
    df = pd.read_csv(io.StringIO(decoded_file), usecols=col_list)
    df_json_string = df.to_json(orient='records')
    df_json = ast.literal_eval(df_json_string)

    print(df_json)
    print(type(df_json))

    return jsonify(df_json)

if __name__ == '__main__':
    app.run()