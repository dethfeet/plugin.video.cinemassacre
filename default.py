import xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import re

thisPlugin = int(sys.argv[1])
baseLink = "http://cinemassacre.com/"

_regex_extractMenu = re.compile("<ul id=\"navlist\">(.*?)<ul id=\"navpages\">", re.DOTALL);

_regex_extractMenuItem = re.compile("<li class=\"cat-item cat-item-[0-9]{1,4}\"><a href=\"(http://cinemassacre.com/category/[a-z0-9\-]*/)\" title=\"(.*?)\">(.*?)</a>", re.DOTALL);
_regex_extractMenuItemSub = re.compile("<li class=\"cat-item cat-item-[0-9]{1,4}\"><a href=\"(http://cinemassacre.com/category/[a-z0-9\-]*/[a-z0-9\-]*/)\" title=\"(.*?)\">(.*?)</a>", re.DOTALL);
_regex_extractMenuItemSubSub = re.compile("<li class=\"cat-item cat-item-[0-9]{1,4}\"><a href=\"(http://cinemassacre.com/category/[a-z0-9\-]*/[a-z0-9\-]*/[a-z0-9\-]*/)\" title=\"(.*?)\">(.*?)</a>", re.DOTALL);

_regex_extractShow = re.compile("<!-- content -->(.*?)<!-- /content -->", re.DOTALL)
_regex_extractRecent = re.compile("<!-- videos -->(.*?)<!-- /videos -->", re.DOTALL);

_regex_extractEpisode = re.compile("<!-- video -->(.*?)<!-- /video -->", re.DOTALL)
_regex_extractEpisodeLink = re.compile("<h3><a href=\"(.*?)\">(.*?)</a></h3>", re.DOTALL)
_regex_extractEpisodeImg = re.compile("<img src=\"(.*?)\" alt=\"(.*?)\" />", re.DOTALL)
_regex_extractEpisodeImg2 = re.compile("<img width=\"[0-9]*\" height=\"[0-9]*\" src=\"(.*?)\" class=\".*?\" alt=\"(.*?)\" title=\".*?\" />", re.DOTALL)

#Bip.tv
#_regex_extractVideoBip = re.compile("<!-- video -->.*?<iframe src=\"(.*?)\".*?allowfullscreen>.*?<!-- /video -->",re.DOTALL);
_regex_extractVideoBip = re.compile("<!-- video -->.*?(http://blip.tv/play/.*?)\".*?<!-- /video -->", re.DOTALL);
_regex_extractVideoFeedURL = re.compile("&file=(.*?)&", re.DOTALL);
_regex_extractVideoFeedURL2 = re.compile("&file=(.*)", re.DOTALL);

#_regex_extractFilesFromFeed = re.compile("<media:group>.*?<media:content url=\"(.*?)\".*?type=\"video/quicktime\".*?<media:content url=\"(.*?)\".*?type=\"video/x-m4v\".*?<media:content url=\"(.*?)\".*?type=\"video/x-flv\"",re.DOTALL);
_regex_extractFilesFromFeedMov = re.compile("<media:content url=\"(.*?)\".*?type=\"video/quicktime\".*?");
_regex_extractFilesFromFeedMp4 = re.compile("<media:content url=\"(.*?)\".*?type=\"video/mp4\".*?");
_regex_extractFilesFromFeedM4v = re.compile("<media:content url=\"(.*?)\".*?type=\"video/x-m4v\".*?");
_regex_extractFilesFromFeedFlv = re.compile("<media:content url=\"(.*?)\".*?type=\"video/x-flv\".*?");

#Youtube
_regex_extractVideoYoutube = re.compile("<!-- content -->.*?<!-- video -->.*?(http://www\.youtube\.com/.*?/.*?)[\?|\"].*?<!-- /video -->.*?<!-- /content -->", re.DOTALL);

_regex_extractVideoYoutubeId = re.compile("http://www.youtube.com/[embed|v]/(.*)")
_regex_extractVideoYoutubeExtractFmtStreamMap = re.compile("url_encoded_fmt_stream_map=(.*itag%3D[0-9]{1,2})&")
_regex_extractVideoInfo = re.compile("(.*?)&.*&type=(.*?)&itag=([0-9]{1,2})")

