# -*- coding: utf-8 -*-
"""Lot U1bis : les 5 pages repères dans le nouveau style visuel.

Aujourd'hui (index), Contacts, Nouvelle campagne, Santé des envois, Réponses.
Elles servent de modèle pour régénérer les 40 autres pages (voir maquettes/GUIDE-STYLE.md).
Données factices uniquement : domaines en .example, aucune IP, aucune personne réelle.
"""
from socle import *  # noqa: F401,F403

P = {}


def _case_tache(titre, sous, droite, cid):
    return ('<li><label class="ligne" for="%s"><input type="checkbox" id="%s" data-toast="Tâche faite." data-annulable>'
            '<span class="quoi"><strong>%s</strong><span>%s</span></span>%s</label></li>' % (cid, cid, E(titre), E(sous), droite))


# ---------------- Aujourd'hui (tableau de bord) ----------------
def _index():
    haut = kpis(
        kpi('Réponses à traiter', '7', 'reponses', 'terracotta', badge('vert', '2 intéressées', '●'), 'reponses.html'),
        kpi('Tâches du jour', '5', 'taches', 'bleu', badge('rouge', '1 en retard', '■'), 'taches.html'),
        kpi('Envoyés hier', '96', 'envoi', 'vert', '', 'sante.html', graph=jauge('Quota', 96, 120, 'vert', '96 / 120')),
        kpi('Venus du site', '5', 'etincelle', 'violet', '3 fiches, 2 rattachements', 'a-valider.html'))
    reponses_ = bloc('Réponses du matin', lignes(
        ligne('Claire Durand', '« Rappelez-moi jeudi. »', initiales('Claire Durand', 'terracotta'), badge('vert', 'Intéressée', '●'), 'reponses.html'),
        ligne('Hugo Petit', '« Envoyez une proposition. »', initiales('Hugo Petit', 'terracotta'), badge('vert', 'Intéressé', '●'), 'reponses.html'),
        ligne('Louis Bernard', '« Ne m’écrivez plus. »', initiales('Louis Bernard', 'gris'), badge('rouge', 'STOP', '■'), 'reponses.html#stop'),
        ligne('4 autres', '3 absences, 1 à rattacher', initiales('4 a', 'gris'), badge('gris', 'À trier', '○'), 'reponses.html')),
        'terracotta', 'reponses', mot='7 à traiter', attrs='aria-label="Réponses du matin"')
    taches_ = bloc('Mes tâches du jour', '<ul class="lignes">%s</ul>' % ''.join([
        _case_tache('Relancer la fédération', 'Fédération des Fêtes', badge('rouge', 'En retard', '■'), 't1'),
        _case_tache('Appeler Claire Durand', 'Garage Durand', badge('bleu', '11:00', '◷'), 't2'),
        _case_tache('Envoyer le devis', 'Club de voile du Lac', badge('bleu', '14:00', '◷'), 't3'),
        _case_tache('Préparer le salon', 'Salon des artisans', badge('gris', 'Sans heure', '○'), 't4')]),
        'bleu', 'taches', mot='5 aujourd’hui', pied=btn('Toutes les tâches', 'petit', 'taches.html', 'fleche'))
    campagne_ = bloc('Campagne à valider', anneau(7, 7, 'vert', '7/7', 'Contrôles au vert', 'Fédérations T1 · 84 personnes'),
                     'ambre', 'campagne', mot='À valider', pied=btn('Relire et valider', 'petit', 'campagne-suivi.html', 'oeil'))
    sante_ = bloc('Santé des envois', points_serie([('claire@', '', 'coche'), ('will@', 'ambre', 'alerte'), ('paul@', '', 'coche'), ('hugo@', '', 'coche')])
                  + '<div style="margin-top:14px">%s</div>' % chiffres([('120', 'possibles'), ('07:05', 'test réussi')]),
                  'vert', 'sante', mot='Normal', pied=btn('Voir la santé', 'petit', 'sante.html', 'fleche'))
    route_ = bloc('Mise en route', anneau(3, 5, 'violet', '3/5', 'Premier message', '≈ 10 minutes'),
                  'violet', 'etincelle', mot='Nouveau', pied=btn('Continuer', 'petit', 'mise-en-route.html', 'fleche'))
    envois_ = bloc('Envoyés cette semaine', barres([('Lun', 84), ('Mar', 102), ('Mer', 110), ('Jeu', 118), ('Ven', 96)], 'bleu', 'Envoyés par jour'), icone='stats')
    courbe_ = bloc('Réponses sur 14 jours', courbe([1, 0, 2, 1, 3, 2, 4, 3, 2, 5, 4, 6, 5, 7], ['19 oct.', '26 oct.', '1er nov.'], 'vert', 'Réponses par jour')
                   + '<div style="margin-top:14px">%s</div>' % chiffres([('45', 'réponses'), ('12', 'intéressées'), ('3', 'STOP')]), icone='reponses')
    normal = (haut
              + '<div class="grille deux">%s%s</div>' % (reponses_, taches_)
              + '<div class="grille trois">%s%s%s</div>' % (campagne_, sante_, route_)
              + '<div class="grille deux">%s%s</div>' % (envois_, courbe_))
    vide = etat_vide('taches', 'Rien à faire aujourd’hui', 'Profitez-en : préparez une campagne.', btn('Créer une campagne', 'plein', 'campagne-nouvelle.html', 'plus'))
    P['index.html'] = page('index', 'Aujourd’hui', 'Bonjour Will. <strong>12 choses</strong> à traiter.', normal, vide,
                           actions=btn('Nouvelle campagne', 'contour', 'campagne-nouvelle.html', 'plus') + btn('Traiter les réponses', 'plein', 'reponses.html', 'reponses'))


