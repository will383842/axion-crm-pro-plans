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
    lignes = [['<a href="campagne-suivi.html"><strong>%s</strong></a>' % r[0], r[1], st(r[2]), r[3]] + ['<span class="chiffre">%s</span>' % x for x in r[4:8]] + [r[8], btn('Ouvrir', 'petit-discret', 'campagne-suivi.html')] for r in rows]
    normal = (tuiles([('En cours', '1', 'Organisateurs Rhône-Alpes'), ('À valider', '1', 'Fédérations T1'), ('Réponses ce mois', '22', 'dont 7 positives'), ('Désinscriptions', '3', '0,9 % des envoyés')])
              + filtres(['Toutes', 'En cours', 'À valider', 'Programmées', 'Terminées', 'Brouillons'])
              + tableau('Campagnes', ['Campagne', 'Nature', 'Statut', 'Étape', 'Joignables', 'Envoyés', 'Réponses (positives)', 'Désinscr.', 'Fin prévue', ''], lignes))
    vide = etat_vide('campagne', 'Aucune campagne', 'Une campagne envoie une suite de 1 à 4 messages à une liste, au rythme de la montée en douceur.', btn('Créer une campagne', 'plein', 'campagne-nouvelle.html'))
    P['campagnes.html'] = page('campagnes', 'Campagnes', '<strong>1 campagne en cours</strong>, 1 à valider. Volume possible aujourd’hui : 120.', normal, vide,
                               actions=btn('Messages types', 'contour', 'messages-types.html', 'message') + btn('Créer une campagne', 'plein', 'campagne-nouvelle.html', 'plus'),
                               onglets_haut='<nav class="onglets" aria-label="Sections de Campagnes"><a href="campagnes.html" aria-current="page">Campagnes</a><a href="messages-types.html">Messages types</a><a href="presse.html">Presse</a><a href="v1-ecrans.html#declenches">Messages déclenchés <span class="repere-v1">V1</span></a><a href="v1-ecrans.html#lettre">Lettre <span class="repere-v1">V1</span></a></nav>')


