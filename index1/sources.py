import logging
import re
import json
import frontmatter

from datetime import date
from pathlib import Path
from typing import TypedDict, List, Callable, NotRequired

from llama_index.schema import Document
from llama_index import ServiceContext
from llama_index.node_parser.file.markdown import MarkdownNodeParser

from MarkdownReader import  dict_string_values

#from index import get_documents

logger = logging.getLogger()


node_parser = MarkdownNodeParser.from_defaults()


# use OpenAI by default
service_context = ServiceContext.from_defaults(
    chunk_size=512,
    # embed_model=embed_model,
    node_parser=node_parser,
    # llm=llm,
)



Source = TypedDict(
    "Source",
    {
        "id": str,
        "path": str,
        "file_metadata": NotRequired[Callable],
        "include_metas": NotRequired[List[str]],
        "examples": NotRequired[List[str]],
        "exclude": NotRequired[List[str]],
        "on_finish": NotRequired[Callable]
    },
)

def get_file_metadata(filename):
    logger.debug("get_file_metadata: {}".format(filename))
    post = frontmatter.load(filename)
    return {"filename": filename, **post.metadata}


sre_files_mapping = {
    "content/support-sre-fabrique/init/.*": {
        "description": [
            "Présentation générale de la plateforme et des services technique de la fabrique"
        ],
    },
    "content/support-sre-fabrique/infrastructure/.*": {
        "description": ["Questions sur l'infrastructure technique de la fabrique"],
    },
    "content/support-sre-fabrique/standards/.*": {
        "description": [
            "Questions sur les standards techniques et conventions de la fabrique"
        ],
    },
    "content/support-sre-fabrique/workshops/.*": {
        "description": ["Workshops proposés aux développeurs(ses) de la fabrique"],
    },
}


def get_sre_metadata(filename):
    logger.debug("get_sre_metadata: {}".format(filename))
    metadata = get_file_metadata(filename)
    for path in sre_files_mapping.keys():
        if bool(re.match(path, filename)):
            return {
                **dict_string_values(sre_files_mapping[path]),
                **metadata,
            }
    return metadata


def get_last_phase(metadata):
    if metadata.get("phases"):
        metadata.get("phases").sort(key=lambda x: x.get("start", date(1970, 1, 1)))
        latest = metadata.get("phases")[-1]
        return latest.get("name")
    return None


incubators = json.loads(Path("./index1/incubators.json").read_text())


def get_se_metadata(filename):
    logger.debug("get_se_metadata: {}".format(filename))
    metadata = get_file_metadata(filename)
    result = {
        "title": metadata.get("title"),
        "description": "Mission de la startup '{}' : {}".format(metadata.get("title"),metadata.get("mission")),
        "incubator": incubators.get(metadata.get("incubator"), {}).get("title"),
        "phase": get_last_phase(metadata),
        "sponsors": ", ".join(metadata.get("sponsors",[])),
    }
    return result


def beta_se_postprocessor(documents, index):
    # create additionnal documents

    # build a markdown table
    
    keys=["title", "phase", "incubator"]
    
    selection = [{key: doc.metadata[key] for key in keys} for doc in documents]
    incubators = set(map(lambda a: a.get("incubator"), selection))
    for incubator in incubators:
        statements=[]
        statements.append("# Liste des startups par phase de l'incubateur {}\n".format(incubator))
        statements.append(" title | phase ")
        statements.append("------ | ------ ")
        for select in [select for select in selection if select.get("incubator")==incubator]:
            statements.append(" {} | {} ".format(select.get("title"), select.get("phase")))

        print("\n".join(statements))
        doc = Document(text="\n".join(statements), metadata={"title": "Liste des startups par phase de l'incubateur {}\n".format(incubator)}) 
        index.insert(doc, service_context=service_context)


