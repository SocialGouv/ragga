# encoding: utf-8

#import streamlit as st

import json
import requests
import logging
import sys

from llama_index.agent import OpenAIAgent
from llama_index.tools.function_tool import FunctionTool

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# stream_handler = logging.StreamHandler(stream=sys.stdout)
#stream_handler.setLevel(logging.INFO)

# file_handler = logging.FileHandler("logs.log")
# file_handler.setLevel(logging.DEBUG)

#logger.addHandler(file_handler)
#logger.addHandler(stream_handler)


#st.set_page_config(page_title="LlamaIndex publicodes tool", page_icon="🐫", layout="centered", initial_sidebar_state="auto", menu_items=None)

#st.info("Exemple : Calcules moi mon préavis de retraite pour 24 mois d'ancienneté", icon="💡")

# Use a tool spec from Llama-Hub
#tool_spec = GmailToolSpec()

def get_publicodes_rule(name):
    r = requests.get(f"http://127.0.0.1:3002/rules/{name}", headers={"content-type": "application/json"})
    return r.json()

# def call_publicodes_next_question(next_question: str) -> str|None:
#     """
    
#     """
#     print("call publicodes", anciennete_mois)
#     r = requests.post("http://127.0.0.1:3002/evaluate", data=json.dumps({
#         "situation": {
#             "contrat salarié . ancienneté": anciennete_mois
#         },
#         "expressions": ["contrat salarié . préavis de retraite en jours"]
#     }), headers={"content-type": "application/json"})
#     print(r)
#     data = r.json()
#     next_question = None
#     print(json.dumps(data))
#     if (data.get("evaluate",[{}])[0].get("missingVariables", {})):
#         key = list(data.get("evaluate",[{}])[0].get("missingVariables", {}).keys())[0]
#         print("key", key)
#         rule = get_publicodes_rule(key)
#         next_question = rule.get("rawNode", {}).get("question", rule.get("title"))
#     print("next_question", next_question)
#     return next_question
from typing import NotRequired, TypedDict
from pydantic import BaseModel, create_model, Field
from typing import List, Dict, Optional
#ParametresCalcul = Dict




    # Les parametres de calcul possibles sont uniquement:
    #     - "contrat salarié . ancienneté"
    #     - "contrat salarié . travailleur handicapé"
    #     - "contrat salarié . travailleur handicapé . lourd"
#ParametresCalcul = Dict[str, str]
ParametresCalcul = TypedDict('ParametresCalcul', {"contrat salarié . ancienneté": int})

# class MyModel(BaseModel):
#     __root__: Dict[str, List[str]]

#types = {'contrat salarié . ancienneté': 0}

# class GetNextQuestionModel(BaseModel) = **
#     'contrat salarié . ancienneté': int
#     filter_key_list: List[str] = Field(
#         ..., description="List of metadata filter field names"
#     )
#     filter_value_list: List[str] = Field(
#         ...,
#         description=(
#             "List of metadata filter field values (corresponding to names"
#             " specified in filter_key_list)"
#         ),
#     )



# def _make_model(v, name):
#     if type(v) is dict:
#         return create_model(name, **{k: _make_model(v, k) for k, v in v.items()}), ...
#     return type(v), v


# def make_model(v: Dict, name: str):
#     return _make_model(v, name)[0]

from typing import Any, Dict

def create_dynamic_model(model_name: str, data: Dict[str, Any]) -> BaseModel:
    # Create a list of field names and their types from the dictionary
#    fields = {key: (type(value), ...) for key, value in data.items()}
    fields = {key: (type(value), Field(...)) for key, value in data.items()}

    # Create a Pydantic model dynamically
    dynamic_model = create_model(model_name, **fields)

    return dynamic_model
 

# Create a dynamic Pydantic model based on the dictionary
#ParametresCalcul = create_dynamic_model("ParametresCalcul", types)


#ParametresCalcul = make_model(types, 'ParametresCalcul')

