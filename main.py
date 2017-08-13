#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import time

# site for scraping
domain = 'http://bongdanet.vn'

def makeSoupFromUrl(domain, url):
	page = requests.get(domain + url)
	soup = BeautifulSoup(page.content, 'html.parser')
	page.close()
	return soup

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
	matches = makeSoupFromUrl(domain, '/link-sopcast').select('div.stream-info div.competeTeams div.livetv-thumbnail a') 

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
	sopcastLinks = makeSoupFromUrl(domain, matchUrl).select('ul.zone-sopcast-links')

	while not sopcastLinks:
		print('No link is available at this moment. Auto retry in a minute.')
		time.sleep(60)
		sopcastLinks = makeSoupFromUrl(domain, matchUrl).select('ul.zone-sopcast-links')

	print ('Links: ')
	for link in sopcastLinks:
		print(link.get_text())

except KeyboardInterrupt:
	exitProgram()