# ---------------- Contacts (personnes) ----------------
_ETAPE = {'À contacter': ('terracotta', '●'), 'Contacté': ('bleu', '▶'), 'Répondu': ('violet', '✦'), 'Rendez-vous': ('vert', '✓'), 'Perdu': ('gris', '×')}
_JOIN = {'oui': ('vert', 'Oui', '✓'), 'revoir': ('ambre', 'À revérifier', '▲'), 'non': ('rouge', 'Ne plus écrire', '■')}
_PERS = [('Paul Martin', 'Boulangerie Martin', 'Gérant', 'Contacté', 'oui', '28 oct.'),
         ('Claire Durand', 'Garage Durand', 'Dirigeante', 'Répondu', 'oui', 'Hier'),
         ('Hugo Petit', 'Club de voile du Lac', 'Président', 'Rendez-vous', 'oui', 'Hier'),
         ('Inès Moreau', 'Fédération des Fêtes', 'Secrétaire', 'À contacter', 'revoir', '—'),
         ('Nadia Roux', 'Comité des fêtes de Lyon', 'Trésorière', 'À contacter', 'oui', '—'),
         ('Marc Lefèvre', 'Imprimerie Lefèvre', 'Gérant', 'Contacté', 'oui', '24 oct.'),
         ('Sophie Garnier', 'Office du tourisme', 'Chargée d’accueil', 'Répondu', 'oui', '30 oct.'),
         ('Louis Bernard', 'Atelier Bernard', 'Artisan', 'Perdu', 'non', '12 oct.')]


