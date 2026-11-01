# -*- coding: utf-8 -*-
"""Fabrique toutes les maquettes HTML, le plan des pages et l'index plan/23-MAQUETTES-INDEX.md.

Usage : python3 maquettes/_fabrique/fabrique.py
Lot M1 : deux produits distincts (CRM Pro, Envoi), menu réel de Will, reprise fidèle de l'existant.
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from socle import *  # noqa: E402,F401,F403
import socle  # noqa: E402
import pages_crm_base  # noqa: E402
import pages_crm_reseau  # noqa: E402
import pages_crm_reglages  # noqa: E402
import pages_envoi  # noqa: E402

MAQ = os.path.dirname(ICI)
DEPOT = os.path.dirname(MAQ)
MODULES = (pages_crm_base, pages_crm_reseau, pages_crm_reglages, pages_envoi)


def groupes():
    """Range chaque page sous l'entrée de menu qui l'allume, dans l'ordre du menu."""
    reg = socle.REGISTRE
    out = []
    for prod, nav in (('crm', NAV_CRM), ('envoi', NAV_ENVOI)):
        for gid, gtitre, items in nav:
            pages = []
            for cle, lib, _i, _c in items:
                f = cle + '.html'
                pages += [f] + sorted(x for x, v in reg.items() if v['menu'] == lib and x != f)
            titre = ('%s · %s' % (PRODUITS[prod]['nom'], gtitre)) if gtitre else PRODUITS[prod]['nom']
            out.append((titre, prod, pages))
    hors = sorted(x for x, v in reg.items() if v['menu'] in ('Hors menu', '—') and x != 'plan-des-pages.html')
    out.append(('Hors coquille (écrans seuls)', 'crm', hors))
    return out


def plan_des_pages():
    reg = socle.REGISTRE
    h = []
    n = 0
    for titre, prod, pages in groupes():
        lig = []
        for f in pages:
            v = reg[f]
            n += 1
            rep = ('<span class="mono">%s</span>' % E(v['reprise'])) if v['reprise'] else badge('violet', 'Nouvelle', '+')
            lig.append(['<a href="%s"><strong>%s</strong></a>' % (f, E(v['titre'])), '<span class="tag-produit %s">%s</span>' % (v['produit'], PRODUITS[v['produit']]['court']), rep])
        h.append(mini_titre(titre) + tableau(titre, ['Page', 'Produit', 'Reprise de'], lig))
    reprises = sum(1 for v in reg.values() if v['reprise'])
    return page('plan-des-pages', 'Toutes les maquettes', '<strong>%d pages</strong> · %d reprises de l’existant · %d nouvelles · 2 produits.' % (n + 1, reprises, n + 1 - reprises),
                ''.join(h), produit='crm', reprise=None)


