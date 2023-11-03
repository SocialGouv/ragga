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

from MarkdownReader import dict_string_values

# from index import get_documents

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
        "title": str,
        "url": str,
        "file_metadata": NotRequired[Callable],
        "include_metas": NotRequired[List[str]],
        "examples": NotRequired[List[str]],
        "exclude": NotRequired[List[str]],
        # "on_finish": NotRequired[Callable],
        "additional_documents": NotRequired[Callable],
        "description": NotRequired[str],
        "get_url": NotRequired[Callable],
    },
)


def get_file_metadata(filename):
    logger.debug("get_file_metadata: {}".format(filename))
    post = frontmatter.load(filename)
    logger.debug(post)
    metadata = {"filename": filename, **post.metadata}
    logger.debug(metadata)
    return metadata


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


incubators = json.loads(Path("./src/incubators.json").read_text())


def get_se_metadata(filename):
    logger.debug("get_se_metadata: {}".format(filename))
    metadata = get_file_metadata(filename)
    result = {
        "title": metadata.get("title"),
        "description": "Mission de la startup '{}' : {}".format(
            metadata.get("title"), metadata.get("mission")
        ),
        "incubator": incubators.get(metadata.get("incubator"), {}).get("title"),
        "phase": get_last_phase(metadata),
        "sponsors": ", ".join(metadata.get("sponsors", [])),
    }
    return result


def beta_se_postprocessor(documents):
    # create additionnal documents

    # build a markdown table

    keys = ["title", "phase", "incubator"]

    selection = [{key: doc.metadata[key] for key in keys} for doc in documents]
    incubators = set(map(lambda a: a.get("incubator"), selection))
    docs = []
    for incubator in incubators:
        statements = []
        statements.append(
            "# Liste des startups par phase de l'incubateur {}\n".format(incubator)
        )
        statements.append(" title | phase ")
        statements.append("------ | ------ ")
        for select in [
            select for select in selection if select.get("incubator") == incubator
        ]:
            statements.append(
                " {} | {} ".format(select.get("title"), select.get("phase"))
            )

        # print("\n".join(statements))
        doc = Document(
            text="\n".join(statements),
            metadata={
                "source": "Startups de {}".format(incubator),
                "title": "Liste des startups par phase de l'incubateur {}".format(
                    incubator
                ),
            },
        )
        docs.append(doc)
        # index.insert(doc, service_context=service_context)
    return docs


def get_wiki_url(filename):
    path = filename.replace("content/www-wiki", "").replace(".md", "")
    return f"https://github.com/SocialGouv/www/wiki/{path}"


def get_beta_startup_url(filename):
    startup = filename.replace("content/startups-beta", "").replace(".md", "")
    return f"https://beta.gouv.fr/startups/{startup}.html"


def get_support_sre_url(filename):
    path = filename.replace("content/support-sre-fabrique", "").replace(".md", "")
    return f"https://socialgouv.github.io/support/docs/{path}"


