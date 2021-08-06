# Financial Chat App

### Description:
This project is designed to test knowledge of back-end web technologies in Python as a part of a Jobsity coding challenge, It assess the ability to create back-​end products with attention to details, standards, and reusability.

### Functionality
The goal to create a simple browser-based chat application using Python. This application should allow several users to talk in a chatroom and also to get stock quotes from an API using a specific command <b>/stock=stock_code</b>.

To achive that objective, SocketIO was used to provide asynchronous services to the Flask applications and access to low latency bi-directional communications between the clients and the server. The client-side application can use any of the SocketIO client libraries in Javascript, Python, or any other compatible client to establish a permanent connection to the server. 

Also, to keep record of the Users, and the chatroom messages, MongoDB helps to create a document-oriented database which stores data in JSON-like documents with dynamic schema. It means you can store your records without worrying about the data structure such as the number of fields or types of fields to store values. Mongo Atlas as a fully-managed cloud database developed by the same people that build MongoDB. Atlas host the database, on GCP cloud service provider.

## Table of Content
* [Environment](#environment)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Examples of use](#examples-of-use)
* [Future Work](#bugs)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Environment
This project is interpreted/tested on macOS Big Sur 11.5.1 using a conda environment python3 (version 3.7.7), wacth [setenv](/setenv) file to set up the environment.

## Installation
* Clone this repository: 
`git clone "https://github.com/campopinillos/ChatApp.git"`
* Access ChatApp directory: `cd ChatApp`
* Run: `python app.py` and go to http://127.0.0.1:5000/ in your browser

## File Descriptions
[app.py](app.py) - Flask app with SocketIO asynchronous service.

[db.py](db.py) - File with database functions to create, store and query Users and Chatroom messages.

[bot.py](bot.py) - ​Decoupled bot that calls an API using the stock_code parameter (​https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcv&h&e=csv​, here aapl.us is the stock_code: /stock=​​aapl.us). The bot  parse the received CSV file and then it sends a message back into the chatroom using a message broker. The message is a stock quote using the following format: “APPL.US quote is $93.42 per share”. The post owner is the bot.

[setenv](setenv) - Configure python virtual environment via conda.

[requirements.txt](requirements.txt) - Python packages.

## Examples of use
```
/stock=​​aapl.us
/stock=amzn.us
```

## Future Work
* Unittest functionality
* Show only the last 50 messages in the chatroom.


## Bugs
No known bugs at this time. 

## Author
Campo Pinillos - [Github](https://github.com/campopinillos)

## License
Public Domain. No copy write protection. 