import re

import flask

from flask import request, jsonify
from flask_cors import CORS

from lxml import etree

from io import StringIO, BytesIO

import urllib

sampleHTML = '<!DOCTYPE html><marquee style="background: coral;">This just in breaking news!</marquee><!--comment--><div style="color: black;" class="sibling-div" disabled id="start">some text for my div<img class="loading" src="none.jpg" /><!--data source only?--></div><div class="sibling-div2"></div>'

deprecated_tags = ['marquee', 'acronym', 'applet', 'basefont', 'font', 'menu', 'center', 'isindex', 'u', 's', 'dir', 'frame', 'frameset', 'spacer', 'blink']

class baseHTMLEntity:
  def __init__(self, entityType, depth, data):
    self.entityType = entityType
    self.depth = depth
    self.data = data

class element(baseHTMLEntity):
  def __init__(self, tag, attributes, depth, data = None):
    baseHTMLEntity.__init__(self, 'Element', depth, data)
    self.tag = tag
    self.attributes = attributes
    self.warnings = []

  def __str__(self):
    return 'Tag: {} \n Attributes: {} \n Depth: {}'.format(self.tag, self.attributes, self.depth)

  def __repr__(self):
    return 'Tag: {} \n Attributes: {} \n Depth: {}'.format(self.tag, self.attributes, self.depth)

  def add_data(self, data):
    self.data = data

  def add_warning(self, warning):
    self.warnings.append(warning)

class declaration(baseHTMLEntity):
  def __init__(self, depth, data = None):
    baseHTMLEntity.__init__(self, 'Declaration', depth, data)


class comment(baseHTMLEntity):
  def __init__(self, depth, data = None):
    baseHTMLEntity.__init__(self, 'Comment', depth, data)


warning_list = {
  'MISSING_ALT_TEXT': {
    'label': 'Missing alt text',
    'description': 'Images should contain alt text describing the image.'
  },
  'DEPRECATED_TAG': {
    'label': 'Deprecated HTML tag',
    'description': 'This tag has been deprecated or marked obsolete, it may not function as expected in new browsers.'
  },
  'INLINE_STYLES': {
    'label': 'Element has inline styles',
    'description': 'Inline styles are not recommended as they can affect performance and can be hard to maintain. Moving them to a stylesheet is recommended.'
  },
}

# Returns true if the attributes contains an alt tag
def getWarning(code):
  return warning_list.get(code)


def imageContainsAltTag(attributes):
  for key, value in attributes.items():
    if key and key == 'alt':
      if len(value) > 0:
        return True
  return False


def hasInlineStyles(attributes):
  for key, value in attributes.items():
    if key and key == 'style':
      if len(value) > 0:
        return True
  return False


def tagIsDeprecated(tag):
  if tag in deprecated_tags:
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


  def start(self, tag, attrib):
    string_tag = str(tag)
    # Update internal counters
    self.current_tag = element(string_tag, dict(attrib), self.depth)
    self.index += 1
    self.depth += 1
    self.counter_elements += 1

    # Update the dictionary
    self.htmlList['elements'][self.index] = self.current_tag


    if tagIsDeprecated(string_tag):
      self.current_tag.add_warning(getWarning('DEPRECATED_TAG'))
      self.counter_warnings += 1

    if hasInlineStyles(attrib):
      self.current_tag.add_warning(getWarning('INLINE_STYLES'))
      self.counter_warnings += 1

    if string_tag == 'img':
      if not imageContainsAltTag(attrib):
        self.current_tag.add_warning(getWarning('MISSING_ALT_TEXT'))
        self.counter_warnings += 1


  def data(self, data):
    if not data.isspace():
      self.current_tag.add_data(data)


  def comment(self, text):
    # Update internal counters
    self.current_tag = comment(self.depth, text)
    self.index += 1
    self.counter_comments += 1

    # Update the dictionary
    self.htmlList['elements'][self.index] = self.current_tag

  def close(self):
    self.htmlList['statistics']['elements'] = self.counter_elements
    self.htmlList['statistics']['comments'] = self.counter_comments
    self.htmlList['statistics']['warnings'] = self.counter_warnings
    return 'Parser is closed'


def parseHTML(htmlText):
  mylist = {
    'statistics': {
      'comments': 0,
      'elements': 0,
      'warnings': 0,
    },
    'elements': {},
  }

  parser = etree.HTMLParser(target = customHTMLParser(mylist))
  etree.parse(StringIO(htmlText), parser)

  return mylist


# Function to serialise the instances of Element class
def serialiseTags(class_list):
  serialised_list = {
    'statistics': {},
    'elements': [],
  }

  for index_id, entity in class_list['elements'].items():
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
    serialised_list['elements'].append(serialised_tag)
  serialised_list['statistics'] = class_list['statistics']

  return serialised_list


def runParser(htmlText):
  return jsonify(serialiseTags(parseHTML(htmlText)))


app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

CORS(app)

@app.route('/sample', methods=['GET'])
def api_sample():
  return runParser(sampleHTML)

@app.route('/process', methods=['GET'])
def api_query():
  html = request.args.get('html')
  url = request.args.get('url')

  if url:
    page = urllib.request.urlopen(url)
    mybytes = page.read()
    htmlString = mybytes.decode('utf8', 'ignore')
    page.close()

    return runParser(urllib.parse.unquote(htmlString))

  elif html:
    return runParser(urllib.parse.unquote(html))


@app.route('/warnings', methods=['GET'])
def api_warnings():
  return warning_list


app.run(host = '0.0.0.0', port = 64232)
