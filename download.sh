#!/bin/bash

set +x
set +e

OUT="./content"

mkdir "$OUT" || true

#tiged https://github.com/betagouv/doc.incubateur.net-communaute "$OUT/documentation-beta" && rm -rf "$OUT/documentation-beta/.git" 
#tiged https://github.com/betagouv/beta.gouv.fr/content/_incubators "$OUT/incubators-beta" && rm -rf "$OUT/incubators-beta/.git" 
#tiged https://github.com/betagouv/beta.gouv.fr/content/_startups "$OUT/startups-beta" && rm -rf "$OUT/startups-beta/.git" 
#tiged https://github.com/betagouv/beta.gouv.fr/content/_organisations "$OUT/organisations-beta" && rm -rf "$OUT/organisations-beta/.git" 
tiged https://github.com/socialgouv/support/docs "$OUT/support-sre-fabrique" && rm -rf "$OUT/support-sre-fabrique/.git" 
git clone https://github.com/SocialGouv/www.wiki.git "$OUT/www-wiki" && rm -rf "$OUT/www-wiki/.git" 


mkdir "$OUT/startups-beta" || true

wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/maison.de.lautisme.md -O "$OUT/startups-beta/maison.de.lautisme.md"
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/psyenfantado.md -O "$OUT/startups-beta/psyenfantado.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/conventionnement.iae.md -O "$OUT/startups-beta/conventionnement.iae.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/tumeplay.md -O "$OUT/startups-beta/tumeplay.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/enfants-du-spectacle.md -O "$OUT/startups-beta/enfants-du-spectacle.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/aides.jeunes.md -O "$OUT/startups-beta/aides.jeunes.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/didoc.md -O "$OUT/startups-beta/didoc.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/1000.jours.md -O "$OUT/startups-beta/1000.jours.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/ethique.en.sante.numerique.md -O "$OUT/startups-beta/ethique.en.sante.numerique.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/fiche.commune.entreprise.fce.md -O "$OUT/startups-beta/fiche.commune.entreprise.fce.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/pmi.md -O "$OUT/startups-beta/pmi.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/mano.md -O "$OUT/startups-beta/mano.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/egalite.professionnelle.md -O "$OUT/startups-beta/egalite.professionnelle.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/reva.md -O "$OUT/startups-beta/reva.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/nata.md -O "$OUT/startups-beta/nata.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/medle.md -O "$OUT/startups-beta/medle.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/domifa.md -O "$OUT/startups-beta/domifa.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/workinfrance.md -O "$OUT/startups-beta/workinfrance.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/l-application-du-cej.md -O "$OUT/startups-beta/l-application-du-cej.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/tremplin.md -O "$OUT/startups-beta/tremplin.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/e-mjpm.md -O "$OUT/startups-beta/e-mjpm.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/archifiltre.md -O "$OUT/startups-beta/archifiltre.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/codedutravail.md -O "$OUT/startups-beta/codedutravail.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/bpco.md -O "$OUT/startups-beta/bpco.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/monpsy.md -O "$OUT/startups-beta/monpsy.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/maraudes.md -O "$OUT/startups-beta/maraudes.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/monsuivipsy.md -O "$OUT/startups-beta/monsuivipsy.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/ozensemble.md -O "$OUT/startups-beta/ozensemble.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/1000.premiers.jours.blues.md -O "$OUT/startups-beta/1000.premiers.jours.blues.md";
wget https://raw.githubusercontent.com/betagouv/beta.gouv.fr/master/content/_startups/qualite-eau.md -O "$OUT/startups-beta/qualite-eau.md";

mkdir "$OUT/notion-fabrique" || true

