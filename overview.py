from parser import parse_XML
from feature.feature import Feature

def get_sentences(number, class_id, annotations="intersected"):
    """Returns number sentences which have the relation type class_id.

    Useful if you need to get an overview over sentences with a certain temporal relation.

    """
    data = parse_XML("fables-100-temporal-dependency.xml", "McIntyreLapata09Resources/fables")

    i=0
    go_to_next_textfile = False

    for txt in data.textfiles:
        go_to_next_textfile = False

        if annotations == "union":
            txt.compute_union_relations()
        elif annotations == "intersected":
            txt.compute_intersection_relations()

        for rel in txt.relations:
            f = Feature(rel)

            if f.get_class() == class_id and go_to_next_textfile == False:
                # Stop if number relations are reached
                if i >= number:
                    break
                i += 1

                if rel.target.sentence == rel.source.sentence:
                    print "---------------"
                    print "Source event: " +rel.source.content
                    print "Target event: " +rel.target.content
                    print rel.target.sentence
                    print
                    print "Source Surrounding: " + rel.source.surrounding
                    print "Target Surrounding: " + rel.target.surrounding
                else:
                    print "---------------"
                    print "Source event: " +rel.source.content
                    print "Whole sentence " +rel.source.sentence
                    print "Surrounding" + rel.source.surrounding
                    print
                    print "Target event: " +rel.target.content
                    print "Whole sentence: " + rel.target.sentence
                    print "Surrounding: " + rel.target.surrounding

                tense_source = f.get_tense_source()
                tense_target = f.get_tense_target()
                if tense_source == 0:
                    print "Estimated tense for source event: None"
                elif tense_source == 1:
                    print "Estimated tense for source event: Present"
                elif tense_source == 2:
                    print "Estimated tense for source event: Past"
                elif tense_source == 3:
                    print "Estimated tense for source event: Future"

                if tense_target == 0:
                    print "Estimated tense for target event: None"
                elif tense_target == 1:
                    print "Estimated tense for target event: Present"
                elif tense_target == 2:
                    print "Estimated tense for target event: Past"
                elif tense_target == 3:
                    print "Estimated tense for target event: Future"

                aspect_source = f.get_aspect_source()
                aspect_target = f.get_aspect_target()
                if aspect_source == 0:
                    print "Estimated aspect for source event: None"
                elif aspect_source == 1:
                    print "Estimated aspect for source event: Progressive"
                elif aspect_source == 2:
                    print "Estimated aspect for source event: Perfect"
                elif aspect_source == 3:
                    print "Estimated aspect for source event: Perfect Progressive"

                if aspect_target == 0:
                    print "Estimated aspect for target event: None"
                elif aspect_target == 1:
                    print "Estimated aspect for target event: Progressive"
                elif aspect_target == 2:
                    print "Estimated aspect for target event: Perfect"
                elif aspect_target == 3:
                    print "Estimated aspect for target event: Perfect Progressive"

                print "Distance between events: " + str(f.get_distance())


                print "---------------"
                print

                # Get next sentence from the next text
                go_to_next_textfile = True

if __name__ == "__main__":
    # Get 20 sentences of class 1
    get_sentences(20, 1)
