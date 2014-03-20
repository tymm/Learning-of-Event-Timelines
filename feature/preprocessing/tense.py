import nltk

class Tenses:
    none = 0
    present = 1
    past = 2
    future = 3

def get_tense(sentence, event_text, num_words_as_event_before_event):
    """Returns a number which represents the tense.

    Return values:
        None: 0
        Present: 1
        Past: 2
        Future: 3
    """
    # Get chunk and tags for the sentence for further analyzing
    # Assumption: chunks and tags have same length. Not always the case though
    chunks = get_chunks(sentence)
    tags = get_tags(sentence)

    # Get the index of the event in chunks
    event_index = get_index_of_event(chunks, event_text, num_words_as_event_before_event)

    # Search through the sentence for the area of interest
    start_index, end_index = get_area_of_interest(tags, event_index)

    # Check what tense we have in the area of interest
    # Order of ifs is important
    if is_Future(tags[start_index:end_index], chunks[start_index:end_index]):
        return Tenses.future
    elif is_Past(tags[start_index:end_index]):
        return Tenses.past
    elif is_Present(tags[start_index:end_index]):
        return Tenses.present
    else:
        return Tenses.none


def get_area_of_interest(tags, event_index):
    """Returns two indeces which describe the area we are interested in for guessing the tense."""
    return (max(event_index-4, 0), event_index+1)

def get_index_of_event(chunks, event_text, num_words_as_event_before_event):
    """Returns the index of the event in the chunks list."""

    # Get the index of the event we are interested in
    k = 0
    event_index = 0
    for i, chunk in enumerate(chunks):
        if event_text in chunk:
            if k == num_words_as_event_before_event:
                event_index = i
                break
            else:
                k += 1

    return event_index

def get_chunks(text):
    """Returns a list of words."""
    text = text.lower()
    return text.split()

def get_tags(text):
    """Takes a text and returns a list of tags for that text."""

    # The default tagger doesn't tag questions in the right way, so lets make him better
    default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
    model = {'Will': 'MD', 'Had': 'VBD', 'Have': 'VBP'}
    tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)

    tokens = nltk.word_tokenize(text)
    tags = tagger.tag(tokens)
    tags = [tag[1] for tag in tags]
    return tags

def is_Present(tags):
    """Returns true if the text is in a present tense. False otherwise."""

    if "VBP" in tags:
        return True
    elif "VBZ" in tags:
        return True
    elif "VB" in tags:
        return True
    elif "VBG" in tags:
        return True
    else:
        return False

def is_Past(tags):
    """Returns true if the tags is in a past tense. False otherwise."""

    if "VBD" in tags:
        return True
    else:
        return False

def is_Future(tags, chunks):
    """Returns true if the tags is in a future tense. False otherwise."""

    # Rules for future tense
    if "will" in chunks:
        return True

    if "going" in chunks and "to" in chunks:
        index_going = chunks.index("going")
        index_to = chunks.index("to")

        if index_going == (index_to - 1):
            return True

    return False


def is_SimplePresent(tags):
    """Returns true if tags is in the simple present tense. False otherwise."""

    # VBZ - he goes
    if 'VBZ' in tags:
        return True

    # VBP - don't / I go
    if 'VBP' in tags:
        return True
    else:
        return False

def is_PresentProgressive(tags):
    """Returns true if tags is in the present progressive tense. False otherwise."""
    # VBZ and VBG - is + ing
    if 'VBZ' in tags and 'VBG' in tags:
        return True

    # VBP and VBG - am/are + ing
    if 'VBP' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_SimplePast(tags):
    """Returns true if tags is in the simple past tense. False otherwise."""

    # VBD - went, liked
    if 'VBD' in tags:
        return True
    else:
        return False

def is_PastProgressive(tags):
    """Returns true if tags is in the past progressive tense. False otherwise."""

    # VBD + VBG - was/were + ing
    if 'VBD' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_SimplePresentPerfect(tags):
    """Returns true if tags is in the simple present perfect tense. False otherwise."""

    # has + past participle
    if 'VBZ' in tags and 'VBN' in tags:
        return True

    # have + past participle
    if 'VBP' in tags and 'VBN' in tags:
        return True
    else:
        return False

def is_PresentPerfectProgressive(tags):
    """Returns true if tags is in the present perfect progressive tense. False otherwise."""

    # have + been + ing
    if 'VBP' in tags and 'VBN' in tags and 'VBG' in tags:
        return True

    # has + been + ing
    if 'VBZ' in tags and 'VBN' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_SimplePastPerfect(tags):
    """Returns true if tags is in the simple past perfect tense. False otherwise."""

    # had + past participle
    if 'VBD' in tags and 'VBN' in tags:
        return True
    else:
        return False

def is_PastPerfectProgressive(tags):
    """Returns true if tags is in the past perfect progressive tense. False otherwise."""

    # had + been + ing
    if 'VBD' in tags and 'VBN' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_WillFuture(tags):
    """Returns true if tags is in the will future tense. False otherwise."""

    # will + infinitiv
    if 'MD' in tags and 'VB' in tags:
        return True
    else:
        return False
