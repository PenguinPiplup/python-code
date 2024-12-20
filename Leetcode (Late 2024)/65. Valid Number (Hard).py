"""
Link: https://leetcode.com/problems/valid-number/description/
"""

class Solution:
    def isNumber(self, s: str) -> bool:
        exp1 = s.find("e")
        exp2 = s.find("E")

        # Case 1: No exponents present
        if exp1 == -1 and exp2 == -1:
            return self.isDecimal(s)
        # Case 2: Multiple exponents clearly present
        elif exp1 > -1 and exp2 > -1:
            return False
        # Case 3: May or may not have only one exponent
        else:
            exp = max(exp1, exp2)
            return self.isDecimal(s[0:exp]) and self.isInteger(s[exp+1:])

    # check if string given is a valid integer number (optional +/- followed by min 1 digits) (without exponents and ".")
    def isInteger(self, string):
        if string == "":
            return False

        # Remove the optional sign if there is any
        if string[0] == "+" or string[0] == "-":
            string = string[1:]
    
        if string == "":
            return False
        else:
            for char in string:
                if not char.isdecimal():
                    return False

            return True

    # check if input is a valid decimal number (optional +/- followed by min 1 digit, max 1 ".") (without exponents)
    def isDecimal(self, string):
        if string == "":
            return False
            
        # Remove the optional sign if there is any
        if string[0] == "+" or string[0] == "-":
            string = string[1:]
    
        if string == "" or string == ".":
            return False
        else:
            dot_count = 0
            for char in string:
                if not char.isdecimal():
                    if dot_count == 0 and char == ".":
                        dot_count += 1
                    else:
                        return False

            return True