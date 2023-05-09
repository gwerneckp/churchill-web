from neo4j import GraphDatabase


class AppAPI:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.cx = None

    def execute_query(self, cypher_query: str, **params):
        if not self.cx:
            self.cx = self.driver.session()

        try:
            result = self.cx.run(cypher_query, **params)
        except Exception as e:
            # Handle the error gracefully, for example by logging the error or
            # returning an error message to the client
            raise e

        return result

    def create_person(self, **kwargs):
        name = kwargs.get('name')
        if not name:
            raise ValueError('Name argument is missing')

        cypher_properties = ", ".join(f"{k}: ${k}" for k in kwargs.keys())
        cypher_query = f"CREATE (:Person {{{cypher_properties}}})"

        self.execute_query(cypher_query, **kwargs)

    def relationship(self, p1: str, relationship: str, p2: str):
        valid_relationships = ['FRIENDS_WITH',
                               'DONT_LIKE', 'GOT_WITH', 'DATED', 'DATING']
        if relationship not in valid_relationships:
            raise ValueError(f"Invalid relationship type: {relationship}")

        cypher_query = "MATCH (p1:Person {name: $p1}), (p2:Person {name: $p2}) " \
            "MERGE (p1)<-[:{relationship}]->(p2)"

        self.execute_query(cypher_query, p1=p1, p2=p2,
                           relationship=relationship)

    def get_person_info(self, name: str):
        cypher_query = "MATCH (p1:Person {name: $name})<-[r]->(p2:Person) RETURN p1, type(r), p2"
        result = self.execute_query(cypher_query, name=name)

        # Extract person properties
        person_node = result.peek()["p1"]
        person_properties = dict(person_node)

        # Extract relationships
        relationships = []
        for record in result:
            p1 = record["p1"]["name"]
            relationship = record["type(r)"]
            p2 = record["p2"]["name"]
            relationships.append(
                {"p1": p1, "relationship": relationship, "p2": p2})

        return {"person": person_properties, "relationships": relationships}

    def search(self, name: str):
        cypher_query = "MATCH (p:Person) WHERE toLower(p.name) CONTAINS toLower($name) RETURN p.name"
        result = self.execute_query(cypher_query, name=name)
        return [record["p.name"] for record in result]


if __name__ == '__main__':
    api = AppAPI("neo4j://localhost:7687", "neo4j", "xxxxxxxx")

    print(api.get_person_info(api.search("gabr")[0]))