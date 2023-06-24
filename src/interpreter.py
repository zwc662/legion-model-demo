
from .get_tables import load_db, run_query
from .serialization import serialize_schema

from dataclasses import dataclass
import json
from datetime import datetime

import sys, os


@dataclass
class Prompt:
    db_id: str
    create_table_sql: str
    question: str

    def load_from_json(self, json_file):
        sample = json.load(open(json_file))
        self.db_id = sample.get('db_id', datetime.now().strftime("%Y%m%d%H%M%S"))
        self.create_table_sql = sample.get('create_table_sql', None)
        self.question = sample.get('question', None)

@dataclass
class Response:
    db_id: str
    query: str

    def load_from_json(self, json_file):
        sample = json.load(open(json_file))
        self.db_id = sample.get('db_id', None)
        self.query = sample.get('query', None)


class Interpreter(object):
    def __init__(self, *args, **kwargs) -> None:
        self.db_path = '.'
        self.schema_cache = dict()
        self.create_table_cache = dict()
 
    def interpret_prompt(self, sample: Prompt, serialize = True):
        db_id = sample.db_id
        db_path = self.db_path + "/" + db_id + "/" + db_id + ".sqlite"
        create_table_sql = sample.create_table_sql
        
        if create_table_sql is not None: 
            base_dir = None
            for sub_dir in db_path.split('/')[1:-1]:
                base_dir = ('' if base_dir is None else (base_dir + '/')) + sub_dir
                if not os.path.exists(base_dir):
                    os.mkdir(base_dir)
            print(db_path)#, create_table_sql)
            
            schema = load_db(db_path, create_table_sql)
            schema['db_id'] = db_id
            self.schema_cache[db_id] = schema
        elif create_table_sql is None:
            schema = self.schema_cache[db_id]
          
        question = sample.question
        question = question.replace('``', "\"").replace("''", "\"")
        if not serialize:
            return question, create_table_sql
        

        kwargs = {
            "question": question,
            "db_path":  self.db_path,
            "db_id": db_id,
            "db_table_names": schema["table_names_original"],
            "db_column_names": [
                {"table_id": table_id, "column_name": column_name}
                for table_id, column_name in schema["column_names_original"]
            ],
            "db_column_types": schema["column_types"],
            "db_primary_keys": [{"column_id": column_id} for column_id in schema["primary_keys"]],
            "db_foreign_keys": [
                {"column_id": column_id, "other_column_id": other_column_id}
                for column_id, other_column_id in schema["foreign_keys"]
            ]
        }

        serialized_schema = serialize_schema(**kwargs)
        return question, serialized_schema
    
    def interpret_query(self, sample):
        db_id = sample.db_id
        db_path = self.db_path + "/" + db_id + "/" + db_id + ".sqlite"
        query = sample.query
        print(db_path, query)
        output = run_query(db_path, query)
        return output
"""   
if __name__ == "__main__":
    intr = Interpreter()
    
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from evaluation_examples.examples import examples
    db_cache = dict()
    for example in examples:
        db_id, create_table_sql, question, query = list(example.values())
        prompt = Prompt(db_id, create_table_sql, question)
        intr.interpret_prompt(prompt)
        response = Response(db_id, query)
        output = intr.interpret_query(response)
        print(output)
"""