from llama_index.query_engine.router_query_engine import RouterQueryEngine
from llama_index.tools.query_engine import QueryEngineTool
from llama_index.selectors.pydantic_selectors import (
    PydanticMultiSelector,
    PydanticSingleSelector,
)
from index import results

def to_query_engine_tool(idx, result):
    index = result[0]
    source = result[1]
    if idx == 0: # not sure why only first has tree_summarize
        query_engine = index.as_query_engine(
            response_mode="compact",
            description=source.get("description", source.get("title")),
            use_async=True,
            streaming=True,
            similarity_top_k=5
        )
    else:
        query_engine = index.as_query_engine(similarity_top_k=5,streaming=True)

    query_engine_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=source.get("description", source.get("title")),
        
    )
    return query_engine_tool


query_engine_tools = map(lambda x: to_query_engine_tool(x[0], x[1]), enumerate(results))

query_engine = RouterQueryEngine(
    selector=PydanticMultiSelector.from_defaults(),
    query_engine_tools=query_engine_tools
)

# res = query_engine.query(
#     "Comment améliorer les performances de ma base de données ?"
# )
# print(res)

res = query_engine.query(
    "A la fabrique des ministères sociaux, qui contacter pour des questions juridiques ?"
)
print(res)

res = query_engine.query(
    "A la fabrique des ministères sociaux, qui contacter pour des questions techniques ?"
)
print(res)

res = query_engine.query(
    "A la fabrique des ministères sociaux, comment facturer mes prestations ?"
)
print(res)


res = query_engine.query(
    "Quelles sont les premières étapes de l'homologation RGS ?"
)
print(res)

res = query_engine.query(
    "Quels sont les points forts de la methode beta.gouv ?"
)
print(res)

res = query_engine.query(
    "Quelles sont les dernières nouvelles de la startup Domifa ?"
)
print(res)

res = query_engine.query(
    "Combien de visites sur le code du travail ?"
)
print(res)
