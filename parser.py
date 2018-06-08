#!/usr/pkg/bin/python

import feedparser
import sys
import codecs
import locale
import time
import re
from subprocess import call, check_output

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://www.prjorgensen.com/feed/'
html_root = '/sdf/arpa/tz/t/tokyogringo/html'
gopher_root = '/sdf/arpa/tz/t/tokyogringo/gopher'

reload(sys)

#
# get data from the feed
#
feed = feedparser.parse(url)

for post in feed.entries:
    year = time.strftime("%Y", post.published_parsed)
    month = time.strftime("%m", post.published_parsed)
    html_dir = html_root + "/" + year + "/" + month
    gopher_dir = gopher_root + "/" + year + "/" + month
    check_output(['mkdir', '-p', html_dir])
    check_output(['mkdir', '-p', gopher_dir])
    dtfn = time.strftime("%d-%H%M", post.published_parsed)
    html_file = html_dir + "/" + dtfn + ".html"
    gopher_file = gopher_dir + "/" + dtfn + ".txt"
    file = open(html_file,"w")
    file.write("<!DOCTYPE html>\n")
    file.write("<html lang=\"en\">\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/><title>" + post.title + "</title>\n")
    file.write("<body>\n<div>")
    for content in post.content:
        file.write("<span class=\'content\'>")
        file.write(content.value)
        file.write("</span>")
    file.write("</br><hr></p><span class=\'footer\'>My original entry is here: <a class=\'link\' href=\'" + post.link + "\'>" + post.title + "</a>. It posted " + post.published + ". </p></span>")
    file.write("<span class=\'category\'>")
    file.write("Filed under: ")
    for tags in post.tags:
        file.write(tags.term + ", ")
    file.write("</span>")
    file.write("</div>\n</body>\n</html>")
    file.close()
    call(["/usr/pkg/bin/tidy", "-m", "-q", "-asxhtml", "-i", "-b", "-omit", "-c", "-utf8", "--show-errors=0", "--show-warnings=0", "--output-xhtml=1", html_file])
    file = open(gopher_file,"w")
    bar = check_output(["/usr/pkg/bin/lynx", "-dump", html_file])
    file.write(bar)
    file.close()