def get_notion_fabrique_url(filename):
    doc = filename.replace("content/notion-fabrique", "").replace(".md", "")
    return f"https://www.notion.so/fabnummas/{doc}"


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
        "title": "Startups beta.gouv",
        "url": "https://beta.gouv.fr/startups/",
        # "topics": [
        #     "Questions concernant les startups beta.gouv",
        # ],
        "path": "./content/startups-beta",
        "file_metadata": get_se_metadata,
        "include_metas": ["contact"],
        "get_url": get_beta_startup_url,
        "additional_documents": beta_se_postprocessor,
        "description": "Questions concernant les startups beta.gouv",
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
            # "Donnes moi une liste des startups en phase de transfert",
            # "Quels sont les contacts de la startup Compost ?",
            # "Donnes moi une liste des startups en phase d'acceleration",
            # "Donnes moi une liste sous forme de tableau de toutes les startups avec leur statut et leur incubateur",
            # "Donnes moi une liste sous forme de tableau des startups liées à l'écologie",
            # "Donnes moi une liste sous forme de tableau des startups liées à au logement",
            # "Donnes moi une liste des startups des ministeres sociaux",
            # "Donnes moi une liste sous forme de tableau des startups des ministeres sociaux avec leur statut",
            # "combien de startups sont gérées à l'incubateur des ministeres sociaux et sont en acceleration ?"
        ],
    },
    {
        "id": "support-sre-fabrique",
        "title": "Support technique de la fabrique",
        "url": "https://socialgouv.github.io/support",
        "description": "Questions concernant le support technique",
        # "topics": [
        #     "Questions techniques sur le fonctionnent de l'hebergement",
        #     "Questions sur kubernetes et la plateforme de la fabrique",
        # ],
        "path": "./content/support-sre-fabrique",
        "file_metadata": get_sre_metadata,
        "get_url": get_support_sre_url,
        "examples": [
            # "Comment me connecter à ma base de données",
            # "Comment configurer mes ressources",
            # "Demander de l'aide",
        ],
    },
    # {
    #     "id": "documentation-beta",
    #     "title": "Documentation beta.gouv",
    #     "url": "https://doc.incubateur.net/",
    #     "description": "Questions sur la methodologie, les services outils, et le fonctionnement des startups d'état beta.gouv",
    #     # "topics": [
    #     #     "Questions sur la méthodologie startups d'état",
    #     #     "Questions sur le fonctionnement, les outils pour gérer sa startup",
    #     #     "Questions sur la communauté beta",
    #     # ],
    #     "path": "./content/documentation-beta",
    #     "exclude": ["*SUMMARY.md",".*README.md"], # bug with long content
    #     # "file_metadata": get_file_metadata,
    #     "examples": [
    #         # "comment lancer un openlab ?",
    #         # "comment accéder à mattermost ?",
    #     ],
    # },
    {
        "id": "notion-fabrique",
        "title": "Notion de la fabrique (partiel)",
        "description": "Questions concernant le fonctionnement interne de la fabrique numérique des ministères sociaux et les personnes à contacter (SocialGouv)",
        "url": "https://www.notion.so/fabnummas",
        "get_url": get_notion_fabrique_url,
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
    # {
    #     "id": "incubators-beta",
    #     "title": "Incubateurs beta.gouv",
    #     "description": "Documentation sur les différents incubateurs de startups de beta.gouv",
    #     "url": "https://beta.gouv.fr/incubateurs/",
    #     # "topics": [
    #     #     "Questions concernant les startups beta.gouv",
    #     # ],
    #     "path": "./content/incubators-beta",
    #     #"file_metadata": get_se_metadata,
    #     "include_metas": ["title", "contact", "website"],
    #     "examples":[
    #        # "c'est quoi l'ADEME ?"
    #     ]
    # },
    # {
    #     "id": "organisations-beta",
    #     "title": "Organisations beta.gouv",
    #     "url": "https://beta.gouv.fr/incubateurs/",
    #     "description": "Documentation sur les différentes organisations de startups de beta.gouv",
    #     # "topics": [
    #     #     "Questions concernant les startups beta.gouv",
    #     # ],
    #     "path": "./content/organisations-beta",
    #     #"file_metadata": get_se_metadata,
    #     #"include_metas": ["title", "contact", "website"],
    #     "examples":[
    #         # "c'est quoi la SGDSN ?",
    #         # "c'est quoi CSAPA ?"
    #     ]
    # },
    {
        "id": "standup-fabrique",
        "title": "Standup de la fabrique (carnets)",
        "url": "https://standup.fabrique.social.gouv.fr",
        # "get_url": lambda filename: "https://standup.fabrique.social.gouv.fr",
        "description": "Actualité des startups de la fabrique : derniers chiffres, KPIS et évenements",
        # "topics": [
        #     "Questions concernant les startups beta.gouv",
        # ],
        "path": "./content/standup-fabrique",
        # "file_metadata": get_standup_metadata,
        # "include_metas": ["title", "contact", "website"],
        "examples": [
            # "Quelles sont les KPIs des SRE ?",
            # "Quelles sont les KPIs de EgaPro ?",
            # "Quelles sont les KPIs de Code du travail ?",
            # "Quels sont les besoins de domifa ?",
            # "Quels sont l'actu d'archifiltre ?",
            # "Combien de visites sur le code du travail ?",
        ],
    },
    {
        "id": "www-wiki",
        "title": "Informations sur le fonctionnement la fabrique (wiki)",
        "url": "https://standup.fabrique.social.gouv.fr",
        "get_url": get_wiki_url,
        "description": "Wiki de la fabrique: glossaire, standup, mattermost et collaboration",
        # "topics": [
        #     "Questions concernant les startups beta.gouv",
        # ],
        "path": "./content/www-wiki",
        # "file_metadata": get_standup_metadata,
        # "include_metas": ["title", "contact", "website"],
        "examples": [
            # "Quelles sont les KPIs des SRE ?",
            # "Quelles sont les KPIs de EgaPro ?",
            # "Quelles sont les KPIs de Code du travail ?",
            # "Quels sont les besoins de domifa ?",
            # "Quels sont l'actu d'archifiltre ?",
            # "Combien de visites sur le code du travail ?",
        ],
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