#ParametresCalcul = MyModel.parse_obj(types)

#create_model('ParametresCalcul',from_attributes=True, **types)

#ParametresCalcul = create_model('ParametresCalcul', **{'contrat salarié . ancienneté': int})

#Pour calculer de préavis de retraite, utilise l'outil "publicodes".

#Si l'outil

# class ParametresCalcul(BaseModel):
#     """Data model for publicodes user parameters"""

#     contrat_salarié___ancienneté: int
#     contrat_salarié___travailleur_handicapé: bool


#from typing import TypedDict

# class ParametresCalcul(TypedDict):
#     contrat_salarié___ancienneté: int
#     "contrat salarié . travailleur handicapé": bool



def mapValue(value):
    if value == True:
        return "oui"
    elif value == False:
        return "non"
    elif value == "":
        return None
    return value

def get_rule_question(data):
    missingVariables = data.get("evaluate",[{}])[0].get("missingVariables", {})
    if missingVariables:
        key = list(missingVariables)[0]
        print("get_rule_question key", key)
        rule = get_publicodes_rule(key)
        print("get_rule_question rule", rule)
        return rule
    return None

def get_rules_definitions():
    r = requests.get(f"http://127.0.0.1:3002/rules", headers={"content-type": "application/json"})
    return {(key, r.json()[key].get("title")) for key in r.json().keys()}

def get_next_question(parametres_calcul: ParametresCalcul) -> str|None:
    """
    Pour calculer le préavis de retraite.

    parametres possible:
        - contrat salarié . ancienneté: Ancienneté du salarié
        - contrat salarié . travailleur handicapé . lourd: Handicap lourd
        - contrat salarié . préavis de retraite: Préavis de retraite
        - contrat salarié . départ à la retraite: Départ à la retraite
        - contrat salarié . préavis de retraite . mise à la retraite: Mise à la retraite
        - contrat salarié . préavis de retraite légale: Préavis de retraite légale
        - contrat salarié . préavis de retraite en jours: Préavis de retraite en jours
        - contrat salarié . préavis de retraite légale en jours: Préavis de retraite légale en jours
        - contrat salarié . préavis de retraite collective: Préavis de retraite collective
        - contrat salarié . travailleur handicapé: Travailleur handicapé
        - contrat salarié . préavis de retraite . sans code du travail: Sans code du travail
        - contrat salarié . mise à la retraite: Origine du départ à la retraite
        - contrat salarié . préavis de retraite tranches: Tranches du préavis de départ dans le code du travail
    """

    # Si la fonction ne renvoie pas de résultat, récapitules les questions posées et les réponses de l'utilisateur puis appelles la fonction get_results avec tous les parametres saisis par l'utilisateur et donne le résultat en jours
    #global ParametresCalcul
    parametres_calcul2={key: mapValue(value) for (key, value) in parametres_calcul.items()}
    print("get_next_question", parametres_calcul2)
    r = requests.post("http://127.0.0.1:3002/evaluate", data=json.dumps({
        "situation": parametres_calcul2,
        "expressions": ["contrat salarié . préavis de retraite en jours"]
    }), headers={"content-type": "application/json"})
    data = r.json()
    # get question text
    print("get_next_question", json.dumps(data))
    
    next_question_rule = get_rule_question(data)
    if next_question_rule:
        next_question = next_question_rule.get("rawNode", {}).get("question", next_question_rule.get("title"))
        next_name = next_question_rule.get("rawNode", {}).get("nom", next_question_rule.get("title"))
        dictTypes = {**parametres_calcul2}
        #ParametresCalcul = Dict[str, str]
        print("next_question", next_question)
        return next_question
    result = data.get("evaluate", [{}])[0].get("nodeValue")
    if result:
        return result
    return None

