import re

def get_polarity(text):
    """Returns 0 for affirmative and 1 for negative."""
    if re.match(r".*(don't|dont|not).*", text):
        return 1
    else:
        return 0
