# -*- coding: utf-8 -*-
"""Pages du groupe « Prospecter ». Données factices."""
from socle import *  # noqa: F401,F403

P = {}

_STATUTS = {'Brouillon': ('gris', '○'), 'À valider': ('terracotta', '●'), 'Programmée': ('bleu', '◷'), 'En cours': ('bleu', '▶'),
            'En pause': ('ambre', '❚❚'), 'Terminée': ('vert', '✓'), 'Annulée': ('gris', '×')}


def st(s):
    t, sym = _STATUTS[s]
    return badge(t, s, sym)


# ---------------- Liste des campagnes ----------------
def _campagnes():
    rows = [('Organisateurs Rhône-Alpes', 'Prospection', 'En cours', 'Message 2 sur 3', '290', '184', '9 (3)', '1', '20 nov.'),
            ('Fédérations T1', 'Prospection', 'À valider', '—', '80', '0', '—', '—', '—'),
            ('Commerces de Lyon', 'Prospection', 'Terminée', 'Fin', '92', '92', '11 (4)', '2', '28 oct.'),
            ('Clubs sportifs', 'Prospection', 'En pause', 'Message 1 sur 3', '140', '40', '2 (0)', '0', '—'),
            ('Relance salon', 'Prospection', 'Brouillon', '—', '—', '—', '—', '—', '—')]
    lignes = [['<a href="campagne-suivi.html"><strong>%s</strong></a>' % r[0], st(r[2]), r[3]] + ['<span class="chiffre">%s</span>' % x for x in r[4:8]] + [r[8], btn('Ouvrir', 'petit-discret', 'campagne-suivi.html')] for r in rows]
    normal = (tuiles([('En cours', '1', 'Organisateurs Rhône-Alpes'), ('À valider', '1', 'Fédérations T1'), ('Réponses ce mois', '22', 'dont 7 positives'), ('Désinscriptions', '3', '0,9 % des envoyés')])
              + filtres(['Toutes', 'En cours', 'À valider', 'Programmées', 'Terminées', 'Brouillons'])
              + tableau('Campagnes', ['Campagne', 'Statut', 'Étape', 'Joignables', 'Envoyés', 'Réponses', 'Désinscr.', 'Fin', ''], lignes))
    vide = etat_vide('campagne', 'Aucune campagne', 'Une campagne envoie une suite de 1 à 4 messages à une liste, au rythme de la montée en douceur.', btn('Créer une campagne', 'plein', 'campagne-nouvelle.html'))
    P['campagnes.html'] = page('campagnes', 'Campagnes', '<strong>1 campagne en cours</strong>, 1 à valider. Volume possible aujourd’hui : 120.', normal, vide,
                               actions=btn('Messages types', 'contour', 'messages-types.html', 'message') + btn('Créer une campagne', 'plein', 'campagne-nouvelle.html', 'plus'),
                               onglets_haut='<nav class="onglets" aria-label="Sections de Campagnes"><a href="campagnes.html" aria-current="page">Campagnes</a><a href="messages-types.html">Messages types</a><a href="presse.html">Presse</a><a href="v1-ecrans.html#declenches">Messages déclenchés <span class="repere-v1">V1</span></a><a href="v1-ecrans.html#lettre">Lettre <span class="repere-v1">V1</span></a></nav>')


