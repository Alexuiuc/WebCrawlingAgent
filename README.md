# **AI-Powered Web Crawler**

**AI Octopus** is an AI-powered web crawler. A small tool to crawl data from a website.

## **Features**

- **Extract links** related to a specific user prompt from a webpage.
- **Scrape relevant content** based on the user’s prompt.
- **Detect dynamic elements** (e.g., buttons, interactive tags) for potential further interaction.
- Save the extracted data in structured JSON format with error handling.

## **Requirements**

Before you begin, ensure you have the following installed:
1. **Python 3.x**
2. **OpenAI API Key**: You need an API key from OpenAI to interact with GPT-3.5 or GPT-4 models.
3. Required packages (listed below).

## **Installation**

### 1. **Clone the Repository**
```bash
git clone git@github.com:Alexuiuc/WebCrawlingAgent.git
cd WebCrawlingAgent
```
### 2. **Set Up a Virtual Environment**
```bash
conda create --name AIOctopus python=3.9
```
### 3. **Install Dependencies**
```bash

pip install -r requirements.txt
playwright install
```
### 4. **Set Up OpenAI API Key**
```bash
export OPENAI_API_KEY="your-openai-api-key"
```
## Usage

```bash
python backend.py
```
In another terminal:
```bash
npm start
```