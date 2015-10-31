from SPARQLWrapper import SPARQLWrapper, JSON

class LocationChecker():
    # LocationChecker allows the user to asks to the DBPedia if a string is
    # a location, region, place, country, city, town or state. Also, it allows
    # to make generic queries to DBPedia.
   
    __dbpedia_url = "http://dbpedia.org/sparql"
    __mandatory_replacements = [(" ", "_"),("'", ""), ('"', "")]

    def __init__(self):
        self.sparql = SPARQLWrapper(self.__dbpedia_url)

    def __replace_capitals(self, s):
        # Returns a list with no repetitions containing:
        #   the given 's'
        #   the given 's' with the first letter in capital
        #   the given 's' with the first letter in capital and all
        #       letters following an underscore in capital too
        s_lower = s[0].upper() + s[1:len(s)].lower()
        s_capital = s.lower().title()
        ret_set = set([s, s_lower, s_capital])
        return ret_set

    def __format_string(self, s):
        # formats a string to use it in a query
        for replacement in self.__mandatory_replacements:
            s = s.replace(replacement[0], replacement[1])
        if '_' in s:
            ret_list = self.__replace_capitals(s)
        else:
            return [s]
        return ret_list

    def query(self, q, res_format=JSON):
        # Makes the query q to DBpedia
        ret_val = -1
        while ret_val == -1:
            self.sparql.setQuery(q)
            self.sparql.setReturnFormat(res_format)
            ret_val = self.sparql.query().convert()
        return ret_val
 
    def ask_query(self, entity_to_check, _type):
        # Makes a query to DBpedia asking if entity_to_check is of type _type
        q = '''PREFIX esdbr: <http://dbpedia.org/resource/>
           PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
           PREFIX umbel-rc: <http://umbel.org/umbel/rc/>
           ASK WHERE {{
               {{esdbr:{0} rdf:type umbel-rc:{1} }}
                UNION {{esdbr:{0} rdf:type dbpedia-owl:{1} }} .
           }}'''
        combinations = self.__format_string(entity_to_check);
        for combination in combinations:
            q_prov = q.format(combination, _type)
            query_result = self.query(q_prov)
            ret_val = query_result["boolean"]
            if ret_val:
                return ret_val
 
        return ret_val
 
    def is_place(self, entity_to_check):
        # Checks if entity_to_check is a place
        return self.ask_query(entity_to_check, "Place")
 
    def is_location(self, entity_to_check):
        # Checks if entity_to_check is a location
        return self.ask_query(entity_to_check, "Location")
   
    def is_country(self, entity_to_check):
        # Checks if entity_to_check is a country
        return self.ask_query(entity_to_check, "Country")
 
    def is_city(self, entity_to_check):
        # Checks if entity_to_check is a city
        return self.ask_query(entity_to_check, "City")
 
    def is_town(self, entity_to_check):
        # Checks if entity_to_check is a town
        return self.ask_query(entity_to_check, "Town")
 
    def is_state(self, entity_to_check):
        # Checks if entity_to_check is a state
        return self.ask_query(entity_to_check, "State")

    def is_region(self, entity_to_check):
        # Checks if entity_to_check is a region
        return self.ask_query(entity_to_check, "Region")
