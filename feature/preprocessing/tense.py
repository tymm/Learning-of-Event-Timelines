import nltk

class Tenses:
    none = 0
    present = 1
    past = 2
    future = 3

def get_tense(text):
    """Returns a number which represents the tense.

    Return values:
        None: 0
        Present: 1
        Past: 2
        Future: 3
    """
    if is_Future(text):
        return Tenses.future
    elif is_Past(text):
        return Tenses.past
    elif is_Present(text):
        return Tenses.present
    else:
        return Tenses.none

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

def is_Present(text):
    """Returns true if the text is in a present tense. False otherwise."""

    if is_SimplePresent(text) or is_PresentProgressive(text) or is_SimplePresentPerfect(text) or is_PresentPerfectProgressive(text):
        return True
    else:
        return False

def is_Past(text):
    """Returns true if the text is in a past tense. False otherwise."""

    if is_SimplePast(text) or is_PastProgressive(text) or is_SimplePastPerfect(text) or is_PastPerfectProgressive(text):
        return True
    else:
        return False

def is_Future(text):
    """Returns true if the text is in a future tense. False otherwise."""

    if is_WillFuture(text):
        return True
    else:
        return False

def is_SimplePresent(text):
    """Returns true if text is in the simple present tense. False otherwise."""
    tags = get_tags(text)

    # VBZ - he goes
    if 'VBZ' in tags:
        return True

    # VBP - don't / I go
    if 'VBP' in tags:
        return True
    else:
        return False

def is_PresentProgressive(text):
    """Returns true if text is in the present progressive tense. False otherwise."""
    tags = get_tags(text)

    # VBZ and VBG - is + ing
    if 'VBZ' in tags and 'VBG' in tags:
        return True

    # VBP and VBG - am/are + ing
    if 'VBP' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_SimplePast(text):
    """Returns true if text is in the simple past tense. False otherwise."""
    tags = get_tags(text)

    # VBD - went, liked
    if 'VBD' in tags:
        return True
    else:
        return False

def is_PastProgressive(text):
    """Returns true if text is in the past progressive tense. False otherwise."""
    tags = get_tags(text)

    # VBD + VBG - was/were + ing
    if 'VBD' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_SimplePresentPerfect(text):
    """Returns true if text is in the simple present perfect tense. False otherwise."""
    tags = get_tags(text)

    # has + past participle
    if 'VBZ' in tags and 'VBN' in tags:
        return True

    # have + past participle
    if 'VBP' in tags and 'VBN' in tags:
        return True
    else:
        return False

def is_PresentPerfectProgressive(text):
    """Returns true if text is in the present perfect progressive tense. False otherwise."""
    tags = get_tags(text)

    # have + been + ing
    if 'VBP' in tags and 'VBN' in tags and 'VBG' in tags:
        return True

    # has + been + ing
    if 'VBZ' in tags and 'VBN' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_SimplePastPerfect(text):
    """Returns true if text is in the simple past perfect tense. False otherwise."""
    tags = get_tags(text)

    # had + past participle
    if 'VBD' in tags and 'VBN' in tags:
        return True
    else:
        return False

def is_PastPerfectProgressive(text):
    """Returns true if text is in the past perfect progressive tense. False otherwise."""
    tags = get_tags(text)

    # had + been + ing
    if 'VBD' in tags and 'VBN' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_WillFuture(text):
    """Returns true if text is in the will future tense. False otherwise."""
    tags = get_tags(text)

    # will + infinitiv
    if 'MD' in tags and 'VB' in tags:
        return True
    else:
        return False