#Gametrailers
_regex_extractVideoGametrailers = re.compile("<a href=\"(http://www.gametrailers.com/video/angry-video-screwattack/(.*))\" target=\"_blank\">")
_regex_extractVideoGametrailersXML = re.compile("<media:content type=\"text/xml\" medium=\"video\" isDefault=\"true\" duration=\"[0-9]{1,4}\" url=\"(.*?)\"/>")
_regex_extractVideoGametrailersStreamURL = re.compile("<src>(.*?)</src>")

#Springboard
#_regex_extractVideoSpringboard = re.compile("<!-- features -->.*?<!-- video -->.*?http://cinemassacre.springboardplatform.com/mediaplayer/springboard/video/(.*?)/(.*?)/(.*?)/.*?<!-- /video -->.*?<!-- /features -->",re.DOTALL);
#_regex_extractVideoSpringboard = re.compile("(<!-- features -->|<!-- content -->).*?<!-- video -->.*?http://cinemassacre.springboardplatform.com/mediaplayer/springboard/video/(.*?)/(.*?)/(.*?)/.*?<!-- /video -->.*?(<!-- /features -->|<!-- /content -->)",re.DOTALL);
_regex_extractVideoSpringboard = re.compile("<!-- (video|content) -->.*?http://(cinemassacre\.springboardplatform\.com|www\.springboardplatform\.com)/mediaplayer/springboard/video/(.*?)/(.*?)/(.*?)/.*?<!-- /(video|content) -->", re.DOTALL);
_regex_extractVideoSpringboardStream = re.compile("<media:content duration=\"[0-9]*?\" medium=\"video\" bitrate=\"[0-9]*?\" fileSize=\"[0-9]*?\" url=\"(.*?)\" type=\".*?\" />");

#Spike.com
_regex_extractVideoSpike = re.compile("<!-- video -->.*?<a href=\"(http://www.spike.com/.*?)\" target=\"_blank\">\".*?<!-- /video -->", re.DOTALL);
#www.bigprox.com http://udat.mtvnservices.com/service1/dispatch.htm?feed=mediagen_arc_feed&account=spike.com&mgid=mgid:arc:content:spike.com:3b691aaf-2216-4fd0-925f-92941a922ddc&site=spike.com&segment=0&mgidOfMrssFeed=mgid:arc:content:spike.com:48f1a226-c6fe-4e99-bccc-10c6af79ff89
#rtmpe
#http://cinemassacre.com/2012/01/19/top-10-horror-remakes/
#http://www.spike.com/video-clips/6j4bsa/cinemassacre-cinemassacre-top-10-horror-remakes
#http://media.mtvnservices.com/pmt/e1/players/mgid:arc:video:spike.com:/config.xml?uri=mgid:arc:video:spike.com:028dac50-33c5-4127-bbe3-688735db95ad&type=network&ref=www.spike.com&geo=DE&group=entertainment&nid=82125&site=spike.com

def mainPage():
    global thisPlugin

    addDirectoryItem("Recent videos", {"action" : "recent", "link": ""})  
    subMenu(level1=0, level2=0)

def subMenu(level1=0, level2=0):
    global thisPlugin
    page = load_page(baseLink)
    mainMenu = extractMenu(page)
    
    if level1 == 0:
        menu = mainMenu
    elif level2 == 0:
        menu = mainMenu[int(level1)]['children']
    else:
        menu = mainMenu[int(level1)]['children'][int(level2)]['children']
    
    counter = 0
    for menuItem in menu:
        menu_name = remove_html_special_chars(menuItem['name']);
        
        menu_link = menuItem['link'];
        if len(menuItem['children']) and level1 == 0:
            addDirectoryItem(menu_name, {"action" : "submenu", "link": counter})  
        elif len(menuItem['children']):
            addDirectoryItem(menu_name, {"action" : "subsubmenu", "link": level1 + ";" + str(counter)})  
        else:        
            addDirectoryItem(menu_name, {"action" : "show", "link": menu_link})
        counter = counter + 1
    xbmcplugin.endOfDirectory(thisPlugin)

