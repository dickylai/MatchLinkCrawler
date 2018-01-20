#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import time
import sys

# site for scraping
DOMAIN = 'http://bongdanet.vn'
# path for saving links
LINKSPATH = sys.argv[1] if len(sys.argv) > 1 else None;

def makeSoupFromUrl(domain, url):
	page = requests.get(domain + url)
	soup = BeautifulSoup(page.content, 'html.parser')
	page.close()
	return soup

def printLinks(links):
	print ('Links are as follows: ')
	print (links[0].get_text().strip())

def saveLinksToFile(links, filePath):
	print ('Saving links to ' + filePath + '...')
	with open(filePath, 'w+') as linksFile:
		linksFile.write(links[0].get_text().strip())
	print ('Done.')

def exitProgram():
	print ()
	exit()

# program starts
try:
	print('+=====================================+')
	print('|                                     |')
	print('|   CRAWL SOPCAST LINKS FOR MATCHES   |')
	print('|                                     |')
	print('+=====================================+')
	print()
	firstTeam, secondTeam = '', ''
	# get inputs from user - first team is compulsory
	while not firstTeam:
		firstTeam = input('Please input the first team: ')
		secondTeam = input('Please input the second team: (OPTIONAL) ')

	# get all the matches
	matches = makeSoupFromUrl(DOMAIN, '/link-sopcast').select('div.stream-info div.competeTeams div.livetv-thumbnail a')

	# get the required match
	matchUrl = ''
	for match in matches:
		if firstTeam.lower() in match.get_text().lower() and (not secondTeam or secondTeam.lower() in match.get_text().lower()):
			matchUrl = match['href']
			print('Match found -', match.get_text())
			break

	if not matchUrl:
		print('No match has been found.')
		exit()

	# get all the sopcast links for the required match
	sopcastLinks = makeSoupFromUrl(DOMAIN, matchUrl).select('ul.zone-sopcast-links')

	while not sopcastLinks:
		print('No link is available at this moment. Auto retry in a minute.')
		time.sleep(60)
		sopcastLinks = makeSoupFromUrl(domain, matchUrl).select('ul.zone-sopcast-links')

	if LINKSPATH is None:
		printLinks(sopcastLinks)
	else:
		saveLinksToFile(sopcastLinks, LINKSPATH)

except KeyboardInterrupt:
	exitProgram()
