## Fuzzy FSM implemented using NFA
import docx2txt
import re

class Automaton:
    def __init__(self, pattern, threshold):
        ## Initialize NFA
        self.pattern = pattern
        self.m = len(pattern)

        ## Monitor Q State
        self.state = 'q0'
        self.position = 0

        ## Monitor NFA Grade
        self.grade = 0

        ## Define Final State
        self.final_state = pattern[(round(len(pattern)*threshold))-1]
        self.final_position = round(len(pattern)*threshold)

    ## Next State Class Function
    def next_state(self, character):
        if not self.state == 'Trap State':
            try:
                if character == self.pattern[self.position]:
                    self.state = self.pattern[self.position]
                    self.position += 1
                else:
                    self.state = 'Trap State'
            except IndexError:
                self.state = 'Trap State'

    ## Membership Grade Class Function
    def membership_grade(self):
        if self.isFinalState():
            self.grade = 1
        else:
            self.grade = self.position/self.m

    ## Final State Class Function
    def isFinalState(self):
        if self.position == self.final_position:
            return True
        else:
            return False

def fuzzyFSM(pattern, string, threshold):
    ## Initialize Automaton
    automaton = Automaton(pattern.lower(), threshold)

    ## Debug Print Line
    print('Now Comparing Word: [{}] and Pattern: [{}]'.format(string, pattern))
    for i in string.lower():
        ## Debug Print Line
        print('Automaton State: ' + automaton.state)
        print('Character Being Read :' + i)

        ## Automaton Next State
        automaton.next_state(i)
        print('Transitioned to Next State Successful')

        ## Debug Print Line
        ## print('Automaton New State: ' + automaton.state)

    ## Calculate Membership Grade of Automaton 
    automaton.membership_grade()
    print('Automaton Membership Grade Successfully Calculated')

    ## Debug Print Line
    print('Results:')
    print('Final Position: ' + str(automaton.final_position))
    print('Position: ' + str(automaton.position))
    print('Final State: ' + str(automaton.isFinalState()))
    print('Grade: ' + str(automaton.grade))
    
    if automaton.grade >= threshold:
        return True
    else:
        return False
        
def get_text_from_docx(filename):
    text = docx2txt.process(filename)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def compare_documents(filename1, filename2, threshold):
    pattern_text = get_text_from_docx(filename1).split()
    string_text = get_text_from_docx(filename2).split()

    ## Min Words between Two DOCX
    n = min(len(pattern_text), len(string_text))

    ## Matches Counter
    matches = 0
    
    ## Iteration
    for i in range(n):
        match_result = fuzzyFSM(pattern_text[i], string_text[i], threshold)

        if match_result:
            print('Match Found\n\n')
            matches += 1
        else:
            print('Match Not Found\n\n')
    print("Matches: " + str(matches))
    print("Total # of String: " + str(n))
    return matches / n

if __name__ == "__main__":
    filename1 = "test 1/document1.docx"
    filename2 = "test 1/document2.docx"
    threshold = 1

    similarity = compare_documents(filename1, filename2, threshold)
    print(f"Similarity: {similarity*100:.2f}%")
