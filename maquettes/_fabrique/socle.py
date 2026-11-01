# -*- coding: utf-8 -*-
"""Socle commun des maquettes : coquille, menu, icônes et petites briques HTML.

Les pages HTML du dossier maquettes/ sont FABRIQUÉES par ce script :
    python3 maquettes/_fabrique/fabrique.py
Modifier ici puis relancer, plutôt que d'éditer les .html à la main.
Données factices uniquement (domaines en .example, aucune IP, aucune personne réelle).
"""
import html

E = html.escape

# ---------- Icônes SVG simples (traits) ----------
_IC = {
    'accueil': '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    'personnes': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14.5c2.3 0 4 1.5 4.6 4"/>',
    'personne': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
    'entreprise': '<rect x="4" y="3" width="11" height="18" rx="1.5"/><path d="M15 9h4.5v12H15"/><path d="M8 7h3M8 11h3M8 15h3"/>',
    'affaires': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2"/><path d="M3 12h18"/>',
    'taches': '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M8 12l3 3 5-6"/>',
    'campagne': '<path d="M3 10v4l11 5V5L3 10z"/><path d="M14 8a4 4 0 010 8"/><path d="M6 14.5l1.5 5h3l-1-4"/>',
    'message': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5L12 13l8.5-6.5"/>',
    'reponses': '<path d="M4 5h16v11H8l-4 4V5z"/><path d="M8 9h8M8 12h5"/>',
    'presse': '<rect x="3" y="4" width="15" height="16" rx="2"/><path d="M18 8h3v10a2 2 0 01-2 2"/><path d="M7 8h7M7 12h7M7 16h4"/>',
    'sante': '<path d="M3 12h4l2-5 4 10 2-5h6"/>',
    'boite': '<path d="M3 13l2.5-7h13L21 13v6H3v-6z"/><path d="M3 13h5l1 2h6l1-2h5"/>',
    'domaine': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.7 3.6 5.7 3.6 9s-1.1 6.3-3.6 9c-2.5-2.7-3.6-5.7-3.6-9S9.5 5.7 12 3z"/>',
    'serveur': '<rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M7 7.5h.01M7 16.5h.01"/>',
    'chauffe': '<path d="M12 3c1 3 4 4.5 4 8.5a4 4 0 01-8 0c0-1.6.6-2.7 1.5-3.6.2 1.4 1 2.1 1.5 2.1C11 7.5 11 5 12 3z"/><path d="M6 15a6 6 0 0012 0"/>',
    'alerte': '<path d="M12 3l9.5 17h-19L12 3z"/><path d="M12 10v4.5M12 17.5h.01"/>',
    'cloche': '<path d="M6 16V11a6 6 0 1112 0v5l1.5 2h-15L6 16z"/><path d="M10 20.5a2 2 0 004 0"/>',
    'interdit': '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
    'stats': '<path d="M4 20V10M10 20V4M16 20v-7M21 20H3"/>',
    'reglages': '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.8l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.8-.3 1.7 1.7 0 00-1 1.5V21a2 2 0 11-4 0v-.1a1.7 1.7 0 00-1.1-1.5 1.7 1.7 0 00-1.8.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.8 1.7 1.7 0 00-1.5-1H3a2 2 0 110-4h.1a1.7 1.7 0 001.5-1.1 1.7 1.7 0 00-.3-1.8l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.8.3H9a1.7 1.7 0 001-1.5V3a2 2 0 114 0v.1a1.7 1.7 0 001 1.5 1.7 1.7 0 001.8-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.8V9a1.7 1.7 0 001.5 1H21a2 2 0 110 4h-.1a1.7 1.7 0 00-1.5 1z"/>',
    'chercher': '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'fermer': '<path d="M6 6l12 12M18 6L6 18"/>',
    'chevron': '<path d="M6 9l6 6 6-6"/>',
    'fleche': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'arret': '<path d="M12 3v8"/><path d="M6.3 7.3a8 8 0 1011.4 0"/>',
    'bouclier': '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/>',
    'journal': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5"/><path d="M9 12h7M9 16h7"/>',
    'sauvegarde': '<ellipse cx="12" cy="5.5" rx="8" ry="2.5"/><path d="M4 5.5v6c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5v-6"/><path d="M4 11.5v6c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5v-6"/>',
    'cle': '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l2 2M15 8l2 2"/>',
    'outil': '<path d="M14.7 6.3a4 4 0 00-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 005.4-5.4l-2.5 2.5-2.4-.6-.6-2.4 2.5-2.5z"/>',
    'collecte': '<path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M4 17v3h16v-3"/>',
    'carte': '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
    'liste': '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>',
    'etiquette': '<path d="M3 12V4h8l10 10-8 8L3 12z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
    'doublon': '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 00-1-1H5a1 1 0 00-1 1v10a1 1 0 001 1h3"/>',
    'calendrier': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'telephone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
    'note': '<path d="M5 3h14v18H5z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    'envoi': '<path d="M21 3L10 14"/><path d="M21 3l-7 18-4-7-7-4 18-7z"/>',
    'oeil': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    'verrou': '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 118 0v3"/>',
    'equipe': '<circle cx="12" cy="7" r="3"/><circle cx="5" cy="10" r="2.2"/><circle cx="19" cy="10" r="2.2"/><path d="M6.5 20c.6-3.5 2.8-5.5 5.5-5.5s4.9 2 5.5 5.5"/><path d="M1.8 18c.3-2 1.5-3.3 3.2-3.5M22.2 18c-.3-2-1.5-3.3-3.2-3.5"/>',
    'lien': '<path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/>',
    'etincelle': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/>',
    'horloge': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'rafraichir': '<path d="M20 11a8 8 0 10-2.3 5.7"/><path d="M20 4v7h-7"/>',
    'pause': '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>',
    'test': '<path d="M9 3h6M10 3v6l-5 9a2 2 0 001.7 3h10.6a2 2 0 001.7-3l-5-9V3"/><path d="M7.5 14h9"/>',
    'export': '<path d="M12 15V3"/><path d="M7 8l5-5 5 5"/><path d="M4 15v5h16v-5"/>',
    'aide': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 114 2c-.9.6-1.5 1.1-1.5 2.5M12 17h.01"/>',
    'pieces': '<path d="M4 7h16M4 12h16M4 17h10"/>',
    'puzzle': '<path d="M10 3a2 2 0 014 0v2h4v4h-2a2 2 0 000 4h2v6H5v-6h2a2 2 0 000-4H5V5h5V3z"/>',
    'coche': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'croix': '<path d="M6 6l12 12M18 6L6 18"/>',
    'filtre': '<path d="M3 5h18l-7 8v6l-4 2v-8L3 5z"/>',
    'fichier': '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5"/>',
    'chevron-d': '<path d="M9 6l6 6-6 6"/>',
    'eclair': '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
    'ajout-personne': '<circle cx="10" cy="8" r="4"/><path d="M2.5 21c.9-4 3.9-6 7.5-6 1.6 0 3 .4 4.2 1.1"/><path d="M19 14v6M16 17h6"/>',
    'cible': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    'fusee': '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M9 15l-3-3c1.5-4.5 5.5-8.5 13-9-.5 7.5-4.5 11.5-9 13l-1-1z"/><circle cx="15" cy="9" r="1.6"/>',
    'carte-france': '<path d="M9 3l5 2 4-1 1 5 2 3-3 5 1 4-6-1-5 1-3-4 1-5-3-3 4-2 2-4z"/>',
}


