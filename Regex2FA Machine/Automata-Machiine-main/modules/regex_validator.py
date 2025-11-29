"""
Regular Expression Validator
Validates regex syntax for the given alphabet {a, b, c}
Supports both | and + for union operations
"""


class RegexValidator:
    def __init__(self, alphabet={'a', 'b', 'c'}):
        self.alphabet = alphabet
        self.operators = {'|', '*', '(', ')', '+'}
        self.valid_chars = self.alphabet | self.operators

    def validate(self, regex):
        """
        Validates the regular expression.
        Returns: (is_valid: bool, error_message: str)
        """
        if not regex:
            return False, "Regular expression cannot be empty"

        # Check for invalid characters
        for i, char in enumerate(regex):
            if char not in self.valid_chars and char != ' ':
                return False, f"Invalid character '{char}' at position {i}. Only {self.alphabet} and operators (|, +, *, (, )) are allowed."

        # Check for balanced parentheses
        paren_count = 0
        for i, char in enumerate(regex):
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    return False, f"Unmatched closing parenthesis at position {i}"

        if paren_count > 0:
            return False, "Missing closing parenthesis"
        elif paren_count < 0:
            return False, "Missing opening parenthesis"

        # Check for invalid repetition (e.g., a++, a**, *a)
        for i in range(len(regex) - 1):
            if regex[i] == '*' and regex[i + 1] == '*':
                return False, f"Invalid repetition '**' at position {i}"
            if regex[i] == '+' and regex[i + 1] == '+':
                return False, f"Invalid repetition '++' at position {i}"

        # Check if * or + appears at the beginning
        if regex[0] in ['*', '+']:
            return False, f"'{regex[0]}' operator cannot be at the beginning"

        # Check for invalid operator placement
        for i in range(len(regex) - 1):
            # Skip spaces
            if regex[i] == ' ' or regex[i + 1] == ' ':
                continue
                
            # Check for empty parentheses
            if regex[i] == '(' and regex[i + 1] == ')':
                return False, f"Empty parentheses at position {i}"

            # Check for | or + at wrong positions
            if regex[i] in ['|', '+']:
                if i == 0 or i == len(regex) - 1:
                    return False, f"Union operator '{regex[i]}' cannot be at the beginning or end"
                if regex[i - 1] in ['|', '+', '(']:
                    return False, f"Invalid operator placement at position {i}"
                if regex[i + 1] in ['|', '+', ')', '*']:
                    return False, f"Invalid operator placement at position {i}"

        return True, "Valid regular expression"

    def preprocess(self, regex):
        """
        Preprocesses the regex by:
        1. Replacing '+' with '|' for union (standardizing to formal notation)
        2. Adding explicit concatenation operator '.'
        """
        # Replace '+' with '|' for standard union operation
        regex = regex.replace('+', '|')
        
        result = []
        concat_operators = self.alphabet | {')', '*'}
        concat_follows = self.alphabet | {'('}

        for i in range(len(regex)):
            # Skip spaces
            if regex[i] == ' ':
                continue
                
            result.append(regex[i])

            if i < len(regex) - 1:
                current = regex[i]
                next_char = regex[i + 1]

                # Skip if next character is space
                if next_char == ' ':
                    continue

                # Add '.' between:
                # - letter and letter: ab -> a.b
                # - letter and '(': a( -> a.(
                # - ')' and letter: )a -> ).a
                # - ')' and '(': )( -> ).(
                # - '*' and letter: a*b -> a*.b
                # - '*' and '(': a*( -> a*.(

                if current in concat_operators and next_char in concat_follows:
                    result.append('.')

        return ''.join(result)