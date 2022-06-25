import requests
from bs4 import BeautifulSoup
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

################################## ARGUMENTS ##################################

parser = ArgumentParser(description="Find the validated challenges that differ from a user to another", formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--user1',      help="The complete name of the first user (in profile URL)")
parser.add_argument('--user2',      help="The complete name of the second user (in profile URL)")
parser.add_argument('--category',   help="Specify a challenge category to filter")
args = parser.parse_args()

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

    page_user2 = get_page(user2)
    soup_user2 = BeautifulSoup(page_user2, 'html.parser')
    links_user2 = soup_user2.find_all("a", {"class": ["vert", "rouge"]})

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
    print(f"[+] Challenges that \x1b[1;32m{user1} flagged\x1b[0m and \x1b[1;31mnot {user2}\x1b[0m:")
    for challenge in challenges:
        if challenge[3] and not challenge[4]:
            print(f"- [{challenge[0]}]  {challenge[1]}  ({challenge[2]} pts)")
    
    print(f"\n[+] Challenges that \x1b[1;32m{user2} flagged\x1b[0m and \x1b[1;31mnot {user1}\x1b[0m:")
    for challenge in challenges:
        if challenge[4] and not challenge[3]:
            print(f"- [{challenge[0]}]  {challenge[1]}  ({challenge[2]} pts)")

################################## MAIN METHOD ##################################

def main():
    if args.user1 and args.user2:
        challenges = get_challenges(args.user1, args.user2, args.category)
        print_diff(args.user1, args.user2, challenges)

    else:
        print()
        parser.print_help()
        print()

if __name__ == '__main__':
    main()