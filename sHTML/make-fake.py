# Fetch an FTML file and extract the first <div> that contains a definition.
#
# Setup/Usage:
#
# python -m venv make-fake-venv
# source make-fake-venv/bin/activate
# pip install requests bs4
# deactivate
#
# Usage:
# source make-fake-venv/bin/activate
# python make-fake.py
# deactivate

import requests
from bs4 import BeautifulSoup
import re
import sys

def fetch_definition(url):
  try:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
      defStr = extract_and_clean_first_definition(response.text)
      print(defStr)
  except Exception as e:
      print(f"An error occurred: {e}")

# Remove all attributes that we do not need from every tag:
def remove_attributes(soup):
  attributes_to_remove = [
    'id',
    'class',
    'style',
    'width',
    'lspace',
    'rspace',
    'stretchy'
  ]
  content = list(soup.find_all(True))
  content.append(soup)
  for tag in content:
    for attr in attributes_to_remove:
      if attr in tag.attrs:
        del tag.attrs[attr]

# Check whether there exists at least one empty tag:
def has_empty_tag(soup):
  for tag in soup.find_all(True):
    if not tag.contents or all(isinstance(content, str) and content.strip() == '' for content in tag.contents):
      return True
  return False

# Remove all empty tags:
def remove_empty_tags(soup):
  if has_empty_tag(soup):
    content = list(soup.find_all(True))
    content.append(soup)
    for tag in content:
      if not tag.contents or all(isinstance(content, str) and content.strip() == '' for content in tag.contents):
        tag.decompose()
    remove_empty_tags(soup)

# Extract the first definition div and clean it up:
def extract_and_clean_first_definition(html):
  soup = BeautifulSoup(html, 'html.parser')
  div = soup.find('div', attrs={'data-ftml-definition': True})
  remove_attributes(div)
  remove_empty_tags(div)
  if div:
    divStr = str(div)
    return divStr
  else:
    print("No definition found.")


n = len(sys.argv)
script_name = sys.argv[0]

if n < 2:
  print('No URL given')
  print('Usage: ', script_name, ' "<URL>"')
  print('Example URL: https://mathhub.info/?a=smglom%2Fcategories&rp=mod%2Fcategory.en.tex')
else:
  url = sys.argv[1]
  fetch_definition(url)
