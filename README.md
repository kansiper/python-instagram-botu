>>> from instagram import Instagram as I
>>> user_info = I.userinfo("hakancelik.py") # get information before signing in
#/ oturum açmadan bilgi alıyoruz
>>> user_info["logging_page_id"] # page_id
>>> user_info["user"]["id"] # for user id
>>> user_info["user"]["full_name"] # for full name
# etc ... for more information read userinfo.md

>>> I = I("username", "password")  
# if you want to use proxy I("username", "password", True)
>>> I.username
username
>>> I.password
password
>>> I.useragent
# gives random useragent
>>> I.s
# gives requests session
>>> I.s.proxies
# you gives fake proxy ex: 165.321.51.21:8050

>>> I.login() # to login instagram
>>> I.logout() # to logout instagram
>>> I.isloggedin  # To check whether loggedin or not
False # or True
>>> I.follow(userid = 3) # for @kevin
{'result': 'following', 'status': 'ok'}
>>> I.follow(username = "hakancelik.py") # for me
{'result': 'following', 'status': 'ok'}
>>> I.unfollow(userid = 3) # for #kevin
{'status': 'ok'}
>>> I.unfollow("hakancelik.py") # for me
{'status': 'ok'}
>>> I.signup(first_name="first_name",email="email") # to signup for instagram