def _contacts():
    lignes_t, liens = [], []
    for i, (n, e, r, et, j, d) in enumerate(_PERS):
        te, se = _ETAPE[et]
        tj, mj, sj = _JOIN[j]
        cel = ('<div class="cellule-personne"><input type="checkbox" id="ch-%d" aria-label="Choisir %s"%s>%s<div><a href="contact.html">%s</a><span class="sous">%s</span></div></div>'
               % (i, E(n), ' checked' if i in (0, 5) else '', initiales(n, te), E(n), E(e)))
        lignes_t.append([cel, E(r), badge(te, et, se), badge(tj, mj, sj), '<span class="chiffre">%s</span>' % d, btn('Ouvrir', 'petit-discret', 'contact.html')])
        liens.append('contact.html')
    haut = kpis(
        kpi('Personnes', '1 248', 'personnes', 'bleu', '+24 cette semaine'),
        kpi('Joignables', '1 102', 'coche', 'vert', '', graph=jauge('Part joignable', 88, 100, 'vert', '88 %')),
        kpi('À contacter', '312', 'cible', 'terracotta', 'jamais écrits', 'contacts.html#a-contacter'),
        kpi('Doublons', '8', 'doublon', 'ambre', 'à vérifier', 'doublons.html'),
        kpi('Venus du site', '5', 'etincelle', 'violet', 'à valider', 'a-valider.html'))
    outils = ('<div class="barre-outils"><label class="champ-recherche" for="cherche-contact">%s<span class="visuellement-cache">Chercher un contact</span>'
              '<input type="search" id="cherche-contact" placeholder="Nom, e-mail, entreprise…"></label>%s</div>'
              % (ic('chercher'), filtres(['Toutes · 1 248', 'Moi · 214', 'À contacter · 312', 'Ont répondu · 58', 'Ne plus écrire · 146'])))
    sel = ('<div class="barre-selection" role="region" aria-label="Sélection"><span style="flex:1 1 160px">2 personnes choisies</span>%s%s%s</div>'
           % (btn('Ajouter à une liste', 'petit', icone='liste'), btn('Étiquette', 'petit', icone='etiquette'), btn('Changer l’étape', 'petit', icone='fleche')))
    normal = haut + outils + tableau('Personnes', ['Personne', 'Rôle', 'Étape', 'Joignable', 'Dernier contact', ''], lignes_t, liens=liens, secondaires=(1, 4, 5)) + sel
    ajout = fenetre('fen-ajout', 'Ajouter un contact',
                    champ('Prénom et nom', 'aj-nom') + champ('E-mail', 'aj-mail', 'email', aide='Doublons vérifiés à la saisie.')
                    + champ('Entreprise', 'aj-ent') + champ('Provenance', 'aj-prov', 'select', ['Choisir…', 'Salon', 'Site internet', 'Recommandation', 'Fichier importé'], aide='Obligatoire.'),
                    '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Contact ajouté.">Ajouter le contact</button>')
    import_ = fenetre('fen-import', 'Importer un fichier',
                      frise(['Fichier', 'Colonnes', 'Contrôle'], 1)
                      + champ('Fichier (CSV ou Excel)', 'imp-fichier', 'text', 'contacts-salon-factice.csv') + champ('Provenance', 'imp-prov', 'select', ['Salon des artisans 2026', 'Autre…']),
                      '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="100 lignes lues : 92 nouvelles, 8 doublons.">Continuer</button>')
    vide = etat_vide('personnes', 'Aucun contact pour l’instant', 'Importez un fichier pour commencer.', btn('Importer un fichier', 'plein', icone='collecte', attrs='data-ouvre="fen-import"'))
    P['contacts.html'] = page('contacts', 'Contacts', '<strong>1 248 personnes</strong>, 1 102 joignables.', normal, vide,
                              actions=btn('Importer', 'contour', icone='collecte', attrs='data-ouvre="fen-import"') + btn('Ajouter un contact', 'plein', icone='ajout-personne', attrs='id="ajout" data-ouvre="fen-ajout"'),
                              onglets_haut=onglets_nav('Sections de Contacts', [('contacts.html', 'Personnes', '1 248'), ('listes.html', 'Listes', '12'), ('listes.html#etiquettes', 'Étiquettes', ''),
                                                                                ('doublons.html', 'Doublons', '8'), ('a-valider.html', 'À valider', '5')], 'contacts.html'),
                              apres=ajout + import_)