# ---------------- Suivi d'une campagne ----------------
def _suivi():
    courbe = ('<figure style="margin:0"><svg class="courbe" viewBox="0 0 600 140" role="img" aria-labelledby="c-titre"><title id="c-titre">Envois par jour : de 20 à 80 en 10 jours</title>'
              '<polyline fill="none" stroke="#2346c8" stroke-width="3" points="0,120 60,112 120,104 180,96 240,86 300,74 360,64 420,52 480,42 540,32 600,28"/>'
              '<line x1="0" y1="130" x2="600" y2="130" stroke="#dde2ea"/></svg><figcaption class="petit">De 20 à 80 envois par jour en 10 jours. <a href="#" data-ouvre="tir-tableau">Voir en tableau</a></figcaption></figure>')
    etapes = tableau('Résultats par message', ['Message', 'Envoyés', 'Réponses', 'Positives', 'Refusées', 'Désinscr.'], [
        ['<strong>Message 1</strong>', '<span class="chiffre">184</span>', '6', '2', '3', '1'],
        ['<strong>Message 2</strong>', '<span class="chiffre">96</span>', '3', '1', '0', '0'],
        ['<strong>Message 3</strong>', '<span class="chiffre">0</span>', '—', '—', '—', '—']])
    normal = (tuiles([('Envoyés', '280', 'sur 290 joignables'), ('Réponses', '9', 'dont 3 positives'), ('Rendez-vous', '1', 'Club de voile du Lac'), ('Désinscriptions', '1', '0,4 %')])
              + '<div class="grille deux">' + bloc('Progression', courbe, 'bleu', 'stats', mot='En cours') + bloc('Ce qui se passe', '<ul class="liste"><li>%s<span class="quoi">Message 2 en cours d’envoi<small>Prochaine vague à 14:00</small></span></li><li>%s<span class="quoi">Arrêtée pour 3 entreprises<small>Une personne a répondu</small></span></li><li>%s<span class="quoi">2 absences du bureau<small>Reprise automatique au retour</small></span></li></ul>' % (badge('bleu', 'En cours', '▶'), badge('vert', 'Fait', '✓'), badge('ambre', 'Pause', '❚❚')), 'gris', 'horloge', mot='Info') + '</div>'
              + bloc('Résultats par message', etapes) + '<p class="petit" style="margin-top:12px">Aucune mesure d’ouverture : seules les réponses comptent.</p>')
    pause = fenetre('fen-pause', 'Mettre en pause « Organisateurs Rhône-Alpes » ?', '<p>Plus aucun nouveau message ne part pour cette campagne. Les réponses continuent d’arriver. Vous pourrez reprendre à tout moment.</p>',
                    '<button type="button" class="btn btn-contour" data-ferme>Ne rien changer</button><button type="button" class="btn btn-danger" data-ferme data-toast="Campagne en pause.">Mettre en pause</button>')
    tab = tiroir('tir-tableau', 'Envois par jour', tableau('Envois par jour', ['Jour', 'Envois'], [['%d nov.' % (i + 1), str(20 + i * 6)] for i in range(10)], cartes=False))
    P['campagne-suivi.html'] = page('campagne-suivi', 'Organisateurs Rhône-Alpes', '%s Message 2 sur 3 · <strong>9 réponses</strong> dont 3 positives · fin prévue le 20 nov.' % st('En cours'), normal,
                                    etat_vide('envoi', 'Pas encore d’envoi', 'La campagne part le 4 nov. à 09:00. Les résultats apparaîtront ici.', btn('Voir la liste figée', 'plein', 'listes.html')),
                                    actions=btn('Mettre en pause', 'contour', icone='pause', attrs='data-ouvre="fen-pause"') + btn('Voir les réponses', 'plein', 'reponses.html', 'reponses'),
                                    fil=[('Campagnes', 'campagnes.html', 'campagnes')], apres=pause + tab)


