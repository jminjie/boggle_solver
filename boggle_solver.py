import enchant 

SIZE = 5;

grid = []
grid.append([]); grid.append([]); grid.append([]); grid.append([]); grid.append([]);
grid[0].append('e');  grid[0].append('i'); grid[0].append('h'); grid[0].append('v'); grid[0].append('r');
grid[1].append('in'); grid[1].append('o'); grid[1].append('y'); grid[1].append('a'); grid[1].append('m');
grid[2].append('r');  grid[2].append('l'); grid[2].append('e'); grid[2].append('u'); grid[2].append('r');
grid[3].append('s');  grid[3].append('n'); grid[3].append('s'); grid[3].append('o'); grid[3].append('c');
grid[4].append('p');  grid[4].append('e'); grid[4].append('n'); grid[4].append('i'); grid[4].append('b');

def printGrid():
    for i in range(SIZE):
        row = ""
        for j in range(SIZE):
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

    def getUnexploredNeighbors(self):
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
        if x < 4:
            if [x+1, y] not in explored:
                unexplored.append(Element(x+1, y, value + grid[x+1][y], newExplored))
        if y > 0:
            if [x, y-1] not in explored:
                unexplored.append(Element(x, y-1, value + grid[x][y-1], newExplored))
        if y < 4:
            if [x, y+1] not in explored:
                unexplored.append(Element(x, y+1, value + grid[x][y+1], newExplored))
        if x > 0 and y > 0:
            if [x-1, y-1] not in explored:
                unexplored.append(Element(x-1, y-1, value + grid[x-1][y-1], newExplored))
        if x < 4 and y < 4:
            if [x+1, y+1] not in explored:
                unexplored.append(Element(x+1, y+1, value + grid[x+1][y+1], newExplored))
        if x < 4 and y > 0:
            if [x+1, y-1] not in explored:
                unexplored.append(Element(x+1, y-1, value + grid[x+1][y-1], newExplored))
        if x > 0 and y < 4:
            if [x-1, y+1] not in explored:
                unexplored.append(Element(x-1, y+1, value + grid[x-1][y+1], newExplored))
        return unexplored;

    def toString(self):
        return "(" + str(self.x) + ", " + str(self.y) + ") " + self.value + " " + str(self.explored)

def testGetUnexplored():
    stack = []
    stack.append(Element(0, 0, grid[0][0], []));
    assert stack[0].value == 'e';

    neighbors = stack[0].getUnexploredNeighbors();
    # order doesn't matter
    assert neighbors[0].value == 'ein'
    assert neighbors[1].value == 'ei'
    assert neighbors[2].value == 'eo'

    secondNeighbors = neighbors[2].getUnexploredNeighbors();
    # 'i' and 'in' are repeated because they're not explored by this search node
    assert secondNeighbors[0].value == 'eoi'
    assert secondNeighbors[1].value == 'eol'
    assert secondNeighbors[2].value == 'eoin'
    assert secondNeighbors[3].value == 'eoy'
    assert secondNeighbors[4].value == 'eoe'
    assert secondNeighbors[5].value == 'eor'
    assert secondNeighbors[6].value == 'eoh'

def load_words():
    with open('scrabble.txt') as word_file:
    #with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

from typing import Tuple


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


def dedupe(sortedList):
    lastword = ""
    nodupes = []
    for word in sortedList:
        if word != lastword:
            nodupes.append(word)
        lastword = word
    return nodupes

printGrid()
testGetUnexplored();

english_words = load_words()
long_english_words = [word.lower() for word in english_words if len(word) >= 4]

assert('fate' in long_english_words)

root = TrieNode('*')
for word in long_english_words:
    add(root, word)

print("Trie constructed, starting main loop")
assert(find_prefix(root, "eohar"))
assert not find_prefix(root, "eohar")[0]

results = []
for i in range(SIZE):
    for j in range(SIZE):
        stack = []
        stack.append(Element(i, j, grid[i][j], []))
        while len(stack) is not 0:
            currentElement = stack.pop()
            if currentElement.value in long_english_words:
                results.append(currentElement.value)
                #print(currentElement.value)
            if find_prefix(root, currentElement.value)[0]:
                stack.extend(currentElement.getUnexploredNeighbors())

sorted_list = sorted(results, key=len)
print(dedupe(sorted_list))