def index_md():
    reg = socle.REGISTRE
    l = ['# 23 : Index des maquettes (lot M1 : deux produits, menu réel, reprise fidèle) : 01/11/2026', '',
         '**But.** Montrer TOUTES les pages avant tout codage d’écran. Ouvrir `maquettes/index.html` dans un navigateur (mode d’emploi : `maquettes/LISEZ-MOI.md`).', '',
         '**Décisions de Will appliquées (lot M1).**',
         '- **D1. Deux produits distincts**, facturés à part : **CRM Pro** (bleu de marque `#2448e5`) et **Envoi** (bleu-vert `#0a6e78`, texte blanc 6,0:1). Chaque page montre son produit : liseré coloré du menu, sélecteur de produit en haut du menu, badge et bande de couleur dans l’en-tête, bouton principal de la couleur du produit.',
         '- **D2. Menu du CRM = menu réel de Will, à l’identique** (`Sidebar.tsx`) : Tableau de bord ; À traiter ; Ma base ; Presse ; Réseaux ; Ciblage ; Alimenter la base ; Réglages ; Technique (accordéon : une section ouverte à la fois). **Envoi** est un espace à part : Campagnes, Réponses, Boîtes d’envoi, Domaines, Serveurs et adresses IP, Chauffe, Santé des envois, Désinscriptions, Alertes d’envoi, Réglages d’envoi.',
         '- **D3. Fidélité à l’existant** : chaque page qui existe dans le CRM réel reprend ses titres, colonnes, filtres, actions et textes (relevé du code, lecture seule). La colonne « Reprise de » donne le composant ; « Nouvelle » sinon. La même note est affichée en tête de chaque page (cadre « Maquette »).',
         '- **D4. Style** : `maquettes/GUIDE-STYLE.md`. **D5. Ajouts** : les 52 ajouts du plan 27 (dont les 15 premiers) ; voir le tableau en fin de fichier. **D6.** La cloche se remplit (6 notifications, des deux produits). **D7.** Données factices réalistes, aucun vrai nom.', '',
         '**États.** Chaque écran a un état normal, vide, erreur et chargement (cadre « Maquette » sous l’en-tête, ou `?etat=vide`, `?etat=erreur`, `?etat=chargement`).', '']
    total = 0
    for titre, prod, pages in groupes():
        l += ['## %s' % titre, '', '| Page | Maquette | Produit | Reprise de |', '|---|---|---|---|']
        for f in pages:
            v = reg[f]
            total += 1
            l.append('| %s | `maquettes/%s` | %s | %s |' % (v['titre'], f, PRODUITS[v['produit']]['nom'], ('`' + v['reprise'] + '`') if v['reprise'] else 'Nouvelle'))
        l.append('')
    rep = sum(1 for v in reg.values() if v['reprise'])
    crm = sum(1 for v in reg.values() if v['produit'] == 'crm')
    l += ['## Totaux', '',
          '- **%d pages** (+ le plan des pages) : **%d reprises** de l’existant, **%d nouvelles**. Produit CRM Pro : %d ; produit Envoi : %d.' % (total, rep, total - rep, crm, total - crm),
          '- Toutes les routes de `routeTree.tsx` ont une page : `/doublons`, `/console/arbitrage`, `/console/propositions`, `/companies(/$id)`, `/console/contacts` (et `/contacts`), `/console/lettre-et-guide(/$id)`, `/console/vivier`, `/console/personnes/$key`, `/media(/$id)`, `/journalists(/$id)`, `/presse/envois`, `/federations(/$id)`, `/evenements(/$id)`, `/audiences(/new, /$id)`, `/listes(/$id)`, `/campaigns(/new, /$id)` (= Collectes), `/coverage`, `/settings`, `/users`, `/tags`, `/rgpd/requests`, `/international/roumanie`, `/scraper-runs`, `/admin/observability`, `/llm/router`, `/llm/proxy-providers`, `/llm/rotations`, `/rgpd/ai-act`, `/audit-logs`, `/login`, `/2fa`, `/magic-link`, `/password-reset`, page introuvable.',
          '- Pages sans entrée de menu (le menu reste celui de Will) : Mes tâches et Affaires (onglets du Tableau de bord), Mon compte (avatar), Sauvegardes (carte de Santé du système) ; côté Envoi : Résultats, Messages types, Calendrier (onglets de Campagnes), Chercher un envoi et Feu vert (onglets de Santé des envois), Configuration (onglet de Serveurs), fiches Boîte et Domaine.',
          '- Pages retirées par rapport au lot U1bis : `a-valider`, `presse`, `reseaux`, `technique`, `statistiques`, `reglages`, `equipe`, `sauvegardes`, `mise-en-route`, `v1-ecrans` (leur contenu est réparti dans les pages ci-dessus, au bon endroit du menu de Will). Les écrans V1/V2 (clients, synchro, API…) restent décrits au plan 20.', '',
          '## Les 15 ajouts prioritaires du plan 27 : où les voir', '',
          '| Rang | Ajout | Maquette |', '|---|---|---|',
          '| 1 | Campagne vers une étiquette | `etiquettes.html` (bouton plein), `entreprise.html`, `campagnes.html`, `campagne-nouvelle.html` (étape 1) |',
          '| 2 | Fiche d’un domaine (30 jours) | `domaine.html` |', '| 3 | Fiche d’une boîte | `boite.html` |',
          '| 4 | État de chaque destinataire | `campagne-suivi.html` (onglet Destinataires), `contact.html` |',
          '| 5 | Résultats par boîte, domaine, liste | `resultats.html` |', '| 6 | Répondre depuis le CRM | `reponses.html` (bloc Répondre, même fil) |',
          '| 7 | Reprogrammer (changer la date) | `campagnes.html`, `campagne-suivi.html` (fenêtre « Changer la date ») |', '| 8 | Dupliquer | `campagnes.html`, `campagne-suivi.html` |',
          '| 9 | Pause depuis la liste | `campagnes.html` (bouton Pause dans la ligne) |', '| 10 | Terminer | `campagnes.html`, `campagne-suivi.html` |',
          '| 11 | Ajouter une adresse IP (et appliquer) | `serveurs.html` (fenêtre), Ctrl K |', '| 12 | Chercher un envoi | `chercher-envoi.html`, Ctrl K, `campagnes.html` |',
          '| 13 | Éditeur ET / OU / SAUF | `audience-nouvelle.html` |', '| 14 | Export d’une liste ou sélection | `entreprises.html`, `contacts.html`, `listes.html`, `liste.html`, `audience.html`, `etiquettes.html` |',
          '| 15 | Export du registre des oppositions | `desinscriptions.html`, `rgpd.html` |',
          '| + | Programmer / reprogrammer, test A/B | `campagne-nouvelle.html` (étapes 2 et 3), `campagne-suivi.html` (onglet Test A/B) |', '',
          '## Fabrication', '',
          'Les fichiers HTML sont produits par `maquettes/_fabrique/fabrique.py` (Python 3, sans dépendance). Contrôle : `python3 maquettes/_fabrique/controle.py --toutes` (Playwright). Ce fichier 23 est régénéré en même temps.', '']
    return '\n'.join(l)


def main():
    pages = {}
    for m in MODULES:
        pages.update(m.P)
    pages['plan-des-pages.html'] = plan_des_pages()
    # Retire les anciennes pages qui ne sont plus fabriquées
    for f in os.listdir(MAQ):
        if f.endswith('.html') and f not in pages:
            os.remove(os.path.join(MAQ, f))
    for nom, contenu in pages.items():
        with open(os.path.join(MAQ, nom), 'w', encoding='utf-8') as fh:
            fh.write(contenu)
    with open(os.path.join(DEPOT, 'plan', '23-MAQUETTES-INDEX.md'), 'w', encoding='utf-8') as fh:
        fh.write(index_md())
    print('%d pages écrites.' % len(pages))


if __name__ == '__main__':
    main()
