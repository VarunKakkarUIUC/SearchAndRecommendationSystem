# Search and Recommendation system - API



## Introduction

A search engine web API for indexing and searching review topics and providing location based results to callers. This API is used by Search and Recommender System - UX to  display search and recommendations based on user inputs and location.

API is written in python and it runs on Flask web framework.



### Project files

Here are details of all code files and project structure

| File/Folder                                                  | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| businessreviews                                              | This folder contains the review data.                        |
| ./businessreviews/businessreviews.dat                        | This file has the business reviews tokenized data obtained from data extraction pipeline of the project. The data is formatted as line-corpus and each line is represented as JSON string. |
| ./businessreviews/line.toml                                  | line.toml config file for MeTA.                              |
| data                                                         | This folder contains the reverse lookup data.                |
| ./data/yelp_pennsylvania_business_ recommendation_dataset.json | This file contains the reverse lookup data for each business. This is data is generated by extraction pipeline of the project and is in JSON format. This information is used in response from API. |
| application.py                                               | Python module defining Flask application and routes. It exposed one GET api named Search. |
| application.test.py                                          | Python module defining tests function. Super useful for debugging and running outside of Flask environment. This module is also used to generate inverted_index and posting files offline/upfront, without API being invoked. |
| apptrace.py                                                  | Python module for collecting and printing trace logs.        |
| config.toml                                                  | MeTA configuration file. It defines the data file, analyzer settings, etc. |
| controller.py                                                | Python module for extracting request parameters, calling indexer, calling lookup and preparing API response. |
| indexer.py                                                   | Python module for indexing, ranking and searching using metapy. |
| lookup.py                                                    | Python module for loading and performing lookup by business Ids. |
| requirements.txt                                             | List all required python modules to be installed by *pip*.   |
| settings.py                                                  | Python modules defining application configuration settings.  |
| stopwords.txt                                                | List Stopwords for MeTA indexing.                            |



#### Configuration

Configuration for API is in file `settings.py`

Here is the description for all configuration settings

| Configuration     | Data type | Description                                                  |
| ----------------- | --------- | ------------------------------------------------------------ |
| debugMode         | bool      | When set to `True`application collects logs. These logs can be retrieved in response by passing `enabletrace` in request query. |
| lookupFilePath    | string    | Relative path to lookup file.                                |
| maxSearchResults  | int       | Number of top items to fetch while searching.                |
| cfg               | string    | path to MeTA config file. It's a config.toml file.           |
| datasetKey        | string    | key for review documents and lookup data.                    |
| bm25_K1           | float     | OkapiBM25 K1 parameter                                       |
| bm25_b            | float     | OkapiBM25 b parameter                                        |
| bm25_k3           | float     | OkapiBM25 k3 parameter                                       |
| useJsonExtraction | bool      | When set to `True` application performs a JSON parsing on document retrieved after search. Document is required to be formatted as JSON string for this to work. |



#### API workflow

Once the request is received by `Search` method in *application.py*, the control is passed to `Search` method of `Controller` class.

`Controller.Search` then extracts the parameters from request and load *lookup* and `indexes`.

It then invokes `queryResults` method of `Indexer` class. `queryResults` method instantiated a `OkapiBM25` ranker and then score and ranks the documents based on query. Method then iterates over ranked document Ids results and builds a list of business Ids based on ranked list. The list of business Ids is then returned back to caller.

`Controller.Search` then invokes method `documentLookup` of `Lookup` class. This method returns the business information based on business Ids passed in.

`Controller.Search` then perform a filter on location data and splits the query results into `searchResults` and `recommendations`.

The `searchResults` and `recommendations` are then sent back as JSON response from API.



#### API request 

API HTTP request will look like

```http
GET <server_endpoint_address>/v1/search?text=good+pizza&city=Pittsburgh&state=PA
```

| Parameter   | Description                                                  | Required  |
| ----------- | ------------------------------------------------------------ | --------- |
| text        | Search Query                                                 | mandatory |
| city        | City for query                                               | optional  |
| state       | Two letter State for query                                   | optional  |
| enabletrace | If passed, response also contains application trace logs when server application `debugMode` is set to `True` | optional  |



#### API response

API response fields

