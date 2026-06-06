from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)
@app.route("/")
def index():
   return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
 try:
     data = request.get_json()
     speech= data.get("speech")
     language = data.get("language")
     if language=="select language":
       return jsonify({"result": "Please select a language."})
     # question_words = ["what", "why", "how", "when", "where", "who", "?" , "write"]

     # speech_lower = speech.lower()

     # if any(word in speech_lower for word in question_words):
     #   return jsonify({"result": "Please speak a coding instruction."})
     prompt=f"""
 You are a voice-to-code syntax converter.

 Your job is ONLY to convert spoken programming syntax into valid {language} code.

 STRICT RULES:

 1. Only translate spoken syntax words into code symbols.
 2. Do NOT create algorithms, logic, or full programs.
 3. Do NOT generate solutions to programming problems.
 4. If the instruction is conceptual (example: "fibonacci", "sorting", "binary search", etc.), return:
    Please speak a coding instruction.
 5. Do NOT explain anything.
 6. Do NOT add markdown or backticks.
 7. Return only the final code.

 Examples:

 Speech: print hello world
 Output: print("hello world")

 Speech: define function add numbers
 Output: def add_numbers():

  

 Speech input:
 {speech}
   """
     completion=client.chat.completions.create(
       model="Qwen/Qwen2.5-Coder-7B-Instruct:nscale",
   
       messages=[
         {
            "role": "user", 
          "content": prompt
         }
       ],
   )
     result=completion.choices[0].message.content
     print(result)
     return jsonify({"result": result})
 except Exception as e:
   return jsonify({'result': str(e)})

if __name__ == "__main__" :
   app.run(host="0.0.0.0" , port=8080 , debug=True)

