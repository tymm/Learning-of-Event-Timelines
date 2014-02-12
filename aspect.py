import re
# determines whether some text is either in the simple-, progressive- or perfect aspect
def get_aspect(text):
    if re.match('.*(was|were|is|are|will be|had been|has been|have been|will have been) \w+ing', text):
        return "progressive"
    elif re.match('.*(had|has|have|will have) \w+ed', text):
        return "perfect"
    elif re.match('.*(will|shall)* \w+(s|ed)*', text):
        return "simple"
    else:
        return None
