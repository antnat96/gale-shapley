import sys
import os.path


class LLNode:
    def __init__(self, val, next_node=None):
        self.val = val
        self.next_node = next_node


class LList:
    def __init__(self):
        self.head_node = None

    def prepend(self, data):
        if self.head_node is None:
            self.head_node = data
        else:
            data.next_node = self.head_node
            self.head_node = data


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
    for pref_line in f:
        pref_lists.append(pref_line.split())

    return pref_lists


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

    return pref_lists


def find():
    print('Finding')

    male_prefs = build_male_prefs()
    female_prefs = build_female_prefs()

    # Start the iteration
    # while curr_man is not None and curr_man['next_proposal'] < len(women):

    # If curr_woman is free, they become engaged

    # If curr_woman is engaged, evaluate the new match against the current one

    # If the new match is better, the pair become engaged and the previous man returns to the men queue

    # If the new match is worse, the man is rejected and returns to the men queue

    # Grab the next man, if there is one

    # Terminate the algorithm


def check():
    output_file_exists = os.path.exists(sys.argv[4])
    if output_file_exists is not True:
        print('Please enter a valid output file name')
        return

    print('Checking')


def gs():
    if len(sys.argv) != 5:
        print('Please input mode name, 2 preference file names, and output file name')
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
