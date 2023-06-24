

import json
import os
import src
from src.inference import model_fn


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
 
def lambda_handler(event, context):
    prompt = event.get('data', {})
    if "body" in event:
        if event["body"] is not None:
            prompt = json.loads(event["body"])['data']
        else:
            prompt = {}
 
    result = get_response(prompt)
    
    return {
        'statusCode': 200,
        'headers':{
            'Content-Type':'application/json',
            'Access-Control-Allow-Origin' : "*", 
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(result)
        } 
 