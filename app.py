# Zero-Shot Visualizer

# Description:
# This Python script creates a zero-shot visualizer, a system that can generate visualizations
# based on a user's input query without any specific training data. The script follows a multi-step process:

# 1. Search Functionality: Implements a search functionality using the SerpApi library to retrieve relevant data based on the user's query.

# 2. Code Generation: Uses a language model (mistralai/Mixtral-8x7B-Instruct-v0.1) from the Together API to generate Python code for visualizing the data.

# 3. Code Parsing and Execution: Parses the generated code to extract necessary components (imports, data definitions, plotting code), and dynamically executes the code to
#create the visualization.

# 4. Visualization: Orchestrates the entire workflow, prompting the user for a query, retrieving data, generating code, parsing the code, and executing the visualization.

import os
from serpapi import GoogleSearch
from together import Together
from langchain.python import PythonREPL
from dotenv import load_dotenv
import textwrap
import re
import ast
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request

#Creating a Flask app instance and set the static folder
app = Flask(__name__)
app.static_folder = 'static'

#Printing the current working directory
print("Current working directory:", os.getcwd())

#Loading environment variables from the .env file
dotenv_path = r'C:/Users/utkar/OneDrive/Desktop/New folder (2)/Variable.env'
load_dotenv(dotenv_path)

#Printing the value of the TOGETHER_API_KEY environment variable
print("TOGETHER_API_KEY:", os.getenv('TOGETHER_API_KEY'))

#Accessing the API key from the environment variable and raise an error if it's not set
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
if TOGETHER_API_KEY is None:
    raise ValueError("TOGETHER_API_KEY environment variable is not set.")

#Initializing the Together client using the API key
client = Together(api_key=TOGETHER_API_KEY)

#Function to search the web using the Google Search API
def search_web(query):
    params = {
        "engine": "google",
        "q": query,
        "num": 10  # Number of search results
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if 'organic_results' in results:
        return results['organic_results']
    else:
        print(f"No search results found for the query: '{query}'")
        return []

#Function to generate code based on the query and data using the Together AI model
def generate_code(query, data):
    if not data:
        prompt = f"Based on the query '{query}', generate a Python code to visualize sample data for the population growth of India in the last 10 years."
    else:
        prompt = f"Based on the query '{query}' and the data: {data}, generate a Python code to visualize the data."
    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}]
    )
    generated_code = response.choices[0].message.content
    print("Generated code:", generated_code)
    return generated_code

#Function to parse the generated code
def parse_code(code):
    try:

#Finding and execute import statements
        import_stmt = re.search(r'import\s+(.+)', code)
        if import_stmt:
            imports = import_stmt.group(1).split(',')
            for imp in imports:
                exec(f'import {imp.strip()}')

#Finding and parse the data definition
        data_def = re.search(r'data\s*=\s*\[(.*?)\]', code, re.DOTALL)
        if data_def:
            data = ast.literal_eval(f'[{data_def.group(1)}]')
        else:
            data = []

#Finding the plotting code
        plotting_code = re.search(r'plt\.figure\(.+?plt\.show\(\)', code, re.DOTALL)
        if plotting_code:
            plotting_code = plotting_code.group()

#Defining a function to execute the plotting code and encode the plot as a base64 string
            def visualize_data():
                buf = io.BytesIO()
                plt.figure()
                exec(str(plotting_code))
                plt.savefig(buf, format='png')
                buf.seek(0)
                plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                plt.close()
                return plot_data

            return visualize_data, data

    except Exception as e:
        print(f"Error parsing the generated code: {e}")
        return None, None

#Flask route for the main page
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

#Getting the query from the form data
        query = request.form['query']

#Searching the web, generating code, and parsing the generated code
        search_results = search_web(query)
        generated_code = generate_code(query, search_results)
        visualize_data, data = parse_code(generated_code)

        if visualize_data:
            if data:

#Executing the visualize_data function and get the plot data
                plot_data = visualize_data()
            else:
                plot_data = None
        else:
            plot_data = None

#Rendering the index.html template with the query and plot data
        return render_template('index.html', query=query, plot_data=plot_data)

#Rendering the index.html template for GET requests
    return render_template('index.html')

#Running the Flask app in debug mode if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)