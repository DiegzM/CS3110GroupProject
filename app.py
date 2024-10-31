# Define the NFA object
class NFA:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
    
    def epsilon_closure(self, state):
        closure = {state}
        stack = [state]

        while stack:
            current_state = stack.pop()
            if (current_state, '') in self.transitions:
                for next_state in self.transitions[(current_state, '')]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def is_digit(self, char):
        return '0' <= char <= '9'
    def is_nonzerodigit(self, char):
        return '1' <= char <= '9'
    def is_hexdigit(self, char):
        return '0' <= char <= '9' or 'A' <= char <= "F" or 'a' <= char <= 'f'
    def is_octdigit(self, char):
        return '0' <= char <= '7'
    
    def accepts(self, input_string):
        current_states = self.epsilon_closure(self.start_state)
        for char in input_string:
            next_states = set()
            for state in current_states:
                # Check for direct character match
                if (state, char) in self.transitions:
                    next_states.update(self.transitions[(state, char)])
                # Check if transition is all digits and character is a digit
                if (state, 'digit') in self.transitions and self.is_digit(char):
                    next_states.update(self.transitions[(state, 'digit')])
                # Check if transition is all nonzerodigits and character is a nonzerodigit
                if (state, 'nonzerodigit') in self.transitions and self.is_nonzerodigit(char):
                    next_states.update(self.transitions[(state, 'nonzerodigit')])
                # Check if transition is all hexdigits and character is a hexdigit
                if (state, 'hexdigit') in self.transitions and self.is_hexdigit(char):
                    next_states.update(self.transitions[(state, 'hexdigit')])
                # Check if transition is all octdigits and character is a octdigit
                if (state, 'octdigit') in self.transitions and self.is_octdigit(char):
                    next_states.update(self.transitions[(state, 'octdigit')])
            current_states = set()
            for state in next_states:
                current_states.update(self.epsilon_closure(state))
            if not current_states:
                return False
        return any(state in self.final_states for state in current_states)

# Function to create the decinteger NFA
def create_integer_nfa():
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14',
              'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30',
              'q31', 'q32', 'q33', 'q34', 'q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q42', 'q43', 'q44', 'q45', 'q46', 'q47'}                  
    alphabet = {'hexdigit', 'o', 'O', 'x', 'X', '_'}                  
    transitions = {
        # Starting state
        ('q0', ''): ['q1', 'q8', 'q15', 'q31'],
        # Decinteger Transitions
        ('q1', 'nonzerodigit'): ['q2'],
        ('q2', ''): ['q3'],
        ('q3', ''): ['q4'],
        ('q4', ''): ['q5'],
        ('q4', '_'): ['q5'],
        ('q5', ''): ['q6'],
        ('q6', 'digit'): ['q7'],
        ('q7', ''): ['q4'],
        ('q8', '0'): ['q9'],
        ('q9', '0'): ['q9'],
        ('q9', ''): ['q10'],
        ('q10', ''): ['q11'],
        ('q11', ''): ['q12'],
        ('q11', '_'): ['q12'],
        ('q12', ''): ['q13'],
        ('q13', '0'): ['q14'],
        ('q14', ''): ['q11'],
        # Hexadecimal Transitions
        ('q15', '0'): ['q16'],
        ('q16', ''): ['q17'],
        ('q17', ''): ['q18', 'q20'],
        ('q18', 'x'): ['q19'],
        ('q19', ''): ['q22'],
        ('q20', 'X'): ['q21'],
        ('q21', ''): ['q22'],
        ('q22', ''): ['q23'],
        ('q22', '_'): ['q23'],
        ('q23', ''): ['q24'],
        ('q24', ''): ['q25'],
        ('q25', 'hexdigit'): ['q26'],
        ('q26', ''): ['q27'],
        ('q27', ''): ['q28'],
        ('q28', ''): ['q29'],
        ('q28', '_'): ['q29'],
        ('q29', 'hexdigit'): ['q30'],
        ('q30', ''): ['q28'],
        # Octal Transitions
        ('q31', '0'): ['q32'],
        ('q32', ''): ['q33'],
        ('q33', ''): ['q34', 'q36'],
        ('q34', 'o'): ['q35'],
        ('q35', ''): ['q38'],
        ('q36', 'O'): ['q37'],
        ('q37', ''): ['q38'],
        ('q38', ''): ['q39'],
        ('q38', '_'): ['q39'],
        ('q39', ''): ['q40'],
        ('q40', 'octdigit'): ['q41'],
        ('q41', ''): ['q42'],
        ('q42', ''): ['q43'],
        ('q43', ''): ['q44'],
        ('q44', ''): ['q45'],
        ('q44', '_'): ['q45'],
        ('q45', ''): ['q46'],
        ('q46', 'octdigit'): ['q47'],
        ('q47', ''): ['q44'],
    }
    start_state = 'q0'                     
    final_states = {'q3', 'q7', 'q10', 'q14', 'q27', 'q30', 'q43', 'q47'} 

    nfa = NFA(states, alphabet, transitions, start_state, final_states)
    return nfa

# Function to remove the sign from the string
def normalize_string(string):
    normalized_string = string
    if string:
        if string[0] in '+-':
            normalized_string = string[1:]
    return normalized_string

# ------- INITIALIZE NFAs ----------
decinteger_nfa = create_integer_nfa()

# ------- PROGRAM MODES ----------
def manual_input_mode():
    while True:
        print()
        input_string = input("Enter a decinteger, hexinteger, octinteger, or type b to go back: ")
        input_string = normalize_string(input_string)
        if input_string == 'b': break
        print(decinteger_nfa.accepts(input_string))

def file_input_mode():
    while True:
        print()
        input_file = input("Enter a file (with extension .txt), or type b to go back: ")
        if input_file == "b": break
        print()
        try:
            with open("out.txt", 'w') as output_file:
                output_file.write("")
            with open(input_file, 'r') as input_file:
                for line in input_file:
                    input_string = line.strip()
                    input_string = normalize_string(input_string)
                    output_text = input_string + ": " + str(decinteger_nfa.accepts(input_string))
                    print(output_text)
                    with open('out.txt', 'a') as output_file:
                        output_file.write(output_text + '\n')
            print('\nResults saved to out.txt')   

        except FileNotFoundError:
            print("Error: File Not Found")


# ------- MAIN PROGRAM LOOP -----------

# Main loop
while True:
    print()
    option = input("Type 1 to manually input literals, or type 2 to read a file of inputs, or type any other key to quit: ")
    if option == '1': manual_input_mode()
    elif option == '2': file_input_mode()
    else: 
        print()
        break