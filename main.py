# Author: Anthony Natale
# Assignment: Gale-Shapley Implementation, Assignment 1
# Class: Design and Analysis of Algorithms, Fall 2022
# Purpose: This program performs two functions.
#   1. Given 2 valid preference files and an output file name, execute the GS
#       algorithm to determine a stable matching for n males and n females
#   2. Given 2 valid preference files and an existing output file name, evaluate the output
#       file and determine whether the matching is stable. If it is not, display a message
#       indicating why the matching is unstable.

# Example Commands to Program:
# python main.py find male_prefs female_prefs output
# python main.py check male_prefs female_prefs output


# Imports
import sys
import os.path


# Node for the queue data structure
class QNode:
    def __init__(self, val=None):
        self.val = val
        self.next_node = None
        self.prev_node = None


# Queue data structure
class Queue:
    def __init__(self):
        self.length = 0
        self.head_node = None
        self.tail_node = None

    def dequeue(self):
        if self.length == 0:
            return None
        curr_head_val = self.head_node.val
        self.head_node = self.head_node.next_node
        self.length -= 1
        if self.length == 0:
            self.tail_node = None
        return curr_head_val

    def enqueue(self, val):
        if self.head_node is None:
            self.head_node = val
            self.tail_node = val
        else:
            self.tail_node.next_node = val
            val.prev_node = self.tail_node
            self.tail_node = val
        self.length += 1


# Node for the linked list data structure
class LLNode:
    def __init__(self, val, next_node=None):
        self.val = val
        self.next_node = next_node


# Linked list data structure
class LList:
    def __init__(self):
        self.head_node = None
        self.curr_node = 0
        self.length = 0

    def get_this_proposal_index(self):
        return self.curr_node

    def increment_proposal_index(self):
        self.curr_node += 1

    def prepend(self, data):
        if self.head_node is None:
            self.head_node = data
        else:
            data.next_node = self.head_node
            self.head_node = data
        self.length += 1

    def show(self):
        if self.head_node is None:
            print('Empty')
        else:
            print(self.head_node.val)
            next_node = self.head_node.next_node
            while next_node is not None:
                print(next_node.val)
                next_node = next_node.next_node


def build_female_prefs():
    f = open(sys.argv[3], "r")
    n = int(f.readline())
    pref_lists = []
    inverse_pref_lists = []
    for pref_line in f:
        pref_lists.append(pref_line.split())
        inverse_pref_lists.append(list(reversed(pref_line.split())))
    f.close()
    return pref_lists, inverse_pref_lists


def build_male_prefs():
    f = open(sys.argv[2], "r")
    n = int(f.readline())
    pref_lists = []
    for pref_line in f:
        pref_list = LList()
        prefs_arr = pref_line.split()
        # Uses a reverse iterator, does not actually copy the list
        for pref in reversed(prefs_arr):
            pref_list.prepend(LLNode(pref))
        pref_lists.append(pref_list)
    f.close()
    return pref_lists


def find():
    print('Finding')

    male_prefs = build_male_prefs()
    female_prefs, inverse_female_prefs = build_female_prefs()

    # Build the initial queue of unengaged males
    unengaged_males = Queue()
    f = open(sys.argv[2], "r")
    n = int(f.readline())
    f.close()
    for male_index in range(n):
        unengaged_males.enqueue(QNode(male_index))

    # Build matching sets
    female_matches = [None] * n
    male_matches = [None] * n

    unengaged_male = unengaged_males.dequeue()

    # While there's an unengaged male, and he still has a female to propose to
    while unengaged_male is not None and male_prefs[unengaged_male].get_this_proposal_index() <= n:
        curr_female = male_prefs[unengaged_male].get_this_proposal_index()
        # If curr_woman is free, they become engaged
        if female_matches[curr_female] is None:
            female_matches[curr_female] = unengaged_male
            male_matches[unengaged_male] = curr_female
        # If curr_woman is engaged
        else:
            # If the new match is better, the pair become engaged and the previous man returns to the men queue
            if inverse_female_prefs[unengaged_male] < inverse_female_prefs[female_matches[curr_female]]:
                unengaged_males.enqueue(QNode(female_matches[curr_female]))
                female_matches[curr_female] = unengaged_male
                male_matches[unengaged_male] = curr_female
            # If the new match is worse, the unengaged male is rejected and returns to the men queue
            else:
                unengaged_males.enqueue(QNode(unengaged_male))

        # Increment this male's proposal index
        male_prefs[unengaged_male].increment_proposal_index()
        # Grab the next unengaged male for the following iteration
        unengaged_male = unengaged_males.dequeue()

    print(male_matches)
    print(female_matches)


def check():
    output_file_exists = os.path.exists(sys.argv[4])
    if output_file_exists is not True:
        print('Please enter a valid output file name')
        return

    print('Checking')


def gs():
    if len(sys.argv) != 5:
        print('Please input mode, 2 preference file names, and 1 output file name')
        return

    if sys.argv[1] != 'find' and sys.argv[1] != 'check':
        print('Please input \'find\' or \'check\' as the mode.')
        return

    male_prefs_exist = os.path.exists(sys.argv[2])
    female_prefs_exist = os.path.exists(sys.argv[3])

    if male_prefs_exist is not True or female_prefs_exist is not True:
        print('Please enter valid preference file names.')
        return

    if sys.argv[1] == 'find':
        find()
    elif sys.argv[1] == 'check':
        check()


if __name__ == '__main__':
    gs()
