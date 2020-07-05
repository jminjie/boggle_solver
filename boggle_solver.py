#!/usr/local/bin/python3
import sys
from typing import Tuple

DICT_FILE = 'scrabble.txt'

def printGrid(grid, size):
    print("Grid:")
    for i in range(size):
        row = ""
        for j in range(size):
            row += grid[i][j]
            if (len(grid[i][j]) == 1):
                row += "  "
            elif (len(grid[i][j]) == 2):
                row += " "
        print(row)

class Element:
    x = 0;
    y = 0;
    value = "X";
    explored = []

    def __init__(self, x, y, value, explored):
        self.x = x
        self.y = y
        self.value = value
        self.explored = explored;

    def getUnexploredNeighbors(self, grid, size):
        unexplored = []
        x = self.x;
        y = self.y;
        value = self.value;
        explored = self.explored;
        newExplored = explored.copy();
        newExplored.append([x, y]);
        if x > 0:
            if [x-1, y] not in explored:
                unexplored.append(Element(x-1, y, value + grid[x-1][y], newExplored))
        if x < (size - 1):
            if [x+1, y] not in explored:
                unexplored.append(Element(x+1, y, value + grid[x+1][y], newExplored))
        if y > 0:
            if [x, y-1] not in explored:
                unexplored.append(Element(x, y-1, value + grid[x][y-1], newExplored))
        if y < (size - 1):
            if [x, y+1] not in explored:
                unexplored.append(Element(x, y+1, value + grid[x][y+1], newExplored))
        if x > 0 and y > 0:
            if [x-1, y-1] not in explored:
                unexplored.append(Element(x-1, y-1, value + grid[x-1][y-1], newExplored))
        if x < (size - 1) and y < (size - 1):
            if [x+1, y+1] not in explored:
                unexplored.append(Element(x+1, y+1, value + grid[x+1][y+1], newExplored))
        if x < (size - 1) and y > 0:
            if [x+1, y-1] not in explored:
                unexplored.append(Element(x+1, y-1, value + grid[x+1][y-1], newExplored))
        if x > 0 and y < (size - 1):
            if [x-1, y+1] not in explored:
                unexplored.append(Element(x-1, y+1, value + grid[x-1][y+1], newExplored))
        return unexplored;

    def toString(self):
        return "(" + str(self.x) + ", " + str(self.y) + ") " + self.value + " " + str(self.explored)


def load_words():
    with open(DICT_FILE) as word_file:
    #with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1

def add(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True

def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter

def parseGrid(userInput, size):
    userGrid = []
    letters = userInput.split();
    for i in range(size):
        userGrid.append([])
        for j in range(size):
            userGrid[i].append(letters.pop())
    return userGrid

def parseSize(userInput):
    userInt = int(userInput)
    return userInt;

# Prints out BOGGLE-BOGGLE-BOGGLE as loading bar for fun
def getNextLoadingBarCharacter(count):
    return "BOGGLE-"[count%7]


def main():
    SIZE = parseSize(input("Input grid size: "))
    GRID = parseGrid(input("Input grid: \n"), SIZE)

    printGrid(GRID, SIZE)

    english_words = load_words()
    long_english_words = [word.lower() for word in english_words if len(word) >= 4]

    root = TrieNode('*')
    for word in long_english_words:
        add(root, word)

    print("Trie constructed, starting main loop")

    results = []
    count = 0;
    for i in range(SIZE):
        for j in range(SIZE):
            stack = []
            stack.append(Element(i, j, GRID[i][j], []))
            while len(stack) is not 0:
                currentElement = stack.pop()
                if currentElement.value in long_english_words:
                    results.append(currentElement.value)
                    sys.stdout.write(getNextLoadingBarCharacter(count))
                    sys.stdout.flush()
                    count += 1
                if find_prefix(root, currentElement.value)[0]:
                    stack.extend(currentElement.getUnexploredNeighbors(GRID, SIZE))

    print()
    sorted_list = sorted(results, key=len)
    print(sorted_list)


if __name__ == "__main__":
    main()
