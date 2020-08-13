from bs4 import BeautifulSoup
import requests

def getHtmlCode(url): # Returns all the html code from the URL
	r = requests.get(url)
  
	return r.text

def isInParentheses(htmlCode, index):
	for i in range(index, 0, -1):
		if htmlCode[i] == '(':
			return True
		elif htmlCode[i] == ')':
			return False
	return False

def getFirstLink(htmlCode): 
	# Returns the first link in the main content
	# The below code uses indices instead of bs4's find function
	# as bs4's find(startID) returns everything in the div including the
	# citations which is unwanted and could take up unnecessary memory
	mainCode = htmlCode[htmlCode.index(startID): htmlCode.index(endID)]
	soup = BeautifulSoup(mainCode, features="html.parser")
	try:
		soup.i.decompose() # Removes all italics as part of the rules
	except:
		pass

	for paragraph in soup.findAll('p'):	# Only use text: no side panels
		for link in BeautifulSoup(str(paragraph), features="html.parser").findAll('a'):
			if 'href=\"/wiki/' in str(link) and not link.attrs['href'] == urlSuffix and not 'href=\"/wiki/File' in str(link):
				indexOfLink = mainCode.index(link['href'])
				if not isInParentheses(mainCode, indexOfLink):
					return link.attrs
	return None

startID = 'mw-content-text'	# Id of the start of the main content
endID = 'mw-data-after-content'	# Id of the end of the main content


urlPrefix = 'https://en.wikipedia.org'

# For Random Test 
#urlSuffix = '/wiki/Special:Random'

# For Input by user 
urlSuffix = '/wiki/' + input('Enter the /wiki/___: ')
path = list()

print("Start: " + urlSuffix)

while True:
	if urlSuffix == '/wiki/Philosophy':	# If we have reached the end
		print("\nWe have reached philosophy!")
		break

	if urlSuffix in path: # If we have entered a loop
		print("\nWe are stuck in a loop!")
		break

	path.append(urlSuffix)
	link = getFirstLink(getHtmlCode(urlPrefix + urlSuffix))

	if link == None: # If no links are returned (blank or referral pages)
		print("\nWe have hit a dead end!")
		break
	else:
		print(link['title'])
		urlSuffix = link['href']