from typing import Optional, List, Dict, Callable
import random
from .bridge_content_encoder import get_database_matches


def serialize_schema(
        question: str,
        db_path: str,
        db_id: str,
        db_column_names: List[Dict[str, str]],
        db_table_names: List[str],
        schema_serialization_type: str = "peteshaw",
        schema_serialization_randomized: bool = False,
        schema_serialization_with_db_id: bool = True,
        schema_serialization_with_db_content: bool = False,
        normalize_query: bool = True,
        **kwargs
    ) -> str:
        
        if schema_serialization_type == "verbose":
            db_id_str = "Database: {db_id}. "
            table_sep = ". "
            table_str = "Table: {table}. Columns: {columns}"
            column_sep = ", "
            column_str_with_values = "{column} ({values})"
            column_str_without_values = "{column}"
            value_sep = ", "
        elif schema_serialization_type == "peteshaw":
            # see https://github.com/google-research/language/blob/master/language/nqg/tasks/spider/append_schema.py#L42
            db_id_str = " | {db_id}"
            table_sep = ""
            table_str = " | {table} : {columns}"
            column_sep = " , "
            column_str_with_values = "{column} ( {values} )"
            column_str_without_values = "{column}"
            value_sep = " , "
        elif schema_serialization_type == "custom":
            # see https://github.com/google-research/language/blob/master/language/nqg/tasks/spider/append_schema.py#L42
            db_id_str = " | {db_id}"
            table_sep = ""
            table_str = " | {table} : {columns}"
            column_sep = " , "
            column_str_with_values = "{column} [ {values} ]"
            column_str_without_values = "{column}"
            value_sep = " ; "
        else:
            raise NotImplementedError

        def get_column_str(table_name: str, column_name: str) -> str:
            column_name_str = column_name.lower() if normalize_query else column_name
            if schema_serialization_with_db_content:
                matches = get_database_matches(
                    question=question,
                    table_name=table_name,
                    column_name=column_name,
                    db_path=(db_path + "/" + db_id + "/" + db_id + ".sqlite"),
                )
                if matches:
                    return column_str_with_values.format(column=column_name_str, values=value_sep.join(matches))
                else:
                    return column_str_without_values.format(column=column_name_str)
            else:
                return column_str_without_values.format(column=column_name_str)

        tables = [
            table_str.format(
                table=table_name.lower() if normalize_query else table_name,
                columns=column_sep.join(
                    map(
                        lambda y: get_column_str(table_name=table_name, column_name=y[1]),
                        filter(
                            lambda y: y[0] == table_id,
                            zip(
                                [
                                    (db_column_name["table_id"],
                                    db_column_name["column_name"]) for db_column_name in db_column_names]
                            ),
                        ),
                    )
                ),
            )
            for table_id, table_name in enumerate(db_table_names)
        ]
        if schema_serialization_randomized:
            random.shuffle(tables)
        if schema_serialization_with_db_id:
            serialized_schema = db_id_str.format(db_id=db_id) + table_sep.join(tables)
        else:
            serialized_schema = table_sep.join(tables)
        return serialized_schema
