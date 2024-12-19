from validator_collection import validators, checkers, errors

response = input("What's your email address? ")
print("Valid") if checkers.is_email(response) else print("Invalid")