# ---------------- Campagne : création en 5 étapes ----------------
def _nouvelle():
    etapes = ['Cible', 'Message', 'Envoi', 'Vérification', 'Lancement']

    def etape(n, titre, icone, corps, suivant=None):
        pied = ''
        if suivant:
            pied += '<button type="button" class="btn btn-plein" data-aller="%d">Continuer : %s %s</button>' % (n + 1, E(suivant), ic('fleche'))
        if n > 1:
            pied += '<button type="button" class="btn btn-contour" data-aller="%d">Retour</button>' % (n - 1)
        return ('<section class="bloc teinte-bleu" data-etape="%d" aria-label="Étape %d"><div class="bloc-tete">%s<h2>%s</h2><span class="mot">Étape %d sur 5</span></div>%s%s</section>'
                % (n, n, ic(icone), E(titre), n, corps, ('<div class="bloc-pied">%s</div>' % pied) if pied else ''))

    def carte_liste(nom, joign, total, coche=False):
        return ('<label><span class="choix-tete"><input type="radio" name="liste"%s><strong>%s</strong></span>'
                '<span class="grand-chiffre">%d</span>%s</label>' % (' checked' if coche else '', E(nom), joign, jauge('Joignables', joign, total, 'vert', '%d sur %d' % (joign, total))))
    e1 = etape(1, 'Qui reçoit ?', 'cible',
               '<div class="choix" role="radiogroup" aria-label="Liste">%s%s%s</div>' % (
                   carte_liste('Organisateurs Rhône-Alpes', 290, 312, True), carte_liste('Fédérations nationales', 80, 84), carte_liste('Salon des artisans 2026', 92, 100))
               + verdict_global('22 oppositions retirées', 'Retirées seules, sans rien faire.', 'vert', 'bouclier')
               + champ('Exclure (facultatif)', 'excl', aide='Adresse, organisation ou domaine.'), 'message')
    seq = '<ol class="sequence">%s</ol>' % ''.join(
        '<li><span class="jour">%s</span><strong>%s</strong>%s%s</li>' % (j, t, badge('vert', 'Validé', '✓'), btn('Aperçu', 'petit-discret', 'message-editeur.html'))
        for j, t in [('Jour 0', 'Premier message'), ('Jour +4', 'Relance'), ('Jour +11', 'Dernier mot')])
    e2 = etape(2, 'Quel message ?', 'message',
               '<div class="choix" role="radiogroup" aria-label="Message type">'
               '<label><span class="choix-tete"><input type="radio" name="mt" checked><strong>Message type n° 1</strong></span><span>%s Organisateurs · v3</span></label>'
               '<label><span class="choix-tete"><input type="radio" name="mt"><strong>Message type n° 2</strong></span><span>%s Fédérations · v1</span></label></div>'
               % (badge('vert', 'Validé', '✓'), badge('vert', 'Validé', '✓'))
               + mini_titre('3 messages, même fil') + seq
               + btn('M’envoyer un test', 'contour', icone='test', attrs='data-ouvre="fen-test"'), 'envoi')

    def boite(adr, vol, etat, coche, cid):
        b = badge('vert', 'Prête', '✓') if etat == 'ok' else badge('bleu', 'En montée', '▶')
        return ('<li><label class="ligne" for="%s"><input type="checkbox" id="%s"%s><span class="quoi"><strong>%s</strong><span>%s par jour</span></span>%s</label></li>'
                % (cid, cid, ' checked' if coche else '', E(adr), vol, b))
    e3 = etape(3, 'Quand et par où ?', 'calendrier',
               '<div class="ligne-champs">' + champ('Départ', 'dep', 'date', '2026-11-04') + champ('Fenêtre d’envoi', 'fen', 'select', ['09:00 – 17:00, jours ouvrés', '10:00 – 16:00, jours ouvrés']) + '</div>'
               + mini_titre('Boîtes d’envoi') + '<ul class="lignes" style="margin-bottom:16px">%s%s%s</ul>' % (
                   boite('claire@prospection-a.example', 40, 'ok', True, 'b1'), boite('will@prospection-b.example', 40, 'ok', True, 'b2'), boite('paul@prospection-c.example', 10, 'montee', False, 'b3'))
               + chiffres([('80', 'par jour'), ('4 jours', 'pour tout envoyer'), ('20 nov.', 'fin prévue')]), 'vérification')
    ctrl = ['Liste figée (312)', 'Oppositions retirées (22)', 'Bloc d’information présent', 'Désinscription en un clic', 'Aucun lien vers le site', 'Aucun mot interdit', 'Boîtes saines (2 sur 2)']
    e4 = etape(4, 'Tout est en règle ?', 'bouclier',
               anneau(7, 7, 'vert', '7/7', 'Tous les contrôles au vert', 'Rien à corriger.')
               + '<ul class="controles" style="margin-top:16px">%s</ul>' % ''.join('<li><span class="p" aria-hidden="true">%s</span>%s</li>' % (ic('coche'), E(c)) for c in ctrl), 'lancement')
    code = ('<fieldset style="border:0;padding:0;margin:16px 0 0"><legend style="font-weight:800;margin-bottom:8px">Code reçu par e-mail</legend><div class="cases-code">%s</div></fieldset>'
            % ''.join('<input type="text" inputmode="numeric" maxlength="1" aria-label="Chiffre %d du code"%s>' % (i + 1, ' autocomplete="one-time-code"' if i == 0 else '') for i in range(6)))
    e5 = ('<section class="bloc teinte-bleu" data-etape="5" aria-label="Étape 5"><div class="bloc-tete">%s<h2>Valider et lancer</h2><span class="mot">Étape 5 sur 5</span></div>%s%s%s'
          '<div class="bloc-pied"><a class="btn btn-plein" href="campagne-suivi.html" data-toast="Campagne validée et programmée.">%sValider et programmer</a><button type="button" class="btn btn-contour" data-aller="4">Retour</button></div></section>'
          % (ic('fusee'), chiffres([('290', 'personnes'), ('4 nov.', 'départ 09:00'), ('3', 'messages'), ('2', 'boîtes')]),
             code, '<p class="petit" style="margin-top:12px">5 minutes pour annuler ensuite.</p>', ic('coche')))
    recap = bloc('Récapitulatif', ''.join('<div class="recap-ligne">%s<div><span>%s</span><strong>%s</strong></div></div>' % (ic(i), E(a), E(b)) for i, a, b in [
        ('cible', 'Cible', 'Organisateurs Rhône-Alpes · 290'), ('message', 'Message', 'Message type n° 1 · 3 envois'),
        ('calendrier', 'Départ', '4 nov. · 09:00'), ('horloge', 'Fin prévue', '20 nov.')]) + '<p class="petit" style="margin-top:12px">Brouillon enregistré à 10:42.</p>',
        'gris', 'liste', mot='Brouillon')
    normal = '<div data-assistant>%s<div class="assistant"><div>%s</div><aside class="recap" aria-label="Récapitulatif">%s</aside></div></div>' % (
        frise(etapes, 1), e1 + e2 + e3 + e4 + e5, recap)
    test = fenetre('fen-test', 'M’envoyer un test', '<label class="case"><input type="checkbox" checked> Moi (will@…)</label><label class="case"><input type="checkbox" checked> Boîtes témoins (4)</label>'
                   + champ('Exemple de destinataire', 'ex-dest', 'select', ['Claire Durand (Garage Durand)', 'Paul Martin (Boulangerie Martin)']) + '<p class="petit">Même chemin qu’un vrai envoi.</p>',
                   '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Test envoyé à 5 adresses.">Envoyer le test</button>')
    vide = etat_vide('liste', 'Aucune liste à cibler', 'Créez d’abord une liste joignable.', btn('Créer une liste', 'plein', 'listes.html', 'plus'))
    P['campagne-nouvelle.html'] = page('campagne-nouvelle', 'Nouvelle campagne', '5 étapes · 5 minutes · rien ne part seul.', normal, vide,
                                       fil=[('Campagnes', 'campagnes.html', 'campagnes')], apres=test)


