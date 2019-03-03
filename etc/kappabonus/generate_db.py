import random
import string
import sys

TEMPLATE = open("db.sql", "r").read()

random.seed(0x13371337)


def genstr():
    return ''.join([random.choice(string.ascii_lowercase) for _ in range(20)])


def gendb(team):
    print(TEMPLATE.format(team=team))


def genuser(team):
    pwd = genstr()
    print(f"CREATE USER '{team}'@'%' IDENTIFIED BY '{pwd}';")
    print(f"{team}:{pwd}", file=sys.stderr)


def grant(teams):
    for db in teams:
        print(f"GRANT SELECT, INSERT, UPDATE, DELETE on {db}.* to {db}@'%';")
        print(f"GRANT SELECT on {db}.lcbc to ''@'%';")
        for user in teams:
            if db == user: continue
            print(f"GRANT SELECT on {db}.lcbc to {user}@'%';")


def gengroup(prefix, num):
    names = [f"{prefix}{i}" for i in range(1, num + 1)]
    for team in names:
        genuser(team)
        gendb(team)
    print()
    grant(names)


gengroup("team", 12)

