#!/bin/bash

OUT="./content7"

mkdir "$OUT" || true

npx --yes tiged https://github.com/betagouv/doc.incubateur.net-communaute "$OUT/documentation-beta" && rm -rf "$OUT/documentation-beta/.git" 
npx --yes tiged https://github.com/betagouv/beta.gouv.fr/content/_incubators "$OUT/incubators-beta" && rm -rf "$OUT/incubators-beta/.git" 
npx --yes tiged https://github.com/betagouv/beta.gouv.fr/content/_startups "$OUT/startups-beta" && rm -rf "$OUT/startups-beta/.git" 
npx --yes tiged https://github.com/betagouv/beta.gouv.fr/content/_organisations "$OUT/organisations-beta" && rm -rf "$OUT/organisations-beta/.git" 
npx --yes tiged https://github.com/socialgouv/support/docs "$OUT/support-sre-fabrique" && rm -rf "$OUT/support-sre-fabrique/.git" 

cd notion-dump && yarn

cd ..

mkdir "$OUT/notion-fabrique" || true

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
node notion-dump/dump.js 2107393f35c849e697bbb72423a877c2 > "$OUT/notion-fabrique/homologation securité rgs.md" 
node notion-dump/dump.js cce1bf7285c1457ab2cc78b8e5d726a8 > "$OUT/notion-fabrique/Mission, Vision, Valeurs.md" 
node notion-dump/dump.js 4fcee800ae7d4abc9c59e0537b3e3335 > "$OUT/notion-fabrique/OPS et SRE.md" 
