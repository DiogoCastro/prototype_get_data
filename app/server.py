# Module import 
"""Allows to dynamically manipulate a file in a given link and stores its content in a formatted way."""
from flask import Flask, jsonify, request
import os
import io
import ast
import requests
import pandas as pd
import json


app = Flask( __name__ )

cf_port = os.getenv("PORT")

@app.route('/send-json', methods=['POST'])
def send_json():
    """Send data from a Json specified by user, read in memory and pass data converted to JSON."""
    try:
        decoded_json = request.data.decode('utf-8')
        widget_response = json.loads(decoded_json).get("easy-form-widget-responses")
        for resp in widget_response:
            if(resp['field-name'] == "attachment_1"):
                if not resp['answer']:
                    return jsonify('Field answer not found.')
                else:
                    id_attachement = resp['answer']
        url = 'http://falconi-test.coupahost.com/api/attachments/' + id_attachement
        headers = {'X-COUPA-API-KEY': '5f9aa3ecacae35a33305ee036e178194e402bf21', 'Accept': 'application/json'}
        r = requests.get(url, headers=headers)
        decoded_file = r.content.decode('utf-8')
        col_list = ["id"]
        df = pd.read_csv(io.StringIO(decoded_file), usecols=col_list)
        df_json_string = df.to_json(orient='records')
        df_json = ast.literal_eval(df_json_string)
    except:
        return jsonify('Error sending data to server. Check if the body is correct and send again.')
    return jsonify(df_json)

if __name__ == '__main__':
	if cf_port is None:
		app.run( host='0.0.0.0', port=5000, debug=True )
	else:
		app.run( host='0.0.0.0', port=int(cf_port), debug=True )