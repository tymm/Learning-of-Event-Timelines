import re
from tense import get_tags, get_chunks, get_area_of_interest, get_index_of_event

class Aspects:
    none = 0
    progressive = 1
    perfect = 2
    perfect_progressive = 3

def get_aspect(sentence, event_text, num_words_as_event_before_event):
    """Determines whether some text is either in the progressive-, perfect-, progressive_perfect aspect or none."""
    # Get chunk and tags for the sentence for further analyzing
    # Assumption: chunks and tags have same length. Not always the case though
    chunks = get_chunks(sentence)
    tags = get_tags(sentence)

    # Get the index of the event in chunks
    event_index = get_index_of_event(chunks, event_text, num_words_as_event_before_event)

    # Search through the sentence for the area of interest
    start_index, end_index = get_area_of_interest(tags, event_index)

    text = " ".join(chunks[start_index:end_index])

    if re.match(r'.*(have been|has been|had been) \w+ing', text):
        return Aspects.perfect_progressive
    elif re.match(r'.*(was|were|is|am|are|be|be) \w+ing', text):
        return Aspects.progressive
    elif is_Perfect_Aspect(tags[start_index:end_index], chunks[start_index:end_index]):
        return Aspects.perfect
    else:
        return Aspects.none

def is_Perfect_Aspect(tags, chunks):
    """Determines if some text is in the perfect aspect."""
    if "have" in chunks or "had" in chunks or "has" in chunks:
        # has + 3. form
        if 'VBZ' in tags and 'VBN' in tags:
            return True

        # had + 3. form
        if 'VBD' in tags and 'VBN' in tags:
            return True

        if 'VB' in tags and 'VBN' in tags:
            return True

        if 'VBP' in tags and 'VBN' in tags:
            return True

    return False