sources: List[Source] = [
    # {
    #     "id": "startups-beta-gouv-sample",
    #     "topics": [
    #         "Questions concernant les startups beta.gouv",
    #         "Questions concernant les startups de la fabrique numérique",
    #     ],
    #     "path": "./content/sample",
    #     "file_metadata": get_se_metadata,
    # },
    {
        "id": "startups-beta",
        # "topics": [
        #     "Questions concernant les startups beta.gouv",
        # ],
        "path": "./content/startups-beta",
        "file_metadata": get_se_metadata,
        "include_metas": ["contact"],
        "on_finish": beta_se_postprocessor,
        "examples": [
      #      "Quelles startups dans le domaine de l'éducation ?",
       #     "Quelles sont les startups du GIP de l'inclusion ?",
        #    "Quelles startups dans le domaine de l'armée ?",
         #   "combien de startups en tout ?",
          #  "combien de startups chez beta en tout ?",
           # "ou en est la startup domifa ?"
            # "Aide dans mon parcours administratif",
            # "Reconnaissance d'image",
            # "Formation continue",
            # "c'est quoi MonAideCyber ?",
            # "cybersécurité",
            # "liste des startups de l'incubateur de l'écologie",
            # "liste des startups de l'incubateur de la DINUM",
            #"Donnes moi une liste des startups en phase de transfert",
            #"Quels sont les contacts de la startup Compost ?",
           # "Donnes moi une liste des startups en phase d'acceleration",
           #"Donnes moi une liste sous forme de tableau de toutes les startups avec leur statut et leur incubateur",
           #"Donnes moi une liste sous forme de tableau des startups liées à l'écologie",
           #"Donnes moi une liste sous forme de tableau des startups liées à au logement",
           #"Donnes moi une liste des startups des ministeres sociaux",
           #"Donnes moi une liste sous forme de tableau des startups des ministeres sociaux avec leur statut",
          # "combien de startups sont gérées à l'incubateur des ministeres sociaux et sont en acceleration ?"
        ],
    },
    {
        "id": "support-sre-fabrique",
        # "topics": [
        #     "Questions techniques sur le fonctionnent de l'hebergement",
        #     "Questions sur kubernetes et la plateforme de la fabrique",
        # ],
        "path": "./content/support-sre-fabrique",
        "file_metadata": get_sre_metadata,
        "examples": [
            # "Comment me connecter à ma base de données",
            # "Comment configurer mes ressources",
            # "Demander de l'aide",
        ],
    },
    {
        "id": "documentation-beta",
        # "topics": [
        #     "Questions sur la méthodologie startups d'état",
        #     "Questions sur le fonctionnement, les outils pour gérer sa startup",
        #     "Questions sur la communauté beta",
        # ],
        "path": "./content/documentation-beta",
        "exclude": ["*SUMMARY.md",".*README.md"], # bug with long content
        # "file_metadata": get_file_metadata,
        "examples": [
            # "comment lancer un openlab ?",
            # "comment accéder à mattermost ?",
        ],
    },
    {
        "id": "notion-fabrique",
        # "topics": [
        #     "Questions sur la méthodologie startups d'état",
        #     "Questions sur le fonctionnement, les outils pour gérer sa startup",
        #     "Questions sur la communauté beta",
        # ],
        "path": "./content/notion-fabrique",
        # "file_metadata": get_file_metadata,
        "examples": [
          #  "c'est quoi CSAPA ?",
          #  "qui gere les sujets infrastructure a la fabrique ?"
            # "que fait la fabrique ?",
            # "comment est organisée la fabrique ?",
            # "quelles sont les valeurs de la fabrique ?",
            # "comment est dirigée fabrique ?",
            # "commet sont selectionnées les projets de la fabrique ?",
            # "quelle personne contacter pour des conseils sur la gestion mon produit ?",
            # "quelle personne contacter pour des conseils techniques ?",
            # "quelle personne contacter sur les questions d'homologations et de conformité ?",
            # "quelle personne contacter sur les questions juridiques ?",
        ],
    },
    {
        "id": "incubators-beta",
        # "topics": [
        #     "Questions concernant les startups beta.gouv",
        # ],
        "path": "./content/incubators-beta",
        #"file_metadata": get_se_metadata,
        "include_metas": ["title", "contact", "website"],
        "examples":[
           # "c'est quoi l'ADEME ?"
        ]
    },
    {
        "id": "organisations-beta",
        # "topics": [
        #     "Questions concernant les startups beta.gouv",
        # ],
        "path": "./content/organisations-beta",
        #"file_metadata": get_se_metadata,
        #"include_metas": ["title", "contact", "website"],
        "examples":[
            # "c'est quoi la SGDSN ?",
            # "c'est quoi CSAPA ?"
        ]
    },
    {
        "id": "standup-fabrique",
        # "topics": [
        #     "Questions concernant les startups beta.gouv",
        # ],
        "path": "./content7/standup-fabrique",
        #"file_metadata": get_se_metadata,
        #"include_metas": ["title", "contact", "website"],
        "examples":[
            # "Quelles sont les KPIs des SRE ?",
            # "Quelles sont les KPIs de EgaPro ?",
            # "Quelles sont les KPIs de Code du travail ?",
            # "Quels sont les besoins de domifa ?",
            # "Quels sont l'actu d'archifiltre ?",
            # "Combien de visites sur le code du travail ?",
        ]
    },
    #  {
    #     "id": "startups-beta-x7",
    #     # "topics": [
    #     #     "Questions concernant les startups beta.gouv",
    #     # ],
    #     "path": "./content/startups-beta",
    #     "file_metadata": get_se_metadata,
    #     "include_metas": ["contact"],
    #     "on_finish": beta_se_postprocessor,
    #     "examples": [
    #         # "Aide dans mon parcours administratif",
    #         # "Reconnaissance d'image",
    #         # "Formation continue",
    #         # "c'est quoi MonAideCyber ?",
    #         # "cybersécurité",
    #         # "liste des startups de l'incubateur de l'écologie",
    #         # "liste des startups de l'incubateur de la DINUM",
    #     #     "Donnes moi une liste des startups en phase de transfert",
    #     #     "Quels sont les contacts de la startup Compost ?",
    #     #     "Donnes moi une liste des startups en phase d'acceleration",
    #         "Donnes moi une liste des startups incubées à l'écologie ?",
    #     #    "Donnes moi une liste des startups par phase",
    #        "Donnes moi une liste des startups en rapport avec la sécurité",
    #     ],
    # },
]
