from llama_index.chat_engine.types import ChatMode

from index import index


query_engine = index.as_query_engine(
    chat_mode=ChatMode.CONTEXT,
    verbose=True,
    similarity_top_k=5,
)

questions = [
    "Quelles sont les KPIs de Domifa ?",
    "Comment me connecter à ma base de données ?",
    "Qui contacter pour les questions juridiques ?",
    "Comment sécuriser mon image Docker ?",
    "Comment lancer mon homologation de sécurité ?",
    "Comment mettre à jour le standup de ma startup ?",
    "Peut-on utiliser google analytics ?",
    "Qui contacter pour une assistance technique ?",
    "Comment deployer une branche de review ?",
]

for question in questions:
    response = query_engine.query(question)

    print(f"# {question}\n")
    print(response)
    print("\n---\n")
