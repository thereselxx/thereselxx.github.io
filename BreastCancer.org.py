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
    for content in body:
        for word_b in content.text.split():
            if word_b.lower() == keyword.lower():
                return True


def find_keywords(url, keywords):
    """Returns True if all keywords are found within the post.

    :param url: Url of the post to be iterated
    :type url: str
    :param keywords: Words to look for in the post
    :type keywords: str
    :return: True
    """
    if type(keywords) is str:
        multi_keywords = keywords.split()
    else:
        multi_keywords = keywords
    match = []
    if len(multi_keywords) == 0:
        if False in match:
            return False
        else:
            return True
    else:
        first_keyword = find_keyword(url, multi_keywords[0])
        match.append(first_keyword)
        smaller_list = multi_keywords[1:]
        return find_keywords(url, smaller_list)


def get_forums(url):
    """Returns a list of url of forums

    :param url: Url of the index page
    :type url: str
    :return: A list of url of forums in the same category
    """
    r = requests.get(url)
    url_contents = r.text
    url_soup = BeautifulSoup(url_contents, 'html.parser')
    forums = url_soup.find_all('h3')[7:57]
    link_list = []
    for forum in forums:
        link = forum.find('a').get('href')
        link = 'https://community.breastcancer.org' + link
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
    posts = url_soup.find_all(title="View this Topic and its replies")
    url_list = []
    for post in posts:
        post_url = 'https://community.breastcancer.org' + post.get('href')
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
    next_page = url_soup.find('', {'class', 'next_page disabled'})
    if next_page is None:
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
    return url_soup.h1.string[7:]


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
    return url_soup.find('', {'class', "user-post"}).find_all('p')[1:]


if __name__ == '__main__':

    breast_cancer_org = 'https://community.breastcancer.org/'

    # Only 4 categories are used for scraping: 1)Not Diagnosed but Concerned, 2)Tests, Treatments & Side Effects,
    # 3)Connecting With Others Who Have a Similar Diagnosis, 4)Day-to-Day Matters

    total_posts = 0
    posts_count = 0
    posts_found = []
    contents = []

    for forum in get_forums(breast_cancer_org):
        page = forum + '?page=1'
        while reach_last_page(page) is False:
            for post in get_posts(page):
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
                print(posts_found)
                print(contents)
                print('Done')
                break
            page = get_next_page(page)

    print('Total posts = ' + str(total_posts))
    print(str(posts_count) + ' posts are found to contain the keywords')
    print(posts_found)
    print(contents)
    print('Done')

