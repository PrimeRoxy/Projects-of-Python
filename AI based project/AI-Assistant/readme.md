This repository contains a set of Python scripts designed to facilitate various tasks related to message classification, action discovery, parameter generation, and API invocation within a system designed to interact with users and perform relevant actions based on their input.

1. Custom Category Classifier (classifier1.py):
Purpose: This script employs OpenAI's GPT-4 model to classify messages into predefined categories such as "INFO SHARED," "ACTION REQUEST," "ASK," and "IMPLICIT ACTION."
Details: It provides a detailed explanation of the message's intent within the context of real estate transactions involving customers and agents.
Usage: Execute the script and provide messages for classification.


2. Discover Action ID (classifier2.py):
Purpose: This script analyzes user queries and matches them with appropriate action IDs from a JSON file containing a list of actions.
Details: It assists in identifying the most suitable action based on the user's intent, providing the corresponding action ID or signaling "No Action Found."
Usage: Run the script and input user queries to discover relevant action IDs.


3. Generate Parameters (classifier3.py):
Purpose: Generates input parameters required for performing a specific action based on the action ID obtained from the previous step.
Details: Extracts necessary information from a JSON file and presents the input parameters necessary for executing the identified action.
Usage: Execute the script, provide action IDs, and receive the corresponding input parameters.


4. User Input Processing (classifier4.py):
Purpose: Guides users through providing input parameters for executing an action, ensuring all required fields are included.
Details: Prompts users for input based on identified parameters, validates the provided data, and requests missing information if necessary.
Usage: Run the script, input queries, and follow the prompts to provide necessary input parameters.


5. User Output Processing (classifier5.py):
Purpose: Formats user input data into JSON and utilizes it to invoke an API for executing a designated action.
Details: Presents the outcome of the action in an elegant manner, completing the interaction loop with the user.
Usage: Execute the script, provide user input data, and observe the outcome of the action execution.


Setup Instructions:

Environment Setup:
Install Python and the required dependencies listed in the respective scripts.
Set up an environment variable OPENAI_API_KEY with your OpenAI API key.

Execution:
Run each script individually in your Python environment.
Follow the prompts to interact with the system, providing necessary input as instructed.


Exiting:
To exit any script, type "exit" when prompted for input.
The script will acknowledge your request and terminate accordingly.

Additional Notes:
Ensure access to required APIs and necessary data files for the scripts to function correctly.
Handle exceptions and errors gracefully to enhance the robustness of the system.
Customize JSON data, prompts, and actions as per specific use cases and requirements.