def recentPage():
    global thisPlugin
    page = load_page(baseLink)
    show = _regex_extractRecent.search(page)    
    extractEpisodes(show)
    
def extractMenu(page):
    menu = _regex_extractMenu.search(page).group(1);
    menuList = []
    
    parent = -1;
    for line in menu.split("\n"):
        menuItem = _regex_extractMenuItem.search(line)
        if menuItem is not None:
            parent = parent + 1
            parent2 = -1
            menuList.append({"name" : menuItem.group(3), "link" : menuItem.group(1), "children" : []})
        else:
            menuItemSub = _regex_extractMenuItemSub.search(line)
            if menuItemSub is not None:
                parent2 = parent2 + 1
                menuList[parent]['children'].append({"name" : menuItemSub.group(3), "link" : menuItemSub.group(1), "children" : []});
            else:
                menuItemSubSub = _regex_extractMenuItemSubSub.search(line)
                if menuItemSubSub is not None:
                    menuList[parent]['children'][parent2]['children'].append({"name" : menuItemSubSub.group(3), "link" : menuItemSubSub.group(1), "children" : []});
    return menuList
    
def showPage(link):
    global thisPlugin
    page = load_page(urllib.unquote(link))
    show = _regex_extractShow.search(page)
    extractEpisodes(show)

def extractEpisodes(show):
    episodes = list(_regex_extractEpisode.finditer(show.group(1)))
    for episode in episodes:
        episode_html = episode.group(1)
        episod_title = _regex_extractEpisodeLink.search(episode_html).group(2)
        episod_title = remove_html_special_chars(episod_title)
        episode_link = _regex_extractEpisodeLink.search(episode_html).group(1)
        episode_img = _regex_extractEpisodeImg.search(episode_html)
        if episode_img is None:
            episode_img = _regex_extractEpisodeImg2.search(episode_html)
        episode_img = episode_img.group(1)
        addDirectoryItem(episod_title, {"action" : "episode", "link": episode_link}, episode_img)
    xbmcplugin.endOfDirectory(thisPlugin)

def showEpisodeBip(videoItem):
    url = videoItem.group(1)
    
    #GET the 301 redirect URL
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    fullURL = response.geturl()
    feedURL = _regex_extractVideoFeedURL.search(fullURL)
    if feedURL is None:
        feedURL = _regex_extractVideoFeedURL2.search(fullURL)
    feedURL = urllib.unquote(feedURL.group(1))

    feed = load_page(feedURL)
    feedGroupMov = _regex_extractFilesFromFeedMov.search(feed);
    feedGroupMp4 = _regex_extractFilesFromFeedMp4.search(feed);
    feedGroupM4v = _regex_extractFilesFromFeedM4v.search(feed);
    feedGroupFlv = _regex_extractFilesFromFeedFlv.search(feed);
    
    playVideo = None
    if feedGroupMov is not None:
        videoMov = feedGroupMov.group(1);
        playVideo = videoMov
    if feedGroupMp4 is not None:
        videoMp4 = feedGroupMp4.group(1);
        if playVideo is None:
            playVideo = videoMp4            
    if feedGroupM4v is not None:
        videoM4v = feedGroupM4v.group(1);
        playVideo = videoM4v
    if feedGroupFlv is not None:
        videoFlv = feedGroupFlv.group(1);
        if playVideo is None:
            playVideo = videoFlv
    
    item = xbmcgui.ListItem(playVideo)
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(playVideo, item)

def showEpisodeYoutube(videoItem):
    url = videoItem.group(1)
            
    youtubeID = _regex_extractVideoYoutubeId.search(url).group(1)
    url = "http://www.youtube.com/get_video_info?video_id=" + youtubeID
    get_info = load_page(url)
    
    fmt_stream_url = _regex_extractVideoYoutubeExtractFmtStreamMap.search(get_info).group(1)
    fmt_stream_url = urllib.unquote(fmt_stream_url)
    fmt_stream_urls = fmt_stream_url.split(',')
    
    for stream_url in fmt_stream_urls:
        stream_url = urllib.unquote(stream_url)[4:]
        stream_url = urllib.unquote(stream_url)

        video_info = _regex_extractVideoInfo.search(stream_url)
        video_url = video_info.group(1)
        video_type = video_info.group(2)
        video_itag = video_info.group(3)
        
        str_end = stream_url.find("quality=")
        stream_url = stream_url[:str_end]
        
        if video_itag == "43":    
            item = xbmcgui.ListItem(stream_url)
            xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(stream_url, item)

