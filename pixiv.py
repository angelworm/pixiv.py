#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import urlparse
import re
import lxml.html

class Illust:
    def __init__(self, id_, dom):
        
        def ectractAuthor():
            userlink = dom.xpath('//a[@calss="user-link"]')
            return {
                id:   userlink.attrib['href'],
                name: userlink.xpath(".//h1")[0].text,
                img:  userlink.xpath(".//img")[0].attrib['src']
                }

        self.id      = id_
        self.title   = title_
        self.author  = author_
        self.imgURL  = imgURL_
        self.pageURL = pageURL_
        
    def __str__(self):
        return "id: " + str(self.id) + ", img: " + self.imgURL

    def description(self):
        return "id: " + str(self.id) + ", img: " + self.imgURL + ", title: " + u"「" + self.title + u"」 / " + self.author


class Thumbnail:
    """pixiv thumbnails and some information"""
    
    def __init__(self, id_, title_, author_, pageURL_, imgURL_):
        self.id      = id_
        self.title   = title_
        self.author  = author_
        self.imgURL  = imgURL_
        self.pageURL = pageURL_
        
    def __str__(self):
        return "id: " + str(self.id) + ", img: " + self.imgURL

    def description(self):
        return "id: " + str(self.id) + ", img: " + self.imgURL + ", title: " + u"「" + self.title + u"」 / " + self.author

def getPage(url):
    req = urllib2.Request(url)
    req.add_header('Referer', 'http://www.pixiv.net')
    req.add_header('Accept-Language', 'ja')
#    open("test.html", "w").write(urllib2.urlopen(req).read())
    return unicode(urllib2.urlopen(req).read(), "utf-8")

def getIllust(id_):
    """ this function is broken! """
    url = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id="+id_
    root = lxml.html.fromstring(getPage(url)).xpath('//div[@class="front-content"]/*')
    mainT = root[0]
    sideT = root[1]

    authorT = sideT.xpath('//h2')[0]
    title = mainT.xpath('//h1')[0].text
    author_img  = authorT.xpath('//a[1]/img[1]/@src')[0]
    author_url  = authorT.xpath('//a[1]/@href')[0]
    author_name = authorT.xpath('//a[1]/img/@title')[0]

    print author_name

    return [title, author_img, author_url, author_name]

def getLargeImage(id_):
    url = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id="+str(id_)
    root = lxml.html.fromstring(getPage(url)).xpath('//img[@border="0"]')[0]
    return [root.attrib['src']]

def searchTag(word, full=True):    
    def makeImageData(tags):
        a   = tags.xpath(".//a")
        h2  = tags.xpath(".//h1")[0].text
        img = tags.xpath(".//img[1]/@src")[0]
        p   = re.compile('.*/member_illust\.php\?mode=medium&illust_id=(\d+)')

        pageURL= urlparse.urljoin("http://www.pixiv.net/", a[0].attrib['href'])
        id_ = int(p.match(pageURL).group(1))
        title = h2
        author = a[1].text
        imgURL = img
        
        return Thumbnail(id_, title, author, pageURL, imgURL)
    
    #部分一致
    qword = urllib.quote_plus(word.encode('utf-8'))
    if full:
        url = "http://www.pixiv.net/search.php?s_mode=s_tag_full&word="+qword
    else:
        url = "http://www.pixiv.net/search.php?s_mode=s_tag&word="+qword
    dom = lxml.html.fromstring(getPage(url))
    return map(makeImageData, dom.xpath('//li[@class="image-item"]'))

def test():
    return searchTag(u"雀")

def pr(img):
    print img

if __name__ == '__main__':
    print "loading"
    print getLargeImage("22818522")
#map(pr, test())
