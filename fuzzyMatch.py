import docx2txt
import math

## Time Complexity: O(nm)
## n = length of text1, map = length of text2
## Compare_Documents function has a for loop that iterates over n and the fuzzy_string_match function has a for loop that iterates over m.

class Automaton:
    def __init__(self, pattern):
        self.pattern = pattern
        self.m = len(pattern)
        self.state = 0
        self.grades = [0] * self.m

    def update(self, character):
        grade = membership_function(character, self.pattern[self.state])
        self.state = next_state(self.state, character, self.pattern)
        self.grades = update_grades(self.grades, grade)
        print(f"Character: {character}, Grade: {grade}, State: {self.state}, Grades: {self.grades}")

# This function returns a new list where each element is the maximum of the corresponding element in grades and grade.
def update_grades(grades, grade):
    return [max(grade, g) for g in grades]

def fuzzy_string_match(T, P, threshold):
    # Get the length of the text
    n = len(T)
    # Create an automaton for the pattern
    automaton = Automaton(P)
    # Initialize a variable to store the maximum membership grade
    max_grade = 0
    # Iterate over the text
    for i in range(n):
        # Update the automaton with the current character in the text
        automaton.update(T[i])
    # Compute the overall grade as the average of all the grades in the list
    overall_grade = sum(automaton.grades) / len(automaton.grades)
    # Test if the overall grade is above the threshold
    if overall_grade >= threshold:
        return True
    else:
        return False

def membership_function(a, b):
    """Calculate the membership grade for two strings.
    
    Args:
    a: string, the first string
    b: string, the second string
    
    Returns:
    float, the membership grade for the two strings
    """
    # Initialize a counter variable
    count = 0
    # Iterate over the characters in the strings
    for c1, c2 in zip(a, b):
        # Increment the counter if the characters are equal
        if c1 == c2:
            count += 1
    # Calculate the membership grade as the ratio of the number of matching characters to the length of the strings
    grade = count / len(a)
    # Return the membership grade
    return grade

def next_state(q, a, P):
    # m is the length of the pattern.
    m = len(P)
    # k is the counter variable used to keep track of how many characters in the pattern match the current character.
    k = 0
    # This while loop increments k for as long as the character at index k in the pattern is equal to the current character and k is less than the length of the pattern.
    while k < m and P[k] == a:
        k += 1
    # Return the minimum of k and q+1 if k is less than m, else return q
    return min(k, q+1) if k < m else q

def get_text_from_docx(filename):
    return docx2txt.process(filename)

def compare_documents(filename1, filename2, threshold):
    # Split the text of the first document into a list of words
    text1 = get_text_from_docx(filename1).split()
    # Split the text of the second document into a list of words
    text2 = get_text_from_docx(filename2).split()
    # Get the minimum number of words between the two documents
    n = min(len(text1), len(text2))
    # Initialize a counter for the number of matches found
    matches = 0
    # Iterate over each word in the documents
    for i in range(n):
        # Get the shifts of the match between the two words
        shifts = fuzzy_string_match(text1[i], text2[i], threshold)
        
        # If there are any shifts, it means that a match was found
        if shifts:
            print("Shifts: " + str(shifts))
            matches += 1
    # Return the ratio of matches to total number of words as the percentage of similarity
    print("Matches: " + str(matches))
    print("Total # of String: " + str(n))
    return matches / n

filename1 = "test 4/document1.docx"
filename2 = "test 4/document2.docx"
threshold = 0.5

similarity = compare_documents(filename1, filename2, threshold)
print(f"Similarity: {similarity*100:.2f}%")
