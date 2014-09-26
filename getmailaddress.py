#!python
#Author: Li Lin
#Date: 2014-08-11

import sys
import mechanize
from bs4 import BeautifulSoup
import re

#brower
br=mechanize.Browser()

#options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

#follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

#debugging?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

#user-agent(This is a cheating.)
br.addheaders=[('User-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1 ')]

#get the e-mail address
r=br.open('http://www.ncbi.nlm.nih.gov/pubmed/?term=RNA-seq')
html=r.read()  # html is a str type
list_paperid=re.findall(r'<div class="rslt"><p class="title"><a href="/pubmed/(\d+)"',html)
list=[]
for i in list_paperid:
	r_paper=br.open('http://www.ncbi.nlm.nih.gov/pubmed/'+i)
	html_paper=r_paper.read()
	mail=re.findall(r' ?([\w\._]+@[\w\.]+)\.</li></ul></div>',html_paper)
	for j in mail:
		list.append(j)
	mail=[]
'''
print list
print len(list)
print '##########################'
'''
#link into the next page
br.open('http://www.ncbi.nlm.nih.gov/pubmed/?term=RNA-seq')
next_page=open('next_page','w')
n=br.follow_link(text_regex=re.compile("Next"))
print n.geturl()
next_page.write("%s" %(n.read()))
next_page.close()
if html==n.read():
	print 'NO!'
else:
	print 'They are different'

'''
soup=BeautifulSoup(html)
print soup.find(id="EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.Page")
#print soup.find(title="Next page of results")
if soup.find(title='next page of results'):
	print 'AAAAA'
	print soup.find(title='next page of results').find('a').get('href')
'''


#write the mail address into files
mail_china=open('mail_china','w')
mail_outofchina=open('mail_outofchina','w')
for each in list:
	if re.search(r'\.edu\.cn$',each):
		mail_china.write(each+'\n')
	else:
		mail_outofchina.write(each+'\n')
mail_china.close()
mail_outofchina.close()

