import nltk

def get_tense(text):
    """Returns a number which represents the tense.

    Return values:
        Simple Present: 0
        Present Progressive: 1
        Simple Past: 2
        Past Progressive: 3
        Simple Present Perfect: 4
        Present Perfect Progressive: 5
        Simple Past Perfect: 6
        Past Perfect Progressive: 7
        Will Future: 8
    """

    # Order matters
    if is_WillFuture(text):
        return 8
    elif is_PresentPerfectProgressive(text):
        return 5
    elif is_PastPerfectProgressive(text):
        return 7
    elif is_SimplePastPerfect(text):
        return 6
    elif is_PresentProgressive(text):
        return 1
    elif is_PastProgressive(text):
        return 3
    elif is_SimplePresentPerfect(text):
        return 4
    elif is_SimplePresent(text):
        return 0
    elif is_SimplePast(text):
        return 2
    else:
        return 9

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
