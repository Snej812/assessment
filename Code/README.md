# Data Platform Challenge

### Overview
This project is a Python script fetch_articles.py designed to fetch articles from an API, process them, and save the data to CSV files. It includes unit tests in testmain.py for testing the functionality of the main script main.py. The project structure also includes configuration files (config.py), a state file (state.txt), a log file (fetch_articles.log), and a folder (files/) to store generated CSV files.

### Project Structure
project_root/ \
│\
|── Dockerfile\
|── docker-compose.yml\
│\
├── code/\
│   ├── main.py\
│   ├── testmain.py\
│   ├── config.py\
│   ├── state.txt\
│   ├── fetch_articles.log\
│   └── files/ \
│      ├── (generated CSV files)\
│\
└── README.md\

**build**: Contains Docker-related files.

&emsp;Dockerfile: Contains instructions for building the Docker image.\
&emsp;docker-compose.yml: Contains configuration for Docker Compose.

**code/**: Contains Python code and related files. \
&emsp;main.py: Contains the main script fetch_articles.py. \
&emsp;testmain.py: Contains unit tests for main.py. \
&emsp;config.py: Contains configuration parameters. \
&emsp;state.txt: State file for storing API call information. \
&emsp;fetch_articles.log: Log file for logging script activities. \
&emsp;files/: Folder to store generated CSV files. \
&emsp;README.md: Markdown file containing project documentation. \

#### Getting Started
To run the script: 

&emsp;1. Ensure Python 3.x is installed on your system. \
&emsp;2. Install the required dependencies by running \
&emsp;&emsp;&emsp;pip install -r requirements.txt. \
&emsp;3.Configure config.py with your API key and other parameters. \
&emsp;4.Run the script using \
&emsp;&emsp;&emsp;python code/main.py.

To run unit tests:

&emsp;1.Navigate to the code/ directory. \
&emsp;2.Run python testmain.py.


#### Docker Support
To build and run the project using Docker:

&emsp;1.Navigate to the project root directory.
&emsp;2.Build the Docker image: docker-compose build.
&emsp;3.Run the Docker container: docker-compose up.