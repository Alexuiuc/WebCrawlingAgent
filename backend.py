from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_input():
    data = request.get_json()
    prompt = data.get('prompt', '')  # Get the prompt from the request
    website = data.get('website', '')  # Get the website to crawl
    model = data.get('model', '')    # Get the selected LLM model
    
    # Simulate some processing based on the model, website, and prompt
    result = f'Using {model}, you crawled: {website}, with the prompt: "{prompt}".'
    
    # Write the result to a file (just like before)
    with open("output.txt", "a") as f:
        f.write(result + '\n')
    
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
