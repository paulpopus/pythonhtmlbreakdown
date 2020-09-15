import re

import flask

from flask import request, jsonify

from html.parser import HTMLParser

mytext = '<div id="id_target" class="test-class class-2" disabled></div><div id="id_target" class="test-class" disabled></div>'

mytext2 = '<img src="source.png" /><div class="parent-div">some text<div class="child-div"></div><div class="sibling-of-child-div"><img src="source.png" /></div></div><div class="sibling-div"><img src="source.png" /></div>'

mytext25 = '<div class="parent-div"><div class="child-div"></div><div class="sibling-of-child-div"></div></div>'

mytext3 = '<!DOCTYPE html><!--comment--><div class="sibling-div" disabled id="start"><img class="loading" src="none.jpg" /><!--data source only?--></div><div class="sibling-div2"></div>'

mylist = {}


class BaseHTMLEntity:
  def __init__(self, entityType, depth, data):
    self.entityType = entityType
    self.depth = depth
    self.data = data

class Element:
  def __init__(self, tag, attributes, depth, data = None):
    self.type = 'Element'
    self.tag = tag
    self.attributes = attributes
    self.depth = depth
    self.data = data

  def __str__(self):
    return "Tag: {} \n Attributes: {} \n Depth: {}".format(self.tag, self.attributes, self.depth)

  def __repr__(self):
    return "Tag: {} \n Attributes: {} \n Depth: {}".format(self.tag, self.attributes, self.depth)

  def add_data(self, data):
    self.data = data


class Declaration(BaseHTMLEntity):
  def __init__(self, depth, data = None):
    BaseHTMLEntity.__init__(self, 'Declaration', depth, data)


class Comment(BaseHTMLEntity):
  def __init__(self, depth, data = None):
    BaseHTMLEntity.__init__(self, 'Comment', depth, data)

class customHTMLParser(HTMLParser):
  def __init__(self):
    # Initialize the base class
    HTMLParser.__init__(self)
    # Keep track of opened tags, expecting them to be closed, otherwise we can assume bad HTML
    self.started_tags = []
    # Keep track of our depth
    self.depth = 0
    # Provide an ID for every tag
    self.index = 1
    # Track the current tag we're modifying that so we can use methods for the given class
    self.current_tag = None

  """ def handle_starttag(self, tag, attrs):
    self.current_tag = Element(str(tag), attrs, self.depth)
    mylist[self.index] = self.current_tag
    self.started_tags.append(tag)
    self.index += 1
    self.depth += 1

  def handle_data(self, data):
    self.current_tag.add_data(data)


  def handle_endtag(self, tag):
    if len(self.started_tags) > 0 and self.depth > 0 and tag == self.started_tags[-1]:
      del self.started_tags[-1]
      self.depth -= 1

  def handle_comment(self, data):
    self.current_tag = Comment(self.depth, data)
    mylist[self.index] = self.current_tag
    self.index += 1 """

  def handle_decl(self, decl):
    self.current_tag = Declaration(self.depth, decl)
    mylist[self.index] = self.current_tag
    self.index += 1


parser = customHTMLParser()
parser.feed(mytext3)


# Recursive function to serialise the instances of Element class
def serialiseTags(class_list):
  custom_list = []

  for index_id, entity in class_list.items():
    serialised_tag = {
      'id': index_id,
      'depth': entity.depth,
      'type': entity.entityType,
      'data': entity.data
    }
    custom_list.append(serialised_tag)

  return custom_list




serialised_list = serialiseTags(mylist)


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False




@app.route('/', methods=['GET'])
def home():
  return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
@app.route('/api', methods=['GET'])
def api_all():
  return jsonify(serialised_list)

app.run(host = '0.0.0.0', port = 64232)







# search(mytext3)

