# Quelles sont les KPIs de Domifa ?

Les KPIs de DomiFa sont les suivants :
- Demandes de domiciliation : 385 463
- Dossiers actifs : 235 779
- Structures : 1 153

---

# Comment me connecter à ma base de données ?

Pour vous connecter à votre base de données, vous pouvez utiliser l'application Teleport Connect. Téléchargez et installez le GUI Teleport Connect, puis lancez l'application. Renseignez l'adresse "teleport.fabrique.social.gouv.fr" et authentifiez-vous avec votre compte GitHub. Ensuite, naviguez dans l'onglet "Databases", choisissez votre serveur Postgres, et cliquez sur "Connect" en utilisant le nom d'utilisateur "PostgresAdmins". Renseignez le nom de la base de données que vous souhaitez accéder et cliquez sur "Run".

---

# Qui contacter pour les questions juridiques ?

Osiris Priso

---

# Comment sécuriser mon image Docker ?

Pour sécuriser votre image Docker, vous pouvez suivre les bonnes pratiques suivantes :

1. Utilisez une image de conteneur officielle ou une image source maintenue par l'équipe SRE de la fabrique des ministères sociaux.
2. Assurez-vous que votre conteneur s'exécute sans privilèges root en utilisant l'option `USER` dans votre fichier Dockerfile.
3. Définissez un UID numérique supérieur à 0 dans votre fichier Dockerfile pour identifier l'utilisateur exécutant le conteneur.
4. Évitez d'embarquer des secrets ou des outils de développement dans votre image.
5. Utilisez la version LTS (Long Term Support) du composant utilisé dans votre image.
6. Utilisez le fichier `.dockerignore` maintenu par l'équipe SRE pour limiter la taille de l'image et optimiser le cache et les builds.
7. Évitez d'utiliser des images de conteneurs basées sur DEBIAN ou UBUNTU.
8. Mettez régulièrement à jour les images de conteneurs pour bénéficier des dernières corrections de sécurité.

En suivant ces recommandations, vous pouvez renforcer la sécurité de votre image Docker.

---

# Comment lancer mon homologation de sécurité ?

Pour lancer votre homologation de sécurité, vous devez vous assurer que votre produit a atteint une certaine maturité et stabilité. De plus, vous devez assurer sa pérennité et obtenir le soutien de la direction métier du ministère. Ensuite, vous devez identifier un AQSSI (Agent Qualifié de la Sécurité des Systèmes d'Information) et un responsable de traitement qui assumeront les responsabilités pénales et juridiques. Une fois ces conditions remplies, vous pouvez suivre les étapes suivantes : collecte des pièces, analyse de risque (EBIOS), tests d'intrusions, plan de traitement des risques et enfin, la commission d'homologation qui validera les travaux réalisés pendant la démarche d'homologation RGS.

---

# Comment mettre à jour le standup de ma startup ?

Pour mettre à jour le standup de votre startup, vous devez suivre les étapes suivantes :

1. Visualisez la dernière publication de votre équipe dans l'application Standup.
2. Assurez-vous que votre équipe a déjà publié dans Carnets, car les slides de Standup sont basés sur les publications effectuées dans cette application.
3. Si votre équipe n'a jamais publié dans Carnets, elle n'aura pas de slide lui étant dédié dans Standup.
4. À la fin du standup, un slide liste les équipes visibles qui n'ont pas de publication dans Carnets. Si votre équipe est dans cette situation, vous aurez l'occasion de vous exprimer si vous le souhaitez.
5. Seule la dernière publication de votre équipe dans Carnets est prise en compte dans Standup.

Assurez-vous de suivre ces étapes pour mettre à jour le standup de votre startup.

---

# Peut-on utiliser google analytics ?

Il est recommandé de ne pas utiliser Google Analytics pour la mesure d'audience, sauf si vous avez recours à l'instance Matomo.

---

# Qui contacter pour une assistance technique ?

Pour une assistance technique, vous pouvez contacter les personnes suivantes :
- Yann-Fanch Madaule
- Vincent Borgis
- Eric
- Victoria
- Caroline de Kerhor
- Osiris PRISO
- Julien Bouquillon
- Igor RENQUIN (Lead Ops)
- Amir Rebzani
- Gary van Woerkens (_**en appui à l’équipe dév et SRE)**_
- Adrien Chauve
- Matéo Mévollon
- Jo Gottfreund
- Igor RENQUIN
- Gary van Woerkens
- Julien Bouquillon

---

# Comment deployer une branche de review ?

Pour déployer une branche de review, vous devez suivre les étapes suivantes :

1. Publiez les images Docker de vos applications sur le registre GitHub.
2. Déployez votre application à partir de ces images.

Assurez-vous également d'ajouter un job dans le fichier `.github/workflows/review.yaml` qui utilise l'action `SocialGouv/actions/autodevops-build-register` pour construire et enregistrer l'image Docker.

Ensuite, ajoutez un deuxième job dans le même fichier `review.yaml` qui utilise l'action de déploiement `SocialGouv/kube-workflow` pour déployer la branche de review dans l'environnement de développement de SocialGouv.

N'oubliez pas de créer un dossier `.kube-workflow` à la racine de votre dépôt, qui contiendra la configuration de votre déploiement au format HELM.

Assurez-vous également de configurer les variables d'environnement nécessaires dans votre dépôt, telles que `KUBECONFIG`, `RANCHER_PROJECT_ID` et `RANCHER_PROJECT_NAME`, pour que le déploiement fonctionne correctement.

Pour plus de détails sur la configuration personnalisée de `kube-workflow`, vous pouvez consulter la documentation sur le lien suivant : [kube-workflow](https://github.com/SocialGouv/kube-workflow).

---

