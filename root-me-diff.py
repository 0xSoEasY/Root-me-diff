#!/usr/bin/python3

import sys
import requests
from bs4 import BeautifulSoup

################################## USAGE MESSAGE ##################################

usage = f"""Usage: [python3] {sys.argv[0]} user1 user2 [category]

--> A username must be written as it is in the URL of its profile
Github: https://github.com/0xSoEasY/Root-me-diff"""

################################## COLORS ##################################

COLOR_RESET = "\x1b[0m"
COLOR_RED   = "\x1b[1;31m"
COLOR_BLUE  = "\x1b[1;32m"
COLOR_YELLOW = "\x1b[1;33m"
COLOR_PURPLE = "\x1b[1;35m"

################################## FUNCTIONS ##################################

def get_page(user):
    s = requests.Session()
    r = s.get(f"https://www.root-me.org/{user}?inc=score&lang=en")

    if r.status_code != 200:
        print(f"[-] Couldn't find user {user}")
        exit(1)
    return r.text


def get_challenges(user1, user2, target_category=None):
    challenges = []
    page_user1 = get_page(user1)
    soup_user1 = BeautifulSoup(page_user1, 'html.parser')
    links_user1 = soup_user1.find_all("a", {"class": ["vert", "rouge"]})
    stats_user1 = soup_user1.find_all("h3")
    rank_user1 = str(stats_user1[4]).strip("</h3>").split(" ")[-1]
    score_user1 = str(stats_user1[5]).strip("</h3>").split(" ")[-1]
    print(f"[*] {user1} is ranked top {COLOR_YELLOW}{rank_user1}{COLOR_RESET} with {COLOR_PURPLE}{score_user1}{COLOR_RESET} points")

    page_user2 = get_page(user2)
    soup_user2 = BeautifulSoup(page_user2, 'html.parser')
    links_user2 = soup_user2.find_all("a", {"class": ["vert", "rouge"]})
    stats_user2 = soup_user2.find_all("h3")
    rank_user2 = str(stats_user2[4]).strip("</h3>").split(" ")[-1]
    score_user2 = str(stats_user2[5]).strip("</h3>").split(" ")[-1]
    print(f"[*] {user2} is ranked top {COLOR_YELLOW}{rank_user2}{COLOR_RESET} with {COLOR_PURPLE}{score_user2}{COLOR_RESET} points\n")

    for i, link in enumerate(links_user1):
        parsed = str(link).split('"')
        category = parsed[3].split("/")[2]
        name = parsed[6].split("\xa0")[1].split("</a>")[0]
        points = parsed[5].split()[0]

        user1_done = True
        if 'rouge' == parsed[1]:
            user1_done = False
        
        user2_done = True
        if 'rouge' == str(links_user2[i]).split('"')[1]:
            user2_done = False

        if target_category == None or target_category.lower() == category.lower():
            challenges.append((category, name, points, user1_done, user2_done))

    return challenges


def print_diff(user1, user2, challenges):
    print(f"[+] Challenges that {COLOR_BLUE}{user1} flagged{COLOR_RESET} and {COLOR_RED}not {user2}{COLOR_RESET}:")
    for challenge in challenges:
        if challenge[3] and not challenge[4]:
            print(f"- [{challenge[0]}]  {challenge[1]}  ({challenge[2]} pts)")
    
    print(f"\n[+] Challenges that {COLOR_BLUE}{user2} flagged{COLOR_RESET} and {COLOR_RED}not {user1}{COLOR_RESET}:")
    for challenge in challenges:
        if challenge[4] and not challenge[3]:
            print(f"- [{challenge[0]}]  {challenge[1]}  ({challenge[2]} pts)")

################################## MAIN METHOD & ARGUMENTS ##################################

if __name__ == '__main__':
	if len(sys.argv) > 2:

		if len(sys.argv) == 3:
			challenges = get_challenges(sys.argv[1], sys.argv[2])
		elif len(sys.argv) == 4:
			challenges = get_challenges(sys.argv[1], sys.argv[2], sys.argv[3])
		else:
			print(usage)
			exit(1)

		print_diff(sys.argv[1], sys.argv[2], challenges)

	else:
		print(usage)
		exit(1)
