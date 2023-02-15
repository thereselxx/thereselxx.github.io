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
    if title is not None:
        for word_t in title.split():
            if word_t.lower() == keyword.lower():
                return True
    body = get_body(url)
    if body is not None:
        for word_b in body.split():
            if word_b.lower() == keyword.lower():
                return True


def get_forums(url):
    """Returns a list of url of forums

    :param url: Url of the index page
    :type url: str
    :return: A list of url of forums in the same category
    """
    r = requests.get(url)
    url_contents = r.text
    url_soup = BeautifulSoup(url_contents, 'html.parser')
    forums = url_soup.find_all('a', {'class', 'forumtitle'})[1:6]
    del forums[3]
    link_list = []
    for forum in forums:
        link = forum.get('href').split('&')
        link = 'https://www.bcaus.org.au/phpBB3' + link[0][1:]
        link_list.append(link)
    return link_list


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
    posts = url_soup.find_all(class_='icon topic_read') + url_soup.find_all(class_='icon topic_read_hot')
    url_list = []
    for post in posts:
        if post.find(class_='pagination') is not None:
            post_url = 'https://www.bcaus.org.au/phpBB3' + post.find(class_='pagination').find_all('li')[-1].find('a').get('href')[1:]
        else:
            post = post.find(class_='topictitle')
            post_url = 'https://www.bcaus.org.au/phpBB3' + post.get('href')[1:]
        url_list.append(post_url)
    return url_list


def get_next_page(url):
    """Returns url of the next page in forum.

    :param url: Url of the current page
    :type url: str
    :return: Url of the next page
    :rtype: str
    """
    url = url.split('=')
    if len(url) == 2:
        url = '='.join(url)
        url = url + '&start=50'
    else:
        url[-1] = str(int(url[-1]) + 50)
        url = '='.join(url)
    return url


def reach_last_page(url):
    """Returns True if the last page in forum is reached

    :param url: Url of the current page
    :type url: str
    :return: True
    """
    r = requests.get(url)
    url_contents = r.text
    url_soup = BeautifulSoup(url_contents, 'html.parser')
    next_page = url_soup.find(class_='next')
    if next_page is not None:
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
    if url_soup.find(class_='topic-title') is not None:
        return url_soup.find(class_='topic-title').string


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
    if url_soup.find_all(lambda tag: tag.get('class') == ['content']):
        if url_soup.find_all(lambda tag: tag.get('class') == ['content'])[-1] is not None:
            return str(url_soup.find_all(lambda tag: tag.get('class') == ['content'])[-1])


if __name__ == '__main__':

    aus_brca_forums = 'https://www.bcaus.org.au/phpBB3'

    total_posts = 0
    posts_count = 0
    posts_found = []
    contents = []

    for forum in get_forums(aus_brca_forums):
        while reach_last_page(forum) is False:
            for post in get_posts(forum):
                if find_keyword(post, 'exemestane') is True:
                    posts_count += 1
                    posts_found.append(get_title(post))
                    contents.append(get_body(post))
                    print('Post found!')
                    print(get_title(post))
                    print(get_body(post))
                total_posts += 1
                print('Posts searched = ' + str(total_posts))
            if posts_count > 50:
                print('Total posts = ' + str(total_posts))
                print(str(posts_count) + ' posts are found to contain the keywords')
                for title in posts_found:
                    print(title)
                for content in contents:
                    print(contents)
                print('Done')
                break
            forum = get_next_page(forum)

    print('Total posts = ' + str(total_posts))
    print(str(posts_count) + ' posts are found to contain the keywords')
    print(posts_found)
    print(contents)
    print('Done')

