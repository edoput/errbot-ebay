from urllib.error import URLError
from urllib.request import urlopen
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from errbot import BotPlugin, botcmd, arg_botcmd, webhook

def is_url(urlstring):
    parsed_url = urlparse(urlstring)
    # is a url if there is a scheme and a network location
    return parsed_url[0] and parsed_url[1]

class Ebay(BotPlugin):
    """
    Show Ebay listing information
    """

    @botcmd(split_args_with=None)
    def ebay(self, message, args):
        urls = filter(is_url, args)

        for url in urls:
            try:
                with urlopen(url) as response:
                    page_content = response.read()
                    soup = BeautifulSoup(page_content, 'html.parser')
                    price = soup.find('span', id='prcIsum').string
                    return '[ %s | %s ]' % (soup.title.string, price)
            except URLError:
                return "Oh oh, something bad happened"
