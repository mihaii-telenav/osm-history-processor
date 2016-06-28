#!/usr/bin/python

import argparse
import wget
import subprocess
import os
import zipfile
import urllib2
from datetime import date

# Import zlib for compression
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED


# Define arguments for the parser
parser = argparse.ArgumentParser(description='History processor for Openstreetmap')
parser.add_argument('date', metavar='date', type=str, help='Date you want to start')
parser.add_argument('days', metavar='days', type=int, help='How many days history?')

args = parser.parse_args()
start_date = date(2012, 9, 12)
end_date = date(int(args.date.split('-')[0]), int(args.date.split('-')[1]), int(args.date.split('-')[2]))
delta = (end_date - start_date).days
days = args.days or 7;

# Utility function to run shell commands
def bash(command):
    "Runs a command in shell"
    subprocess.call(command, shell=True)
    return

# OSM repication server url
osm_replication_url = "http://planet.osm.org/replication/day/"

# Read users from users.list
users = open('users.list', 'r').readlines()

if __name__ == "__main__":

    # Create a dir for the files
    bash("mkdir fisiere")
    bash("cd fisiere")
    line = []
    while days>=0:

        # Set the current edition number
        # Find the exact replication location based on http://wiki.openstreetmap.org/wiki/Planet.osm/diffs
        # Add 1 since we want the edition of the following day which contains changes of the previuos day
        edition = delta - days + 1
        aaa = "000"
        bbb = str(edition/1000).zfill(3)
        ccc = str(edition%1000).zfill(3)

        url =  osm_replication_url+aaa+"/"+bbb+"/"+ccc+".osc.gz"
        print '# Replication URL', url

        # Download the replication
        wget.download(url)

        # Unzip the file
        bash("gzip -d {}".format(ccc + ".osc.gz"))

        line.append(ccc)

        # Process previous edition number
        days-=1

bash('osmconvert {}.osc --out-o5m | osmconvert - {}.osc --out-o5m | osmconvert - {}.osc --out-o5m | osmconvert - {}.osc --out-o5m | osmconvert - {}.osc --out-o5m | osmconvert - -o=unitedall.osc'.format(line[0],line[1],line[2],line[3],line[4]))




hardcoded = "unitedall"
for user in users:
    user = user.strip('\n')
    print '# Processing ' + user +"'s changes"
    # Filter the edits for a particular user from the edition
    bash('osmfilter {}.osc --keep="@user={}" -o={}.osm'.format(hardcoded, user, user))
    # Cleanup

bash("rm *.osc")