# ---------------- Création en 5 étapes ----------------
def _nouvelle():
    etapes = ['Cible', 'Message', 'Envoi', 'Vérification', 'Lancement']
    frise = '<ol class="frise" aria-label="Étapes de la campagne">%s</ol>' % ''.join(
        '<li><button type="button"%s><span class="n">%d</span><span class="txt">%s</span></button></li>' % (' aria-current="step"' if i == 0 else '', i + 1, e) for i, e in enumerate(etapes))
    suiv = lambda n, lib: '<div class="bloc-pied"><button type="button" class="btn btn-plein" data-aller="%d">Continuer : %s</button>%s</div>' % (n, lib, ('<button type="button" class="btn btn-discret" data-aller="%d">Retour</button>' % (n - 2)) if n > 2 else '')
    e1 = ('<h2>Qui reçoit la campagne ?</h2><p class="petit" style="margin:4px 0 16px">Choisissez une liste. On retire tout seul les oppositions et les adresses refusées.</p>'
          '<div class="choix" role="radiogroup" aria-label="Liste"><label><span><input type="radio" name="liste" checked> <strong>Organisateurs Rhône-Alpes</strong></span><small>312 personnes · 290 joignables</small></label>'
          '<label><span><input type="radio" name="liste"> <strong>Fédérations nationales</strong></span><small>84 personnes · 80 joignables</small></label>'
          '<label><span><input type="radio" name="liste"> <strong>Salon des artisans 2026</strong></span><small>100 personnes · 92 joignables</small></label></div>'
          + champ('Exclure une adresse, une organisation ou un domaine', 'excl', aide='Facultatif. Exemple : concurrent.example')
          + suiv(2, 'message'))
    e2 = ('<h2>Quel message ?</h2><p class="petit" style="margin:4px 0 16px">Une suite de 1 à 4 messages. Les relances partent dans le même fil.</p>'
          '<div class="choix"><label><span><input type="radio" name="mt" checked> <strong>Message type n° 1</strong></span><small>Organisateurs · validé · v3</small></label><label><span><input type="radio" name="mt"> <strong>Message type n° 2</strong></span><small>Fédérations · validé · v1</small></label></div>'
          '<ol class="liste"><li>%s<span class="quoi"><strong>Message 1</strong><small>Jour 0</small></span>%s</li><li>%s<span class="quoi"><strong>Message 2 (relance)</strong><small>+ 4 jours ouvrés si pas de réponse</small></span>%s</li><li>%s<span class="quoi"><strong>Message 3</strong><small>+ 7 jours ouvrés</small></span>%s</li></ol>'
          % (badge('vert', 'Validé', '✓'), btn('Aperçu', 'petit-discret', 'message-editeur.html'), badge('vert', 'Validé', '✓'), btn('Aperçu', 'petit-discret', 'message-editeur.html'), badge('vert', 'Validé', '✓'), btn('Aperçu', 'petit-discret', 'message-editeur.html'))
          + '<div class="bloc-pied">%s</div>' % btn('M’envoyer un test', 'petit', icone='test', attrs='data-ouvre="fen-test"') + suiv(3, 'envoi'))
    e3 = ('<h2>Quand et par quelles boîtes ?</h2>'
          '<div class="ligne-champs">' + champ('Départ', 'dep', 'date', '2026-11-04') + champ('Fenêtre d’envoi', 'fen', 'select', ['09:00 – 17:00, jours ouvrés', '10:00 – 16:00, jours ouvrés']) + '</div>'
          '<fieldset style="border:0;padding:0;margin:0 0 16px"><legend class="lib" style="font-weight:600;margin-bottom:6px">Boîtes d’envoi</legend>'
          '<label class="case"><input type="checkbox" checked> claire@prospection-a.example · 40 par jour</label><label class="case"><input type="checkbox" checked> will@prospection-b.example · 40 par jour</label><label class="case"><input type="checkbox"> paul@prospection-c.example · en montée en douceur (jour 6)</label></fieldset>'
          '<p class="petit">Fin prévue le 20 nov. au rythme actuel. Arrêt automatique pour une entreprise dès qu’une personne répond.</p>' + suiv(4, 'vérification'))
    ctrl = ['Liste figée possible (312 personnes)', 'Oppositions retirées (22)', 'Bloc d’information présent', 'Lien de désinscription en un clic', 'Aucun lien vers le site d’Axion', 'Aucun mot interdit', 'Boîtes saines (2 sur 2)']
    e4 = ('<h2>Tout est-il en règle ?</h2><p class="petit" style="margin:4px 0 16px">7 contrôles sur 7 au vert.</p><ul class="liste">%s</ul>' % ''.join('<li>%s<span class="quoi">%s</span></li>' % (feu('vert', 'OK'), c) for c in ctrl)
          + suiv(5, 'lancement'))
    e5 = ('<h2>Valider et lancer</h2><p style="margin:8px 0 16px">Liste figée le 2 nov. à 07:10 : <strong>290 personnes</strong>. Départ le 4 nov. à 09:00. Vous avez 5 minutes pour annuler après la validation.</p>'
          + champ('Votre code reçu par e-mail', 'code-valid', aide='Validation d’un envoi : code redemandé.', attrs='inputmode="numeric" autocomplete="one-time-code"')
          + '<div class="bloc-pied"><a class="btn btn-plein" href="campagne-suivi.html" data-toast="Campagne validée et programmée.">Valider et programmer</a><button type="button" class="btn btn-discret" data-aller="4">Retour</button></div>')
    panneaux = ''.join('<div class="bloc" data-etape="%d">%s</div>' % (i + 1, c) for i, c in enumerate([e1, e2, e3, e4, e5]))
    recap = bloc('Récapitulatif', '<dl><dt>Cible</dt><dd>Organisateurs Rhône-Alpes · 290</dd><dt>Message</dt><dd>Message type n° 1 · 3 messages</dd><dt>Envoi</dt><dd>4 nov. · 2 boîtes · 80 par jour</dd><dt>Fin prévue</dt><dd>20 nov.</dd></dl><p class="petit" style="margin-top:12px">Brouillon enregistré à 10:42.</p>', 'gris', 'liste', mot='Brouillon')
    normal = '<div data-assistant>%s<div class="assistant"><div>%s</div><aside class="recap" aria-label="Récapitulatif">%s</aside></div></div>' % (frise, panneaux, recap)
    test = fenetre('fen-test', 'M’envoyer un test', '<label class="case"><input type="checkbox" checked> Moi (will@…)</label><label class="case"><input type="checkbox" checked> Boîtes témoins (4)</label>' + champ('Destinataire d’exemple', 'ex-dest', 'select', ['Claire Durand (Garage Durand)', 'Paul Martin (Boulangerie Martin)']) + '<p class="petit">Le test passe par la même porte qu’un vrai envoi. Il ne compte pas dans la montée en douceur.</p>',
                   '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-contour" data-ferme data-toast="Test envoyé à 5 adresses.">Envoyer le test</button>')
    vide = etat_vide('liste', 'Aucune liste à cibler', 'Créez d’abord une liste de contacts joignables.', btn('Créer une liste', 'plein', 'listes.html'))
    P['campagne-nouvelle.html'] = page('campagne-nouvelle', 'Nouvelle campagne', 'Cinq étapes, environ 5 minutes. Rien ne part sans votre validation.', normal, vide,
                                       fil=[('Campagnes', 'campagnes.html', 'campagnes')], apres=test)


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


