import sys
from DBPediaAccessor_classes import LocationChecker
from sys import argv

dbpedia = LocationChecker()

call_map = {
    "place": dbpedia.is_place,
    "location": dbpedia.is_location,
    "country": dbpedia.is_country,
    "city": dbpedia.is_city,
    "town": dbpedia.is_town,
    "state": dbpedia.is_state,
    "region": dbpedia.is_region
}

type_variables = None

if len(sys.argv) != 1:
    cmdargs = sys.argv;
    type_variables = cmdargs.pop().lower()
    if not type_variables in call_map.keys():
        print "Last parameter must be a value in:", call_map.keys()
        exit(1)
    l = []
    for filename in cmdargs[1:]:
        try:
            f = open(filename)
            for line in f:
                line = line.replace("\n","").replace("\r", "")
                l.append(line)
            f.close()
        except Exception,e :
            print "Problem while reading the file " + filename + ": " + str(e)
else:
    program_name = argv[0]
    if "/" in program_name:
        program_name = program_name[program_name.rindex("/")+1:]
    print "Usage: " + program_name + " filename1 [filename2 filename3 ...] option"
    print "Where option is one of the following: " + str(call_map.keys())
    exit(1)

count = 0
func = call_map[type_variables.lower()]

for entity in l:
    print "Is " + entity + " a " + type_variables + "?"
    res = func(entity)
    print res
    count += res
    print "============"

print "Correct: ",count, " out of ", len(l)
