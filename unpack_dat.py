
import sys

import codecs
from unidecode import unidecode

# To remove html code
import justext
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor

# Options here: bs4, justext, boilerpipe, html

if len(sys.argv) < 2:
    print "USAGE: python unpack_dat.py <PATH_TO_DAT_FILES> <PARSER [boilerpipe, justext, bs4, html]>"
    sys.exit(0)

#ex. python unpack_dat.py ../original_files/part8/ boilerpipe
input_file = open(sys.argv[1], "r")
html_parser = sys.argv[2]

content = ""
for line in input_file:

    if line.startswith("#UID:"):
        uid = line.strip().split("#UID:")[1]
    elif line.startswith("#DATE:"):
        date = line.strip().split("#DATE:")[1]
    elif line.startswith("#URL:"):
        url = line.strip().split("#URL:")[1]
    elif line.strip() == "#EOR":
        print uid, date, url

        content = unidecode(content.decode("utf8"))

        if html_parser == "bs4":
            soup = BeautifulSoup(content, "html.parser")
            tags_to_remove = ["script"]
            for tag in tags_to_remove:
                for x in soup.body(tag):
                    x.decompose()
            text = soup.body.get_text()

        elif html_parser == "justext":
            paragraphs = justext.justext(content, justext.get_stoplist('English'))
            text = "\n"
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate: # and not paragraph.is_header:
                    text = text + paragraph.text + "\n"

        elif html_parser == "boilerpipe":
            extractor = Extractor(extractor='ArticleExtractor', html=content)
            text = extractor.getText()

        elif html_parser == "html":
            text = content

        else:
            print "WRONG HTML PARSER: options are 'bs4', 'justext' or 'boilerpipe'"
            import sys
            sys.exit(0)

        filename = uid
        if html_parser == "bs4":
            filename += ".bs4"
        elif html_parser == "justext":
            filename += ".jus"
        elif html_parser == "boilerpipe":
            filename += ".boi"

        #with codecs.open(filename,'w', encoding='utf8') as f:
        with codecs.open(filename,'w', encoding="utf8") as f:
            f.write(uid + "\n")
            f.write(date + "\n")
            f.write(url + "\n")
            f.write(text)

        content = ""

    else:
        content += line


