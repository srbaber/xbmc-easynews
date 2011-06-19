#!/usr/bin/python
#Code Heavily modified from  Demo by TV DASH - by You 2008.
#
# Written by Ksosez with help from anarchintosh
# Released under GPL(v2)

import urllib,urllib2,htmllib
import re,string
import os,sys
import xbmcplugin,xbmcaddon,xbmcgui,xbmc

import utils
import gethtml
import megavideo
#import img_merge


#pluginurl string (added in addDir etc)
__type__ = sys.argv[0]+'?type=video'
 
pluginhandle = int(sys.argv[1])

# 3rd Party video Sites that are currently supported are listed below

SUPPORTEDSITES = ["xvideos", "pornhub", "xhamster","empflix", "deviantclip", "tnaflix", "redtube", "you_porn", "megarotic"]


def get_html(url):
     return gethtml.get(url,utils.__datapath__)

                
def CATEGORIES():
        # didn't need to pass search a url. so i was lazy and passed it the utils.__mainurl__ as a dummy
	addDir('Search',utils.__mainurl__,5)
	
        if utils.__login__:
            addDir(utils.__uc__+"'s Videos",utils.__mainurl__+'user/'+utils.__lc__+'/videos/save_date',1,utils.__avatar__)           
            addDir(utils.__uc__+"'s Collections",utils.__mainurl__+'user/'+utils.__lc__+'/collections',2,utils.__avatar__)
            addDir(utils.__uc__+"'s Favourited Collections",utils.__mainurl__+'user/'+utils.__lc__+'/collections/favorited',2,utils.__avatar__)
            addDir(utils.__uc__+"'s Rated Collections",utils.__mainurl__+'user/'+utils.__lc__+'/collections/rated',2,utils.__avatar__)
             
	mode = 1
	addDir('Popular Today',utils.__mainurl__+'videos/popular/today/',mode)
	addDir('Popular Last 7 Days',utils.__mainurl__+'videos/popular/7days/',mode)
	addDir('Popular Last Month',utils.__mainurl__+'videos/popular/31days/',mode)
	addDir('Popular All Time',utils.__mainurl__+'videos/popular/all_time/',mode)
	addDir('Upcoming',utils.__mainurl__+'videos/upcoming/',mode)

	mode = 2
	addDir('Collections Popular Today',utils.__mainurl__+'videos/collections/popular/today/',mode)
	addDir('Collections Popular Last 7 Days',utils.__mainurl__+'videos/collections/popular/7days/',mode)
	addDir('Collections Popular Last Month',utils.__mainurl__+'videos/collections/popular/31days/',mode)
	addDir('Collections Popular All Time',utils.__mainurl__+'videos/collections/popular/all_time/',mode)
	
	xbmcplugin.endOfDirectory(pluginhandle)

