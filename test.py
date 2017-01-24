import handler, cssselect, requests, lxml
from lxml import html

def function(json):
    #Function does not currently need to use json
    def wikiSpider():
        """Scrapes the wiki to generate a bad fact"""

        #Get first page info
        url = 'https://simple.wikipedia.org/wiki/Special:Random'
        page = requests.get(url)
        tree = html.fromstring(page.content)
        title = tree.cssselect("h1:first-of-type")[0].text_content().split()
        print(title) #Testing

        #summary of wikipedia page
        summary = tree.get_element_by_id("mw-content-text")
        #Clearing infoboxes:
        if summary.find_class("infobox"):
            summary.find_class("infobox")[0].drop_tree()

        p = summary.cssselect("p:first-of-type")[0]
        body = p.text_content().replace('"', "").split()

        #clearing the body of topic text
        try:
            temptitle = tree.cssselect("b:first-of-type")[0].text_content().split()
        except:
            temptitle = title
        tempbody = body[:]
        for tidbit in tempbody[0:len(temptitle) + 2]:
            if temptitle:
                body.remove(tidbit)
                if tidbit in temptitle:
                    temptitle.remove(tidbit)

        #Allowing alexa to say to instead of -
        body = [item if item != "-" else "to" for item in body]

        if len(body) > 35:
            body = body[:35]
            body.append(". Oops! I ran out of memory!")

        return title, body

    #If bad unicode, only body needs to be regenerated
    def regen_body_text():
        body = wikiSpider()[1]
        body_text = "";
        ok = True #Handling Unicode characters
        for tidbit in body:
            body_text += tidbit + " "
        try:
            body_text.decode("ascii")
        except:
            print("Bad utf-8/ASCII formatting, regenerating fact")
            ok = False
        if not ok:
            return regen_body_text()
        return body_text

    def bad_fact_generator():
        """Generates a bad fact with no original topic"""
        topic = wikiSpider()[0]
        body = regen_body_text()
        fact = ""
        #print(body) testing

        for tidbit in topic:
            fact += tidbit + " "
        fact += body
        
        return fact
    return bad_fact_generator()

if __name__ == '__main__':
    handler.invoking(function)
