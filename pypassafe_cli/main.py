# PYTHON_ARGCOMPLETE_OK

from pypassafe.vault import Vault

from argparse import ArgumentParser
from arghandler import ArgumentHandler, subcmd
from getpass import getpass

def context_parser(args):
    return {"vault": args.vault}

def get_master() -> str:
    return getpass(prompt="master password [hidden input]:")

def login_to_str(login):
    return f"name: {login.name}\nurl: {login.url}\npassword: {login.password}"

@subcmd
def get(parser: ArgumentParser, context, cargs):
    cmds = ["password", "name", "url", "login"]
    if cargs[0] not in cmds:
        parser.error(f"one of the commands {cmds} is expected")

    if cargs[0] != "password":
        parser.add_argument("--password", dest="password", metavar="PASSWORD", help="the login's password")
    if cargs[0] != "url":
        parser.add_argument("--url", dest="url", metavar="URL", help="the login's url")
    if cargs[0] != "name":
        parser.add_argument("--name", dest="name", metavar="NAME", help="the login's name")

    parser.add_argument("-c", "--count", dest="count", metavar="COUNT", help="number of items to get")

    parsed = parser.parse_args(cargs[1:])

    vault = Vault(context["vault"])
    if cargs[0] == "password":
        print('\n'.join(vault.get_password(
            url=parsed.url,
            name=parsed.name,
            count=parsed.count,
            master=get_master())))
    if cargs[0] == "url":
        print(vault.get_url(password=parsed.password, name=parsed.name, count=parsed.count, master=get_master()))
    if cargs[0] == "name":
        print(vault.get_name(password=parsed.password, url=parsed.url, count=parsed.count, master=get_master()))
    if cargs[0] == "login":
        print("*** found logins ***",
                ('*' * 10 + '\n').join(map(login_to_str,
                vault.get_login(
                password=parsed.password,
                url=parsed.url,
                name=parsed.name,
                count=parsed.count,
                master=get_master()))),
            sep='\n')

@subcmd
def add(parser: ArgumentParser, context, cargs):
    cmds = ["login"]
    if cargs[0] not in cmds:
        parser.error(f"one of the commands {cmds} is expected")

    parser.add_argument("--password", dest="password", metavar="PASSWORD", help="the new login's password")
    parser.add_argument("--url", dest="url", metavar="URL", help="the new login's url")
    parser.add_argument("--name", dest="name", metavar="NAME", help="the new login's name")

    parsed = parser.parse_args(cargs[1:])

    vault = Vault(context["vault"])
    vault.add_login(
            password=parsed.password,
            url=parsed.url,
            name=parsed.name,
            master=get_master())
    print("added")

@subcmd
def set(parser: ArgumentParser, context, cargs):
    cmds = ["login"]
    if cargs[0] not in cmds:
        parser.error(f"one of the commands {cmds} is expected")

    parser.add_argument("--password", dest="password", metavar="PASSWORD", help="the login's password")
    parser.add_argument("--url", dest="url", metavar="URL", help="the login's url")
    parser.add_argument("--name", dest="name", metavar="NAME", help="the login's name")

    parser.add_argument("--new-password", dest="new_password", metavar="PASSWORD", help="the login's password to set")
    parser.add_argument("--new-url", dest="new_url", metavar="URL", help="the login's url to set")
    parser.add_argument("--new-name", dest="new_name", metavar="NAME", help="the login's name to set")

    parser.add_argument("-c", "--count", dest="count", metavar="COUNT", help="number of items to set", default=1)

    parsed = parser.parse_args(cargs[1:])

    vault = Vault(context["vault"])
    vault.set_login(
            password=parsed.password,
            url=parsed.url,
            name=parsed.url,
            new_password=parsed.new_password,
            new_url=parsed.new_url,
            new_name=parsed.new_name,
            count=parsed.count,
            master=get_master())
    print("updated")

def main() -> None:
    main_parser = ArgumentHandler(description="local password manager")
    main_parser.add_argument("--vault", dest="vault", required=True, metavar="PATH", help="path to the vault")
    main_parser.run(context_fxn=context_parser)

if __name__ == "__main__":
    main()
