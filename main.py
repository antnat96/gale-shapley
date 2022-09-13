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
# python main.py find males females output
# python main.py check males females output


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

    def prefers(self, first, second):
        if self.head_node is None:
            return False
        if self.head_node.next_node is None:
            return False

        node = self.head_node
        found_first = False
        found_second = False
        while node is not None:
            if node.val == first:
                found_first = True
            if node.val == second:
                found_second = True
            if found_first is True and found_second is False:
                return True
            elif found_second is True and found_first is False:
                return False
            node = node.next_node

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


def to_int_index(my_str):
    return int(my_str) - 1


def to_int(my_str):
    return int(my_str)


def cleanse_result(result):
    if result is None:
        return None
    return result + 1


def build_female_prefs():
    f = open(sys.argv[3], "r")
    n = int(f.readline())
    pref_lists = []
    inverse_pref_lists = []
    for pref_line in f:
        int_pref_list = list(map(to_int_index, pref_line.split()))
        pref_lists.append(int_pref_list)
        inverse_pref_list = [None] * n
        for i in int_pref_list:
            inverse_pref_list[int_pref_list[i]] = i
        inverse_pref_lists.append(inverse_pref_list)
    f.close()
    return pref_lists, inverse_pref_lists


def build_male_prefs():
    f = open(sys.argv[2], "r")
    f.readline()
    pref_lists = []
    for pref_line in f:
        pref_list = LList()
        int_pref_list = list(map(to_int_index, pref_line.split()))
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

    step = 1

    # While there's an unengaged male, and he still has a female to propose to
    while unengaged_male is not None and male_prefs[unengaged_male].has_more_proposals():
        print("-----STEP {0}------".format(step))
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
        step += 1

    # Write to the output file
    output_file = open(sys.argv[4], "w")
    male_id = 1
    for female_id in list(map(cleanse_result, male_matches)):
        if male_id > 1:
            output_file.write("\n")
        output_file.write("{0} {1}".format(str(male_id), str(female_id)))
        male_id += 1
    output_file.close()
    print("Done writing output to {0}".format(sys.argv[4]))


def find_curr_partner_female(female_index, matches):
    for match in matches:
        if match[1] == female_index:
            return match[0]
    return None


def find_curr_partner_male(male_index, matches):
    for match in matches:
        if match[0] == male_index:
            return match[1]
    return None


def check():
    output_file_exists = os.path.exists(sys.argv[4])
    if output_file_exists is not True:
        print('Please enter a valid output file name, it appears that this file does not exist.')
        return

    doubtful = open(sys.argv[4], "r")
    matches = []
    males = []
    females = []
    for matching in doubtful:
        line = matching.split()
        if len(line) >= 1:
            males.append(int(line[0]))
        if len(line) >= 2:
            females.append(int(line[1]))
        cleansed_matches = list(map(to_int_index, line))
        matches.append(cleansed_matches)
    doubtful.close()

    # Check that no individual is represented more than once (matching property)
    for gender in [males, females]:
        for individual in gender:
            if gender.count(individual) > 1:
                print(individual, 'exists more than once, '
                                  'therefore the output file fails to satisfy the matching property.')
                return

    # Check that no individual is unmatched (perfectness property)
    male_preference_file = open(sys.argv[2], "r")
    female_preference_file = open(sys.argv[3], "r")
    expected_matches_count_males = int(male_preference_file.readline())
    expected_matches_count_females = int(female_preference_file.readline())
    # Ensure preference files have the same n value
    if expected_matches_count_females != expected_matches_count_males:
        print('The preference files do not have matching n values, therefore the perfectness property '
              'cannot be satisfied')
        return

    # Ensure output file and preference files have the same n value
    expected_matches_count = expected_matches_count_males
    if len(males) != expected_matches_count or len(females) != expected_matches_count:
        print('The expected number of matches from the preference files is different than the number of matches in'
              'the output file, therefore the output file fails to satisfy the perfectness property.')
        return

    # Check that each match is stable (stability property)
    # Build preference lists
    male_prefs = build_male_prefs()
    female_prefs, inverse_female_prefs = build_female_prefs()

    female_index = 0
    for female in females:
        # Find the males that are preferable to this female's current partner, if any
        preferable_males = []
        curr_male_partner = find_curr_partner_female(female_index, matches)
        if curr_male_partner is None:
            print('Could not find the current partner of female', female)
            return
        for pref in female_prefs[female_index]:
            if pref == curr_male_partner:
                break
            preferable_males.append(pref)
        # Ensure each of those preferable males would not prefer this female to his current partner
        for male in preferable_males:
            curr_female_partner = find_curr_partner_male(male, matches)
            if male_prefs[male].prefers(female_index, curr_female_partner):
                print('male', male + 1, 'prefers female', female, 'to female', curr_female_partner + 1,
                      'therefore the matching is unstable')
                return

        female_index += 1

    print('The matching is stable!')


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