def showEpisodeGametrailers(videoItem):
    url = videoItem.group(1)
    videoId = videoItem.group(2)
    urlXml = "http://www.gametrailers.com/neo/?page=xml.mediaplayer.Mrss&mgid=mgid%3Amoses%3Avideo%3Agametrailers.com%3A" + videoId + "&keyvalues={keyvalues}"
    xml1 = load_page(urlXml)
    urlXml = _regex_extractVideoGametrailersXML.search(xml1).group(1)
    urlXml = urlXml.replace("&amp;", "&")
    xml2 = load_page(urlXml)
    stream_url = _regex_extractVideoGametrailersStreamURL.search(xml2).group(1)
    item = xbmcgui.ListItem(stream_url)
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(stream_url, item)

def showEpisodeSpringboard(videoItem):
    siteId = videoItem.group(4)
    contentId = videoItem.group(5)
    feedUrl = "http://cms.springboard.gorillanation.com/xml_feeds_advanced/index/" + siteId + "/rss3/" + contentId + "/"
    feed = load_page(feedUrl)
    feedItem = _regex_extractVideoSpringboardStream.search(feed);
    stream_url = feedItem.group(1)
    item = xbmcgui.ListItem(stream_url)
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(stream_url, item)

def showEpisode(link):
    link = urllib.unquote(link)
    page = load_page(link)
    
    videoItem = _regex_extractVideoBip.search(page)
    
    if videoItem is not None:
        showEpisodeBip(videoItem)
    else:
        videoItem = _regex_extractVideoYoutube.search(page)
        if videoItem is not None: #Youtube
            showEpisodeYoutube(videoItem)
        else:
            videoItem = _regex_extractVideoGametrailers.search(page)
            if videoItem is not None: #Gametrailers.com
                showEpisodeGametrailers(videoItem)
            else:
                videoItem = _regex_extractVideoSpringboard.search(page)
                if videoItem is not None: #Springboard
                    showEpisodeSpringboard(videoItem)
                else:
                    #stream_url = "http://udat.mtvnservices.com/service1/dispatch.htm?feed=mediagen_arc_feed&account=spike.com&mgid=mgid:arc:content:spike.com:3b691aaf-2216-4fd0-925f-92941a922ddc&site=spike.com&segment=0&mgidOfMrssFeed=mgid:arc:content:spike.com:48f1a226-c6fe-4e99-bccc-10c6af79ff89"
                    #stream_url = "rtmpe://cp22372.edgefcs.net/ondemand/mtvnorigin/gsp.spikecomstor/contentstore/media/3/1/8/6/4/3186465_700.flv"
                    #stream_url = "rtmpe://cp22372.edgefcs.net/ondemand/mtvnorigin/gsp.spikecomstor/contentstore/media/3/1/8/6/4/3186465_300.flv"
                    #item = xbmcgui.ListItem(stream_url)
                    #xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(stream_url, item)
                    pass

def load_page(url):
    print url
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link

def addDirectoryItem(name, parameters={}, pic=""):
    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

def remove_html_special_chars(inputStr):
    inputStr = inputStr.replace("&#8211;", "-")
    inputStr = inputStr.replace("&#8217;", "'")#\x92
    inputStr = inputStr.replace("&#039;", chr(39))# '
    inputStr = inputStr.replace("&#038;", chr(38))# &
    return inputStr
    
def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    
    return param
    
if not sys.argv[2]:
    mainPage()
else:
    params = get_params()
    if params['action'] == "show":
        showPage(params['link'])
    elif params['action'] == "submenu":
        subMenu(params['link'])
    elif params['action'] == "subsubmenu":
        levels = urllib.unquote(params['link']).split(";")
        subMenu(levels[0], levels[1])
    elif params['action'] == "recent":
        recentPage()
    elif params['action'] == "episode":
        print "Episode"
        showEpisode(params['link'])
    else:
        mainPage()
