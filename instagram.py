import time
import sys
import random
import json
import requests
import browser

class Instagram():
    def __init__(self, username, password, proxy = False):
        self.username = username
        self.password = password
        self.isloggedin = False
        self.instagram_url = "https://www.instagram.com/"
        self.instagram_login_url = "https://www.instagram.com/accounts/login/ajax/"
        self.instagram_signup_url = "https://www.instagram.com/accounts/web_create_ajax/"
        self.instagram_logout_url = "https://www.instagram.com/accounts/logout/"
        self.user_info_url = "https://www.instagram.com/{}/?__a=1"
        self.follow_url = "https://www.instagram.com/web/friendships/{}/follow/"
        self.unfollow_url = "https://www.instagram.com/web/friendships/{}/unfollow/"
        self.useragent = self.random_ua()["User-Agent"]
        self.s = requests.Session()
        self.s.proxies = self.random_proxy() if proxy else {}
        self.s_get = self.s.get("https://www.instagram.com/")

    def json_loads(self, req):
        r = {}
        try:
            r = json.loads(req.text)
        except Exception as e:
            print("An Error Occured! Details :\n",sys.exc_info())
        try:
            if r["authenticated"] == True:
                self.isloggedin = True
        except:
            pass
        finally:
             self.s_get = self.s.get(self.instagram_url)
             return r

    def login(self):
        form_data={"username": self.username, "password": self.password}
        self.s.headers.update({
            'UserAgent': self.useragent,
            'x-instagram-ajax': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'origin': self.instagram_url,
            'ContentType': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'authority': 'www.instagram.com',
            'Host' : 'www.instagram.com',
            'Accept-Language': 'en-US;q=0.6,en;q=0.4',
            'Accept-Encoding': 'gzip, deflate'
            })
        self.s.headers.update({'X-CSRFToken': self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.post(self.instagram_login_url, data=form_data)
        return self.json_loads(r)

    def logout(self):
        r = self.s.get(self.instagram_logout_url)
        self.isloggedin = False
        return r

    def follow(self,username = False, userid = None):
        if self.isloggedin:
            if userid is not None:
                follow_url = self.follow_url.format(userid)
            elif userid is None and user:
                userid = self.userinfo(username)["user"]["id"]
                follow_url = self.follow_url.format(userid)
            else:
                return "you can not enter two parameters at the same time"
            self.s.headers.update({'X-CSRFToken': self.s_get.cookies.get_dict()['csrftoken']})
            r = self.s.post(follow_url)
            return self.json_loads(r)
        else:
            print("You must login first")

    def unfollow(self,username = False, userid = None):
        if self.isloggedin:
            if userid is not None:
                unfollow_url = self.unfollow_url.format(userid)
            elif userid is None and username:
                userid = self.userinfo(username)["user"]["id"]
                unfollow_url = self.unfollow_url.format(userid)
            else:
                return "you can not enter two parameters at the same time"
            self.s.headers.update({'X-CSRFToken': self.s_get.cookies.get_dict()['csrftoken']})
            r = self.s.post(unfollow_url)
            return self.json_loads(r)
        else:
            print("You must login first")

    def signup(self, first_name, email):
        form_data={
            "email": email,
            "password": self.password,
            "username": self.username,
            "first_name": first_name,
            "seamless_login_enabled": "1"
            }
        self.s.headers.update({
            'UserAgent': self.useragent,
    		'x-instagram-ajax': '1',
    		'X-Requested-With': 'XMLHttpRequest',
    		'Host': self.instagram_url,
    		'ContentType': 'application/x-www-form-urlencoded',
    		'Connection': 'keep-alive',
    		'Accept': '*/*',
    		'Referer': self.instagram_url,
    		'authority': 'www.instagram.com',
    		'Host' : 'www.instagram.com',
    		'Accept-Language': 'en-US;q=0.6,en;q=0.4',
    		'Accept-Encoding': 'gzip, deflate'
    	})
        self.s.headers.update({'X-CSRFToken': self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.post(self.instagram_signup_url, data=form_data)
        return self.json_loads(r)

    def userinfo(self,username): # oturum acildiktan sonra erisilebilen bilgiler
        if self.isloggedin:
            user_info = self.user_info_url.format(username)
            req = self.s.get(user_info)
        else:
            user_info = "https://www.instagram.com/{}/?__a=1".format(username)
            req = requests.get(user_info)
        info = json.loads(req.text)
        return info

    @staticmethod
    def random_ua():
        explorer = ["chrome", "opera", "firefox", "internetexplorer", "safari"]
        ex = fake.ua["browsers"][explorer[random.randrange(len(explorer))]]
        useragent = ex[random.randrange(len(ex))]
        return {'User-Agent': useragent}

    @staticmethod
    def random_proxy():
        json_data = requests.get("https://freevpn.ninja/free-proxy/json").json()
        # possible alternate proxies
        # "https://gimmeproxy.com/api/getProxy"
        # "https://getproxylist.com/"

        json_ip = []
        # We are just selecting https and http types
        for i in json_data:
            if i["type"] in ["http", "https"]:
                json_ip.append({"type": i["type"], "proxy": i["proxy"]})

        if len(json_ip) == 0: # If we dont have any http / https proxies
            return {}

        num = random.randrange(len(json_ip))
        json_proxy = json_ip[num]
        return {json_proxy["type"]: "{}://{}".format(json_proxy["type"], json_proxy["proxy"])}
