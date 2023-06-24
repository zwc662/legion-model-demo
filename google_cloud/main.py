
import os
import src
from src.inference import model_fn
import json

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_DIR='./model/'

def get_response(prompt):
    result = {}
    if 'db_id' in prompt.keys():
        db_id = prompt.get('db_id')
        if 'create_table_sql' in prompt.keys():
            create_table_sql=prompt.get('create_table_sql')
            if 'question' in prompt.keys():
                question = prompt.get('question')
                if 'test' in prompt.keys():
                    result.update({"Result": "NULL"})
                result = model_fn(MODEL_DIR)([db_id, create_table_sql, question])
    return result

@app.route('/', methods=['POST'])
def load_from_request():
    prompt = request.json
     
    if prompt is None:
        prompt = request.args
    result=get_response(prompt)
    response = jsonify(result)
     
    return response

"""
@app.route('/', methods=['POST'])
def load_from_request():
    prompt = json.loads(request.data)
    if prompt is None:
        prompt=json.loads({
            'db_id': request.args.get('bd_id'),
            'create_table_sql': request.args.get('create_table_sql'),
            'question': request.args.get('question')
        })
    result=get_response(prompt)
    response = make_response(str(result))
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
    response.headers["Access-Control-Allow-Methods"] = "POST"
    response.headers["Access-Control-Allow-Origin"] = '*'
    return response

"""
 
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))