def ic(nom, classe=''):
    c = 'ic' + (' ' + classe if classe else '')
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>' % (c, _IC[nom])


# ---------- Menu (barre latérale groupée) ----------
NAV = [
    ('travailler', 'Travailler', [
        ('index', 'Aujourd’hui', 'accueil', '12'),
        ('contacts', 'Contacts', 'personnes', ''),
        ('entreprises', 'Entreprises', 'entreprise', ''),
        ('affaires', 'Affaires', 'affaires', ''),
        ('taches', 'Tâches', 'taches', '5'),
    ]),
    ('prospecter', 'Prospecter', [
        ('campagnes', 'Campagnes', 'campagne', '1'),
        ('messages-types', 'Messages types', 'message', ''),
        ('reponses', 'Réponses', 'reponses', '7'),
        ('presse', 'Presse', 'presse', ''),
    ]),
    ('envois', 'Envois', [
        ('sante', 'Santé des envois', 'sante', ''),
        ('boites', 'Boîtes d’envoi', 'boite', ''),
        ('domaines', 'Domaines', 'domaine', ''),
        ('serveurs', 'Serveurs', 'serveur', ''),
        ('chauffe', 'Montée en douceur', 'chauffe', ''),
        ('alertes', 'Alertes', 'alerte', '1'),
        ('desinscriptions', 'Désinscriptions', 'interdit', ''),
    ]),
    ('mesurer', 'Mesurer', [
        ('statistiques', 'Statistiques', 'stats', ''),
    ]),
]
PIED = [
    ('reglages', 'Réglages', 'reglages', ''),
    ('plan-des-pages', 'Toutes les maquettes', 'liste', ''),
]
TITRE_NAV = {k: lib for _, _, items in NAV for k, lib, _, _ in items}
TITRE_NAV.update({k: lib for k, lib, _, _ in PIED})


