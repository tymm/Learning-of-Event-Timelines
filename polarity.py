import re

# returns 0 for affirmative and 1 for negative
def get_polarity(text):
    if re.match(r".*(don't|dont|not).*", text):
        return 1
    else:
        return 0