def SEARCH(url):
     # define the keyboard
     kb = xbmc.Keyboard('', 'Search Fantasti.cc Videos', False)

     # call the keyboard
     kb.doModal()

     # if user presses enter
     if (kb.isConfirmed()):

          # get text from keyboard
          search = kb.getText()

          # if the search text is not nothing
          if search is not '':

                  # encode the search phrase to put in url (ie replace ' ' with '+' etc)
                  # normally you would use: search = urllib.quoteplus(search)
                  # but fantasti's search urls are a bit weird
                  search = re.sub('  ','+',search) # this one is just in case the user accidently enters two spaces
                  search = re.sub(' ','+',search)

                  # create the search url
                  search_url = utils.__mainurl__ + 'search/' + search + '/videos/'
                  print 'SEARCH:',search_url
                  
                  # get the source code of first page
                  first_page = get_html(search_url)

                  # do a search to see if no results found
                  no_results_found = re.search('did not match any content.',first_page)

                  # if there are results on page...
                  if no_results_found: print 'no search results found'
                        
                  # if there are results on page...
                  if not no_results_found:
                        
                          # scrape to get the number of all the results pages (this is listed on the first page)
                          match = re.compile('/videos/page_(.+?)\"\>').findall(first_page)
                          print 'Number of pages:',match

                          # if there weren't any multiple pages of search results
                          if not match:
                                  # ...directly call the results scraper for the first page to add the directories.
                                  SEARCH_RESULTS(url=False,html=first_page)

                          # if there were any multiple pages of search results
                          if match:

                                  # convert the list of strings produced by re.compile to a list of integers, so we can use them for calculations
                                  match = [int(result) for result in match]
                          
                                  # get the highest results page number, to get the total number of results pages.
                                  # this gets the highest integer in the list of integers
                                  total_pages = max(match)

                                  # generate a list of numbers 1 to total_pages (eg if total_pages is 3 generate: 1,2,3)
                                  num = 1
                                  numlist = list('1')
                                  while num < total_pages:
                                      num = num+1
                                      numlist.append(str(num))
        
                                  # for every number in the list
                                  for thenumber in numlist:

                                          # transform thenumber from an integer to a string, to use in name and url strings
                                          thenumber = str(thenumber)
                                  
                                          # make the page name
                                          name = 'Page      --      ' + thenumber

                                          # make the page url
                                          url = search_url + 'page_' + thenumber

                                          # add the results page as a directory
                                          addDir(name,url,6)



def SEARCH_RESULTS(url,html=False):
        # this function scrapes the search results pages
        # accepts page source code (html) for any searches where there is only one page of results
       
	if html is False: html = get_html(url)
	match=re.compile('<a href="(.+?)" onclick="document.cookie = \'ii=1;path=/\';"  class="xxx" target="_blank"><img alt="(.+?)"   src="(.+?)"').findall(html)
	for gurl,name,thumbnail in match:
			for each in SUPPORTEDSITES:
				if each in gurl:
					realurl = "http://fantasti.cc%s" % gurl
					mode = 4
					addLink(name,realurl, mode, thumbnail)
				else: pass
       

   
def INDEX(url):
                print 'ARRGGH',url
		html = get_html(url)
		if "collection" in url: # Collections
                        match=re.compile('<a href=(.+?)" title="(.+?)">\s*<img src="(.+?)" border="0" alt="(.+?)"  width="100" height="100" class="collection_image" />').findall(html)
			for gurl,name,thumbnail,junk in match:
				id = string.split(gurl, "=")[2][:-5]
				realurl = "http://fantasti.cc/video.php?id=%s" % id
				mode = 4
				print realurl
				addLink(name,realurl, mode, thumbnail)
			html = get_html(url)
#			match = re.compile('container_[0-9]*').findall(html)
			match = re.compile('\(\'(.+?)\', ([0-9]*),\'(.+?)\', \'(.+?)\'\);return false;" href="#">next').findall(html)
			if len(match) >= 1:
				fixedNext = None
				for next in match:
					print next
					mode = 1
					page = next[0][-1]
					id = next[1]
					#id = string.split(next, '_')[1]
					fixedNext = "http://fantasti.cc/ajax/pager.php?page=%s&pid=%s&div=collection_%s&uid=14657" % (page, id, id)
					print fixedNext
				addDir('Next Page',fixedNext,mode )
			xbmcplugin.endOfDirectory(pluginhandle)
			 

		else:  
                       match=re.compile('<a href="(.+?)" >                 <img src="(.+?)" alt="(.+?)" border="0" >').findall(html)
		       for gurl,thumbnail,name in match:
				for each in SUPPORTEDSITES:
					if each in gurl:
						realurl = "http://fantasti.cc%s" % gurl
						mode = 4
						addLink(name,realurl, mode, thumbnail)
					else:
						pass
                       html = get_html(url)
                       match = re.compile('<a href="(.+?)">next &gt;&gt;</a></span></div>').findall(html)
		       for next in match:
				mode = 1
				next = string.split(next, '"')[-1]
				fixedNext = "http://fantasti.cc%s" % next
				addDir('Next Page',fixedNext,mode )
		       xbmcplugin.endOfDirectory(pluginhandle)


			
			
			

