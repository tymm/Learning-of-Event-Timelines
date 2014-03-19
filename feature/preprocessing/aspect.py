import re
from tense import get_tags

class Aspects:
    none = 0
    progressive = 1
    perfect = 2
    perfect_progressive = 3

def get_aspect(text):
    """Determines whether some text is either in the progressive-, perfect-, progressive_perfect aspect or none."""
    if re.match(r'.*(was|were|is|am|are|will be|would be) \w+ing', text):
        return Aspects.progressive
    elif re.match(r'.*(have been|has been|had been|will have been|would have been) \w+ing', text):
        return Aspects.perfect_progressive
    elif is_Perfect_Aspect(text):
        return Aspects.perfect
    else:
        return Aspects.none

def is_Perfect_Aspect(text):
    """Determines if some text is in the perfect aspect."""
    tags = get_tags(text)

    # has + gone
    if 'VBZ' in tags and 'VBN' in tags:
        return True

    # have + gone
    if 'VBD' in tags and 'VBN' in tags:
        return True

    # will + have + gone
    if 'MD' in tags and 'VB' in tags and 'VBN' in tags:
        return True

    # will + have + gone
    if 'MD' in tags and 'VBP' in tags and 'VBN' in tags:
        return True
    else:
        return False
