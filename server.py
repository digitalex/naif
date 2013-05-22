from classifier import *
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import json
import re

define("port", default=8888, help="run on the given port", type=int)

def tokenize(doc):
    splitter = re.compile('\\W*')
    for w in splitter.split(doc):
        if len(w) > 2 and len(w) < 20:
            yield w.lower()

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, classifier):
        self.classifier = classifier

    def get(self):
        self.write("<html><body>")
        self.write("<h2>Categories:</h2><ul>")
        for category, size in self.classifier.doccounts.iteritems():
            self.write("<li>%s (%i)</li>" % (category, size))
        self.write("</ul></body></html>")

class TrainHandler(tornado.web.RequestHandler):
    def initialize(self, classifier):
        self.classifier = classifier

    def post(self):
        self.set_header("Content-Type", "application/json")
        data = json.loads(self.request.body)
        document = tokenize(data['text'])
        category = data['cat']
        self.classifier.train(document, category)
        self.write("{'status':'success'}")

def main():
    tornado.options.parse_command_line()
    classifier = Classifier()
    properties = dict(classifier = classifier)
    app = tornado.web.Application([
        (r"/", MainHandler, properties),
        (r"/train", TrainHandler, properties),
        #(r"/classify", ClassifyHandler, properties),
    ])
    app.listen(options.port)

    print "Application ready and listening @ %i" % (options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
