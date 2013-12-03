from lxml import etree
# Count how many events we have per text

def union(event_sets):
    all_in_one = []
    for events in event_sets:
        all_in_one = all_in_one + events

    return [x for i, x in enumerate(all_in_one) if x not in [y for y in all_in_one[:i]]]

def intersection(event_sets):
    events_intersection = event_sets[0]
    for events in event_sets[1:]:
        events_intersection = (set(events) & set(events_intersection))

    return events_intersection


tree = etree.parse("fables-100-temporal-dependency.xml")
root = tree.getroot()

events_per_text_and_annotator = []
count_union = 0
count_intersection = 0

for txt in root.iterchildren('file'):
    # Looking at certain texts

    for annotator in txt.iterdescendants('annotator'):
        # Get the events the annotator annotated
        events = [event.get("text") for event in annotator.iterdescendants('event')]
        events_per_text_and_annotator.append(events)

    # Whats the union of the events annotated for a certain text
    len_union = len(union(events_per_text_and_annotator))
    count_union += len_union

    # Whats the intersection
    len_intersection = len(intersection(events_per_text_and_annotator))
    count_intersection += len_intersection

    del events_per_text_and_annotator[:]

print "Union: " + str(count_union)
print "Intersection: " + str(count_intersection)