# ---------------- Messages types ----------------
def _messages_types():
    lignes = [['<a href="message-editeur.html"><strong>%s</strong></a>' % n, v, badge(*s), u, d, btn('Ouvrir', 'petit-discret', 'message-editeur.html')] for n, v, s, u, d in [
        ('Message type n° 1 · Organisateurs', 'v3', ('vert', 'Validé', '✓'), '1 campagne', '28 oct.'),
        ('Message type n° 2 · Fédérations', 'v1', ('vert', 'Validé', '✓'), '1 campagne', '30 oct.'),
        ('Relance courte', 'v2', ('terracotta', 'À valider', '●'), '—', 'hier'),
        ('Commerces (ancien)', 'v4', ('gris', 'Archivé', '■'), '1 campagne terminée', '2 oct.')]]
    normal = filtres(['Tous', 'Validés', 'À valider', 'Brouillons', 'Archivés']) + tableau('Messages types', ['Nom', 'Version', 'Statut', 'Utilisé par', 'Modifié le', ''], lignes)
    P['messages-types.html'] = page('messages-types', 'Messages types', '<strong>4 messages types</strong> · 1 à valider. Une campagne utilise toujours une version figée.', normal,
                                    etat_vide('message', 'Aucun message type', 'Un message type sert de base aux campagnes. Écrivez le premier en 10 minutes.', btn('Nouveau message type', 'plein', 'message-editeur.html')),
                                    actions=btn('Nouveau message type', 'plein', 'message-editeur.html', 'plus'),
                                    onglets_haut='<nav class="onglets" aria-label="Sections de Campagnes"><a href="campagnes.html">Campagnes</a><a href="messages-types.html" aria-current="page">Messages types</a><a href="presse.html">Presse</a></nav>')


# ---------------- Éditeur de message ----------------
def _editeur():
    gauche = bloc('Texte', champ('Objet', 'objet', valeur='Votre prochaine fête, sans tableur') + '<div class="bloc-pied" style="margin:0 0 12px">%s</div>' % btn('Ajouter une version de l’objet', 'petit-discret', icone='plus')
                  + champ('Message', 'corps', 'textarea', 'Bonjour {prénom},\n\nJ’ai vu que {entreprise} organise des événements dans la région. Nous aidons les organisateurs à gérer les inscriptions sans tableur.\n\nUn échange de 15 minutes ? {lien_rdv}\n\nWill', attrs='rows="9"')
                  + '<div class="bloc-pied">%s %s</div>' % (btn('Insérer un champ', 'petit', icone='plus'), btn('M’envoyer un test', 'petit', icone='test', attrs='data-toast="Test envoyé à 5 adresses."')))
    droite = bloc('Aperçu', '<p class="petit" style="margin-bottom:8px">Pour : Claire Durand · Garage Durand</p><div class="apercu-mail"><p><strong>Votre prochaine fête, sans tableur</strong></p><hr class="sep"><p>Bonjour <span class="champ-var">Claire</span>,</p><p style="margin-top:10px">J’ai vu que <span class="champ-var">Garage Durand</span> organise des événements dans la région…</p><p style="margin-top:10px">Un échange de 15 minutes ? <span class="champ-var">lien de rendez-vous</span></p><hr class="sep"><p class="petit">Bloc d’information · Ne plus recevoir de messages (un clic)</p></div>'
                  + '<ul class="liste" style="margin-top:12px"><li>%s<span class="quoi">Aucun mot interdit</span></li><li>%s<span class="quoi">Aucun lien vers axion-ia.com</span></li><li>%s<span class="quoi">Aucun pixel de suivi</span></li></ul>' % (feu('vert', 'OK'), feu('vert', 'OK'), feu('vert', 'OK')), 'vert', 'oeil', mot='Contrôles')
    normal = '<p class="petit" style="margin-bottom:12px">Enregistré à 10:42 · version 3 (brouillon)</p><div class="grille deux">%s%s</div>' % (gauche, droite)
    P['message-editeur.html'] = page('message-editeur', 'Message type n° 1', 'Brouillon de la version 3. Les campagnes en cours gardent la version 2.', normal,
                                     etat_vide('message', 'Message vide', 'Commencez par l’objet : une phrase courte, sans majuscules partout.', btn('Écrire l’objet', 'plein', attrs='data-toast="Curseur placé dans l’objet."')),
                                     actions=btn('Archiver', 'contour', attrs='data-toast="Message archivé." data-annulable') + btn('Demander la validation', 'plein', attrs='data-toast="Envoyé pour validation."'),
                                     fil=[('Campagnes', 'campagnes.html', 'messages-types'), ('Messages types', 'messages-types.html')])


