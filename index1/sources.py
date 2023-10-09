import logging
import re
import json
import frontmatter

from datetime import date
from pathlib import Path
from typing import TypedDict, List, Callable, NotRequired

from MarkdownReader import  dict_string_values


logger = logging.getLogger()



Source = TypedDict(
    "Source",
    {
        "id": str,
        "path": str,
        "file_metadata": NotRequired[Callable],
        "include_metas": NotRequired[List[str]],
        "examples": NotRequired[List[str]],
        "exclude": NotRequired[List[str]]
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
        "description": metadata.get("mission"),
        "incubateur": incubators.get(metadata.get("incubator"), {}).get("title"),
        "phase": get_last_phase(metadata)
        # "sponsors": metadata.get("sponsors"),
    }
    return result


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
    # {
    #     "id": "startups-beta",
    #     # "topics": [
    #     #     "Questions concernant les startups beta.gouv",
    #     # ],
    #     "path": "./content/startups-beta",
    #     "file_metadata": get_se_metadata,
    #     "include_metas": ["contact"],
    #     "examples": [
    #         # "Aide dans mon parcours administratif",
    #         # "Reconnaissance d'image",
    #         # "Formation continue",
    #         # "c'est quoi MonAideCyber ?",
    #         # "cybersécurité",
    #         # "liste des startups de l'incubateur de l'écologie",
    #         # "liste des startups de l'incubateur de la DINUM",
    #         "Donnes moi une liste des startups en phase de transfert",
    #         "Donnes moi une liste des startups en phase d'investigation",
    #         "Donnes moi une liste des startups en phase d'acceleration",
    #     ],
    # },
    # {
    #     "id": "support-sre-fabrique",
    #     # "topics": [
    #     #     "Questions techniques sur le fonctionnent de l'hebergement",
    #     #     "Questions sur kubernetes et la plateforme de la fabrique",
    #     # ],
    #     "path": "./content/support-sre-fabrique",
    #     "file_metadata": get_sre_metadata,
    #     "examples": [
    #         "Comment me connecter à ma base de données",
    #         "Comment configurer mes ressources",
    #         "Demander de l'aide",
    #     ],
    # },
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
            "comment lancer un openlab ?",
            "comment accéder à mattermost ?",
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
            # "que fait la fabrique ?",
            # "comment est organisée la fabrique ?",
            # "quelles sont les valeurs de la fabrique ?",
            "comment est dirigée fabrique ?",
            "commet sont selectionnées les projets de la fabrique ?",
            "quelle personne contacter pour des conseils sur la gestion mon produit ?",
            "quelle personne contacter pour des conseils techniques ?",
            "quelle personne contacter sur les questions d'homologations et de conformité ?",
            "quelle personne contacter sur les questions juridiques ?",
        ],
    },
]
