from bs4 import BeautifulSoup
import requests


class Community(object):
    def __init__(self, url):
        self.url = url

    @classmethod
    def get_soup(cls, url):
        r = requests.get(url)
        url_contents = r.text
        url_soup = BeautifulSoup(url_contents, 'html.parser')
        return url_soup

    @classmethod
    def find_keyword(cls, url, keyword):
        """Returns True if the keyword is found within the post.

            :param url: Url of the post to be iterated
            :type url: str
            :param keyword: Word to look for in the post
            :type keyword: str
            :return: True
            """
        title = Community.get_title(url)
        body = Community.get_body(url)
        for word_t in title.split():
            if word_t.lower() == keyword.lower():
                return True
        for word_b in body.split():
            if word_b.lower() == keyword.lower():
                return True

    @classmethod
    def find_keywords(cls, url, keywords):
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
            first_keyword = Community.find_keyword(url, multi_keywords[0])
            match.append(first_keyword)
            smaller_list = multi_keywords[1:]
            return Community.find_keywords(url, smaller_list)

    @classmethod
    def get_posts(cls, url):
        """Returns a list of url of all the posts in a single page in forum.

        :return: A list of url of a single post in the page
        :rtype: list
        """
        return []

    @classmethod
    def get_next_page(cls, current_url, delimiter):
        """Returns url of the next page in forum.

        :param current_url: Url of the current page
        :type current_url: str
        :param delimiter: Delimiter to split up the url of the current page
        :type delimiter: str
        :return: Url of the next page
        :rtype: str
        """
        current_url = current_url.split(delimiter)
        current_url[-1] = str(int(current_url[-1]) + 1)
        current_url = delimiter.join(current_url)
        return current_url

    @classmethod
    def reach_last_page(cls, url):
        """Returns True if the last page in forum is reached

        :param url: Url of the current page
        :type url: str
        :return: True
        """
        return False

    @classmethod
    def get_title(cls, url):
        """Returns title of a post

        :param url: Url of the post
        :type url: str
        :return: Title of the post
        :rtype: str
        """
        return ''

    @classmethod
    def get_body(cls, url):
        """Returns body content of a post

        :param url: Url of the post
        :type url: str
        :return: Body content of the post
        :rtype: str
        """
        return ''


class BRCANowForum(Community):
    def __init__(self, url):
        super().__init__(url)
        self.url = 'https://forum.breastcancernow.org/t5/forums/recentpostspage/post-type/thread/page/1'

    def get_posts(self, url):
        url_soup = Community.get_soup(url)
        posts = url_soup.find_all('', {'class', 'page-link lia-link-navigation lia-custom-event'})
        url_list = []
        for post in posts:
            post_url = 'http://forum.breastcancernow.org' + post['href']
            url_list.append(post_url)
        return url_list

    def reach_last_page(self, url):
        current = url[url.rfind('/') + 1:]
        if int(current) != 1:
            r = requests.get(url)
            url_contents = r.text
            url_soup = BeautifulSoup(url_contents, 'html.parser')
            next_page = url_soup.find('', {'class',
                                           'lia-link-navigation lia-js-data-pageNum-' + current + ' lia-link-disabled'})
            if next_page is None:
                return False
        else:
            return False

    def get_title(self, url):
        url_soup = Community.get_soup(url)
        return url_soup.title.string.replace('<title>', '').rsplit('-', 2)[0]

    def get_body(self, url):
        url_soup = Community.get_soup(url)
        return str(url_soup.find('', {'class', 'lia-message-body-content'}))


class BRCAOrg(Community):
    def __init__(self, url):
        super().__init__(url)
        self.url = 'https://community.breastcancer.org/'

    def find_keyword(self, url, keyword):
        title = Community.get_title(url)
        body = Community.get_body(url)
        for word_t in title.split():
            if word_t.lower() == keyword.lower():
                return True
        for content in body:
            for word_b in content.text.split():
                if word_b.lower() == keyword.lower():
                    return True

    @classmethod
    def get_forums(cls, url):
        """Returns a list of url of forums

        :param url: Url of the index page
        :type url: str
        :return: A list of url of forums in the same category
        """
        url_soup = Community.get_soup(url)
        forums = url_soup.find_all('h3')[3:57]
        link_list = []
        for forum in forums:
            link = forum.find('a').get('href')
            link = 'https://community.breastcancer.org' + link
            link_list.append(link)
        return link_list

    def get_posts(self, url):
        url_soup = Community.get_soup(url)
        posts = url_soup.find_all(title="View this Topic and its replies")
        url_list = []
        for post in posts:
            post_url = 'https://community.breastcancer.org' + post.get('href')
            url_list.append(post_url)
        return url_list

    def reach_last_page(self, url):
        url_soup = Community.get_soup(url)
        next_page = url_soup.find('', {'class', 'next_page disabled'})
        if next_page is None:
            return False

    def get_title(self, url):
        url_soup = Community.get_soup(url)
        return url_soup.h1.string[7:]

    def get_body(self, url):
        url_soup = Community.get_soup(url)
        return url_soup.find('', {'class', "user-post"}).find_all('p')[1:]