# ---------------- Réponses ----------------
def _reponses():
    file_ = '<ul class="file-rep" aria-label="Réponses à traiter">%s</ul>' % ''.join(
        '<li><a href="#"%s><strong>%s</strong> %s<br><small>%s</small></a></li>' % (' aria-current="true"' if i == 0 else '', n, badge(t, s, '●'), x) for i, (n, t, s, x) in enumerate([
            ('Claire Durand', 'terracotta', 'Intéressé', '« Pouvez-vous me rappeler jeudi ? »'),
            ('Hugo Petit', 'terracotta', 'Intéressé', '« Envoyez-moi une proposition. »'),
            ('Inès Moreau', 'gris', 'Absent', 'Absente jusqu’au 12 nov.'),
            ('Louis Bernard', 'rouge', 'STOP', '« Ne m’écrivez plus. »'),
            ('inconnu@exemple.example', 'ambre', 'À rattacher', 'Adresse inconnue')]))
    msg = ('<article class="message" aria-label="Réponse de Claire Durand"><div class="bloc-tete"><h2>Claire Durand · Garage Durand</h2>%s</div><p class="petit">Hier 16:20 · réponse au message 2 · campagne Organisateurs Rhône-Alpes</p>'
           '<blockquote>Bonjour, c’est intéressant. Pouvez-vous me rappeler jeudi matin ? Claire</blockquote>'
           '<p><strong>Suggestion :</strong> Intéressé → créer la tâche « Rappeler jeudi » et arrêter la campagne pour Garage Durand.</p>'
           '<div class="bloc-pied"><button type="button" class="btn btn-plein" data-toast="Réponse traitée : tâche créée, campagne arrêtée pour l’entreprise." data-annulable>Appliquer la suggestion</button></div>'
           '<div class="gestes" role="group" aria-label="Classer autrement">%s%s%s%s</div><p class="petit" style="margin-top:12px">Raccourcis : 1 à 4 pour classer, S pour STOP, J/K pour suivante/précédente.</p></article>'
           % (badge('terracotta', 'Intéressé', '●'), btn('Pas intéressé', 'petit', attrs='data-toast="Classée : pas intéressé." data-annulable'), btn('Plus tard', 'petit', attrs='data-toast="Classée : plus tard." data-annulable'),
              btn('Absent', 'petit', attrs='data-toast="Classée : absent." data-annulable'), btn('STOP', 'petit', attrs='data-ouvre="fen-stop"')))
    normal = (onglets('Réponses', [('a-traiter', 'À traiter (7)', '<div class="reponses">%s%s</div>' % (file_, msg)),
                                   ('stop', 'STOP à confirmer (1)', bloc('Louis Bernard', '<blockquote>« Ne m’écrivez plus. »</blockquote>', 'terracotta', 'interdit', pied=btn('Confirmer l’opposition', 'petit', attrs='data-ouvre="fen-stop"'))),
                                   ('rattacher', 'À rattacher (1)', '<p>%s</p>' % lien('Ouvrir les réponses à rattacher', 'reponses-a-rattacher.html')),
                                   ('toutes', 'Toutes', '<p class="petit">Historique complet des réponses, filtrable par campagne.</p>')]))
    stop = fenetre('fen-stop', 'Enregistrer l’opposition de Louis Bernard ?', '<p>Plus aucun message ne lui sera envoyé, par aucune campagne. C’est définitif.</p><label class="case"><input type="checkbox"> Pour toute l’organisation (Atelier Bernard)</label>',
                   '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-danger" data-ferme data-toast="Opposition enregistrée.">Enregistrer l’opposition</button>')
    P['reponses.html'] = page('reponses', 'Réponses', '<strong>7 réponses</strong> à traiter : 2 intéressées, 1 STOP, 1 à rattacher. La plus ancienne date d’hier 16:20.', normal,
                              etat_vide('reponses', 'Aucune réponse à traiter', 'Tout est traité. Les nouvelles réponses arrivent ici dès leur relève (toutes les 5 min).', btn('Voir toutes les réponses', 'plein', attrs='data-toast="Filtre « Toutes » appliqué."')),
                              apres=stop)


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


for f in (_campagnes, _nouvelle, _suivi, _messages_types, _editeur, _reponses, _a_rattacher, _presse):
    f()
