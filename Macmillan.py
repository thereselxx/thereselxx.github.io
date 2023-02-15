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
    posts = url_soup.find_all('h4', {'class', 'post-name'})
    url_list = []
    for post in posts:
        if len(post.get('class')) != 1:
            posts.remove(post)
        else:
            post_url = 'https://community.macmillan.org.uk' + post.find('a').get('href')
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
    url[-1] = str(int(url[-1]) + 1)
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
    next_page = url_soup.find('a', {'class', 'next'})
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
    if url_soup.find('h4', {'class', 'post-name'}) is not None:
        return url_soup.find('h4', {'class', 'post-name'}).string


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
    tags = url_soup.find(lambda tag: tag.get('class') == ['content']).find_all('p')
    body = ''
    for tag in tags:
        if tag.string is not None:
            body = body + tag.string
    return body


if __name__ == '__main__':

    macmillan = 'https://community.macmillan.org.uk/cancer_types/breast-cancer/discussions?pi5752=1'

    total_posts = 0
    posts_count = 0
    posts_found = []
    contents = []

    while reach_last_page(macmillan) is False:
        for post in get_posts(macmillan):
            if find_keyword(post, 'abraxane') is True:
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
            print(posts_found)
            print(contents)
            print('Done')
            break
        macmillan = get_next_page(macmillan)

    print('Total posts = ' + str(total_posts))
    print(str(posts_count) + ' posts are found to contain the keywords')
    print(posts_found)
    print(contents)
    print('Done')


