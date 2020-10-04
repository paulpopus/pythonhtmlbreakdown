import re

import flask

from flask import request, jsonify
from flask_cors import CORS

from html.parser import HTMLParser

import urllib.parse

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


class HTMLHelpers():
  # Returns true if the attributes contains an alt tag
  def test():
    pass


def ImageContainsAltTag(attributes):
  for attribute in attributes:
    if attribute[0] and attribute[0] == "alt":
      if len(attribute[1]) > 0:
        return True
  return False

def isDataEmpty(data):
  reg = '(\\n)+(\s)'

  if re.match(reg, data):
    return True

  return False

class customHTMLParser(HTMLParser):
  def __init__(self, htmlList):
    # Initialize the base class
    HTMLParser.__init__(self)
    # Keep track of opened tags, expecting them to be closed, otherwise we can assume bad HTML
    self.started_tags = []
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

  def handle_starttag(self, tag, attrs):
    # Update internal counters
    self.current_tag = Element(str(tag), attrs, self.depth)
    self.started_tags.append(tag)
    self.index += 1
    self.depth += 1
    self.counter_elements += 1
    # Update the dictionary
    self.htmlList["elements"][self.index] = self.current_tag
    self.htmlList["statistics"]["elements"] = self.counter_elements

    if str(tag) == "img":
      if not ImageContainsAltTag(attrs):
        self.current_tag.add_warning({"label": "Missing alt text", "description":"Images should contain alt text describing the image."})
        self.counter_warnings += 1
        self.htmlList["statistics"]["warnings"] = self.counter_warnings

  def handle_data(self, data):
    if not data.isspace():
      self.current_tag.add_data(data)


  def handle_endtag(self, tag):
    if len(self.started_tags) > 0 and self.depth > 0 and tag == self.started_tags[-1]:
      del self.started_tags[-1]
      self.depth -= 1

  def handle_comment(self, data):
    # Update internal counters
    self.current_tag = Comment(self.depth, data)
    self.index += 1
    self.counter_comments += 1
    # Update the dictionary
    self.htmlList["elements"][self.index] = self.current_tag
    self.htmlList["statistics"]["comments"] = self.counter_comments

  def handle_decl(self, decl):
    # Update internal counters
    self.current_tag = Declaration(self.depth, decl)
    self.index += 1
    self.counter_declarations += 1
    # Update the dictionary
    self.htmlList["elements"][self.index] = self.current_tag
    self.htmlList["statistics"]["declarations"] = self.counter_declarations


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
  parser = customHTMLParser(mylist)
  parser.feed(htmlText)

  return mylist


# Recursive function to serialise the instances of Element class
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

@app.route('/process', methods=['GET', 'POST'])
def api_query():
  html = request.args.get('html')
  encoded = request.args.get('encoded')

  decoded_html = urllib.parse.unquote(html)

  if encoded:
    return runParser(urllib.parse.unquote(html))
  else:
    return runParser(html)


app.run(host = '0.0.0.0', port = 64232)

