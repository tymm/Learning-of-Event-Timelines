from parser import parse_XML
from feature.feature import Feature

def get_sentences(number, class_id, annotations="union"):
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

                print "---------------"
                print "Source event: " +rel.source.content
                print rel.source.sentence
                print
                print "Target event: " +rel.target.content
                print rel.target.sentence
                print "---------------"
                print

                # Get next sentence from the next text
                go_to_next_textfile = True

if __name__ == "__main__":
    get_sentences(3, 1)
