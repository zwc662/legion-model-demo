import os
import torch
from transformers import AutoTokenizer, pipeline
from transformers.pipelines.base import Pipeline

from text2sql.interpreter import Interpreter, Prompt, Response
from functools import partial

from sqlite3 import Error as sqliteError  

import json

class Text2Sql_Pipeline:
    def __init__(self):
        self.intrp = Interpreter()
        self.prompt = Prompt
        self.response = Response
    
    def load_from_json(self, filename):
        with open(filename) as f:
            inputs = json.load(f)
            for p_id, prompt in inputs.items():
                yield (p_id, prompt)

    def wrapper(self, generator, input_path, *args, **kwargs):
        for (p_id, prompt) in self.load_from_json(input_path):
            db_id, create_table_sql, question = prompt.values()
            prompt = self.prompt(db_id, create_table_sql, question)
            question, serialized_schema = self.intrp.interpret_prompt(prompt)
            model_inputs = f"question: {question} schema: {serialized_schema}"
            outputs = generator(model_inputs, *args, **kwargs)
            response = self.response(db_id, outputs[0]['generated_text'])
            try:
                outputs[0]['Result'] = self.intrp.interpret_query(response)
            except sqliteError as e:
                print(e)
            yield (p_id, outputs)
        
def model_fn(model_dir):
    model = torch.load(os.path.join(model_dir, 'model.pt'))
    tokenizer = AutoTokenizer.from_pretrained(model_dir)

    if torch.cuda.is_available():
        device = 0
    else:
        device = -1

    text2sql_pipeline = Text2Sql_Pipeline()
    generation = pipeline(
        "text2text-generation", model=model, tokenizer=tokenizer, device=device
    )

    return partial(text2sql_pipeline.wrapper, generation)