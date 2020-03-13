import sys
import ruamel.yaml
import requests
import re
import os
import sys

def main():
    args = sys.argv
    if len(args) == 1:
        print("add package-name => add package")
        print("remove package-name => remove package")
        sys.exit(0)

    action = args[1]

    if action == "add":
        if len(args) < 3:
            print("Please provide package name")
            sys.exit(0)

        name = args[2]
        print("Adding package: " + name)
        add_package(name)
    elif action == "remove":
        if len(args) < 3:
            print("Please provide package name")
            sys.exit(0)

        name = args[2]
        print("Removing package: " + name)
        remove_package(name)
    else:
        print("Wrong afgument!")
        print("add package-name => add package")
        print("remove package-name => remove package")
        sys.exit(0)

    
    print("Done!")

def get_data_from_spec():
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    with open('pubspec.yaml') as fp:
        data = yaml.load(fp)

    return data

def write_spec(data):
    yaml = ruamel.yaml.YAML()
    with open('pubspec.yaml', 'w') as fp:
         yaml.dump(data, fp)
    fp.close()
    print("Saved to pubspec.yaml")


def run_clean():
    print("Running flutter pub get command")
    os.system("flutter pub get")


def remove_package(name):
    data = get_data_from_spec()
    depend = data["dependencies"]
    depend.pop(name)
    write_spec(data)
    run_clean()
    print("Removed")


def add_package(name):
    data = get_data_from_spec()
    depend = data["dependencies"]

    if name in depend:
        if not yn_choice("Package installed, do you want to update it to latest version?"):
            print("OK! Bye")
            sys.exit(0)

    url = "https://pub.dev/packages/" + name

    import urllib.request

    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    html = mybytes.decode("utf8")
    fp.close()

    x = re.search('"version":"([^"]+)"', html) 
    if not x:
        print("Package not found")
        sys.exit(0)
    version = x.group(1)
    print("Latest version found: " + version)
    depend[name] = '^' + version

    write_spec(data)
    run_clean()
    print("Added")


def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if choices == 'Y/n' else ('y', 'yes')
    return choice.strip().lower() in values


main()