def _lien_nav(cle, lib, icone, compteur, actif):
    cur = ' aria-current="page"' if cle == actif else ''
    badge = ''
    if compteur:
        badge = '<span class="compteur" aria-hidden="true">%s</span><span class="visuellement-cache">, %s à traiter</span>' % (compteur, compteur)
    if cle == 'sante':
        badge = '<span class="point-feu" aria-hidden="true"></span><span class="visuellement-cache">, état : bon</span>'
    return '<li><a class="nav-lien" href="%s.html" title="%s"%s>%s<span class="lib">%s</span>%s</a></li>' % (cle, E(lib), cur, ic(icone), E(lib), badge)


def barre_laterale(actif):
    h = ['<aside class="barre" id="barre-laterale" aria-label="Barre latérale">',
         '<a class="barre-marque" href="index.html"><span class="barre-logo" aria-hidden="true">A</span><span><strong>Axion CRM Pro</strong></span></a>',
         '<button type="button" class="espace" data-ouvre="fen-espace" aria-label="Espace actuel : Axion-IA. Changer d’espace"><span class="repere" aria-hidden="true"></span><span class="nom">Axion-IA</span>%s</button>' % ic('chevron', 'petite'),
         '<nav aria-label="Navigation principale">']
    for gid, gtitre, items in NAV:
        h.append('<div class="groupe"><button type="button" class="groupe-titre" aria-expanded="true" aria-controls="g-%s">%s %s</button>' % (gid, E(gtitre), ic('chevron', 'petite')))
        h.append('<ul id="g-%s">' % gid)
        for cle, lib, icone, cpt in items:
            h.append(_lien_nav(cle, lib, icone, cpt, actif))
        h.append('</ul></div>')
    h.append('</nav><div class="barre-pied"><ul class="liste-pied">')
    for cle, lib, icone, cpt in PIED:
        h.append(_lien_nav(cle, lib, icone, cpt, actif))
    h.append('</ul></div></aside>')
    return '\n'.join(h)


PALETTE = [
    ('Actions', [('campagne-nouvelle.html', 'Nouvelle campagne', 'plus'), ('contacts.html#ajout', 'Ajouter un contact', 'plus'),
                 ('reponses.html', 'Traiter les réponses', 'reponses'), ('desinscriptions.html', 'Puis-je écrire à… ?', 'interdit'),
                 ('sante.html', 'Tout arrêter', 'arret'), ('domaines.html', 'Ajouter un domaine', 'domaine')]),
    ('Pages', [(k + '.html', TITRE_NAV[k], 'fleche') for _, _, it in NAV for k, _, _, _ in it] + [('reglages.html', 'Réglages', 'reglages')]),
    ('Récents', [('entreprise.html', 'Boulangerie Martin', 'entreprise'), ('contact.html', 'Paul Martin', 'personne'), ('campagne-suivi.html', 'Organisateurs Rhône-Alpes', 'campagne')]),
]


