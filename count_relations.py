from parser import parseXML

data = parseXML("fables-100-temporal-dependency.xml")

# Unions
union_count = 0
union_overlap = 0
union_after = 0
union_before = 0
union_sameas = 0
union_iscontainedin = 0
union_contains= 0
union_includes= 0
union_isincluded= 0
union_norelation= 0

for txt in data.textfiles:
    txt.compute_union_relations()
    for rel in txt.relations_union:
        if rel.time_type == "same_as":
            union_sameas += 1
        elif rel.time_type == "overlap":
            union_overlap += 1
        elif rel.time_type == "after":
            union_after += 1
        elif rel.time_type == "is_contained_in":
            union_iscontainedin += 1
        elif rel.time_type == "before":
            union_before += 1
        elif rel.time_type == "contains":
            union_contains += 1
        elif rel.time_type == "includes":
            union_includes += 1
        elif rel.time_type == "is_included":
            union_isincluded += 1
        elif rel.time_type == "no relations":
            union_norelation += 1
    union_count += txt.relations_union_count


# Intersections
intersetion_count = 0
intersection_overlap = 0
intersection_after = 0
intersection_before = 0
intersection_sameas = 0
intersection_iscontainedin = 0
intersection_contains= 0
intersection_includes= 0
intersection_isincluded= 0
intersection_norelation = 0

for txt in data.textfiles:
    txt.compute_intersection_relations()
    for rel in txt.relations_intersection:
        if rel.time_type == "same_as":
            intersection_sameas += 1
        elif rel.time_type == "overlap":
            intersection_overlap += 1
        elif rel.time_type == "after":
            intersection_after += 1
        elif rel.time_type == "is_contained_in":
            intersection_iscontainedin += 1
        elif rel.time_type == "before":
            intersection_before += 1
        elif rel.time_type == "contains":
            intersection_contains += 1
        elif rel.time_type == "includes":
            intersection_includes += 1
        elif rel.time_type == "is_included":
            intersection_isincluded += 1
        elif rel.time_type == "no relations":
            intersection_norelation += 1
    intersetion_count += txt.relations_intersection_count

print "Intersecting relations: " + str(intersetion_count)
print "same_as: " + str(intersection_sameas)
print "overlap: " + str(intersection_overlap)
print "after: " + str(intersection_after)
print "is_contained_in: " + str(intersection_iscontainedin)
print "before :" + str(intersection_before)
print "contains:" + str(intersection_contains)
print "includes:" + str(intersection_includes)
print "is_included:" + str(intersection_isincluded)
print "no relations:" + str(intersection_norelation)
print
print "Union relations: " + str(union_count)
print "same_as: " + str(union_sameas)
print "overlap: " + str(union_overlap)
print "after: " + str(union_after)
print "is_contained_in: " + str(union_iscontainedin)
print "before :" + str(union_before)
print "contains:" + str(union_contains)
print "includes:" + str(union_includes)
print "is_included:" + str(union_isincluded)
print "no relations:" + str(union_norelation)
