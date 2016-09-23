"""This program finds duplicates in directory that was given as a command line argument."""

import sys
import argparse
import os
import re
import hashlib
import collections

def get_file_hash(filename):
    hasher = hashlib.sha1()
    with open(filename, 'rb') as f:
        a = f.read(7200)
        while (a):
            hasher.update(a)
            a = f.read(7200)
    return hasher.hexdigest()    
    

def walk_through_directories(top_dir):
    dic = collections.defaultdict(list)
    for root, _, files in os.walk(top_dir):
        for filename in files:
            if (not pattern.match(filename)):
                fullname = os.path.join(root, filename)
                a = get_file_hash(fullname)
                dic[a].append(os.path.relpath(fullname, top_dir))
    return dic

def output(dic):
    for hsh in dic:
        if len(dic[hsh]) > 1:
            print(":".join(dic[hsh]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('top_dir', type=str, help='The name of top directory')
    args = parser.parse_args()
    pattern = re.compile("^[.~]")
    dic = walk_through_directories(args.top_dir)        
    output(dic)            
            
    