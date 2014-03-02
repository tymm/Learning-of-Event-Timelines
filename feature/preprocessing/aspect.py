import re
from tense import get_tags
def get_aspect(text):
    """Determines whether some text is either in the simple-, progressive- or perfect aspect."""
    if re.match(r'.*(was|were|is|are|will be|had been|has been|have been|will have been) \w+ing', text):
        return "progressive"
    elif is_PerfectAspect(text):
        return "perfect"
    elif re.match('.*(will|shall)* \w+(s|ed)*', text):
        return "simple"
    else:
        return None

def is_PerfectAspect(text):
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
