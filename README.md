# ZeroShot_Visualizer
This repository showcases the integration of large language models (LLMs) and their application in building conversational AI systems like chatbots.

Description:

This project creates a zero-shot visualizer, a web application that can generate visualizations based on a user's input query without any specific training data. 
The project follows a multi-step process:

1. SEARCH FUNCTIONALITY : Implements a search functionality using the SerpApi library to retrieve relevant data based on the user's query.

2. CODE GENERATION : Uses a language model (mistralai/Mixtral-8x7B-Instruct-v0.1) from the Together API to generate Python code for visualizing the data.

3. CODE PARSING & EXECUTION : Parses the generated code to extract necessary components (imports, data definitions, plotting code), and dynamically executes the code to create the visualization.

4. VISUALIZATION : Orchestrates the entire workflow, prompting the user for a query, retrieving data, generating code, parsing the code, and executing the visualization.

5. WEB INTERFACE : Integrates the core functionality with a Flask web application, providing a user-friendly interface where users can enter their queries and view the generated visualizations.                   
   The web interface is built using HTML, CSS, and Flask templates.

6. LANGUAGE MODEL INTEGRATION : The project leverages the Together API, which provides access to language models like mistralai/Mixtral-8x7B-Instruct-v0.1. This language model is
   responsible for generating the Python code based on the query and data.

7. CODE EXECUTION: Demonstrates the concept of dynamically executing generated code using LangChain, a framework for building applications with large language models. LangChain is used to execute the generated code 
   without needing to write it to a file first.
