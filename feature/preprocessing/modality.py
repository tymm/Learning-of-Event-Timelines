import re

def get_modality(text):
    """Returns 1 if there is a modal verb, 0 otherwise."""
    if re.match(r".*(may|can|must|ought|will|shall|need|dare|might|could|would|should).*", text):
        return 1
    else:
        return 0
