#This program finds duplicates in directory that was given as a command line argument.

import sys
import argparse
import os
import re
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('top_dir', type=str, help='The name of top directory')
args = parser.parse_args()

pattern = re.compile("^[.~]")

hasher = hashlib.sha1()
dic = dict()

for root, dirs, files in os.walk(args.top_dir):
    for filename in files:
        if (not pattern.match(filename)):
            fullname = root + ("/" if (len(root) > 0) and root[-1] != "/" else "") + filename
            print(fullname)
            stats = os.stat(fullname)
            with open(fullname, 'rb') as f:
                z = f.read(1024)
                print(z)
                hasher.update(z)
                a = hasher.hexdigest()
                print(a)
                if (not a in dic):
                    dic[a] = []
                prefix = root[len(args.top_dir):]
                dic[a].append(prefix + ("/" if (len(prefix) > 0 and prefix[-1] != "/") else "") + filename)

for hsh in dic:
    if len(dic[hsh]) > 1:
        for a in dic[hsh]:
            print(a, end=(":" if a != dic[hsh][-1] else "\n"))

            
            
    