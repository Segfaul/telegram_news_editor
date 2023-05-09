import requests
from lxml import html

from googletrans import Translator
from random import choice

from cfg import user_agents


class NewsParser:

    def __init__(self, main_link: str, proxy: dict = None):
        # main_link is our catalog link, proxy is required however it can be separately set for each function
        # Also we need a translator class_ex to translate all the articles to 'ru' lang
        self.link = main_link
        self.proxy = proxy
        self.translator = Translator()

    @classmethod
    def get_response(cls, link: str, proxy: dict = None) -> requests.Request or int:

        if proxy is None:
            proxy = {}

        try:

            request = requests.get(link, headers={'user-agent': choice(user_agents)}, proxies=proxy)

            if request.status_code != 200:
                print("Unsuccessful request")
                return -1

            return request

        except requests.exceptions.RequestException as error:
            print(error.__class__.__name__, error.args[0])
            return -1

    @classmethod
    def text_main_info(cls, tree: html.HtmlElement) -> str:

        try:
            content: [str] = []
            intro_info: str = \
                tree.xpath('//div[@class="post-content"]/p')[0].text_content().split('. ')[0].strip('.') + '\n'
            content.append(intro_info)

            heading_paragraphs: [str] = tree.xpath('//div[@class="post-content"]/h2/following-sibling::*[1]')

            for paragraph in heading_paragraphs:

                if ':' != paragraph.text_content()[-1]:
                    content.append(
                        paragraph.text_content().split('. ')[0].strip('\n.') + '.'
                    )

            if 'magazine' in tree.xpath('//div[@class="post-content"]/p')[-1].text_content().split('. ')[0].lower():
                outro_info: str = tree.xpath('//div[@class="post-content"]/p')[-2].text_content().split('. ')
            else:
                outro_info: str = tree.xpath('//div[@class="post-content"]/p')[-1].text_content().split('. ')

            if len(outro_info[-1]) == 1:
                if len(outro_info) > 1:
                    content.append(outro_info[-2].strip('\n.') + '.')
            else:
                content.append(outro_info[-1].strip('\n.') + '.')

            return '\n'.join(content)

        except ValueError as error:
            print(error.__class__, error.args[0])
            return ''

        except TypeError as error:
            print(error.__class__, error.args[0])
            return ''

    @property
    def get_news_list(self) -> [str] or int:

        try:

            request = self.get_response(self.link, self.proxy)

            tree = html.fromstring(request.content)

            news_links = [url.attrib['href'] for url in tree.xpath('//*[@id="__layout"]/div/div[1]/main/div/div/div[2]/'
                                                                   'div/ul/li[*]/div/article/a')
                          if "news/" in url.attrib['href']]

            if not news_links:
                raise TypeError("Empty list given while expected [str]")

            return news_links

        except TypeError as error:
            print(error.__class__.__name__, error.args[0])
            return -1

    def get_news_page(self, link: str) -> dict or int:
        # We need a link argument here, because we parse all the sub_pages taking main link from __init__
        try:

            request = self.get_response(self.link + link, self.proxy)

            if request.status_code != 200:
                print("Unsuccessful request")
                return -1

            tree = html.fromstring(request.content)

            news_content = {'title': self.translator.translate(
                                        text=tree.xpath('//*[contains(@id, "article-")]/h1')[0].text.strip(' '),
                                        src='en',
                                        dest='ru').text,
                            # No idea why, but unfortunately xpath form for content doesn't work at all
                            'content': self.translator.translate(
                                        text=self.text_main_info(tree),
                                        src='en',
                                        dest='ru').text
                            }

            if not news_content:
                raise TypeError("Empty dict given while expected {'title': ... , 'content': ... ,}")

            return news_content

        except TypeError as error:
            print(error.__class__.__name__, error.args[0])
            return -1

    def __str__(self):
        return f"Just a news_parser class_ex for {self.link}"
