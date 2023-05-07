from parse_news import NewsParser


def main() -> None:
    # Int type given if request was unsuccessful or Value/Type errors occurred

    base_link: str = "https://cointelegraph.com/"

    news_parser = NewsParser(base_link)

    links: list or int = news_parser.get_news_list()

    content: dict or int = news_parser.get_news_page(links[0])

    print(content)


if __name__ == '__main__':
    main()
