# graph_retriever.py
from db_config import neo4j_driver

def retrieve_related_entities(entity_name: str):
    query = """
    MATCH (e)-[r]-(related)
    WHERE e.name = $entity_name
    RETURN related.name AS name, type(r) AS relation
    """
    with neo4j_driver.session() as session:
        results = session.run(query, entity_name=entity_name)
        return [{"name": record["name"], "relation": record["relation"]} for record in results]