```json
{
    "searchResults" : [
        {
          "address": "422 Greenfield Ave",
          "averageUserRating": "4.526315789473684",
          "business_id": "2d9yZ11uVa83OEQWxe4vlQ",
          "categories": "Pizza, Restaurants",
          "city": "Pittsburgh",
          "name": "Conicella Pizza",
          "reviewCount": "38",
          "sentiment": "0.8938315789473686",
          "state": "PA"
    	}
    ],
    "recommendations": [
        {
          "address": "3939 William Penn Hwy",
          "averageUserRating": "4.5576923076923075",
          "business_id": "X4QbkHl7pOTVsgLa7XuUBg",
          "categories": "Gluten-Free, Restaurants, Pizza, Salad, Fast Food",
          "city": "Monroeville",
          "name": "Blaze Fast Fire'd Pizza",
          "reviewCount": "104",
          "sentiment": "0.8639048076923076",
          "state": "PA"
        }
    ]
}
```



We have hosted this application at following endpoint `http://13.77.179.28`.

Feel free to call this API for example 

`GET http://13.77.179.28/v1/search?text=good%20pizza&city=Pittsburgh&state=PA`





To host and run the application yourself, please follow through rest of this file.

## System Requirements

We have used Ubuntu Server 18.04 LTS as our server. However, API should work on any stable distribution of Linux. Please ensure that you have following installed on your Linux machine.

- Python3    

  - This comes by default in Linux

- Nginx   

  -  It is a very popular HTTP, reverse proxy server, and a generic TCP/UDP proxy server


### Modules

All required python modules are listed in file 

```shell
./sarsapi/requirements.txt
```

The modules can be classified into following

| Area                 | Modules                                                      | Description                                                  |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Python virtual env   | wheel, venv                                                  | These are used for creating virtual environment.             |
| Python MeTA bindings | metapy, pytoml                                               | **M**od**e**rn **T**ext **A**nalysis libraries               |
| Flask and related    | Flask, itsdangerous, Jinja2, MarkupSafe, Werkzeug, flask-jsonpify, flask-restful, flask-cors | Flask web framework modules                                  |
| Web Server           | gunicorn                                                     | WSGI HTTP server for Python apps.. metapy libraries are not compatible within a Flask development server and hence gunicorn is needed. |



## Installation

Clone this repository to a folder and then open shell and change directory to folder *sarsapi*

Let's ensure *pip* is installed. On the shell prompt execute

```shell
sudo apt-get install python3-pip
```

Make sure *pip* and *setuptools* are the latest version

```shell
pip3 install --upgrade pip setuptools
```

Install *python3-dev* and *python3-virtualenv*

```shell
sudo apt-get install python3-dev python3-virtualenv
```

We installed [virtualenv](https://virtualenv.pypa.io/en/latest/) and [pip](https://pypi.org/project/pip) to handle our application dependencies. Let's create virtual environment.

We will create the environment in current folder represented by . (dot) and activate it.

```shell
python3 -m venv .
source ./bin/activate
```

Our prompt will change when the *virutalenv* is activated and will look like this

```shell
(sarsapi) premp3@linux:~$ 
```

Now, lets ensure we have latest *pip* in virtual environment

```shell
pip install --upgrade pip
```

Now we will install all listed modules from file *requirements.txt*

```shell
pip install -r requirements.txt
```

When this command finishes, you will have all the required modules installed and we are ready to start the API.

Before starting the API, let's create the *index* files which will be used by API to perform search. This step saves time when API starts as required *indexes* and *postings* are created upfront.

File *application.test.py has the code to initiate creation of *inverted index* and perform a test search. Let's run this file in python

```shell
python ./application.test.py
```

When this execution is complete, we are ready to launch our API.

We could run our app with the Flask development server using the `python application.py` command. However, *metapy* libraries are incompatible and hence we will run the *Flask* app with *Gunicorn*.

To start the API, execute

```shell
gunicorn -w4 application:app
```

Our API is now be running at address `http://127.0.0.1:8000`

Now, let's expose this API endpoint on port 80 using Nginx web server

##### Install Nginx

Execute following to get Nginx installed

```shell
sudo apt update
sudo apt install nginx
```

After installation is complete, enable firewall rule for nginx

```shell
sudo ufw allow 'Nginx HTTP'
```

We are only allowing HTTP endpoints, if needed we can also both *HTTP* and *HTTPS* using *`Nginx Full`*.

Now, lets configure *nginx* to proxy for our *python gunicorn* server running on port *8000*

##### Configure Nginx

Execute following to edit Nginx configuration

```shell
sudo nano /etc/nginx/sites-available/default
```

Then edit the content as below.

```
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }
```

Save the file and then restart *nginx*.

```shell
sudo systemctl restart nginx
```



#### That's it. 

Our API is now available on port 80 i.e. `http://127.0.0.1` or whatever is the external IP or address.



