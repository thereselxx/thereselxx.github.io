from bs4 import BeautifulSoup
import requests


def find_keyword(url, keyword):
    """Returns True if the keyword is found within the post.

        :param url: Url of the post to be iterated
        :type url: str
        :param keyword: Word to look for in the post
        :type keyword: str
        :return: True
        """
    title = get_title(url)
    body = get_body(url)
    for word_t in title.split():
        if word_t.lower() == keyword.lower():
            return True
    for word_b in body.split():
        if word_b.lower() == keyword.lower():
            return True


def get_posts(url):
    """Returns a list of url of all the posts in a single page in forum.

        :param url: Url of the page to be iterated
        :type url: str
        :return: A list of url of a single post in the page
        :rtype: list
        """
    r = requests.get(url)
    url_contents = r.text
    url_soup = BeautifulSoup(url_contents, 'html.parser')
    posts = url_soup.find_all(class_='alt1')
    url_list = []
    for post in posts:
        if post.find('div') is not None:
            if post.find('div').find('a') is not None:
                post_url = post.div.a.get('href')
                if 'cancer-breast' in post_url:
                    url_list.append(post_url)
    del url_list[-1]
    return url_list


def get_next_page(url):
    """Returns url of the next page in forum.

    :param url: Url of the current page
    :type url: str
    :return: Url of the next page
    :rtype: str
    """
    r = requests.get(url)
    url_contents = r.text
    url_soup = BeautifulSoup(url_contents, 'html.parser')
    return url_soup.find(rel='next').get('href')


def reach_last_page(url):
    """Returns True if the last page in forum is reached

    :param url: Url of the current page
    :type url: str
    :return: True
    """
    r = requests.get(url)
    url_contents = r.text
    url_soup = BeautifulSoup(url_contents, 'html.parser')
    if url_soup.find(rel='next') is not None:
        return False


def get_title(url):
    """Returns title of a post

    :param url: Url of the post
    :type url: str
    :return: Title of the post
    :rtype: str
    """
    r = requests.get(url)
    url_contents = r.text
    url_soup = BeautifulSoup(url_contents, 'html.parser')
    tags = url_soup.find_all(style='display: inline-block;')
    for tag in tags:
        if tag.find('strong') is not None:
            return tag.find('strong').string


def get_body(url):
    """Returns body content of a post

        :param url: Url of the post
        :type url: str
        :return: Body content of the post
        :rtype: str
        """
    r = requests.get(url)
    url_contents = r.text
    url_soup = BeautifulSoup(url_contents, 'html.parser')
    return str(url_soup.find(class_='alt1'))


if __name__ == '__main__':

    health_boards = 'https://www.healthboards.com/boards/cancer-breast/index1.html'

    total_posts = 0
    posts_count = 0
    posts_found = []
    contents = []

    while reach_last_page(health_boards) is False:
        for post in get_posts(health_boards):
            if find_keyword(post, 'abraxane') is True:
                posts_count += 1
                posts_found.append(get_title(post))
                contents.append(get_body(post))
                print('Post found!')
                print(get_title(post))
                print(get_body(post))
            total_posts += 1
            print('Posts searched = ' + str(total_posts))
        if posts_count > 100:
            print('Total posts = ' + str(total_posts))
            print(str(posts_count) + ' posts are found to contain the keywords')
            print(posts_found)
            print(contents)
            print('Done')
            break
        health_boards = get_next_page(health_boards)

    print('Total posts = ' + str(total_posts))
    print(str(posts_count) + ' posts are found to contain the keywords')
    print(posts_found)
    print(contents)
    print('Done')