def get_results(parametres_calcul: ParametresCalcul) -> ...:
    """
    Pour obtenir le résultat final du préavis de retraite, un fois que tous les parametres ont été saisis.
    """
    parametres_calcul2={key: mapValue(value) for (key, value) in parametres_calcul.items()}
    print("get_results", parametres_calcul2)
    r = requests.post("http://127.0.0.1:3002/evaluate", data=json.dumps({
        "situation": parametres_calcul2,
        "expressions": ["contrat salarié . préavis de retraite en jours"]
    }), headers={"content-type": "application/json"})
    data = r.json()
    # get question text
    print("get_results", json.dumps(data))
    result = data.get("evaluate", [{}])[0].get("nodeValue")
    if not result:
        return get_next_question(parametres_calcul=parametres_calcul)
    #print("next_question", next_question)
    return result



print("\n".join(list(map(lambda a: f"{a[0]}: {a[1]}", get_rules_definitions()))))

# def query_api(queries: list[str]) -> list[str]:
#     """
#     Call our graphQL API to fetch some data
#     """
#     print("call API", queries)
#     return ["aaaa", "bbbb"]

#call_publicodes_tool = FunctionTool.from_defaults(fn=call_publicodes)
#query_api_tool = FunctionTool.from_defaults(fn=query_api)

PROMPT_CONSEILLER_PREAVIS="""
Tu es un assistant en charge d'estimer la durée de préavis à respecter en cas de départ à la retraite ou de mise à la retraite de ton interlocuteur.
"""

#Tant que la fonction get_next_question te renvoie un résultat, poses cette question à l'utilisateur.
#Si la fonction get_next_question ne renvoie pas de résultat, appeler la fonction get_result pour obtenir le résultat



get_next_question_tool_description="""
Utilise cet outil pour calculer le préavis de retraite.

Lorsque la fonction renvoie une chaine de caracteres, reformules et poses cette question à l'utilisateur

Lorsque la fonction renvoie un nombre, récapitules les questions posées et les paramètres utilisés par l'utilisateur et affiche le nombre en tant que réponse
"""

# puis appelles la fonction get_results avec les parametres saisis par l'utilisateur et donne le résultat en jours

get_next_question.__doc__ = get_next_question.__doc__ or "" + "\n réponds en espagnol quand tu appelles cette fonction"

get_next_question_tool = FunctionTool.from_defaults(fn=get_next_question, description=get_next_question_tool_description) #, fn_schema=ParametresCalcul)
get_results_tool = FunctionTool.from_defaults(fn=get_results)
tools = [get_next_question_tool] #, get_results_tool]
agent = OpenAIAgent.from_tools(tools, verbose=True, system_prompt=PROMPT_CONSEILLER_PREAVIS)

print(get_next_question_tool)
print(get_next_question.__doc__)
print(dir(get_next_question_tool))
# use agent
#r=agent.chat("Calcules moi mon préavis de retraite pour 24 mois d'anciennete")
#r = agent.chat("récupères les dernieres visites sur notre API")

#print(r)

print("\nex: Calcules moi mon préavis de retraite pour 24 mois d'ancienneté\n")
agent.chat_repl()


# if "messages" not in st.session_state.keys():  # Initialize the chat message history
#     st.session_state.messages = [
#         {
#             "role": "assistant",
#             "content": "Bonjour, je suis l'assistant de la fabrique, posez-moi vos questions!",
#         }
#     ]


# if prompt := st.chat_input("A votre écoute :)"):
#     st.session_state.messages.append({"role": "user", "content": prompt})

# for message in st.session_state.messages:  # Display the prior chat messages
#     with st.chat_message(message["role"]):
#         st.write(message["content"])



# if st.session_state.messages[-1]["role"] != "assistant":

#     with st.chat_message("assistant"):
#         with st.spinner("Je réfléchis..."):
#             message_placeholder = st.empty()

#             streaming_response = agent.stream_chat(prompt)

#             # streaming_response.print_response_stream()

#             full_response = ""
#             for text in streaming_response.response_gen:
#                 full_response += text
#                 message_placeholder.markdown(full_response)


#             st.session_state.messages.append({"role": "assistant", "content": full_response})