# ---------------- Santé des envois ----------------
def _sante():
    haut = kpis(
        kpi('Boîtes prêtes', '4', 'boite', 'vert', '', 'boites.html', unite='/ 4', graph=jauge('Prêtes', 4, 4, 'vert', '100 %')),
        kpi('Volume du jour', '120', 'envoi', 'bleu', '', unite='possibles', graph=jauge('Envoyés', 68, 120, 'bleu', '68 envoyés')),
        kpi('Adresses refusées', '0,8 %', 'interdit', 'vert', 'limite : 2 %', graph=jauge('Part de la limite', 8, 20, 'vert', '40 %')),
        kpi('Plaintes', '0 %', 'alerte', 'vert', 'limite : 0,1 %', graph=jauge('Part de la limite', 0, 10, 'vert', '0 %')))
    feux_ = '<div class="feux">%s%s%s</div>' % (
        tuile_feu('prospection-a.example', 'vert', '2 boîtes', chiffres([('48/80', 'envoyés'), ('0,4 %', 'refus')]) + jauge('Quota', 48, 80, 'vert', '60 %'), 'domaines.html'),
        tuile_feu('prospection-b.example', 'ambre', '1 boîte', chiffres([('12/40', 'envoyés'), ('3 %', 'refus temp.')]) + jauge('Quota', 12, 40, 'ambre', 'ralenti ÷ 2'), 'domaines.html'),
        tuile_feu('prospection-c.example', 'bleu', 'jour 6 sur 30', chiffres([('8/10', 'envoyés'), ('0 %', 'refus')]) + jauge('Montée', 6, 30, 'bleu', 'jour 6'), 'chauffe.html'))
    test_ = bloc('Test du matin', chiffres([('07:05', 'heure'), ('4/4', 'témoins'), ('100 %', 'en réception')])
                 + mini_titre('7 derniers matins')
                 + points_serie([('Lun', '', 'coche'), ('Mar', '', 'coche'), ('Mer', 'ambre', 'alerte'), ('Jeu', '', 'coche'), ('Ven', '', 'coche'), ('Sam', '', 'coche'), ('Dim', '', 'coche')]),
                 'vert', 'test', mot='Réussi', pied=btn('Voir les serveurs', 'petit', 'serveurs.html', 'serveur'))
    alerte_ = bloc('Une boîte ralentie', '<p style="font-weight:700;margin-bottom:12px;overflow-wrap:anywhere">will@prospection-b.example</p>'
                   + chiffres([('3 %', 'refus temp.'), ('÷ 2', 'volume'), ('09:30', 'depuis')])
                   + '<p class="petit" style="margin-top:12px">Rien à faire si ça baisse.</p>',
                   'ambre', 'alerte', mot='Attention', pied=btn('Voir ce qui s’est passé', 'plein', 'alertes.html', 'oeil'))
    volume_ = bloc('Envoyés sur 14 jours', courbe([40, 52, 60, 64, 70, 0, 0, 78, 84, 102, 110, 118, 96, 68], ['19 oct.', '26 oct.', 'Aujourd’hui'], '', 'Envoyés par jour'), icone='stats')
    arret_ = bloc('Arrêt d’urgence', chiffres([('2 clics', 'pour tout couper'), ('0', 'message perdu')]),
                  'rouge', 'arret', mot='Sécurité', pied='<button type="button" class="btn btn-danger" data-ouvre="fen-arret">%sTout arrêter</button>' % ic('arret'))
    normal = (verdict_global('Envois normaux', '4 boîtes prêtes · 1 ralentie', 'vert', 'coche', badge('vert', 'Vérifié il y a 3 min', '✓'))
              + haut + mini_titre('Feux par domaine') + feux_
              + '<div class="grille deux" style="margin-top:24px">%s%s</div>' % (alerte_, test_)
              + '<div class="grille deux">%s%s</div>' % (volume_, arret_))
    erreur = etat_erreur('Chiffres illisibles. Par prudence, pas de vert.', 'État des envois inconnu')
    P['sante.html'] = page('sante', 'Santé des envois', '%s <strong>Tout va bien.</strong> Une boîte ralentie.' % feu('vert'), normal,
                           etat_vide('sante', 'Aucun envoi pour l’instant', 'Ajoutez un domaine pour commencer.', btn('Ajouter un domaine', 'plein', 'domaines.html', 'plus')), erreur,
                           actions=btn('Lancer un test', 'contour', icone='test', attrs='data-toast="Test lancé : résultat dans 2 min."'),
                           onglets_haut=onglets_nav('Sections des envois', [('sante.html', 'Vue d’ensemble', ''), ('boites.html', 'Boîtes', '4'), ('domaines.html', 'Domaines', '3'),
                                                                            ('chauffe.html', 'Montée en douceur', ''), ('desinscriptions.html', 'Désinscriptions', ''), ('alertes.html', 'Alertes', '1'), ('serveurs.html', 'Serveurs', '')], 'sante.html'))


