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
        self.curr_node = self.head_node
        self.proposal_count = 0
        self.length = 0

    def has_more_proposals(self):
        return self.proposal_count < self.length

    def get_curr_proposal_subject(self):
        self.proposal_count += 1
        temp = self.curr_node.val
        self.curr_node = self.curr_node.next_node
        return temp

    def prepend(self, data):
        if self.head_node is None:
            self.head_node = data
        else:
            data.next_node = self.head_node
            self.head_node = data
        self.curr_node = self.head_node
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


def to_int(str):
    return int(str) - 1


def cleanse_result(result):
    if result is None:
        return None
    return result + 1


def build_female_prefs():
    f = open(sys.argv[3], "r")
    # Get
    f.readline()
    pref_lists = []
    inverse_pref_lists = []
    for pref_line in f:
        int_pref_list = list(map(to_int, pref_line.split()))
        pref_lists.append(int_pref_list)
        inverse_pref_lists.append(list(reversed(int_pref_list)))
    f.close()
    return pref_lists, inverse_pref_lists


def build_male_prefs():
    f = open(sys.argv[2], "r")
    f.readline()
    pref_lists = []
    for pref_line in f:
        pref_list = LList()
        int_pref_list = list(map(to_int, pref_line.split()))
        # Uses a reverse iterator, does not actually copy the list
        for pref in reversed(int_pref_list):
            pref_list.prepend(LLNode(pref))
        pref_lists.append(pref_list)
    f.close()
    return pref_lists


def find():
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
    while unengaged_male is not None and male_prefs[unengaged_male].has_more_proposals():
        print('\n'
              '-------STEP-------')
        # Get the subject of this iteration's proposal
        curr_proposal_subject = male_prefs[unengaged_male].get_curr_proposal_subject()

        # If curr_proposal_subject is free, an engagement occurs
        if female_matches[curr_proposal_subject] is None:
            print(unengaged_male + 1, 'proposes to', curr_proposal_subject + 1, 'and they get engaged')
            # The female is matched to the male
            female_matches[curr_proposal_subject] = unengaged_male
            # The male is matched to the female
            male_matches[unengaged_male] = curr_proposal_subject

        # But if the curr_proposal_subject is engaged already
        else:
            # If the new match is better for the female
            if inverse_female_prefs[curr_proposal_subject][unengaged_male] \
                    < inverse_female_prefs[curr_proposal_subject][female_matches[curr_proposal_subject]]:
                print(unengaged_male + 1, 'proposes to', curr_proposal_subject + 1,
                      'and they get engaged, she dumps her old partner')
                # The old partner is returned to the unengaged_males queue
                unengaged_males.enqueue(QNode(female_matches[curr_proposal_subject]))
                # The old partner is recorded as being free
                male_matches[female_matches[curr_proposal_subject]] = None
                # The female is matched to the new male
                female_matches[curr_proposal_subject] = unengaged_male
                # The male is matched to the female
                male_matches[unengaged_male] = curr_proposal_subject

            # If the new match is worse
            else:
                print(unengaged_male + 1, 'proposes to', curr_proposal_subject + 1, 'and she rejects him')
                # The unengaged male is rejected and returns to the men queue
                unengaged_males.enqueue(QNode(unengaged_male))

        # Grab the next unengaged male for the following iteration
        unengaged_male = unengaged_males.dequeue()

    # Write to the output file
    output_file = open(sys.argv[4], "w")
    male_id = 1
    for female_id in list(map(cleanse_result, male_matches)):
        output_file.write("{0} {1}\n".format(str(male_id), str(female_id)))
        male_id += 1
    output_file.close()


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