echo "> downloading notion content"
# NEED NOTION_TOKEN env
node notion-dump/dump.js bb52915dfbe747419c4c914921fc19d4 > "$OUT/notion-fabrique/La fabrique in a nutshell.md" 
node notion-dump/dump.js df455e8378cb4b1c88c72ce38150459d > "$OUT/notion-fabrique/Firebase.md" 
#node notion-dump/dump.js 5392bff70bbc4d8b89ae9eff2e348943 > "$OUT/notion-fabrique/La fabrique pour tous4.md" 
#node notion-dump/dump.js 18c0f050420846379e0e971402c2f58c > "$OUT/notion-fabrique/La fabrique pour tous.md" 
node notion-dump/dump.js f10f2220dd4843d1aeb652e833ca5133 > "$OUT/notion-fabrique/Le trombi de la core team de la fabrique.md" 
node notion-dump/dump.js 2a381ef62c874772a7f8a6f8f57970e6 > "$OUT/notion-fabrique/Créer une fiche produit.md" 
node notion-dump/dump.js 0aa0f79d450e485dae19ba00a8a0986d > "$OUT/notion-fabrique/Les outils de la fabrique.md" 
node notion-dump/dump.js 71fd4b164b1b4c64a031f477f3f32abe > "$OUT/notion-fabrique/Lexique.md" 
#node notion-dump/dump.js bf40fbf1c07c4c6f99f7a4b73e377226 > "$OUT/notion-fabrique/Liste startups.md" 
node notion-dump/dump.js f93d6ced8bf54426ae59847149e10b93 > "$OUT/notion-fabrique/juridique et rgpd.md" 
node notion-dump/dump.js be5eaa1809744da0a7ed1dd01935aa75 > "$OUT/notion-fabrique/homologation securité rgs.md" 
node notion-dump/dump.js cce1bf7285c1457ab2cc78b8e5d726a8 > "$OUT/notion-fabrique/Mission, Vision, Valeurs.md" 
node notion-dump/dump.js 4fcee800ae7d4abc9c59e0537b3e3335 > "$OUT/notion-fabrique/OPS et SRE.md" 
# node notion-dump/dump.js b9bf84869eb94da4bb1b251f5cd5ee2f > "$OUT/notion-fabrique/agrément SIG pour obtenir des noms de domaine.md"  #confidential
node notion-dump/dump.js 7db7efeb28f0486c9b2f3a0cf4df16b8 > "$OUT/notion-fabrique/Plateforme - offre de valeur.md" 

OUTPATH="$OUT/standup-fabrique"
mkdir "$OUTPATH" || true

echo "> downloading standup content"
curl 'https://hasura-carnets.fabrique.social.gouv.fr/v1/graphql' \
  -H 'content-type: application/json' \
  --data-raw '{"query":"{\n  posts(\n    distinct_on: team_slug,\n    order_by: {team_slug: asc, created_at: desc}\n    where: {team_slug: {_nin: [\"fce\", \"transition-collective\", \"dora\", \"emjpm\", \"carnet-de-bord\", \"nos1000jours\", \"enfants-du-spectacle\"]}}\n  ) {\n    id\n    mood\n    term\n    needs\n    author\n    team_slug\n    priorities\n    created_at\n    team {\n      name\n      privacy\n      avatarUrl\n      description\n      parentTeam {\n        name\n      }\n      members(first: 100) {\n        nodes {\n          login\n          name\n          avatarUrl\n        }\n      }\n    }\n    kpis {\n      id\n      value\n      name\n    }\n  }\n}"}' \
  --compressed | jq -c '.data.posts[]' - |
while IFS=$'\n' read -r c; do
    startup=$(echo "$c" | jq -r '.team.name')
    team_slug=$(echo "$c" | jq -r '.team_slug')
    privacy=$(echo "$c" | jq -r '.team.privacy')
    created_at=$(echo "$c" | jq -r '.created_at')
    needs=$(echo "$c" | jq -r '.needs')
    priorities=$(echo "$c" | jq -r '.priorities')
    term=$(echo "$c" | jq -r '.term')
    ([ "$privacy" = "SECRET" ] || [ "$startup" = "null" ]) && continue # skip some
    OUTFILE="$OUTPATH/$team_slug.md"
    echo "---" > "$OUTFILE"
    echo "" >> "$OUTFILE"
    echo "startup: $startup" >> "$OUTFILE"
    echo "updated_at: ${created_at:0:10}" >> "$OUTFILE"
    echo "title: Dernieres nouvelles de la startup $startup" >> "$OUTFILE"
    echo "" >> "$OUTFILE"
    echo "---" >> "$OUTFILE"
    echo "" >> "$OUTFILE"
    echo "# Dernieres nouvelles de la startup $startup" >> "$OUTFILE"
    echo "" >> "$OUTFILE"
    echo "Date de mise à jour : ${created_at:0:10}" >> "$OUTFILE"
    echo "" >> "$OUTFILE"
    if [ "$needs" != "" ]; then
        echo "## Besoins" >> "$OUTFILE"
        echo "" >> "$OUTFILE"
        echo "$needs" >> "$OUTFILE"
        echo "" >> "$OUTFILE"
    fi
    if [ "$priorities" != "" ]; then
        echo "## Priorités" >> "$OUTFILE"
        echo "" >> "$OUTFILE"
        echo "$priorities" >> "$OUTFILE"
        echo "" >> "$OUTFILE"
    fi
    if [ "$term" != "" ]; then
        echo "## Écheances" >> "$OUTFILE"
        echo "" >> "$OUTFILE"
        echo "$term" >> "$OUTFILE"
        echo "" >> "$OUTFILE"
    fi
    echo "## KPIs" >> "$OUTFILE"
    echo "" >> "$OUTFILE"
    echo "$c" | jq -rc '.kpis[] | " - \(.name): \(.value)"' >> "$OUTFILE"

done