def entete(fil):
    pal = ['<dialog class="palette" id="palette" aria-label="Rechercher ou agir"><label class="visuellement-cache" for="palette-champ">Rechercher une page, une fiche ou une action</label>',
           '<input id="palette-champ" type="search" placeholder="Rechercher ou agir…" autocomplete="off"><ul id="palette-liste">']
    for g, items in PALETTE:
        pal.append('<li class="groupe-pal" aria-hidden="true">%s</li>' % E(g))
        for href, lib, icone in items:
            pal.append('<li><a href="%s">%s%s</a></li>' % (href, ic(icone, 'petite'), E(lib)))
    pal.append('</ul></dialog>')
    fil_html = ''.join(
        ('<li><a href="%s">%s</a></li>' % (h, E(t))) if h else ('<li aria-current="page">%s</li>' % E(t)) for t, h in fil)
    return '''
<div class="bandeau-arret" id="bandeau-arret" role="alert" hidden>%s<span style="flex:1 1 200px">Tous les envois sont arrêtés depuis 10:42 par Will.</span><button type="button" class="btn petit-btn" data-reprendre>Reprendre les envois</button></div>
<header class="entete">
  <button type="button" class="bouton-icone bouton-menu" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="barre-laterale">%s</button>
  <nav class="fil" aria-label="Fil d’Ariane"><ol>%s</ol></nav>
  <button type="button" class="recherche" data-palette aria-label="Rechercher ou agir (Ctrl K)">%s<span class="lib-recherche">Rechercher ou agir…</span><kbd>Ctrl K</kbd></button>
  <a class="feu-entete" href="sante.html" aria-label="État des envois : normaux"><span aria-hidden="true">●</span><span class="mot-feu">Envois : normaux</span></a>
  <button type="button" class="bouton-icone" id="bouton-cloche" aria-label="Alertes : 3 non lues" aria-expanded="false" aria-controls="panneau-alertes">%s<span class="pastille" aria-hidden="true">3</span></button>
  <button type="button" class="btn btn-danger petit-btn bouton-arret" data-ouvre="fen-arret" aria-label="Tout arrêter">%s<span class="mot-arret">Tout arrêter</span></button>
  <a href="compte.html" class="avatar" aria-label="Mon compte (Will)">W</a>
</header>
<div class="panneau-alertes" id="panneau-alertes" hidden role="region" aria-label="Dernières alertes">
  <h2 style="margin-bottom:8px">Alertes</h2>
  <ul class="liste">
    <li><span class="badge ambre" data-s="▲">Attention</span><span class="quoi"><strong>Boîte « claire@ » ralentie</strong><small>Refus temporaires : 3 %%. Il y a 12 min.</small></span></li>
    <li><span class="badge terracotta" data-s="●">À faire</span><span class="quoi"><strong>2 réponses intéressées</strong><small>Il y a 25 min.</small></span></li>
    <li><span class="badge vert" data-s="✓">Fait</span><span class="quoi"><strong>Test du matin réussi</strong><small>07:05, 4 témoins sur 4.</small></span></li>
  </ul>
  <div class="bloc-pied"><a class="btn btn-contour petit-btn" href="alertes.html">Voir toutes les alertes</a><a class="btn btn-discret petit-btn" href="reglages-alertes.html">Régler les alertes</a></div>
</div>
%s
<dialog id="fen-arret" aria-labelledby="t-arret">
  <div class="fen-tete">%s<h2 id="t-arret">Tout arrêter · Axion-IA ?</h2></div>
  <div class="fen-corps"><p>Plus aucun message ne part, toutes boîtes et campagnes confondues. Rien n’est perdu : les envois reprennent quand vous cliquez sur « Reprendre ».</p></div>
  <div class="fen-pied"><button type="button" class="btn btn-contour" data-ferme>Ne rien changer</button><button type="button" class="btn btn-danger-plein" data-ferme data-arreter>Arrêter tous les envois</button></div>
</dialog>
<dialog id="fen-espace" aria-labelledby="t-espace">
  <div class="fen-tete"><h2 id="t-espace">Changer d’espace</h2><button type="button" class="bouton-icone" data-ferme aria-label="Fermer">%s</button></div>
  <div class="fen-corps"><ul class="liste">
    <li><span class="repere" style="width:12px;height:12px;border-radius:50%%;background:#2346c8" aria-hidden="true"></span><span class="quoi"><strong>Axion-IA</strong><small>Espace actuel</small></span><span class="badge vert" data-s="✓">Actuel</span></li>
    <li><span class="repere" style="width:12px;height:12px;border-radius:50%%;background:#b45309" aria-hidden="true"></span><span class="quoi"><strong>Garage Durand (factice)</strong><small>Client · V1</small></span><a class="btn btn-contour petit-btn" href="v1-ecrans.html#clients">Ouvrir</a></li>
  </ul></div>
</dialog>''' % (ic('arret'), ic('menu'), fil_html, ic('chercher'), ic('cloche'), ic('arret'), '\n'.join(pal), ic('alerte'), ic('fermer'))


SELECTEUR = '''<form class="selecteur-etat" aria-label="Maquette : choisir l’état affiché" onsubmit="return false"><fieldset><legend>Maquette</legend>
<label><input type="radio" name="etat" value="normal" checked><span>Normal</span></label>
<label><input type="radio" name="etat" value="vide"><span>Vide</span></label>
<label><input type="radio" name="etat" value="erreur"><span>Erreur</span></label>
<label><input type="radio" name="etat" value="chargement"><span>Chargement</span></label>
</fieldset></form>'''

SQUELETTE = '''<div id="squelette" class="squelette" hidden aria-label="Chargement en cours"><div class="os" style="height:34px;width:40%"></div><div class="os" style="height:20px;width:60%"></div>
<div class="kpis" style="margin:0"><div class="os" style="height:150px"></div><div class="os" style="height:150px"></div><div class="os" style="height:150px"></div><div class="os" style="height:150px"></div></div><div class="os" style="height:280px"></div></div>'''


def document(titre, corps, description=''):
    return '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="%s">
