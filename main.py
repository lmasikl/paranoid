# coding=utf-8
from time import sleep
import requests


class VKApi(object):
    """
    Class collect data about user
    """
    api_url = 'https://api.vk.com/method/'
    token = None
    friends = []
    groups = []
    walls = []
    posts = []
    bad_responses = []

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = None

    # def auth(self):
    #     request = requests.get(
    #         'https://oauth.vk.com/access_token?'
    #         'client_id=5046345&'
    #         'client_secret=E7o2YjmzonM96u0Nkuh7&'
    #         'v=5.37&grant_type=client_credentials'
    #     )
    #     self.token = request.json()['access_token']

    def __get_data(self, response):
        """
        Return response items
        """
        try:
            return response.json()['response']['items']
        except KeyError:
            self.bad_responses.append(response)
            return None

    def get_friends(self):
        """
        Collect user friends
        """
        response = requests.get(
            self.api_url + 'friends.get?'
            'user_id=' + str(self.user_id) + '&v=5.37'
        )
        data = self.__get_data(response)
        if data is not None:
            self.friends = data

    # def get_groups(self):
    #     response = requests.get(
    #         self.api_url + 'groups.get?'
    #         'user_id=' + self.user_id + '&v=5.37'
    #     )
    #     self.groups = self.__get_data(response)

    def get_wall(self, user_id=None):
        """
        Return user wall
        """
        if user_id is None:
            user_id = self.user_id
        response = requests.get(
            self.api_url + 'wall.get?'
            'owner_id=' + str(user_id) + '&v=5.37'
        )
        return self.__get_data(response)

    def get_liked(self, post):
        """
        Return post likes
        """
        response = requests.get(
            self.api_url + 'likes.getList?'
            'type=' + post['post_type'] +
            '&owner_id=' + str(post['owner_id']) +
            '&item_id=' + str(post['id']) + '&v=5.37'
        )
        return self.__get_data(response)

    def get_comments(self, post):
        """
        Return post comments
        """
        response = requests.get(
            self.api_url + 'wall.getComments?'
            'owner_id=' + str(post['owner_id']) +
            '&post_id=' + str(post['id']) + '&v=5.37'
        )
        return self.__get_data(response)

    def collect_walls(self):
        """
        Collect user friends walls
        """
        for friend in self.friends:
            wall = self.get_wall(friend)
            if wall is not None:
                self.walls.append(wall)

            sleep(0.3)

    def collect_user_likes(self):
        """
        Collect posts with user likes
        """
        for wall in self.walls:
            for post in wall:
                data = self.get_liked(post)
                if data is not None and self.user_id in data:
                    self.posts.append(post)
                sleep(0.3)

    def collect_user_comments(self):
        """
        Collect posts with user comments
        """
        for friend in self.friends:
            wall = self.get_wall(friend)
            if wall is None:
                continue

            for post in wall:
                data = self.get_comments(post)
                if data is not None and self.user_id in data:
                    self.posts.append(post)
                sleep(0.3)

    def print_posts(self):
        """
        Print post with user likes or comments
        """
        for post in self.posts:
            url = 'https://vk.com/id{owner_id}?w=wall{from_id}_{id}'.format(
                owner_id=post['owner_id'],
                from_id=post['from_id'],
                id=post['id']
            )
            print url

    def print_bad_responses(self):
        for response in self.bad_responses:
            print response.text


if __name__ == '__main__':
    api = VKApi(105295423)
    # api.auth()
    api.get_friends()
    # api.get_groups()
    api.collect_walls()
    api.collect_user_likes()
    # api.collect_user_comments()
    api.print_posts()
    # api.print_bad_responses()
