import re

import flask

from flask import request, jsonify
from flask_cors import CORS

from lxml import etree

from io import StringIO, BytesIO

import urllib

sampleHTML = '<!DOCTYPE html><!--comment--><div class="sibling-div" disabled id="start">some text for my div<img class="loading" src="none.jpg" /><!--data source only?--></div><div class="sibling-div2"></div>'


class BaseHTMLEntity:
  def __init__(self, entityType, depth, data):
    self.entityType = entityType
    self.depth = depth
    self.data = data

class Element(BaseHTMLEntity):
  def __init__(self, tag, attributes, depth, data = None):
    BaseHTMLEntity.__init__(self, 'Element', depth, data)
    self.tag = tag
    self.attributes = attributes
    self.warnings = []

  def __str__(self):
    return "Tag: {} \n Attributes: {} \n Depth: {}".format(self.tag, self.attributes, self.depth)

  def __repr__(self):
    return "Tag: {} \n Attributes: {} \n Depth: {}".format(self.tag, self.attributes, self.depth)

  def add_data(self, data):
    self.data = data

  def add_warning(self, warning):
    self.warnings.append(warning)

class Declaration(BaseHTMLEntity):
  def __init__(self, depth, data = None):
    BaseHTMLEntity.__init__(self, 'Declaration', depth, data)


class Comment(BaseHTMLEntity):
  def __init__(self, depth, data = None):
    BaseHTMLEntity.__init__(self, 'Comment', depth, data)


class WarningsList():
  # Returns true if the attributes contains an alt tag
  def test():
    pass


def ImageContainsAltTag(attributes):
  for attribute in attributes:
    if attribute[0] and attribute[0] == "alt":
      if len(attribute[1]) > 0:
        return True
  return False

class customHTMLParser():
  def __init__(self, htmlList):
    # Keep track of our depth
    self.depth = 0
    # Provide an ID for every tag
    self.index = 0
    # Track the current tag we're modifying that so we can use methods for the given class
    self.current_tag = None
    # Track statistics for different types of tags
    self.counter_declarations = 0
    self.counter_elements = 0
    self.counter_comments = 0
    self.counter_warnings = 0

    self.htmlList = htmlList
    self.statistics = htmlList["statistics"]

  def start(self, tag, attrib):
    # Update internal counters
    self.current_tag = Element(str(tag), dict(attrib), self.depth)
    self.index += 1
    self.depth += 1
    self.counter_elements += 1
    # Update the dictionary
    self.htmlList["elements"][self.index] = self.current_tag
    self.htmlList["statistics"]["elements"] = self.counter_elements

    if str(tag) == "img":
      if not ImageContainsAltTag(attrib):
        self.current_tag.add_warning({"label": "Missing alt text", "description":"Images should contain alt text describing the image."})
        self.counter_warnings += 1
        self.htmlList["statistics"]["warnings"] = self.counter_warnings


  def data(self, data):
    if not data.isspace():
      self.current_tag.add_data(data)

  def comment(self, text):
    # Update internal counters
    self.current_tag = Comment(self.depth, text)
    self.index += 1
    self.counter_comments += 1
    # Update the dictionary
    self.htmlList["elements"][self.index] = self.current_tag
    self.htmlList["statistics"]["comments"] = self.counter_comments

  def close(self):
    print("close")
    return "closed!"


def parseHTML(htmlText):
  mylist = {
    "statistics": {
      "declarations": 0,
      "comments": 0,
      "elements": 0,
      "warnings": 0,
    },
    "elements": {},
  }

  parser = etree.HTMLParser(target = customHTMLParser(mylist))
  etree.parse(StringIO(htmlText), parser)

  print(mylist)

  return mylist


# Function to serialise the instances of Element class
def serialiseTags(class_list):
  serialised_list = {
    "statistics": {},
    "elements": [],
  }

  for index_id, entity in class_list["elements"].items():
    if entity.entityType != 'Element':
      serialised_tag = {
        'id': index_id,
        'depth': entity.depth,
        'type': entity.entityType,
        'data': entity.data
      }
    else:
      serialised_tag = {
        'id': index_id,
        'depth': entity.depth,
        'type': entity.entityType,
        'tag': entity.tag,
        'attributes': entity.attributes,
        'data': entity.data,
        'warnings': entity.warnings,
      }
    serialised_list["elements"].append(serialised_tag)
  serialised_list["statistics"] = class_list["statistics"]

  return serialised_list


def runParser(htmlText):
  return jsonify(serialiseTags(parseHTML(htmlText)))


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False

CORS(app)


@app.route('/', methods=['GET'])
def home():
  return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/sample', methods=['GET'])
def api_sample():
  return runParser(sampleHTML)

@app.route('/process', methods=['GET'])
def api_query():
  html = request.args.get('html')

  decoded_html = urllib.parse.unquote(html)

  if encoded:
    return runParser(urllib.parse.unquote(html))
  else:
    return runParser(html)


app.run(host = '0.0.0.0', port = 64232)