# ---------------- Réponses ----------------
def _reponses():
    file_ = '<ul class="file-rep" aria-label="Réponses à traiter">%s</ul>' % ''.join(
        '<li><a href="#"%s>%s<span class="quoi"><span class="rang"><strong>%s</strong>%s</span><span class="extrait">%s</span><span class="heure">%s</span></span></a></li>'
        % (' aria-current="true"' if i == 0 else '', initiales(n, ti), E(n), badge(t, s, sy), E(x), E(h)) for i, (n, ti, t, s, sy, x, h) in enumerate([
            ('Claire Durand', 'terracotta', 'vert', 'Intéressée', '●', '« Rappelez-moi jeudi. »', 'Hier 16:20'),
            ('Hugo Petit', 'terracotta', 'vert', 'Intéressé', '●', '« Envoyez une proposition. »', 'Hier 11:05'),
            ('Inès Moreau', 'gris', 'gris', 'Absente', '○', 'Retour le 12 nov.', 'Hier 09:12'),
            ('Louis Bernard', 'gris', 'rouge', 'STOP', '■', '« Ne m’écrivez plus. »', '31 oct.'),
            ('inconnu@exemple.example', 'violet', 'violet', 'À rattacher', '✦', 'Adresse inconnue', '30 oct.')]))
    geste = lambda touche, lib, toast_, sorte='btn-contour': (
        '<button type="button" class="btn %s" data-toast="%s" data-annulable><span class="touche">%s</span>%s</button>' % (sorte, E(toast_), touche, E(lib)))
    msg = ('<article class="message" aria-label="Réponse de Claire Durand">'
           '<div class="message-tete">%s<div class="quoi"><h2>Claire Durand</h2><span class="petit">Garage Durand · hier 16:20</span></div>%s</div>'
           '<blockquote>Bonjour, c’est intéressant. Pouvez-vous me rappeler jeudi matin ? Claire</blockquote>'
           '<div class="suggestion"><div class="suggestion-tete">%s<span style="flex:1 1 140px">Suggestion</span>%s</div>'
           '<ul class="effets"><li>%sTâche : rappeler jeudi</li><li>%sCampagne arrêtée ici</li><li>%sÉtape : Répondu</li></ul>'
           '<div><button type="button" class="btn btn-plein" data-toast="Réponse traitée : tâche créée, campagne arrêtée pour l’entreprise." data-annulable>%sAppliquer la suggestion</button></div></div>'
           '%s<div class="gestes" role="group" aria-label="Classer autrement">%s%s%s%s</div>'
           '<p class="petit">Raccourcis : J / K pour naviguer.</p></article>'
           % (initiales('Claire Durand', 'terracotta').replace('initiales ', 'initiales grand '), badge('vert', 'Intéressée', '●').replace('class="badge', 'class="badge gros'),
              ic('etincelle'), badge('violet', 'Sûre à 92 %', '✦'), ic('calendrier'), ic('pause'), ic('fleche'), ic('coche'),
              mini_titre('Ou classer autrement'),
              geste('1', 'Pas intéressé', 'Classée : pas intéressé.'), geste('2', 'Plus tard', 'Classée : plus tard.'), geste('3', 'Absent', 'Classée : absent.'),
              '<button type="button" class="btn btn-danger" data-ouvre="fen-stop"><span class="touche">S</span>STOP</button>'))
    haut = kpis(
        kpi('À traiter', '7', 'reponses', 'terracotta', 'la plus ancienne : hier'),
        kpi('Intéressées', '2', 'etincelle', 'vert', 'à rappeler'),
        kpi('STOP à confirmer', '1', 'interdit', 'rouge', 'Louis Bernard'),
        kpi('À rattacher', '1', 'lien', 'violet', 'adresse inconnue', 'reponses-a-rattacher.html'))
    stop_ = bloc('Louis Bernard', '<blockquote style="margin:0 0 12px;padding:14px 18px;background:var(--surface-2);border-radius:12px;font-size:18px">« Ne m’écrivez plus. »</blockquote>',
                 'rouge', 'interdit', mot='STOP', pied='<button type="button" class="btn btn-danger" data-ouvre="fen-stop">%sConfirmer l’opposition</button>' % ic('interdit'))
    ratt_ = lignes(ligne('inconnu@exemple.example', '3 fiches proposées', initiales('in', 'violet'), badge('violet', 'À rattacher', '✦'), 'reponses-a-rattacher.html'))
    toutes_ = lignes(ligne('Organisateurs Rhône-Alpes', '9 réponses, 3 intéressées', initiales('O R', 'bleu'), badge('bleu', 'En cours', '▶'), '#'),
                     ligne('Commerces de Lyon', '11 réponses, 4 intéressées', initiales('C L', 'vert'), badge('vert', 'Terminée', '✓'), '#'))
    normal = haut + onglets('Réponses', [
        ('a-traiter', 'À traiter <span class="nb">7</span>', '<div class="reponses">%s%s</div>' % (file_, msg)),
        ('stop', 'STOP à confirmer <span class="nb">1</span>', stop_),
        ('rattacher', 'À rattacher <span class="nb">1</span>', ratt_),
        ('toutes', 'Toutes', toutes_)])
    stop = fenetre('fen-stop', 'Enregistrer l’opposition ?', '<p style="margin-bottom:8px"><strong>Louis Bernard</strong> ne recevra plus rien. Définitif.</p><label class="case"><input type="checkbox"> Toute l’organisation (Atelier Bernard)</label>',
                   '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-danger-plein" data-ferme data-toast="Opposition enregistrée.">Enregistrer l’opposition</button>')
    P['reponses.html'] = page('reponses', 'Réponses', '<strong>7 réponses</strong> à traiter.', normal,
                              etat_vide('reponses', 'Aucune réponse à traiter', 'Tout est traité. Bravo !', btn('Voir toutes les réponses', 'plein', icone='reponses', attrs='data-toast="Filtre « Toutes » appliqué."')),
                              apres=stop)


for f in (_index, _contacts, _nouvelle, _sante, _reponses):
    f()