# ---------------- Réponses à rattacher ----------------
def _a_rattacher():
    normal = (bloc('Réponse de inconnu@exemple.example', '<blockquote style="margin:0 0 12px;padding:12px 16px;background:#fff;border-radius:12px">« Bonjour, je transmets à notre présidente, Mme Moreau. »</blockquote><p class="petit">Reçue ce matin 08:12 · boîte claire@ · campagne Fédérations T1</p>', 'ambre', 'reponses', mot='À rattacher')
              + '<h2 class="mini-titre">Fiches proposées</h2>'
              + tableau('Fiches proposées', ['Fiche', 'Pourquoi', ''], [
                  ['<strong>Inès Moreau</strong><span class="sous">Fédération des Fêtes de Village</span>', 'Nom cité dans le message · même organisation', '<button type="button" class="btn btn-plein petit-btn" data-toast="Réponse rattachée à Inès Moreau." data-annulable>Rattacher à Inès Moreau</button>'],
                  ['<strong>Fédération des Fêtes de Village</strong><span class="sous">Entreprise</span>', 'Domaine de l’adresse', btn('Rattacher', 'petit', attrs='data-toast="Réponse rattachée." data-annulable')],
                  ['<strong>Hugo Petit</strong><span class="sous">Club de voile du Lac</span>', 'Même campagne', btn('Rattacher', 'petit', attrs='data-toast="Réponse rattachée." data-annulable')]])
              + '<div class="bloc-pied">%s</div>' % btn('Créer la personne', 'contour', icone='plus', attrs='data-toast="Fiche créée avec la provenance « réponse »."'))
    P['reponses-a-rattacher.html'] = page('reponses-a-rattacher', 'Réponses à rattacher', '<strong>1 réponse</strong> venue d’une adresse inconnue. Choisissez la bonne fiche.', normal,
                                          etat_vide('reponses', 'Rien à rattacher', 'Chaque réponse est reliée à sa fiche. Bravo.', btn('Retour aux réponses', 'plein', 'reponses.html')),
                                          fil=[('Réponses', 'reponses.html', 'reponses')])


# ---------------- Presse (existant : médias, journalistes, communiqués) ----------------
def _presse():
    med = tableau('Médias', ['Média', 'Rubrique', 'Provenance', 'Mise à jour', ''], [
        ['<strong>Journal régional factice</strong>', 'Économie', badge('vert', 'Fiable', '✓'), '12 oct.', btn('Ouvrir', 'petit-discret')],
        ['<strong>Radio locale factice</strong>', 'Société', badge('ambre', 'À revoir', '▲'), '3 sept.', btn('Ouvrir', 'petit-discret')]])
    jou = tableau('Journalistes', ['Journaliste', 'Média', 'Sujets', ''], [['<strong>Nora Lefèvre</strong>', 'Journal régional factice', 'Numérique, PME', btn('Ouvrir', 'petit-discret')]])
    com = tableau('Communiqués envoyés', ['Communiqué', 'Envoyé le', 'Destinataires', 'Retombées', ''], [['<strong>Lancement du Tour de France de l’IA</strong>', '15 oct.', '41', '2', btn('Ouvrir', 'petit-discret')]])
    normal = onglets('Presse', [('medias', 'Médias', med), ('journalistes', 'Journalistes', jou), ('communiques', 'Communiqués envoyés', com)])
    P['presse.html'] = page('presse', 'Presse', '<strong>41 contacts presse</strong> · 1 communiqué envoyé ce mois · 2 retombées.', normal,
                            etat_vide('presse', 'Aucun contact presse', 'Ajoutez un média ou un journaliste pour préparer un communiqué.', btn('Ajouter un média', 'plein', attrs='data-toast="Fenêtre d’ajout ouverte."')),
                            actions=btn('Nouveau communiqué', 'plein', icone='plus', attrs='data-toast="Éditeur de communiqué ouvert."'))


for f in (_campagnes, _suivi, _messages_types, _editeur, _a_rattacher, _presse):
    f()
