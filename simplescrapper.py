from lxml import html
import requests

def wikiSpider():
    """Scrapes the wiki to generate a bad fact"""

    #Get first page info
    url = 'https://simple.wikipedia.org/wiki/Special:Random'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    title = tree.cssselect("h1:first-of-type")[0].text_content().split()

    #summary of wikipedia page
    summary = tree.get_element_by_id("mw-content-text")
    p = summary.cssselect("p:first-of-type")[0]
    body = p.text_content().replace('"', "").split()

    #clearing the body of topic text
    temptitle = title[:]
    tempbody = body[:]
    for tidbit in tempbody[0:len(title) + 2]:
        if temptitle:
            body.remove(tidbit)
            if tidbit in temptitle:
                temptitle.remove(tidbit)

    return title, body

def bad_fact_generator():
    """Generates a bad fact with no original topic"""
    topic = wikiSpider()[0]
    body = wikiSpider()[1]
    fact = ""
    ok = True #Handling unicode characters

    for tidbit in topic + body:
        fact += tidbit + " "

    try:
        fact.decode("ascii")
    except:
        print("Bad utf-8/ASCII formatting, regenerating fact")
        ok = False

    if not ok:
        return bad_fact_generator()
    return fact