def INDEXCOLLECT(url):   # Index Collections Pages
	print "URL Loading: %s" % url
 	html = get_html(url)
	match = re.compile('<div style="font-size:24px; line-height:30px; "><a href="(.+?)">(.+?)</a>(.+?)<span id="chunk.+?\>(.+?)</div>',re.DOTALL).findall(html)
	for gurl,name,chtml,description in match:
		realurl = "http://fantasti.cc%s" % gurl
		name = unescape(name)
		mode = 1

                #scrape number of vids
                num_of_vids = (re.compile('line-height:100\%;">(.+?) videos<br>',re.DOTALL).findall(chtml))[0]
                #trim whitespace from beginning of string
                num_of_vids = re.sub('^[ \t\r\n]+','',num_of_vids)
                
                # do some cool stuff to get the images and join them.
                icons = re.compile('<img src="(.+?)"').findall(chtml)

                addDir(name+' *'+num_of_vids+' vids*',realurl, mode,icons[0])

                        
	match = re.compile('<a href="(.+?)">next &gt;&gt;</a></span></div>').findall(html)
	for next in match:
		print "Next: %s" % next
		mode = 2 
		next = string.split(next, '"')[-1]
		fixedNext = "http://fantasti.cc%s" % next
		print "FixedNext: %s" % fixedNext
		addDir('Next Page',fixedNext, mode )
		
	xbmcplugin.endOfDirectory(pluginhandle)  
		

def PLAY(url):
	print "Play URL:%s" % url
	if "id=" in url: realurl = GET_LINK(url, 1)
	else: realurl = GET_LINK(url, 0)
	print "Real url:%s" % realurl
	item = xbmcgui.ListItem(path=realurl)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
		
	
