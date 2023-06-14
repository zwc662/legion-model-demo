function request(){
    let dbElement = document.getElementById('question');
    let db_id = dbElement.value;
    
    let questionElement = document.getElementById('question');
    let question = questionElement.value;
    
    let schemaElement = document.getElementById('schema');
    let schema = schemaElement.value;
     
    let query = document.getElementById("query");
    let data = document.getElementById("data")

    getResult(db_id, question, schema)
        .then(res => {
            return printResult(res);
        })
        .then(res => console.log(res))
        .catch(error => {
            console.log(error);
        });
    
  }
  function printResult(res){
    let query = document.getElementById("query");
    query.innerHTML=res['generated_text'];
    let data = document.getElementById("data");
    data.innerHTML=res['Result'];
    return res;
  }
  function printContent(id, content){
    let element = document.getElementById(id);
    //add the <p> element to the <div>
    element.innerHTML=content;
  }

  async function getResult(db_id, question, schema){
    const res= await fetch("https://text2sql-s4vjhcroda-ue.a.run.app/", { 
        method: 'POST',
        headers: {
            /*'Accept': 'application/json',*/
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "db_id": db_id,
            "question": question,
            "create_table_sql": schema
        })
    });
    
    const res_json = await res.json(); 
     
    return res_json;
}

/*
let db_id="customer_complaints";
let schema="";
let question="Give the state that has the most customers.";
 
getResult(db_id, question, schema)
        .then((res)=>console.log(res));
 
*/