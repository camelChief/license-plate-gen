import os
import math

os.system('mode con: cols=65')
print('\033[90;107m')

lexiconFile = open('lexicon.txt', 'r')

rawLexicon = []
lexiconSize = 0
for word in lexiconFile:
    rawLexicon.append(word.rstrip())
    lexiconSize += 1

substitutes = {
    'A': 4,
    'B': 8,
    'E': 3,
    'I': 1,
    'O': 0,
    'S': 5,
}

class PlateSearch:
    def __init__(self, plateFormat):
        self.lexicon = []
        self.plates = []
        
        self.plateFormat = plateFormat
        self.plateLength = len(plateFormat)
        self.numericalIndex = []

        for word in rawLexicon:
            if len(word) == self.plateLength:
                self.lexicon.append(word)

        for index in range(self.plateLength):
            if self.plateFormat[index] == '1':
                self.numericalIndex.append(index)

    def search(self):
        searchSize = 0
        
        for word in self.lexicon:
            plate = list(word.upper())
            hasSubstitute = True

            searchSize += 1
            if searchSize % 1096 == 0 and searchSize < 58000:
                display(
                    'Searching lexicon...',
                    ['█' * (searchSize // 1096)],
                    False,
                    False
                )
            
            for index in self.numericalIndex:
                if plate[index] not in substitutes:
                    hasSubstitute = False
                    break

                plate[index] = str(substitutes[plate[index]])

            if hasSubstitute:
                plate = ''.join(plate)
                self.plates.append(plate)

        display(
            'Search complete.',
            [
                '█' * 53,
                '',
                '58,109 words searched.',
                '{} plates discovered.'.format(len(self.plates))
            ],
            {
                'p': 'Print plates',
                'q': 'Return home'
            },
            True
        )
        # print('Search complete.')

    def print(self):
        '''
            calculate how many columns there should be
            divide the total number by the number of columns
                ceiling that number
            split plates list into segments of that number
            add in order from each to rows
        '''
        
        columns = 53 // (self.plateLength + 1)
        rows = math.ceil(len(self.plates) / columns)

        printList = []
        for c in range(columns):            
            for r in range(rows):
                if c == 0:
                    printList.append('')

                index = r + (c * rows)
                if index == len(self.plates):
                    break
                
                printList[r] += self.plates[index] + ' '

        display(
            'Generated plates:',
            printList,
            {
                'q': 'Return home'
            },
            True
        )
            
# 49 options
# 54 heading
def display(heading, body, actions, acceptInput):
    os.system('cls')

    render = '\n\
    ╔═══════════════════════════════════════════════════════╗\n\
    ║  ▄▄▄▄  ▄      ▄▄▄  ▄▄▄▄▄  ▄▄▄       ▄▄▄   ▄▄▄  ▄   ▄  ║\n\
    ║  █   █ █     █   █   █     ▄█▄  ♦  █ ▄▄▄   ▄█▄ █▀▄ █  ║\n\
    ║  █▀▀▀  █▄▄▄▄ █▀▀▀█   █   ▀▄▄▄▀     ▀▄▄▄▀ ▀▄▄▄▀ █  ▀█  ║\n\
    ║                                                       ║\n\
    ║            A DUMB APP FROM CALEB CAMPBELL             ║\n\
    ╚═══════════════════════════════════════════════════════╝\n'

    render += '\
    ┌───────────────────────────────────────────────────────┐\n\
    │ {} │\n'.format(heading.ljust(53))

    if body:
        render += '\
    ├───────────────────────────────────────────────────────┤\n'

        for line in body:
            line = line.ljust(53)
            render += '    │ {} │\n'.format(line)

    render += '\
    └───────────────────────────────────────────────────────┘\n'

    if actions:
        render += '\
    ┌───────────────────────────────────────────────────────┐\n'
        
        for key in actions:
            action = actions[key].ljust(48)
            render += '    │ ({}): {} │\n'.format(key, action)
            
        render += '\
    └───────────────────────────────────────────────────────┘\n'

    if acceptInput:
        render += '     >> '

    print(render, end = '')

def generate():
    display(
        'Enter the format of the plate:',
        [
            'Must be in format \'AA11AA\' where \'A\' represents a',
            'single alphabet character and \'1\' represents a single',
            'numerical character.'
        ],
        False,
        True
    )

    plateFormat = input()
    newPlateSearch = PlateSearch(plateFormat)

    newPlateSearch.search()
    tempInput = input()
    if tempInput in ('p', 'P'):
        newPlateSearch.print()
        input()
    elif tempInput in ('q', 'Q'):
        return

def generateWithFormatting():
    return # do nothing

def generateMultiple():
    return # do nothing

def displayHelp():
    display(
        'Help:',
        [
            'This app generates all words you can make with a',
            'certain format of plate, where some numbers on the',
            'plate represent letters - e.g. \'GR34SY\'. In order',
            'to generate plates, go to the generate function',
            'and enter the format of the plate.',
            '',
            'For example, if the plates in your state are always',
            'in the format \'ABC12D\' (three letters, two digits',
            'and a letter) and you\'d like to generate plates in',
            'that format, enter the value \'AAA11A\'. As denote',
            'letters, 1s denote digits.',
        ],
        {
            'q': 'Return home'
        },
        True
    )

    actionKey = input()
    if actionKey in ('q', 'Q'):
        return

def main():
    while True:
        
        # clear the screen
        os.system('cls')

        # set text values before displaying
        title = 'Select an option to continue:'
        body = False
        actions = {
            'g': 'Generate a plate',
            # 'f': 'Generate a plate with formatting',
            # 'm': 'Generate multiple plates',
            'h': 'Help',
            'q': 'Quit'
        }
        acceptInput = True
        # display home screen
        display(title, body, actions, acceptInput)

        # read user selection
        actionKey = input()
        if actionKey in ('g', 'G'):
            generate()
        # elif actionKey in ('f', 'F'):
            # generateWithFormatting()
        # elif actionKey in ('m', 'M'):
            # generateMultiple()
        elif actionKey in ('h', 'H'):
            displayHelp()
        elif actionKey in ('q', 'Q'):
            print('\033[0m')
            os.system('cls')
            quit()

# get the party started
main()