def GET_LINK(url,collections):    # Get the real video link and feed it into XBMC
	print "GET_LINK URL: %s" % url
	html = get_html(url)
	if collections == 1:   # Make sure we get a url we can parse
		match = re.compile('<link rel="canonical" href="(.+?)" />').findall(html)
		for each in match: url = each

	if "xvideos" in url:
			match = re.compile('<param name="flashvars" value="(.+?)" />').findall(html)
			for id in match:
				getit = string.split(id, "=")[1]
			urlget2="http://www.xvideos.com/video%s" % getit
			html = get_html(urlget2)
			match = re.compile('allowscriptaccess="always" flashvars="(.+?)"').findall(html)
			for text in match:
				match2 = re.compile('flv_url=(.+?)&amp').findall(html)
				for each in match2:
					fetchurl=urllib.unquote(each)
					print "fetchurl: %s" % fetchurl
			return fetchurl
	elif "pornhub" in url:
			match = re.compile(
				'<param name="FlashVars" value="(.+?)"/>'
			 ).findall(html)
			for gurl in match:
					urlget2 = "http://www.pornhub.com/embed_player.php?id=" + string.split(gurl, "=")[2]
			html = get_html(urlget2)
			match = re.compile(
				'<video_url>(.+?)</video_url>'
				).findall(html)
			for each in match:
				fetchurl=urllib.unquote(each)
				print "fetchurl: %s" % fetchurl
			return fetchurl
	elif "empflix" in url:
			match = re.compile('<a style="color:#BBB;" href="(.+?)" target="_blank" rel="nofollow">empflix</a></span>').findall(html)
			for gurl in match:
					urlget2 = gurl
			html = get_html(urlget2)
			match = re.compile('<a href="(.+?)" class="downloadButton">Download FLV</a>').findall(html)
			for each in match:
				fetchurl=urllib.unquote(each)
				print "fetchurl: %s" % fetchurl
			return fetchurl
	elif "tnaflix" in url:
			match = re.compile('<param name="FlashVars" value="(.+?)"/>').findall(html)
			for gurl in match:
				print "gurl %s" % gurl
				purl = string.split(gurl, "?")[1]
				print purl
				urlget2 = "http://www.tnaflix.com/embedding_player/embedding_feed.php?viewkey=" + purl
				print urlget2
			html = get_html(urlget2)
			match = re.compile('<file>(.+?)</file>').findall(html)
			for each in match:
				fetchurl=each
				print "fetchurl: %s" % fetchurl
			return fetchurl
	elif "xhamster" in url:
			match = re.compile('<iframe class="ui-layout-center" src="(.+?)"').findall(html)
			for gurl in match:
				urlget2 = gurl
			html = get_html(urlget2)
			match = re.compile("'file': '(.+?)'").findall(html)
		 	for each in match:
				fetchurl = "http://xhamster.com/flv2/" + urllib.quote(each)
				print "fetchurl: %s" % fetchurl
			return fetchurl
	elif "deviantclip" in url:
			match = re.compile('<a style="color:#BBB;" href="(.+?)" target="_blank" rel="nofollow">deviantclip</a>').findall(html)
			for gurl in match:
				urlget2 = gurl
			html = get_html(urlget2)
			match = re.compile('"file":"(.+?)"').findall(html)
			for each in match:
				fetchurl = urllib.unquote(each)
			return fetchurl
	elif "redtube" in url:
			match = re.compile('<param name="FlashVars" value="(.+?)">').findall(html)
			for gurl in match:
				id = string.split(string.split(gurl, "&")[0], "=")[1]
				urlget2 = "http://www.redtube.com/%s" % id
			html = get_html(urlget2)
			match = re.compile('"flashvars","(.+?)"').findall(html)
			for each in match:
				fetchurl = string.split(string.split(each, "&")[8], "=")[1]
				fetchurl = urllib.unquote(fetch)
			return fetchurl
	elif "you_porn" in url:
			match = re.compile('<a id="side_sitelink" href="(.+?)" target="_blank" rel="nofollow" title="you_porn">you_porn</a></span>').findall(html)
			for gurl in match:
				urlget2 = gurl
			html = get_html(urlget2)
			match = re.compile("so.addVariable('file', encodeURIComponent('(.+?)'));").findall(html)
			for each in match:
				urlget3 = each
			html = get_html(urlget3)
			match = re.compile('<location>(.+?)</location>').findall(html)
			for each in match:
				fetchurl = urllib.unquote(each)
			return fetchurl
	elif "megarotic":
			match = re.compile('<param name="movie" value="(.+?)">').findall(html)
			for gurl in match:
				urlget2 = gurl

			videoid = string.split(urlget2, "/v/")[1]
			videoid = videoid[0:8]
			print 'MEGAROTIC VIDEOID: '+videoid
			fetchurl = (megavideo.resolveURL('porn', None, videoid))[0]
			print "Megaporn/Megarotic Fetchurl:%s" % fetchurl
			return fetchurl

	else:
		pass


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addLink(name,url,mode,iconimage=None):
        if iconimage == None or iconimage == '': iconimage = utils.__defaultimage__
	u=__type__+"&url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage=None):
        if iconimage == None or iconimage == '': iconimage = utils.__defaultimage__
        u=__type__+"&url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
     
def unescape(s):
	p = htmllib.HTMLParser(None)
	p.save_bgn()
	p.feed(s)
	return p.save_end()              

params=get_params()
url=None
name=None
mode=None
cookie=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
    print "Generate Main Menu"
    CATEGORIES()

elif mode == 1:
   print "Indexing Videos"
   INDEX(url)

elif mode == 2:
	print "Indexing Collections"
	INDEXCOLLECT(url)

elif mode == 4:
    print "Play Video"
    PLAY(url)

elif mode == 5:
    print "Category: Search"
    SEARCH(url)

elif mode == 6:
    print "Category: SEARCH_RESULTS"
    SEARCH_RESULTS(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))