<meta name="robots" content="noindex">
<title>%s · Axion CRM Pro (maquette)</title>
<link rel="stylesheet" href="style.css">
</head>
%s
<script src="app.js"></script>
</html>
''' % (E(description or titre), E(titre), corps)


def page(cle, titre, phrase, normal, vide=None, erreur=None, actions='', fil=None, onglets_haut='', apres=''):
    """Écran dans la coquille. `actions` = boutons d'en-tête affichés seulement à l'état normal."""
    actif = cle if cle in TITRE_NAV else (fil[0][2] if fil and len(fil[0]) > 2 else cle)
    fil_simple = [(t, h) for (t, h, *_r) in (fil or [])] + [(titre, None)]
    if vide is None:
        vide = etat_vide('liste', 'Rien à afficher pour le moment', 'Les éléments apparaîtront ici dès qu’il y en aura.', '')
    if erreur is None:
        erreur = etat_erreur()
    tete = '''<div class="tete-page"><div class="titres"><h1>%s</h1><p class="phrase-etat" data-seulement="normal">%s</p></div>%s</div>''' % (
        E(titre), phrase, ('<div class="actions" data-seulement="normal">%s</div>' % actions) if actions else '')
    corps = '''<body>
<a class="lien-evitement" href="#contenu">Aller au contenu</a>
<div class="coquille">
%s
<div class="principal">
%s
%s
<main id="contenu" class="contenu" tabindex="-1">
%s
%s
<section data-etat="normal" aria-label="Contenu">%s</section>
<section data-etat="vide" hidden aria-label="Aucun élément">%s</section>
<section data-etat="erreur" hidden aria-label="Erreur">%s</section>
%s
</main>
</div>
</div>
<div class="toasts" id="toasts" aria-live="polite"></div>
%s
</body>''' % (barre_laterale(actif), entete(fil_simple), SELECTEUR, tete, onglets_haut, normal, vide, erreur, SQUELETTE, apres)
    return document(titre, corps, re_texte(phrase))


def re_texte(h):
    import re
    return re.sub('<[^>]+>', '', h)


def ecran_seul(titre, contenu, selecteur=True):
    corps = '<body><main id="contenu" class="ecran-seul" tabindex="-1">%s%s</main><div class="toasts" id="toasts" aria-live="polite"></div></body>' % (
        SELECTEUR if selecteur else '', contenu)
    return document(titre, corps)


# ---------- Briques ----------
def btn(texte, sorte='contour', href=None, icone=None, attrs=''):
    cl = {'plein': 'btn btn-plein', 'contour': 'btn btn-contour', 'discret': 'btn btn-discret', 'danger': 'btn btn-danger',
          'petit': 'btn btn-contour petit-btn', 'petit-discret': 'btn btn-discret petit-btn'}[sorte]
    i = ic(icone) if icone else ''
    if href:
        return '<a class="%s" href="%s" %s>%s%s</a>' % (cl, href, attrs, i, E(texte))
    return '<button type="button" class="%s" %s>%s%s</button>' % (cl, attrs, i, E(texte))


def badge(teinte, mot, s='●'):
    return '<span class="badge %s" data-s="%s">%s</span>' % (teinte, s, E(mot))


FEU = {'vert': ('vert', '●', 'Bon'), 'ambre': ('ambre', '▲', 'Attention'), 'rouge': ('rouge', '■', 'Arrêté'), 'gris': ('gris', '○', 'Inconnu')}


def feu(etat, mot=None):
    t, s, m = FEU[etat]
    return badge(t, mot or m, s)


def tuiles(items):
    h = ['<div class="tuiles">']
    for it in items:
        lib, val, meta = it[0], it[1], it[2] if len(it) > 2 else ''
        h.append('<div class="tuile"><div class="lib">%s</div><div class="val">%s</div><div class="meta">%s</div></div>' % (E(lib), val, meta))
    h.append('</div>')
    return ''.join(h)


MOTS = {'terracotta': 'À faire', 'bleu': 'En cours', 'vert': 'Fait', 'ambre': 'Attention', 'violet': 'Nouveau', 'gris': 'Info'}


def bloc(titre, contenu, teinte=None, icone=None, mot=None, pied='', attrs=''):
    cl = 'bloc' + (' teinte-' + teinte if teinte else '')
    tete = '<div class="bloc-tete">%s<h2>%s</h2>%s</div>' % (ic(icone) if icone else '', E(titre),
                                                          ('<span class="mot">%s</span>' % E(mot or MOTS[teinte])) if teinte else '')
    return '<section class="%s" %s>%s%s%s</section>' % (cl, attrs, tete, contenu, ('<div class="bloc-pied">%s</div>' % pied) if pied else '')


def tableau(legende, colonnes, lignes, cartes=True, liens=None, secondaires=()):
    """secondaires = index des colonnes masquées entre 768 et 1180 px (classe col-sec)."""
    h = ['<div class="tableau-cadre"><table%s><caption class="visuellement-cache">%s</caption><thead><tr>' % (' class="cartes"' if cartes else '', E(legende))]
    for k, c in enumerate(colonnes):
        h.append('<th scope="col"%s>%s</th>' % (' class="col-sec"' if k in secondaires else '', E(c) if c else '<span class="visuellement-cache">Actions</span>'))
    h.append('</tr></thead><tbody>')
    for n, l in enumerate(lignes):
        h.append('<tr data-href="%s">' % liens[n] if liens and liens[n] else '<tr>')
        for i, cellule in enumerate(l):
            lab = colonnes[i] if i < len(colonnes) else ''
            cls = (['actions-ligne'] if lab == '' else []) + (['col-sec'] if i in secondaires else [])
            cl = (' class="%s"' % ' '.join(cls)) if cls else ''
            h.append('<td data-label="%s"%s>%s</td>' % (E(lab), cl, cellule))
        h.append('</tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def etat_vide(icone, titre, phrase, bouton):
    return '<div class="etat-vide">%s<h2>%s</h2><p>%s</p>%s</div>' % (ic(icone, 'grande'), E(titre), phrase, bouton)


def etat_erreur(phrase='Les données n’ont pas pu être lues. Rien n’est perdu. Réessayez dans un instant.', titre='Lecture impossible'):
    return '<div class="etat-erreur" role="alert">%s<h2>%s</h2><p>%s</p>%s</div>' % (
        ic('alerte', 'grande'), E(titre), phrase, '<button type="button" class="btn btn-plein" data-reessayer>Réessayer</button>')


def onglets(nom, items):
    """items = [(id, libellé, contenu)] ; onglets accessibles (role=tablist)."""
    t = ['<div class="onglets" role="tablist" aria-label="%s">' % E(nom)]
    p = []
    for i, (oid, lib, contenu) in enumerate(items):
        t.append('<button type="button" role="tab" id="tab-%s" aria-controls="pan-%s" aria-selected="%s">%s</button>' % (oid, oid, 'true' if i == 0 else 'false', lib))
        p.append('<div role="tabpanel" id="pan-%s" aria-labelledby="tab-%s" tabindex="0"%s>%s</div>' % (oid, oid, '' if i == 0 else ' hidden', contenu))
    t.append('</div>')
    return ''.join(t) + ''.join(p)


def champ(lib, cid, type_='text', valeur='', aide='', attrs=''):
    a = ('<span class="aide" id="%s-aide">%s</span>' % (cid, aide)) if aide else ''
    da = (' aria-describedby="%s-aide"' % cid) if aide else ''
    if type_ == 'textarea':
        f = '<textarea id="%s"%s %s>%s</textarea>' % (cid, da, attrs, E(valeur))
    elif type_ == 'select':
        f = '<select id="%s"%s %s>%s</select>' % (cid, da, attrs, ''.join('<option>%s</option>' % E(o) for o in valeur))
    else:
        f = '<input type="%s" id="%s" value="%s"%s %s>' % (type_, cid, E(valeur), da, attrs)
    return '<div class="champ"><label for="%s">%s</label>%s%s</div>' % (cid, E(lib), f, a)


def interrupteur(lib, sous, cid, coche=True):
    return '<div class="interrupteur"><label for="%s"><strong>%s</strong><small style="display:block">%s</small></label><input class="bascule" type="checkbox" role="switch" id="%s"%s></div>' % (
        cid, E(lib), sous, cid, ' checked' if coche else '')


def fenetre(fid, titre, corps, pied):
    return '<dialog id="%s" aria-labelledby="t-%s"><div class="fen-tete"><h2 id="t-%s">%s</h2><button type="button" class="bouton-icone" data-ferme aria-label="Fermer">%s</button></div><div class="fen-corps">%s</div><div class="fen-pied">%s</div></dialog>' % (
        fid, fid, fid, E(titre), ic('fermer'), corps, pied)


def tiroir(fid, titre, corps, pied=''):
    return '<dialog class="tiroir" id="%s" aria-labelledby="t-%s"><div class="fen-tete"><h2 id="t-%s">%s</h2><button type="button" class="bouton-icone" data-ferme aria-label="Fermer">%s</button></div><div class="fen-corps">%s</div>%s</dialog>' % (
        fid, fid, fid, E(titre), ic('fermer'), corps, ('<div class="fen-pied">%s</div>' % pied) if pied else '')


def filtres(puces, unique=True):
    return '<div class="filtres" role="group" aria-label="Filtres"%s>%s</div>' % (
        ' data-unique' if unique else '',
        ''.join('<button type="button" class="puce" aria-pressed="%s">%s</button>' % ('true' if i == 0 else 'false', p) for i, p in enumerate(puces)))


def lien(texte, href):
    return '<a href="%s">%s</a>' % (href, E(texte))


# =====================================================================
# Briques visuelles U1bis (voir maquettes/GUIDE-STYLE.md)
# Sens des teintes : terracotta = à faire, bleu = en cours, vert = fait,
# ambre = attention, violet = nouveau, rouge = arrêté, gris = neutre.
# =====================================================================
def kpi(lib, val, icone, teinte='bleu', meta='', href=None, graph='', unite=''):
    """Tuile chiffre : grosse icône, libellé, GROS chiffre, détail court, mini-graphique. Cliquable si href."""
    u = ('<small> %s</small>' % E(unite)) if unite else ''
    corps = ('<div class="kpi-tete">%s<span class="kpi-lib">%s</span></div><div class="kpi-val">%s%s</div>%s%s'
             % (ic(icone), E(lib), val, u, ('<div class="kpi-meta">%s</div>' % meta) if meta else '', graph))
    if href:
        return '<a class="kpi teinte-%s" href="%s">%s</a>' % (teinte, href, corps)
    return '<div class="kpi teinte-%s">%s</div>' % (teinte, corps)


def kpis(*tuiles_):
    return '<div class="kpis">%s</div>' % ''.join(tuiles_)


def jauge(lib, val, maxi, teinte='bleu', texte=None):
    """Jauge horizontale accessible (role=meter)."""
    pct = 0 if not maxi else max(0, min(100, round(100.0 * val / maxi)))
    t = texte if texte is not None else '%s / %s' % (val, maxi)
    return ('<div class="jauge %s" role="meter" aria-valuemin="0" aria-valuemax="%s" aria-valuenow="%s" aria-label="%s : %s">'
            '<div class="jauge-lib"><span>%s</span><span>%s</span></div><div class="jauge-piste"><span style="width:%d%%"></span></div></div>'
            % (teinte, maxi, val, E(lib), E(t), E(lib), E(t), pct))


def anneau(val, maxi, teinte='vert', centre=None, titre='', sous=''):
    """Anneau SVG (part d'un total) avec texte à droite."""
    import math
    r = 46.0
    tour = 2 * math.pi * r
    part = 0 if not maxi else max(0.0, min(1.0, float(val) / maxi))
    c = centre if centre is not None else '%s/%s' % (val, maxi)
    svg = ('<svg viewBox="0 0 112 112" role="img" aria-label="%s : %s sur %s"><circle class="piste" cx="56" cy="56" r="46" fill="none" stroke-width="14"/>'
           '<circle class="arc" cx="56" cy="56" r="46" fill="none" stroke-width="14" stroke-dasharray="%.1f %.1f" transform="rotate(-90 56 56)"/>'
           '<text x="56" y="65" text-anchor="middle">%s</text></svg>' % (E(titre or 'Part'), val, maxi, tour * part, tour, E(c)))
    txt = ('<div class="anneau-txt"><strong>%s</strong><span class="petit">%s</span></div>' % (E(titre), sous)) if titre or sous else ''
    return '<div class="anneau %s">%s%s</div>' % (teinte, svg, txt)


def barres(points, teinte='', libelle='Graphique en barres'):
    """Barres verticales : points = [(axe, valeur)] ou [(axe, valeur, teinte)]."""
    m = max([p[1] for p in points] or [1]) or 1
    cols = []
    for p in points:
        t = p[2] if len(p) > 2 else teinte
        cols.append('<div class="col"><span class="val">%s</span><span class="tige %s" style="height:%d%%"></span><span class="axe">%s</span></div>'
                    % (p[1], t, max(3, round(100.0 * p[1] / m)), E(p[0])))
    resume = ', '.join('%s : %s' % (p[0], p[1]) for p in points)
    return '<figure style="margin:0"><div class="barres" role="img" aria-label="%s. %s">%s</div></figure>' % (E(libelle), E(resume), ''.join(cols))


def courbe(valeurs, axe, teinte='', libelle='Courbe'):
    """Courbe SVG avec aire : valeurs = [nombres] ; axe = libellés (début, milieu, fin…)."""
    n = len(valeurs)
    m = max(valeurs) or 1
    pts = ['%.1f,%.1f' % (300.0 * i / (n - 1), 96 - 88.0 * v / m) for i, v in enumerate(valeurs)]
    aire = '0,100 ' + ' '.join(pts) + ' 300,100'
    grille = ''.join('<line class="grille-l" x1="0" x2="300" y1="%d" y2="%d"/>' % (y, y) for y in (8, 52, 96))
    svg = ('<svg class="courbe %s" viewBox="0 0 300 100" preserveAspectRatio="none" role="img" aria-label="%s : de %s à %s, maximum %s">%s'
           '<polygon class="aire" points="%s"/><polyline class="ligne" points="%s"/></svg>' % (teinte, E(libelle), valeurs[0], valeurs[-1], m, grille, aire, ' '.join(pts)))
    return '<div class="courbe-cadre">%s<div class="axe-x" aria-hidden="true">%s</div></div>' % (svg, ''.join('<span>%s</span>' % E(a) for a in axe))


def points_serie(items):
    """Série de pastilles rondes : items = [(libellé, teinte, icône)] ; teinte '' = vert."""
    return '<ul class="points">%s</ul>' % ''.join(
        '<li><span class="p %s" role="img" aria-label="%s : %s">%s</span>%s</li>' % (t, E(l), {'': 'bon', 'ambre': 'attention', 'rouge': 'échec', 'gris': 'inconnu'}[t], ic(i), E(l)) for l, t, i in items)


def chiffres(items):
    """Mini-tuiles dans un bloc : items = [(chiffre, libellé)]."""
    return '<div class="chiffres">%s</div>' % ''.join('<div><b>%s</b><span>%s</span></div>' % (v, E(l)) for v, l in items)


_ICONE_FEU = {'vert': 'coche', 'ambre': 'alerte', 'rouge': 'arret', 'bleu': 'chauffe', 'gris': 'aide'}
_MOT_FEU = {'vert': 'Bon', 'ambre': 'Attention', 'rouge': 'Arrêté', 'bleu': 'En montée', 'gris': 'Inconnu'}
_SYM_FEU = {'vert': '●', 'ambre': '▲', 'rouge': '■', 'bleu': '▶', 'gris': '○'}


def tuile_feu(nom, etat, sous, contenu='', href=None):
    """Grande tuile colorée d'état (feu) : rond plein + nom + pastille + contenu."""
    tete = ('<div class="tuile-feu-tete"><span class="rond" aria-hidden="true">%s</span><div class="tuile-feu-nom"><strong>%s</strong><span>%s</span></div></div>'
            % (ic(_ICONE_FEU[etat]), E(nom), badge(etat, _MOT_FEU[etat], _SYM_FEU[etat]) + ' <span class="petit">%s</span>' % E(sous) if sous else badge(etat, _MOT_FEU[etat], _SYM_FEU[etat])))
    if href:
        return '<a class="tuile-feu %s" href="%s">%s%s</a>' % (etat, href, tete, contenu)
    return '<div class="tuile-feu %s">%s%s</div>' % (etat, tete, contenu)


def verdict_global(titre, sous, teinte='vert', icone='coche', droite=''):
    return '<div class="verdict-global %s" role="status"><span class="rond" aria-hidden="true">%s</span><div class="quoi"><strong>%s</strong><span>%s</span></div>%s</div>' % (
        '' if teinte == 'vert' else teinte, ic(icone), E(titre), sous, droite)


def initiales(nom, teinte=''):
    ini = ''.join(m[0] for m in nom.replace('’', ' ').split() if m[0].isalpha())[:2].upper()
    return '<span class="initiales %s" aria-hidden="true">%s</span>' % (teinte, ini)


def ligne(titre, sous, gauche='', droite='', href=None, attrs=''):
    """Grande ligne cliquable (≥ 68 px) : pastille à gauche, titre + détail, statut à droite."""
    corps = '%s<span class="quoi"><strong>%s</strong><span>%s</span></span>%s' % (gauche, titre, sous, droite)
    if href:
        return '<li><a class="ligne" href="%s" %s>%s%s</a></li>' % (href, attrs, corps, ic('chevron-d', 'fleche-ligne'))
    return '<li><div class="ligne" %s>%s</div></li>' % (attrs, corps)


def lignes(*items):
    return '<ul class="lignes">%s</ul>' % ''.join(items)


def frise(etapes, courant=1):
    """Stepper visuel numéroté ; boutons pilotés par app.js ([data-assistant])."""
    return '<ol class="frise" aria-label="Étapes">%s</ol>' % ''.join(
        '<li><button type="button"%s%s><span class="n">%s</span><span class="txt">%s</span></button></li>' % (
            ' aria-current="step"' if i + 1 == courant else '', ' class="fait"' if i + 1 < courant else '',
            ic('coche') if i + 1 < courant else str(i + 1), E(e)) for i, e in enumerate(etapes))


def mini_titre(t):
    return '<h2 class="mini-titre">%s</h2>' % E(t)


def onglets_nav(nom, items, actif):
    """Onglets de navigation (liens) : items = [(href, libellé, nombre)]."""
    return '<nav class="onglets" aria-label="%s">%s</nav>' % (E(nom), ''.join(
        '<a href="%s"%s>%s%s</a>' % (h, ' aria-current="page"' if h == actif else '', E(l), (' <span class="nb">%s</span>' % n) if n else '') for h, l, n in items))