class Macmillan(Community):
    def __init__(self):
        super().__init__(url)
        self.url = 'https://community.macmillan.org.uk/cancer_types/breast-cancer/discussions?pi5752=1'

    def get_posts(self, url):
        url_soup = Community.get_soup(url)
        posts = url_soup.find_all('h4', {'class', 'post-name'})
        url_list = []
        for post in posts:
            if len(post.get('class')) != 1:
                posts.remove(post)
            else:
                post_url = 'https://community.macmillan.org.uk/' + post.find('a').get('href')
                url_list.append(post_url)
        return url_list

    def reach_last_page(self, url):
        url_soup = Community.get_soup(url)
        next_page = url_soup.find('a', {'class', 'next'})
        if next_page is not None:
            return False

    def get_title(self, url):
        url_soup = Community.get_soup(url)
        return url_soup.find('h4', {'class', 'post-name'}).string

    def get_body(self, url):
        url_soup = Community.get_soup(url)
        tags = url_soup.find(lambda tag: tag.get('class') == ['content'])
        body = ''
        for tag in tags:
            if tag.string is not None:
                body = body + tag.string
        return body


class AUSBRCAForum(Community):
    def __init__(self, url):
        super().__init__(url)
        self.url = 'https://www.bcaus.org.au/phpBB3'

    @classmethod
    def get_forums(cls, url):
        """Returns a list of url of forums

        :param url: Url of the index page
        :type url: str
        :return: A list of url of forums in the same category
        """
        url_soup = Community.get_soup(url)
        forums = url_soup.find_all('a', {'class', 'forumtitle'})[1:6]
        del forums[3]
        link_list = []
        for forum in forums:
            link = forum.get('href')
            link = 'https://www.bcaus.org.au/phpBB3' + link[1:]
            link_list.append(link)
        return link_list

    def get_posts(self, url):
        url_soup = Community.get_soup(url)
        posts = url_soup.find_all(class_='icon topic_read') + url_soup.find_all(class_='icon topic_read_hot')
        url_list = []
        for post in posts:
            if post.find(class_='pagination') is not None:
                print(post.find(class_='pagination').find_all('li')[-1])
                post_url = 'https://www.bcaus.org.au/phpBB3' + post.find(class_='pagination').find_all('li')[-1].find(
                    'a').get('href')[1:]
            else:
                post = post.find(class_='topictitle')
                post_url = 'https://www.bcaus.org.au/phpBB3' + post.get('href')[1:]
            url_list.append(post_url)
        return url_list

    def get_next_page(self, url, delimiter):
        delimiter = '='
        url = url.split(delimiter)
        if len(url) == 2:
            url = url[0] + '&start=50'
        else:
            url[-1] = str(int(url[-1]) + 50)
            url = delimiter.join(url)
        return url

    def reach_last_page(self, url):
        url_soup = Community.get_soup(url)
        next_page = url_soup.find(class_='next')
        if next_page is not None:
            return False

    def get_title(self, url):
        url_soup = Community.get_soup(url)
        return url_soup.find(class_='topic-title').string

    def get_body(self, url):
        url_soup = Community.get_soup(url)
        return str(url_soup.find_all(lambda tag: tag.get('class') == ['content'])[-1])


class KoreaVenus(Community):
    def __init__(self, url):
        super().__init__(url)
        self.url = 'http://www.koreavenus.com/db/index.html?table=noh_qna'


class CancerSuvivorsNetwork(Community):
    def __init__(self, url):
        super().__init__(url)
        self.url = 'https://csn.cancer.org/forum/127'

    def get_posts(self, url):
        url_soup = Community.get_soup(url)
        posts = url_soup.find_all('td', {'class', 'title'})
        url_list = []
        for post in posts:
            if post.div.a.string != '*Abbreviations* for all our Newbies':
                post_url = 'https://csn.cancer.org' + post.div.a.get('href')
                url_list.append(post_url)
        return url_list

    def get_next_page(self, url, delimiter):
        delimiter = '='
        url = url.split(delimiter)
        if len(url) == 1:
            url = url[0] + '?page=1'
        else:
            url[-1] = str(int(url[-1]) + 1)
            url = delimiter.join(url)
        return url

    def reach_last_page(self, url):
        url_soup = Community.get_soup(url)
        if url_soup.find(class_='pager-current last') is None:
            return False

    def get_title(self, url):
        url_soup = Community.get_soup(url)
        return url_soup.find(class_='with-tabs').string

    def get_body(self, url):
        url_soup = Community.get_soup(url)
        return str(url_soup.find('p').contents)

class HealthBoards(Community):
    def __init__(self, url):
        super().__init__(url)
        self.url = 'https://www.healthboards.com/boards/cancer-breast/index1.html'

    def get_posts(self, url):
        url_soup = Community.get_soup(url)
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

    def get_next_page(self, url, delimiter):
        # no delimiter is needed
        url_soup = Community.get_soup(url)
        return url_soup.find(rel='next').get('href')

    def reach_last_page(self, url):
        url_soup = Community.get_soup(url)
        if url_soup.find(rel='next') is not None:
            return False

    def get_title(self, url):
        url_soup = Community.get_soup(url)
        tags = url_soup.find_all(style='display: inline-block;')
        for tag in tags:
            if tag.find('strong') is not None:
                return tag.find('strong').string

    def get_body(self, url):
        url_soup = Community.get_soup(url)
        return str(url_soup.find(class_='alt1'))