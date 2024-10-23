from flask import Flask, request, jsonify
import json
import os
import threading
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from openai import OpenAI
app = Flask(__name__)

# Function to handle main crawling logic
def crawl_website(data, filename, max_depth=1):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Start scraping the given website
            
            result = recursive_crawl(page, data,filename)

            browser.close()

    except Exception as e:
        # Handle errors and store them in the file
        with open(filename+"_error", 'w') as f:
            json.dump({'error': str(e)}, f, indent=4)

def extract_links_related_to_prompt(html, prompt):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find_all('a', href=True)  # Extract all links
    
    # Create a list of links with the href and anchor text
    links_data = [{"url": link['href'], "text": link.get_text()} for link in all_links]
    
    # Ask GPT to filter links based on the prompt
    prompt_for_gpt = f"User prompt: {prompt}\nHere are some links from the HTML page: {links_data}. Which links are related to the user prompt? return only the links in format as python array"
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt_for_gpt
            }
            ]
    )

    # Extract the response text
    related_links = response.choices[0].message
    return related_links

# Function to extract content from the current page related to the user prompt
def extract_related_content(html, prompt):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract all text from the HTML
    all_text = soup.get_text(separator="\n", strip=True)
    
    # Ask GPT to find the content related to the prompt
    prompt_for_gpt = f"User prompt: {prompt}\nHere is the full text from the HTML page: {all_text}. What content is relevant to the user's prompt?"
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt_for_gpt
            }
            ]
    )

    # Extract the response text
    related_content = response.choices[0].message
    
    return related_content

# Function to detect dynamic elements like buttons and interactive tags
def detect_dynamic_elements(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find common interactive elements
    buttons = soup.find_all('button')
    clickable_divs = soup.find_all('div', {'onclick': True})
    interactive_elements = buttons + clickable_divs
    
    # Format the output to include tag names and attributes for interaction
    dynamic_content_data = []
    for element in interactive_elements:
        tag_info = {
            "tag": element.name,
            "attributes": element.attrs,
            "text": element.get_text(strip=True)
        }
        dynamic_content_data.append(tag_info)
    
    return dynamic_content_data

# 1. method to crawl links within a page and follow them up to a certain depth
def recursive_crawl(page, data, filename, depth=1):
    cache={}

    def crwal():
        url = data.get('website')
        prompt= data.get('prompt')

        page.goto(url)

        html = page.content()

        scraped_data = extract_related_content(html, prompt)

        synthesize_document(scraped_data, data, filename)

        dynamic_content_data = detect_dynamic_elements(html)

        related_links = extract_links_related_to_prompt(html, prompt)

        return dynamic_content_data,related_links
    
    dynamic_content_data,related_links = crwal()
    return dynamic_content_data,related_links # for future functions to handle 


# Synthesize document into a structured format (JSON)
def synthesize_document(scraped_data, data, filename):
    # Load existing content if the file exists
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                document = json.load(f)
        except json.JSONDecodeError:
            # In case of corrupt or empty file, start fresh
            document = []
    else:
        document = []

    # Prepare the new data entry
    new_entry = {
        'prompt': data.get('prompt'),
        'website': data.get('website'),
        'model': data.get('model'),
        'scraped_data': scraped_data,
        'timestamp': data.get('timestamp')
    }

    # Append the new entry to the document
    document.append(new_entry)

    # Save the updated document back to the JSON file
    with open(filename, 'w') as f:
        json.dump(document, f, indent=4)

# Flask route to handle the input and start crawling
@app.route('/process', methods=['POST'])
def process_input():
    data = request.get_json()
    prompt = data.get('prompt', '')  # Get the prompt from the request
    website = data.get('website', '')  # Get the website to crawl
    model = data.get('model', '')    # Get the selected LLM model
    
    # Create a filename based on the current time and website
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_name = website.split('//')[-1].split('/')[0]  # Extract domain name
    filename = f"crawl_{domain_name}_{timestamp}.json"
    file_path = os.path.join(os.getcwd(), filename)

    # Add the inputs (url, prompt, model) into the JSON structure
    data_to_save = {
        'prompt': prompt,
        'website': website,
        'model': model,
        'timestamp': timestamp
    }

    # Start a new thread to handle the crawling
    crawl_thread = threading.Thread(target=crawl_website, args=(data_to_save, file_path))
    crawl_thread.start()

    # Return success message immediately, without waiting for the thread to finish
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
