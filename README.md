Naïf
====

Naïf is a python library and server for text classification. It currently implements a Naïve Bayes classifier, 
which is accessed through a simple REST-based interface handling JSON-formatted data. 

In time, Naif will be offered as a service, providing access to simple, scalable text classification in the cloud.

Installation
------------

    git clone git://github.com/digitalex/naif.git
    cd naif
    pip install -r requirements.txt
    python server.py
  
Training
-----

    curl -X POST -H "Content-Type: application/json" -d '{"text":"the quick brown fox", "cat":"good"}' http://localhost:8888/train
  

Classifying
-----------

    curl -X POST -H "Content-Type: application/json" -d '{"text":"the quick foolish monkey"}' http://localhost:8888/classify
