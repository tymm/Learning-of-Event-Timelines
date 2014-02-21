import nltk

def get_tense(text):
    """
    SimplePresent: 0
    PresentProgressive: 1
    SimplePast: 2
    PastProgressive: 3
    SimplePresentPerfect: 4
    PresentPerfectProgressive: 5
    SimplePastPerfect: 6
    PastPerfectProgressive: 7
    WillFuture: 8
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

# nltk tags:
# V Verb (is, has, make, do, see, run)
# VD Past Tense (said, took, told, made, asked)
# VG present participle (making, going, playing, working)
# VN past participle (given, taken, begun, sung)

def get_tags(text):
    # The default tagger doesn't tag questions in the right way, so lets make him better
    default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
    model = {'Will': 'MD', 'Had': 'VBD', 'Have': 'VBP'}
    tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)

    tokens = nltk.word_tokenize(text)
    tags = tagger.tag(tokens)
    tags = [tag[1] for tag in tags]
    return tags

def is_SimplePresent(text):
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
    tags = get_tags(text)

    # VBD - went, liked
    if 'VBD' in tags:
        return True
    else:
        return False

def is_PastProgressive(text):
    tags = get_tags(text)

    # VBD + VBG - was/were + ing
    if 'VBD' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_SimplePresentPerfect(text):
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
    tags = get_tags(text)

    # had + past participle
    if 'VBD' in tags and 'VBN' in tags:
        return True
    else:
        return False

def is_PastPerfectProgressive(text):
    tags = get_tags(text)

    # had + been + ing
    if 'VBD' in tags and 'VBN' in tags and 'VBG' in tags:
        return True
    else:
        return False

def is_WillFuture(text):
    tags = get_tags(text)

    # will + infinitiv
    if 'MD' in tags and 'VB' in tags:
        return True
    else:
        return False
