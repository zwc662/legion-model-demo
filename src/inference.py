
import os
import torch
from transformers import AutoTokenizer, pipeline 

from .interpreter import Interpreter, Prompt, Response
from functools import partial

from sqlite3 import Error as sqliteError  

class Text2Sql_Pipeline:
    def __init__(self):
        self.intrp = Interpreter()
        self.prompt = Prompt
        self.response = Response
    def wrapper(self, generator, inputs, *args, **kwargs):
        db_id, create_table_sql, question = inputs
        prompt = self.prompt(db_id, create_table_sql, question)
        question, serialized_schema = self.intrp.interpret_prompt(prompt)
        model_inputs = f"question: {question} schema: {serialized_schema}"
        outputs = generator(model_inputs, *args, **kwargs)
            
        response = self.response(db_id, outputs[0]['generated_text'])
        try:
            outputs[0]['Result'] = self.intrp.interpret_query(response)
            outputs[0]['db_id'] = prompt.db_id
            outputs[0]['create_table_sql'] = prompt.create_table_sql
            outputs[0]['question'] = prompt.question
        except sqliteError as e:
            print(e)
        return outputs[0]
        
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
