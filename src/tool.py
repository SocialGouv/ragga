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
from typing import List, Dict
ParametresCalcul = TypedDict('ParametresCalcul', {'contrat salarié . ancienneté': int})
#ParametresCalcul = TypedDict('ParametresCalcul', {'contrat salarié . ancienneté': int, 'contrat salarié . travailleur handicapé': bool})

# class MyModel(BaseModel):
#     __root__: Dict[str, List[str]]

types = {'contrat salarié . ancienneté': 0}

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
    return value

def get_rule_question(data):
    missingVariables = data.get("evaluate",[{}])[0].get("missingVariables", {})
    if missingVariables:
        key = list(missingVariables)[0]
        print("call_publicodes key", key)
        rule = get_publicodes_rule(key)
        return rule.get("rawNode", {}).get("question", rule.get("title"))
    return None

def get_next_question(parametres_calcul: ParametresCalcul) -> str|None:
    """
    Pour calculer le préavis de retraite.
    """
    global ParametresCalcul
    parametres_calcul2={key: mapValue(value) for (key, value) in parametres_calcul.items()}
    print("call_publicodes", parametres_calcul2)
    r = requests.post("http://127.0.0.1:3002/evaluate", data=json.dumps({
        "situation": parametres_calcul2,
        "expressions": ["contrat salarié . préavis de retraite en jours"]
    }), headers={"content-type": "application/json"})
    data = r.json()
    # get question text
    print("call_publicodes", json.dumps(data))
    
    next_question = get_rule_question(data)
    #if next_question:
        #ParametresCalcul = TypedDict('ParametresCalcul', {'contrat salarié . ancienneté': int, 'contrat salarié . travailleur handicapé': bool})
    print("next_question", next_question)
    return next_question

def get_results(parametres_calcul: ParametresCalcul) -> int:
    """
    Pour obtenir le résultat final du préavis de retraite.
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
    #print("next_question", next_question)
    return result




# def query_api(queries: list[str]) -> list[str]:
#     """
#     Call our graphQL API to fetch some data
#     """
#     print("call API", queries)
#     return ["aaaa", "bbbb"]

#call_publicodes_tool = FunctionTool.from_defaults(fn=call_publicodes)
#query_api_tool = FunctionTool.from_defaults(fn=query_api)

PROMP_CONSEILLER_PREAVIS="""
Tu es un assistant en charge d'estimer la durée de préavis à respecter en cas de départ à la retraite ou de mise à la retraite de ton interlocuteur.
"""

#Tant que la fonction get_next_question te renvoie un résultat, poses cette question à l'utilisateur.
#Si la fonction get_next_question ne renvoie pas de résultat, appeler la fonction get_result pour obtenir le résultat



get_next_question_tool_description="""
Utilise cet outil pour calculer le préavis de retraite.
Tant que la fonction te renvoie un résultat, poses la nouvelle question à l'utilisateur.
Si la fonction ne renvoie pas de résultat, récapitules les questions posées et les réponses de l'utilisateur
"""
get_next_question_tool = FunctionTool.from_defaults(fn=get_next_question, description=get_next_question_tool_description) #, fn_schema=ParametresCalcul)
get_results_tool = FunctionTool.from_defaults(fn=get_results)
tools = [get_next_question_tool] #, get_results_tool]
agent = OpenAIAgent.from_tools(tools, verbose=True, system_prompt=PROMP_CONSEILLER_PREAVIS)

# use agent
#r=agent.chat("Calcules moi mon préavis de retraite pour 24 mois d'anciennete")
#r = agent.chat("récupères les dernieres visites sur notre API")

#print(r)

print("\nex: Calcules moi mon préavis de retraite pour 24 mois d'anciennete\n")
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
