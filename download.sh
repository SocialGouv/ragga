#!/bin/bash

set +x
set +e

OUT="./content"

mkdir "$OUT" || true

tiged https://github.com/betagouv/doc.incubateur.net-communaute "$OUT/documentation-beta" && rm -rf "$OUT/documentation-beta/.git" 
tiged https://github.com/betagouv/beta.gouv.fr/content/_incubators "$OUT/incubators-beta" && rm -rf "$OUT/incubators-beta/.git" 
tiged https://github.com/betagouv/beta.gouv.fr/content/_startups "$OUT/startups-beta" && rm -rf "$OUT/startups-beta/.git" 
#tiged https://github.com/betagouv/beta.gouv.fr/content/_organisations "$OUT/organisations-beta" && rm -rf "$OUT/organisations-beta/.git" 

