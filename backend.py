from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_input():
    data = request.get_json()
    prompt = data.get('prompt', '')  # Get the prompt from the request
    model = data.get('model', '')    # Get the selected LLM model from the request
    
    # Simulate some processing based on the model
    result = f'You selected {model} and searched for: "{prompt}".'
    
    # Write the result to a file (same as before)
    with open("output.txt", "a") as f:
        f.write(result + '\n')
    
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
