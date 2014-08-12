"""
Student code for Word Wrangler game

Author: John Liu
Date: 2014-20-Jul
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    newlist = []
    for index in range(len(list1)):
        if list1[index] not in newlist:
            newlist.append(list1[index])
    return newlist

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    newlist = []
    for index1 in range(len(list1)):
        if list1[index1] in list2:
            newlist.append(list1[index1])
    return newlist

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """     
    alist = list(list1)
    blist = list(list2)
    newlist = []
    while len(alist)>0 and len(blist)>0:
        if alist[0] < blist[0]:
            newlist.append(alist.pop(0))
        elif alist[0] > blist[0]:
            newlist.append(blist.pop(0))
        else:
            newlist.append(alist.pop(0))
            newlist.append(blist.pop(0))
    if alist:
        newlist.extend(alist)
    if blist:
        newlist.extend(blist)
    return newlist   

                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        midlen = len(list1)//2
        lista = merge_sort(list1[:midlen])
        listb = merge_sort(list1[midlen:])
        return merge(lista,listb)
    
    
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        newlist = list(rest_strings)
        for perm in rest_strings:
            for position in range(len(perm)):
                newlist.append(perm[:position]+first+perm[position:])
            newlist.append(perm+first)
        return newlist
        
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    newlist = []
    url = "http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt"
    ffile = urllib2.urlopen(url)
    for line in ffile.readlines():
        newlist.append(line[:-1])
    return newlist

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()

#print gen_all_strings('ab')    
