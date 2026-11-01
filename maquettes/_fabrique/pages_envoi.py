# -*- coding: utf-8 -*-
"""Lot M1 · produit ENVOI (facturé à part, couleur bleu-vert).

Toutes ces pages sont NOUVELLES (le CRM réel n'a pas de moteur d'envoi : plan 28 § 1.2).
Elles intègrent les 15 ajouts prioritaires du plan 27 : cibler une étiquette, fiches domaine
et boîte, état par destinataire, résultats par boîte/domaine/liste, répondre depuis le CRM,
reprogrammer, dupliquer, pause depuis la liste, terminer, ajouter une adresse IP, chercher
un envoi, exports ; plus programmer et le test de deux versions (A/B).
Données factices : domaines en .example, adresses IP de documentation (192.0.2.x).
"""
from socle import *  # noqa: F401,F403

P = {}
ST = {'Brouillon': ('gris', '○'), 'À valider': ('ambre', '▲'), 'Programmée': ('violet', '◷'), 'En cours': ('bleu', '▶'), 'En pause': ('ambre', '❚❚'), 'Terminée': ('vert', '✓'), 'Arrêtée': ('rouge', '■')}


def st(s):
    t, sy = ST[s]
    return badge(t, s, sy)


ONG_CAMP = lambda a: onglets_nav('Sections des campagnes', [('campagnes.html', 'Campagnes', '6'), ('resultats.html', 'Résultats', ''), ('messages-types.html', 'Messages types', '4'), ('calendrier-envois.html', 'Calendrier', '')], a)
ONG_SANTE = lambda a: onglets_nav('Sections de la santé', [('sante.html', 'Vue d’ensemble', ''), ('chercher-envoi.html', 'Chercher un envoi', ''), ('feu-vert.html', 'Feu vert', '13/15')], a)
ONG_SERV = lambda a: onglets_nav('Sections des serveurs', [('serveurs.html', 'Serveurs et adresses IP', ''), ('configuration.html', 'Configuration', '1')], a)
ONG_REP = lambda a: onglets_nav('Sections des réponses', [('reponses.html', 'Réponses', '7'), ('reponses-a-rattacher.html', 'À rattacher', '1')], a)
ONG_REG = lambda a: onglets_nav('Sections des réglages d’envoi', [('reglages-envoi.html', 'Vue d’ensemble', ''), ('regles-prudence.html', 'Règles et horaires', ''), ('identite.html', 'Identité', ''), ('reglages-alertes.html', 'Alertes et avis', '')], a)
BOUTONS_FEN = lambda ok, toast, sorte='btn-plein': '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn %s" data-ferme data-toast="%s">%s</button>' % (sorte, E(toast), E(ok))

FEN_PAUSE = fenetre('fen-pause', 'Mettre en pause ?', '<p><strong>Organisateurs Rhône-Alpes</strong> s’arrête tout de suite. Rien n’est perdu : reprise quand vous voulez.</p>', BOUTONS_FEN('Mettre en pause', 'Campagne en pause.'))
FEN_DATE = fenetre('fen-date', 'Changer la date', '<div class="filtres" role="group" data-unique aria-label="Raccourcis"><button type="button" class="puce" aria-pressed="true">Demain 9:00</button><button type="button" class="puce" aria-pressed="false">Lundi 9:00</button><button type="button" class="puce" aria-pressed="false">Autre…</button></div>'
                   + '<div class="ligne-champs">%s%s</div><p class="petit">Liste et messages inchangés.</p>' % (champ('Jour', 'fd-jour', 'date', '2026-11-02'), champ('Heure', 'fd-heure', 'time', '09:00')), BOUTONS_FEN('Reprogrammer', 'Campagne reprogrammée : lundi 2 nov. à 09:00.'))
FEN_DUP = fenetre('fen-dupliquer', 'Dupliquer la campagne', champ('Nom de la copie', 'fdu-nom', valeur='Organisateurs Rhône-Alpes (copie)') + '<label class="case"><input type="checkbox" checked> Garder la même cible (recalculée)</label><label class="case"><input type="checkbox" checked> Garder les messages</label><label class="case"><input type="checkbox"> Exclure ceux qui ont déjà reçu</label>',
                  BOUTONS_FEN('Créer la copie (brouillon)', 'Copie créée en brouillon.'))
FEN_FIN = fenetre('fen-terminer', 'Terminer définitivement ?', '<p>Plus aucun message ne partira pour cette campagne, relances comprises. Les réponses restent traitées. <strong>On ne peut pas la relancer</strong> (mais on peut la dupliquer).</p>',
                  BOUTONS_FEN('Terminer la campagne', 'Campagne terminée.', 'btn-danger-plein'))
FENS_CAMP = FEN_PAUSE + FEN_DATE + FEN_DUP + FEN_FIN


def _act(*cles):
    d = {'pause': '<button type="button" class="btn btn-contour petit-btn" data-ouvre="fen-pause">%sPause</button>' % ic('pause'),
         'reprendre': btn('Reprendre', 'petit', icone='lecture', attrs='data-toast="Campagne reprise."'),
         'date': '<button type="button" class="btn btn-contour petit-btn" data-ouvre="fen-date">%sChanger la date</button>' % ic('calendrier'),
         'dup': '<button type="button" class="btn btn-discret petit-btn" data-ouvre="fen-dupliquer">%sDupliquer</button>' % ic('copie'),
         'fin': '<button type="button" class="btn btn-discret petit-btn" data-ouvre="fen-terminer">Terminer</button>',
         'ouvrir': btn('Ouvrir', 'petit-discret', 'campagne-suivi.html'), 'valider': btn('Relire et valider', 'petit', 'campagne-suivi.html', 'oeil')}
    return '<div class="ligne-actions">%s</div>' % ''.join(d[c] for c in cles)


# ======================= CAMPAGNES =======================
CAMPS = [('Organisateurs Rhône-Alpes', 'En cours', 'Audience · 290', 168, 290, '9 (3 intéressées)', 'Aujourd’hui 14:00', ('pause', 'dup', 'fin'), True),
         ('Fédérations — automne', 'Programmée', 'Étiquette · salon-artisans-2026 · 388', 0, 388, '—', 'Mer. 4 nov. 09:00', ('date', 'dup', 'fin'), False),
         ('Presse régionale AURA', 'À valider', 'Audience presse · 186', 0, 186, '—', 'À valider', ('valider', 'dup'), False),
         ('Commerces de Vienne', 'En pause', 'Liste · Invités salon · 127', 64, 127, '4 (1 intéressée)', 'En pause depuis 10:12', ('reprendre', 'date', 'fin'), False),
         ('Clubs d’entreprises Savoie', 'Terminée', 'Audience · 212', 212, 212, '17 (6 intéressées)', '—', ('dup',), False),
         ('Relance printemps', 'Brouillon', 'Étiquette · relance-printemps · 96', 0, 96, '—', '—', ('ouvrir', 'dup'), False)]


def _campagnes():
    lig, liens = [], []
    for n, s, cible, fait, tot, rep, proch, acts, ab in CAMPS:
        nom = '<a href="campagne-suivi.html"><strong>%s</strong></a>%s<span class="sous">%s</span>' % (E(n), (' ' + badge('violet', 'Test A/B', '✦')) if ab else '', E(cible))
        lig.append([nom, st(s), jauge('Envoyés', fait, tot, 'vert' if s == 'Terminée' else 'bleu', '%d / %d' % (fait, tot)), E(rep), E(proch), _act(*acts)])
        liens.append('campagne-suivi.html')
    haut = kpis(kpi('En cours', '1', 'lecture', 'bleu', '168 / 290 envoyés'), kpi('Programmées', '1', 'calendrier', 'violet', 'mer. 4 nov. 09:00'),
                kpi('À valider', '1', 'alerte', 'ambre', 'Presse régionale AURA', 'campagne-suivi.html'), kpi('Réponses (30 j)', '30', 'reponses', 'vert', '10 intéressées', 'reponses.html'))
    outils = ('<div class="barre-outils"><label class="champ-recherche" for="cherche-envoi">%s<span class="visuellement-cache">Chercher une campagne ou un envoi</span>'
              '<input type="search" id="cherche-envoi" placeholder="Campagne, ou adresse e-mail d’un destinataire…"></label>%s%s</div>'
              % (ic('chercher'), btn('Chercher un envoi', 'contour', 'chercher-envoi.html', 'chercher'), btn('Exporter', 'contour', icone='export', attrs='data-toast="Liste des campagnes exportée (CSV)."')))
    f = filtres(['Toutes · 6', 'En cours · 1', 'Programmées · 1', 'À valider · 1', 'En pause · 1', 'Terminées · 1', 'Brouillons · 1'])
    normal = haut + outils + f + tableau('Campagnes', ['Campagne', 'Statut', 'Progression', 'Réponses', 'Prochain envoi', 'Actions'], lig, liens=liens, secondaires=(3, 4))
    vide = etat_vide('envoi', 'Aucune campagne pour l’instant', 'Choisissez une étiquette, une audience ou une liste.', btn('Nouvelle campagne', 'plein', 'campagne-nouvelle.html', 'plus'))
    P['campagnes.html'] = page('campagnes', 'Campagnes', '<strong>1 en cours</strong>, 1 programmée, 1 à valider.', normal, vide,
                               actions=btn('Campagne vers une étiquette', 'contour', 'campagne-nouvelle.html?cible=etiquette', 'diese') + btn('Nouvelle campagne', 'plein', 'campagne-nouvelle.html', 'plus'),
                               onglets_haut=ONG_CAMP('campagnes.html'), apres=FENS_CAMP)


def _nouvelle():
    etapes = ['Cible', 'Message', 'Quand', 'Vérification', 'Lancement']

    def etape(n, titre, icone, corps, suivant=None):
        pied = ('<button type="button" class="btn btn-plein" data-aller="%d">Continuer : %s %s</button>' % (n + 1, E(suivant), ic('fleche'))) if suivant else ''
        if n > 1:
            pied += '<button type="button" class="btn btn-contour" data-aller="%d">Retour</button>' % (n - 1)
        return ('<section class="bloc teinte-bleu" data-etape="%d" aria-label="Étape %d"><div class="bloc-tete">%s<h2>%s</h2><span class="mot">Étape %d sur 5</span></div>%s%s</section>'
                % (n, n, ic(icone), E(titre), n, corps, ('<div class="bloc-pied">%s</div>' % pied) if pied else ''))

    def carte(nom, sorte, joign, total, coche=False, groupe='cible'):
        return ('<label><span class="choix-tete"><input type="radio" name="%s"%s><strong>%s</strong></span><span>%s</span><span class="grand-chiffre">%d</span>%s</label>'
                % (groupe, ' checked' if coche else '', E(nom), badge({'Étiquette': 'violet', 'Audience': 'bleu', 'Liste': 'gris'}[sorte], sorte, '●'), joign, jauge('Joignables', joign, total, 'vert', '%d sur %d' % (joign, total))))
    e1 = etape(1, 'Qui reçoit ?', 'cible',
               filtres(['Étiquette', 'Audience', 'Liste']) +
               '<div class="choix" role="radiogroup" aria-label="Cible">%s%s%s</div>' % (carte('salon-artisans-2026', 'Étiquette', 388, 412, True), carte('Organisateurs Rhône-Alpes', 'Audience', 290, 312), carte('Invités salon des artisans', 'Liste', 112, 127))
               + verdict_global('46 adresses retirées d’office', 'Oppositions (22), clients et affaires en cours (18), adresses partagées (6).', 'vert', 'bouclier')
               + champ('Exclure aussi (facultatif)', 'excl', aide='Adresse, organisation, domaine ou étiquette.'), 'message')
    ab = ('<div class="version-ab"><div class="carte teinte-bleu"><p><strong>Version A</strong> · objet</p><p>« Une idée pour votre prochain salon »</p></div>'
          '<div class="carte teinte-violet"><p><strong>Version B</strong> · objet</p><p>« Salon des artisans : on en parle ? »</p></div></div>'
          + chiffres([('20 %', 'part testée'), ('50 / 50', 'partage'), ('48 h', 'puis gagnant'), ('réponses', 'critère')]))
    seq = '<ol class="sequence">%s</ol>' % ''.join('<li><span class="jour">%s</span><strong>%s</strong>%s</li>' % (j, t, badge('vert', 'Validé', '✓')) for j, t in [('Jour 0', 'Premier message'), ('Jour +4', 'Relance'), ('Jour +11', 'Dernier mot')])
    e2 = etape(2, 'Quel message ?', 'message',
               '<div class="choix" role="radiogroup" aria-label="Message type"><label><span class="choix-tete"><input type="radio" name="mt" checked><strong>Organisateurs · v3</strong></span>%s</label>'
               '<label><span class="choix-tete"><input type="radio" name="mt"><strong>Fédérations · v1</strong></span>%s</label></div>' % (badge('vert', 'Validé', '✓'), badge('vert', 'Validé', '✓'))
               + mini_titre('3 messages, même fil') + seq + interrupteur('Tester deux versions (A/B)', 'Sur 20 % de la cible ; la meilleure part ensuite.', 'ab', True) + ab
               + '<div class="bandeau ambre" style="margin-top:16px">%s<span>Champ « prénom » vide pour 12 personnes : « Bonjour » sera utilisé (valeur de repli).</span></div>' % ic('alerte')
               + btn('M’envoyer un test', 'contour', icone='test', attrs='data-ouvre="fen-test"'), 'quand')

    def boite(adr, vol, ok, coche, cid):
        return ('<li><label class="ligne" for="%s"><input type="checkbox" id="%s"%s><span class="quoi"><strong>%s</strong><span>%s par jour</span></span>%s</label></li>'
                % (cid, cid, ' checked' if coche else '', E(adr), vol, badge('vert', 'Prête', '✓') if ok else badge('bleu', 'En chauffe', '▶')))
    e3 = etape(3, 'Quand et par où ?', 'calendrier',
               '<div class="filtres" role="group" data-unique aria-label="Départ"><button type="button" class="puce" aria-pressed="false">Dès la validation</button><button type="button" class="puce" aria-pressed="true">Programmer</button></div>'
               + '<div class="ligne-champs">' + champ('Jour', 'dep', 'date', '2026-11-04') + champ('Heure', 'dep-h', 'time', '09:00') + champ('Fenêtre d’envoi', 'fen', 'select', ['09:00 – 17:00, jours ouvrés', '10:00 – 16:00, jours ouvrés'])
               + champ('Plafond de cette campagne', 'plaf', 'number', '80', 'par jour, toutes boîtes') + '</div>'
               + '<label class="case"><input type="checkbox" checked> Heure du destinataire (Outre-mer : heure locale)</label>'
               + mini_titre('Boîtes d’envoi') + '<ul class="lignes" style="margin-bottom:16px">%s%s%s</ul>' % (
                   boite('claire@prospection-a.example', 40, True, True, 'b1'), boite('will@prospection-b.example', 40, True, True, 'b2'), boite('paul@prospection-c.example', 10, False, False, 'b3'))
               + chiffres([('80', 'par jour'), ('5 jours', 'pour tout envoyer'), ('11 nov.', 'fin prévue')]), 'vérification')
    ctrl = ['Liste figée (388)', 'Oppositions retirées (22)', 'Clients exclus (18)', 'Bloc d’information présent', 'Désinscription en un clic', 'Texte simple, sans pièce jointe', 'Valeurs de repli prêtes', 'Boîtes saines (2 sur 2)']
    e4 = etape(4, 'Tout est en règle ?', 'bouclier', anneau(8, 8, 'vert', '8/8', 'Tous les contrôles au vert', 'Rien à corriger.')
               + '<ul class="controles" style="margin-top:16px">%s</ul>' % ''.join('<li><span class="p" aria-hidden="true">%s</span>%s</li>' % (ic('coche'), E(c)) for c in ctrl), 'lancement')
    code = ('<fieldset style="border:0;padding:0;margin:16px 0 0"><legend style="font-weight:800;margin-bottom:8px">Code reçu par e-mail</legend><div class="cases-code">%s</div></fieldset>'
            % ''.join('<input type="text" inputmode="numeric" maxlength="1" aria-label="Chiffre %d du code">' % (i + 1) for i in range(6)))
    e5 = ('<section class="bloc teinte-bleu" data-etape="5" aria-label="Étape 5"><div class="bloc-tete">%s<h2>Valider et programmer</h2><span class="mot">Étape 5 sur 5</span></div>%s%s<p class="petit" style="margin-top:12px">5 minutes pour annuler ensuite.</p>'
          '<div class="bloc-pied"><a class="btn btn-plein" href="campagne-suivi.html" data-toast="Campagne validée et programmée.">%sValider et programmer</a><button type="button" class="btn btn-contour" data-aller="4">Retour</button></div></section>'
          % (ic('fusee'), chiffres([('388', 'personnes'), ('4 nov.', 'départ 09:00'), ('3', 'messages'), ('A/B', '20 %')]), code, ic('coche')))
    recap = bloc('Récapitulatif', ''.join('<div class="recap-ligne">%s<div><span>%s</span><strong>%s</strong></div></div>' % (ic(i), E(a), E(b)) for i, a, b in [
        ('diese', 'Cible', 'Étiquette salon-artisans-2026 · 388'), ('message', 'Message', 'Organisateurs v3 · A/B sur l’objet'), ('calendrier', 'Départ', 'Mer. 4 nov. · 09:00'), ('horloge', 'Fin prévue', '11 nov.')])
        + '<p class="petit" style="margin-top:12px">Brouillon enregistré à 10:42.</p>', 'gris', 'liste', mot='Brouillon')
    normal = '<div data-assistant>%s<div class="assistant"><div>%s</div><aside class="recap" aria-label="Récapitulatif">%s</aside></div></div>' % (frise(etapes, 1), e1 + e2 + e3 + e4 + e5, recap)
    test = fenetre('fen-test', 'M’envoyer un test', '<label class="case"><input type="checkbox" checked> Moi (will@…)</label><label class="case"><input type="checkbox" checked> Boîtes témoins (4)</label><label class="case"><input type="checkbox" checked> Les deux versions (A et B)</label>'
                   + champ('Exemple de destinataire', 'ex-dest', 'select', ['Paul Morin (Boulangerie des Tilleuls)', 'Nadia Haddad (Imprimerie du Lac)']), BOUTONS_FEN('Envoyer le test', 'Test envoyé à 5 adresses.'))
    P['campagne-nouvelle.html'] = page('campagne-nouvelle', 'Nouvelle campagne', 'Étiquette, audience ou liste · 5 étapes · <strong>rien ne part seul</strong>.', normal,
                                       etat_vide('liste', 'Rien à cibler', 'Créez une étiquette, une audience ou une liste dans le CRM.', btn('Ouvrir les étiquettes', 'plein', 'etiquettes.html', 'diese')),
                                       fil=[('Campagnes', 'campagnes.html', 'campagnes')], apres=test)


def _suivi():
    haut = kpis(kpi('Envoyés', '168', 'envoi', 'bleu', 'sur 290', graph=jauge('Envoyés', 168, 290, 'bleu', '58 %')), kpi('Réponses', '9', 'reponses', 'vert', '3 intéressées', 'reponses.html'),
                kpi('Refusés', '2', 'interdit', 'vert', '1,2 % · limite 2 %'), kpi('Désinscriptions', '1', 'croix', 'gris', '0,6 %'))
    dest = (filtres(['Tous · 290', 'En file · 118', 'Partis · 159', 'Refusés · 2', 'Ont répondu · 9', 'Exclus · 2'])
            + tableau('Destinataires', ['Personne', 'État', 'Message', 'Détail'], [
                ['<div class="cellule-personne">%s<div><a href="contact.html">Paul Morin</a><span class="sous">Boulangerie des Tilleuls</span></div></div>' % initiales('Paul Morin'), badge('vert', 'A répondu', '✓'), 'Message 1', 'Relances annulées'],
                ['<div class="cellule-personne">%s<div><a href="contact.html">Nadia Haddad</a><span class="sous">Imprimerie du Lac</span></div></div>' % initiales('Nadia Haddad'), badge('bleu', 'Parti', '▶'), 'Relance', 'Accepté par le serveur'],
                ['<div class="cellule-personne">%s<div><a href="contact.html">Yves Roche</a><span class="sous">Atelier Bois &amp; Forme</span></div></div>' % initiales('Yves Roche', 'gris'), badge('rouge', 'Refusé', '■'), 'Message 1', 'Adresse inexistante (550)'],
                ['<div class="cellule-personne">%s<div><a href="contact.html">Lina Costa</a><span class="sous">Office de tourisme du Val</span></div></div>' % initiales('Lina Costa'), badge('gris', 'En file', '○'), 'Message 1', 'Départ prévu 14:00']],
                liens=['contact.html'] * 4) + '<div class="bloc-pied">%s</div>' % btn('Exporter l’état des destinataires', 'petit', icone='export', attrs='data-toast="290 lignes exportées (CSV)."'))
    ab = '<div class="grille deux">%s%s</div>' % (
        bloc('Version A · « Une idée pour votre prochain salon »', chiffres([('29', 'envoyés'), ('3', 'réponses'), ('10,3 %', 'taux')]) + jauge('Taux de réponse', 103, 150, 'vert', '10,3 %'), 'vert', 'ab', mot='En tête'),
        bloc('Version B · « Salon des artisans : on en parle ? »', chiffres([('29', 'envoyés'), ('1', 'réponse'), ('3,4 %', 'taux')]) + jauge('Taux de réponse', 34, 150, 'gris', '3,4 %'), icone='ab'))
    ab += '<p class="petit" style="margin-top:12px">Gagnant choisi seul dans 22 h (critère : réponses). Vous pouvez choisir avant.</p>'
    msgs = tableau('Par message', ['Message', 'Envoyés', 'Réponses', 'Refus'], [['Jour 0 · Premier message', '140', '7', '2'], ['Jour +4 · Relance', '28', '2', '0'], ['Jour +11 · Dernier mot', '0', '—', '—']])
    boites_ = tableau('Par boîte', ['Boîte', 'Envoyés', 'Réponses', 'Refus'], [['<a href="boite.html">claire@prospection-a.example</a>', '92', '6', '1'], ['<a href="boite.html">will@prospection-b.example</a>', '76', '3', '1']])
    prog = '<div class="grille deux">%s%s</div>' % (bloc('Envoyés par jour', barres([('Ven', 40), ('Sam', 0), ('Dim', 0), ('Lun', 64), ('Auj.', 64)], 'bleu', 'Envoyés par jour'), icone='stats'),
                                                    bloc('Ce qui se passe', lignes(ligne('Prochain départ', 'Aujourd’hui 14:00 · 40 messages', ic('horloge'), badge('bleu', 'Prévu', '◷')),
                                                                                   ligne('Paul Morin a répondu', 'Relances annulées pour lui', ic('reponses'), badge('vert', 'Intéressé', '●'), 'reponses.html')), icone='sante'))
    normal = (verdict_global('Campagne en cours', '168 envoyés sur 290 · fin prévue le 6 nov.', 'vert', 'lecture', st('En cours'))
              + haut + onglets('Suivi', [('prog', 'Progression', prog), ('dest', 'Destinataires <span class="nb">290</span>', dest), ('ab', 'Test A/B', ab), ('msg', 'Par message', msgs), ('boites', 'Par boîte', boites_)]))
    lot = fenetre('fen-lot', 'Ajouter un lot de destinataires', '<p style="margin-bottom:12px">La liste reste figée : le lot est une nouvelle liste, avec sa propre validation.</p>' + champ('Ajouter', 'lot-src', 'select', ['Étiquette : relance-printemps (96)', 'Liste : Invités salon (127)']),
                  BOUTONS_FEN('Préparer le lot', 'Lot de 96 préparé : validation demandée.'))
    P['campagne-suivi.html'] = page('campagne-suivi', 'Organisateurs Rhône-Alpes', st('En cours') + ' <strong>168 / 290</strong> envoyés · 9 réponses', normal,
                                    actions='<button type="button" class="btn btn-plein" data-ouvre="fen-pause">%sMettre en pause</button>' % ic('pause')
                                    + '<button type="button" class="btn btn-contour" data-ouvre="fen-date">%sChanger la date</button>' % ic('calendrier')
                                    + '<button type="button" class="btn btn-contour" data-ouvre="fen-dupliquer">%sDupliquer</button>' % ic('copie')
                                    + '<button type="button" class="btn btn-contour" data-ouvre="fen-lot">%sAjouter un lot</button>' % ic('plus')
                                    + '<button type="button" class="btn btn-danger" data-ouvre="fen-terminer">%sTerminer</button>' % ic('stop-carre'),
                                    fil=[('Campagnes', 'campagnes.html', 'campagnes')], apres=FENS_CAMP + lot)


def _resultats():
    def t(titre, cols, rows, lien=None):
        return tableau(titre, cols, rows, liens=[lien] * len(rows) if lien else None) + '<div class="bloc-pied">%s</div>' % btn('Exporter (CSV)', 'petit', icone='export', attrs='data-toast="Résultats exportés."')
    cols = ['Nom', 'Envoyés', 'Refusés', 'Plaintes', 'Réponses', 'Intéressées']
    par_boite = t('Par boîte', cols, [['<a href="boite.html">claire@prospection-a.example</a>', '1 240', '0,6 %', '0', '58', '19'], ['<a href="boite.html">will@prospection-b.example</a>', '1 120', '1,9 %', '0', '41', '12'], ['<a href="boite.html">paul@prospection-c.example</a>', '86', '0 %', '0', '4', '1']], 'boite.html')
    par_dom = t('Par domaine', cols, [['<a href="domaine.html">prospection-a.example</a>', '1 960', '0,7 %', '0', '81', '27'], ['<a href="domaine.html">prospection-b.example</a>', '400', '2,8 %', '1', '18', '4'], ['<a href="domaine.html">prospection-c.example</a>', '86', '0 %', '0', '4', '1']], 'domaine.html')
    par_liste = t('Par cible', cols, [['Audience · Organisateurs Rhône-Alpes', '168', '1,2 %', '0', '9', '3'], ['Audience · Clubs d’entreprises Savoie', '212', '0,9 %', '0', '17', '6'], ['Liste · Invités salon', '64', '1,6 %', '0', '4', '1']])
    par_msg = t('Par message type', ['Message type', 'Version', 'Envoyés', 'Réponses', 'Taux'], [['Organisateurs', 'v3', '820', '61', '7,4 %'], ['Organisateurs', 'v2', '640', '28', '4,4 %'], ['Fédérations', 'v1', '300', '14', '4,7 %']])
    haut = kpis(kpi('Envoyés (30 j)', '2 446', 'envoi', 'bleu', ''), kpi('Taux de réponse', '4,2 %', 'reponses', 'vert', '103 réponses'), kpi('Refusés', '1,1 %', 'interdit', 'vert', 'limite 2 %'), kpi('Plaintes', '0,04 %', 'alerte', 'vert', 'limite 0,1 %'))
    normal = haut + '<p class="petit" style="margin-bottom:16px">Pas de mesure des ouvertures : seules les réponses comptent.</p>' + onglets('Résultats', [('b', 'Par boîte', par_boite), ('d', 'Par domaine', par_dom), ('l', 'Par cible', par_liste), ('m', 'Par message type', par_msg)])
    P['resultats.html'] = page('resultats', 'Résultats', 'Comparer boîtes, domaines, cibles et messages · <strong>30 derniers jours</strong>', normal,
                               actions=btn('Exporter tout', 'contour', icone='export', attrs='data-toast="Résultats exportés (CSV)."'), onglets_haut=ONG_CAMP('resultats.html'), menu='campagnes')


def _messages_types():
    M = [('Organisateurs', 'v3', 'Validé', 'vert', 'Organisateurs Rhône-Alpes'), ('Fédérations', 'v1', 'Validé', 'vert', 'Fédérations — automne'), ('Presse', 'v2', 'À relire', 'ambre', 'Presse régionale AURA'), ('Relance printemps', 'v1', 'Brouillon', 'gris', '—')]
    lig = [['<a href="message-editeur.html"><strong>%s</strong></a>' % n, v, badge(t, s, '●'), E(u), btn('Ouvrir', 'petit-discret', 'message-editeur.html')] for n, v, s, t, u in M]
    haut = kpis(kpi('Messages types', '4', 'message', 'bleu', 'jamais supprimés : archivés'), kpi('Validés', '2', 'coche', 'vert', ''), kpi('À relire', '1', 'alerte', 'ambre', ''), kpi('Blocs réutilisables', '6', 'pieces', 'violet', 'signatures, appels'))
    normal = haut + tableau('Messages types', ['Message type', 'Version', 'Statut', 'Utilisé par', ''], lig, liens=['message-editeur.html'] * 4)
    P['messages-types.html'] = page('messages-types', 'Messages types', '<strong>4 messages</strong>, 2 validés.', normal,
                                    actions=btn('Brouillon par l’IA', 'contour', icone='etincelle', attrs='data-toast="Brouillon de séquence proposé (à relire)."') + btn('Nouveau message', 'plein', 'message-editeur.html', 'plus'),
                                    onglets_haut=ONG_CAMP('messages-types.html'), menu='campagnes')


def _editeur():
    ed = bloc('Message 1 · Jour 0', champ('Objet', 'm-obj', valeur='Une idée pour votre prochain salon') + champ('Texte', 'm-txt', 'textarea', 'Bonjour {prénom | Bonjour},\n\nJ’ai vu que {entreprise} organise des événements…\n\n{signature}', 'Texte simple. Pas de pièce jointe en prospection.')
              + '<p><span class="champ-var">{prénom}</span> <span class="champ-var">{entreprise}</span> <span class="champ-var">{ville}</span> <span class="champ-var">{signature}</span></p>', 'bleu', 'message', mot='v3')
    blocs_ = bloc('Blocs réutilisables', lignes(ligne('Signature Will', 'Utilisée 12 fois', ic('pieces'), btn('Insérer', 'petit-discret')), ligne('Appel : 15 min au téléphone', 'Utilisé 5 fois', ic('pieces'), btn('Insérer', 'petit-discret'))), 'violet', 'pieces', mot='Nouveau')
    apercu = bloc('Aperçu réel', filtres(['Ordinateur', 'Téléphone']) + '<div class="apercu-mail"><p><strong>Objet :</strong> Une idée pour votre prochain salon</p><hr class="sep"><p>Bonjour Paul,</p><p style="margin-top:8px">J’ai vu que Boulangerie des Tilleuls organise des événements…</p><p style="margin-top:8px">Will</p><hr class="sep"><p class="petit">Bloc d’information · Se désinscrire en un clic</p></div>'
                  + champ('Voir pour', 'm-pour', 'select', ['Paul Morin (Boulangerie des Tilleuls)', 'Sans prénom (valeur de repli)']), icone='oeil')
    ctrl = bloc('Contrôles', '<ul class="controles">%s</ul>' % ''.join('<li><span class="p" aria-hidden="true">%s</span>%s</li>' % (ic('coche'), c) for c in ['Aucun mot interdit', 'Aucun lien raccourci', 'Valeurs de repli prêtes', 'Texte simple']), 'vert', 'bouclier', mot='4/4')
    normal = '<div class="grille deux"><div class="pile">%s%s</div><div class="pile">%s%s</div></div>' % (ed, blocs_, apercu, ctrl)
    P['message-editeur.html'] = page('message-editeur', 'Organisateurs · v3', 'Objet, texte, aperçu réel, <strong>contrôles au vert</strong>.', normal,
                                     actions=btn('M’envoyer un test', 'contour', icone='test', attrs='data-toast="Test envoyé à 5 adresses."') + btn('Enregistrer la version', 'plein', icone='coche', attrs='data-toast="Version 4 enregistrée (la v3 est gardée)."'),
                                     fil=[('Messages types', 'messages-types.html', 'campagnes')], menu='campagnes')


def _calendrier():
    jours = [('Lun 2', [('Organisateurs RA', 40, 'bleu')]), ('Mar 3', [('Organisateurs RA', 40, 'bleu')]), ('Mer 4', [('Organisateurs RA', 30, 'bleu'), ('Fédérations — automne', 50, 'violet')]),
             ('Jeu 5', [('Fédérations — automne', 80, 'violet')]), ('Ven 6', [('Fédérations — automne', 80, 'violet')])]
    cols = ''.join('<section class="colonne"><h2><span>%s</span><span class="badge gris" data-s="●">%d</span></h2>%s</section>' % (j, sum(x[1] for x in it), ''.join(
        '<div class="carte-affaire"><a href="campagne-suivi.html">%s</a><div class="bas">%s</div></div>' % (E(n), badge(t, '%d messages' % v, '●')) for n, v, t in it)) for j, it in jours)
    normal = kpis(kpi('Cette semaine', '470', 'calendrier', 'bleu', 'messages prévus'), kpi('Plafond total', '120', 'boite', 'vert', 'par jour, 4 boîtes'), kpi('Jour le plus chargé', 'Jeudi', 'stats', 'ambre', '80 / 120')) + '<div class="colonnes">%s</div>' % cols
    P['calendrier-envois.html'] = page('calendrier-envois', 'Calendrier des envois', 'La semaine <strong>d’un coup d’œil</strong>, toutes campagnes.', normal, onglets_haut=ONG_CAMP('calendrier-envois.html'), menu='campagnes')


# ======================= RÉPONSES =======================
def _reponses():
    file_ = '<ul class="file-rep" aria-label="Réponses à traiter">%s</ul>' % ''.join(
        '<li><a href="#"%s>%s<span class="quoi"><span class="rang"><strong>%s</strong>%s</span><span class="extrait">%s</span><span class="heure">%s</span></span></a></li>'
        % (' aria-current="true"' if i == 0 else '', initiales(n, ti), E(n), badge(t, s, sy), E(x), E(h)) for i, (n, ti, t, s, sy, x, h) in enumerate([
            ('Paul Morin', 'terracotta', 'vert', 'Intéressé', '●', '« Rappelez-moi jeudi. »', 'Hier 16:20'),
            ('Nadia Haddad', 'terracotta', 'vert', 'Intéressée', '●', '« Envoyez une proposition. »', 'Hier 11:05'),
            ('Lina Costa', 'gris', 'gris', 'Absente', '○', 'Retour le 12 nov.', 'Hier 09:12'),
            ('Yves Roche', 'gris', 'rouge', 'STOP', '■', '« Ne m’écrivez plus. »', '31 oct.')]))
    fil = ('<div class="fil-message"><div class="bulle moi"><div class="qui"><span>Will · claire@prospection-a.example</span><span class="petit">28 oct. 09:12</span></div><p>Bonjour Paul, j’ai vu que la Boulangerie des Tilleuls organise des événements…</p></div>'
           '<div class="bulle"><div class="qui"><span>Paul Morin</span><span class="petit">Hier 16:20</span></div><p style="font-size:18px">Bonjour, c’est intéressant. Pouvez-vous me rappeler jeudi matin ? Paul</p></div></div>')
    rep = ('<div class="bloc teinte-bleu" style="margin-top:14px"><div class="bloc-tete">%s<h2>Répondre</h2><span class="mot">Même fil, même boîte</span></div>'
           '<div class="filtres" role="group" aria-label="Réponses rapides"><button type="button" class="puce" aria-pressed="false">Merci, je vous rappelle</button><button type="button" class="puce" aria-pressed="false">Proposer un rendez-vous</button><button type="button" class="puce" aria-pressed="false">Envoyer la plaquette</button></div>'
           '%s<div class="ligne-champs">%s</div><div class="bloc-pied">%s</div></div>' % (
               ic('repondre'), champ('Votre réponse', 'rep-txt', 'textarea', 'Bonjour Paul, avec plaisir. Je vous appelle jeudi à 10 h. Will'),
               champ('Attribuer à', 'rep-qui', 'select', ['Moi (Will)', 'Sophie Renard', 'Karim Saidi']),
               btn('Envoyer la réponse', 'contour', icone='envoi', attrs='data-toast="Réponse envoyée depuis claire@prospection-a.example (même fil)."')))
    msg = ('<article class="message" aria-label="Réponse de Paul Morin"><div class="message-tete">%s<div class="quoi"><h2>Paul Morin</h2><span class="petit">Boulangerie des Tilleuls · Organisateurs Rhône-Alpes</span></div>%s</div>%s'
           '<div class="suggestion"><div class="suggestion-tete">%s<span style="flex:1 1 140px">Suggestion</span>%s</div><ul class="effets"><li>%sTâche CRM : rappeler jeudi</li><li>%sRelances arrêtées</li><li>%sÉtape : Qualifié</li></ul>'
           '<div><button type="button" class="btn btn-plein" data-toast="Réponse traitée : tâche créée, relances arrêtées." data-annulable>%sAppliquer la suggestion</button></div></div>%s'
           '<div class="gestes" role="group" aria-label="Classer autrement">%s%s%s<button type="button" class="btn btn-danger" data-ouvre="fen-stop"><span class="touche">S</span>STOP</button></div></article>'
           % (initiales('Paul Morin', 'terracotta').replace('initiales ', 'initiales grand '), badge('vert', 'Intéressé', '●'), fil, ic('etincelle'), badge('violet', 'Sûre à 92 %', '✦'),
              ic('taches'), ic('pause'), ic('fleche'), ic('coche'), rep,
              *['<button type="button" class="btn btn-contour" data-toast="Classée." data-annulable><span class="touche">%s</span>%s</button>' % (k, l) for k, l in [('1', 'Pas intéressé'), ('2', 'Plus tard'), ('3', 'Absent')]]))
    haut = kpis(kpi('À traiter', '7', 'reponses', 'terracotta', 'la plus ancienne : hier'), kpi('Intéressées', '2', 'etincelle', 'vert', 'à rappeler'),
                kpi('STOP à confirmer', '1', 'interdit', 'rouge', 'Yves Roche'), kpi('À rattacher', '1', 'lien', 'violet', 'adresse inconnue', 'reponses-a-rattacher.html'))
    stop = fenetre('fen-stop', 'Enregistrer l’opposition ?', '<p style="margin-bottom:8px"><strong>Yves Roche</strong> ne recevra plus rien. Définitif. Visible aussi dans le CRM.</p><label class="case"><input type="checkbox"> Toute l’organisation (Atelier Bois &amp; Forme)</label>',
                   BOUTONS_FEN('Enregistrer l’opposition', 'Opposition enregistrée.', 'btn-danger-plein'))
    normal = haut + '<div class="reponses">%s%s</div>' % (file_, msg)
    P['reponses.html'] = page('reponses', 'Réponses', '<strong>7 réponses</strong> à traiter. Répondez sans quitter l’outil.', normal,
                              etat_vide('reponses', 'Aucune réponse à traiter', 'Tout est traité. Bravo !', ''), onglets_haut=ONG_REP('reponses.html'), apres=stop)


def _rattacher():
    prop = lignes(*[ligne(n, s, initiales(n, 'bleu'), btn('Rattacher', 'petit', attrs='data-toast="Réponse rattachée à %s."' % n)) for n, s in [
        ('Paul Morin', 'Boulangerie des Tilleuls · même domaine'), ('Julie Morin', 'Boulangerie des Tilleuls · même nom de famille'), ('Boulangerie des Tilleuls', 'Fiche entreprise · adresse générique')]])
    normal = ('<article class="message"><div class="message-tete">%s<div class="quoi"><h2>p.morin@boulangerie-tilleuls.example</h2><span class="petit">Adresse inconnue · hier 18:02</span></div>%s</div>'
              '<blockquote>Je réponds depuis mon autre adresse : je suis partant pour jeudi.</blockquote></article>' % (initiales('p m', 'violet'), badge('violet', 'À rattacher', '✦'))
              + bloc('3 fiches proposées', prop, 'violet', 'lien', mot='Choisir', pied=btn('Créer une nouvelle fiche dans le CRM', 'petit', icone='ajout-personne')))
    P['reponses-a-rattacher.html'] = page('reponses-a-rattacher', 'Réponse à rattacher', 'Une adresse inconnue · <strong>3 fiches proposées</strong>', normal,
                                          onglets_haut=ONG_REP('reponses-a-rattacher.html'), menu='reponses')


# ======================= INFRASTRUCTURE =======================
BOITES = [('claire@prospection-a.example', 'vert', 'Prête', 40, 40, 32, '0,6 %', '4 réponses'), ('sophie@prospection-a.example', 'vert', 'Prête', 40, 40, 28, '0,4 %', '2 réponses'),
          ('will@prospection-b.example', 'ambre', 'Ralentie', 20, 40, 12, '3 % temp.', '1 réponse'), ('paul@prospection-c.example', 'bleu', 'En chauffe', 10, 10, 8, '0 %', '—')]


def _boites():
    feux = '<div class="feux">%s</div>' % ''.join(tuile_feu(a, e, s, chiffres([('%d/%d' % (f, q), 'envoyés'), (r, 'refus')]) + jauge('Quota', f, q, e if e != 'bleu' else 'bleu', '%d / %d' % (f, q)), 'boite.html') for a, e, s, q, mx, f, r, rp in BOITES)
    haut = kpis(kpi('Boîtes', '4', 'boite', 'bleu', '3 domaines'), kpi('Prêtes', '2', 'coche', 'vert', ''), kpi('Ralentie', '1', 'alerte', 'ambre', 'will@ · ÷ 2'), kpi('En chauffe', '1', 'chauffe', 'bleu', 'jour 6 sur 30', 'chauffe.html'))
    ajout = fenetre('fen-boite', 'Ajouter une boîte d’envoi', champ('Adresse', 'bo-adr', 'email', 'hugo@prospection-c.example') + champ('Domaine', 'bo-dom', 'select', ['prospection-c.example', 'prospection-a.example']) + champ('Nom affiché', 'bo-nom', valeur='Hugo · Axion-IA')
                    + '<div class="bandeau vert" style="margin:0">%s<span>Test de connexion réussi (envoi et réception).</span></div>' % ic('coche'), BOUTONS_FEN('Ajouter (chauffe 30 jours)', 'Boîte ajoutée : chauffe lancée.'))
    normal = haut + feux
    P['boites.html'] = page('boites', 'Boîtes d’envoi', '<strong>4 boîtes</strong> · 2 prêtes, 1 ralentie, 1 en chauffe.', normal,
                            etat_vide('boite', 'Aucune boîte d’envoi', 'Ajoutez d’abord un domaine, puis une boîte.', btn('Ajouter une boîte', 'plein', icone='plus', attrs='data-ouvre="fen-boite"')),
                            actions=btn('Ajouter une boîte', 'plein', icone='plus', attrs='data-ouvre="fen-boite"'), apres=ajout)


def _boite():
    haut = kpis(kpi('Envoyés (30 j)', '1 120', 'envoi', 'bleu', ''), kpi('Refusés', '1,9 %', 'interdit', 'ambre', 'limite 2 %'), kpi('Réponses', '41', 'reponses', 'vert', '12 intéressées'), kpi('Quota du jour', '20', 'boite', 'ambre', 'ralenti ÷ 2', unite='/ 40'))
    courbe_ = bloc('30 derniers jours', courbe([30, 32, 35, 36, 38, 40, 40, 0, 0, 40, 40, 40, 38, 40, 40, 0, 0, 40, 40, 40, 40, 40, 0, 0, 40, 36, 30, 20, 20, 20], ['2 oct.', '16 oct.', 'Aujourd’hui'], '', 'Envoyés par jour'), icone='stats')
    refus = bloc('Derniers refus (raison en clair)', tableau('Refus', ['Quand', 'Destinataire', 'Raison'], [
        ['Aujourd’hui 09:30', 'contact@atelier-x.example', 'Boîte pleine, on réessaie (452)'], ['Aujourd’hui 09:28', 'info@grossiste-y.example', 'Trop d’envois vers ce serveur : ralentir (421)'],
        ['Hier 15:02', 'yves@bois-forme.example', 'Adresse inexistante (550)']]), 'ambre', 'interdit', mot='3 aujourd’hui')
    chauffe_ = bloc('Chauffe', jauge('Montée', 30, 30, 'vert', 'terminée le 12 oct.') + chiffres([('40', 'plafond'), ('÷ 2', 'depuis 09:30')]), 'vert', 'chauffe', mot='Faite')
    normal = (verdict_global('Boîte ralentie', 'Refus temporaires à 3 % depuis 09:30 : volume divisé par 2, seul.', 'ambre', 'alerte', badge('ambre', 'Attention', '▲'))
              + haut + '<div class="grille deux-un">%s<div class="pile">%s</div></div>' % (courbe_, chauffe_) + refus)
    P['boite.html'] = page('boite', 'will@prospection-b.example', 'Domaine <a href="domaine.html">prospection-b.example</a> · ' + badge('ambre', 'Ralentie', '▲'), normal,
                           actions=btn('Mettre en pause', 'contour', icone='pause', attrs='data-toast="Boîte en pause."') + btn('Voir les campagnes', 'contour', 'campagnes.html', 'envoi'),
                           fil=[('Boîtes d’envoi', 'boites.html', 'boites')])


DOMS = [('prospection-a.example', 'vert', '2 boîtes', 'quarantaine', 'Propre'), ('prospection-b.example', 'ambre', '1 boîte', 'aucune', '1 liste'), ('prospection-c.example', 'bleu', 'jour 6 sur 30', 'aucune', 'Propre')]


def _domaines():
    feux = '<div class="feux">%s</div>' % ''.join(tuile_feu(d, e, s, chiffres([('5/5', 'DNS'), (dm, 'DMARC'), (ln, 'listes noires')]), 'domaine.html') for d, e, s, dm, ln in DOMS)
    haut = kpis(kpi('Domaines', '3', 'domaine', 'bleu', ''), kpi('DNS au vert', '3', 'coche', 'vert', 'sur 3'), kpi('DMARC à durcir', '2', 'etincelle', 'violet', 'prochain : 15 nov.'), kpi('Listé', '1', 'alerte', 'ambre', 'prospection-b.example', 'domaine.html'))
    assist = fenetre('fen-domaine', 'Ajouter un domaine', champ('Domaine', 'dn-nom', valeur='prospection-d.example') + '<p class="lib">Enregistrements à créer</p>' + ''.join('<p><span class="code-dns">%s</span></p>' % x for x in ['TXT  v=spf1 include:envoi.example -all', 'CNAME  dkim1._domainkey → dkim.envoi.example', 'TXT  _dmarc  v=DMARC1; p=none; rua=…']),
                     BOUTONS_FEN('Vérifier les DNS', '5 enregistrements sur 5 trouvés.'))
    normal = haut + feux
    P['domaines.html'] = page('domaines', 'Domaines', '<strong>3 domaines</strong> · DNS au vert · 1 sur une liste noire.', normal,
                              etat_vide('domaine', 'Aucun domaine', 'Ajoutez un domaine d’envoi : l’assistant donne les DNS à copier.', btn('Ajouter un domaine', 'plein', icone='plus', attrs='data-ouvre="fen-domaine"')),
                              actions=btn('Qui envoie en votre nom ?', 'contour', icone='oeil', attrs='data-toast="Rapport DMARC : 2 sources connues, 0 inconnue."') + btn('Ajouter un domaine', 'plein', icone='plus', attrs='data-ouvre="fen-domaine"'),
                              apres=assist)


def _domaine():
    haut = kpis(kpi('Envoyés (30 j)', '1 960', 'envoi', 'bleu', ''), kpi('Refusés', '0,7 %', 'interdit', 'vert', 'limite 2 %'), kpi('Plaintes', '0', 'alerte', 'vert', 'limite 0,1 %'), kpi('Réputation', 'Bonne', 'bouclier', 'vert', 'tableaux des messageries'))
    hist = bloc('Historique 30 jours', courbe([50, 52, 60, 64, 70, 0, 0, 78, 80, 80, 80, 80, 0, 0, 80, 80, 80, 80, 80, 0, 0, 80, 80, 80, 80, 80, 0, 0, 78, 64], ['2 oct.', '16 oct.', 'Aujourd’hui'], '', 'Envoyés par jour')
                + chiffres([('0,7 %', 'refus moyen'), ('0', 'plainte'), ('81', 'réponses')]), icone='stats')
    dns = bloc('DNS', '<ul class="controles">%s</ul>' % ''.join('<li><span class="p" aria-hidden="true">%s</span>%s</li>' % (ic('coche'), x) for x in ['SPF', 'DKIM', 'DMARC', 'Retour (PTR)', 'MTA-STS et rapports TLS']), 'vert', 'coche', mot='5/5')
    dmarc = bloc('DMARC progressif', '<ol class="etapes-com"><li class="passe">Aucune (none)</li><li aria-current="step">Quarantaine</li><li>Rejet (reject)</li></ol><p style="margin-top:12px">Prochaine étape le <strong>15 nov.</strong> si aucun envoi inconnu.</p>',
                 'violet', 'etincelle', mot='Rappel', pied=btn('Passer à « rejet » maintenant', 'petit', attrs='data-toast="Rappel gardé : rien n’est changé sans vos DNS."'))
    ln = bloc('Listes noires', lignes(ligne('Liste A (grand public)', 'Propre · vérifié il y a 1 h', '', badge('vert', 'Propre', '✓')), ligne('Liste B (spécialisée)', 'Propre · vérifié il y a 1 h', '', badge('vert', 'Propre', '✓'))), 'vert', 'bouclier', mot='Propre')
    normal = haut + '<div class="grille deux-un">%s<div class="pile">%s%s</div></div>' % (hist, dns, dmarc) + ln
    P['domaine.html'] = page('domaine', 'prospection-a.example', feu('vert') + ' 2 boîtes · DNS 5/5 · <strong>DMARC en quarantaine</strong>', normal,
                             actions=btn('Vérifier les DNS', 'contour', icone='rafraichir', attrs='data-toast="5 enregistrements sur 5 trouvés."'), fil=[('Domaines', 'domaines.html', 'domaines')])


def _serveurs():
    haut = kpis(kpi('Serveur d’envoi', 'En ligne', 'serveur', 'vert', 'depuis 41 jours'), kpi('Adresses IP', '2', 'reseau', 'bleu', '1 en chauffe'), kpi('Test du matin', '4/4', 'test', 'vert', '07:05 · boîtes témoins'), kpi('Configuration', 'À jour', 'reglages', 'vert', 'version 14', 'configuration.html'))
    ips = tableau('Adresses IP', ['Adresse', 'Flux', 'Domaine', 'État', 'Volume du jour', ''], [
        ['<span class="mono">192.0.2.10</span>', 'Prospection', 'prospection-a.example', badge('vert', 'Prête', '✓'), '68', btn('Ouvrir', 'petit-discret', 'domaine.html')],
        ['<span class="mono">192.0.2.11</span>', 'Lettre', 'prospection-c.example', badge('bleu', 'En chauffe', '▶'), '8', btn('Ouvrir', 'petit-discret', 'chauffe.html')]], secondaires=(2,))
    temoins = bloc('Test du matin', chiffres([('07:05', 'heure'), ('4/4', 'témoins'), ('100 %', 'en réception')]) + mini_titre('7 derniers matins')
                   + points_serie([('Lun', '', 'coche'), ('Mar', '', 'coche'), ('Mer', 'ambre', 'alerte'), ('Jeu', '', 'coche'), ('Ven', '', 'coche'), ('Sam', '', 'coche'), ('Dim', '', 'coche')]), 'vert', 'test', mot='Réussi')
    flux = bloc('Flux séparés', lignes(ligne('Prospection', '192.0.2.10 · prospection-a/b', ic('envoi'), badge('vert', 'Isolé', '✓')), ligne('Lettre d’information', '192.0.2.11 · prospection-c', ic('message'), badge('vert', 'Isolé', '✓')),
                                       ligne('Codes de connexion', 'Serveur à part', ic('cle'), badge('vert', 'Isolé', '✓'))), icone='reseau')
    ajout = fenetre('ajout-ip', 'Ajouter une adresse IP', champ('Adresse IP', 'ip-adr', valeur='192.0.2.12') + champ('Flux', 'ip-flux', 'select', ['Prospection', 'Lettre d’information'])
                    + champ('Domaine', 'ip-dom', 'select', ['prospection-a.example', 'prospection-b.example', 'prospection-c.example'])
                    + '<div class="bandeau vert" style="margin:0">%s<span>Retour (PTR) trouvé · listes noires propres · chauffe de 30 jours prévue.</span></div>' % ic('coche'),
                    BOUTONS_FEN('Ajouter et appliquer', 'Adresse ajoutée et configuration appliquée (version 15).'))
    normal = haut + bloc('Adresses IP', ips, icone='reseau') + '<div class="grille deux">%s%s</div>' % (temoins, flux)
    P['serveurs.html'] = page('serveurs', 'Serveurs et adresses IP', feu('vert') + ' Serveur en ligne · <strong>2 adresses IP</strong>', normal,
                              actions=btn('Lancer le test', 'contour', icone='test', attrs='data-toast="Test lancé : résultat dans 2 min."') + btn('Ajouter une adresse IP', 'plein', icone='plus', attrs='data-ouvre="ajout-ip"'),
                              onglets_haut=ONG_SERV('serveurs.html'), apres=ajout)


def _configuration():
    diff = bloc('Version 15 prête', lignes(ligne('+ Adresse IP 192.0.2.12', 'Flux prospection · domaine prospection-b.example', ic('plus'), badge('vert', 'Ajout', '+')),
                                          ligne('~ Plafond de will@', '40 → 20 par jour (ralentie)', ic('rafraichir'), badge('ambre', 'Changement', '~'))), 'bleu', 'reglages', mot='Prête',
                pied=btn('Appliquer la version 15', 'plein', icone='coche', attrs='data-toast="Version 15 appliquée. Retour automatique si le test échoue."'))
    hist = bloc('Historique', tableau('Versions', ['Version', 'Quand', 'Par', 'Résultat'], [['14', '28 oct. 10:02', 'Will', badge('vert', 'Appliquée', '✓')], ['13', '20 oct. 09:40', 'Will', badge('gris', 'Remplacée', '○')], ['12', '12 oct. 16:10', 'Système', badge('ambre', 'Retour automatique', '▲')]]), icone='horloge')
    normal = verdict_global('Une version attend', 'Différences en clair ci-dessous. Retour automatique en cas d’échec.', 'ambre', 'reglages') + '<div class="grille deux">%s%s</div>' % (diff, hist)
    P['configuration.html'] = page('configuration', 'Configuration du serveur', 'Version 14 en service · <strong>version 15 prête</strong>', normal, onglets_haut=ONG_SERV('configuration.html'), menu='serveurs')


def _chauffe():
    haut = kpis(kpi('En chauffe', '1', 'chauffe', 'bleu', 'paul@prospection-c.example'), kpi('Jour', '6', 'calendrier', 'bleu', 'sur 30', graph=jauge('Montée', 6, 30, 'bleu', '20 %')), kpi('Volume du jour', '10', 'envoi', 'vert', 'prévu : 10'), kpi('Fin prévue', '25 nov.', 'horloge', 'violet', ''))
    c = bloc('Courbe de montée · paul@prospection-c.example', courbe([2, 4, 6, 8, 10, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40], ['Jour 1', 'Jour 10', 'Jour 30'], '', 'Plafond prévu par jour')
             + '<p class="petit" style="margin-top:8px">Texte équivalent : 2 messages le jour 1, puis +2 par jour ouvré, jusqu’à 40.</p>', icone='chauffe')
    t = tableau('Boîtes', ['Boîte', 'Jour', 'Plafond aujourd’hui', 'État'], [['<a href="boite.html">paul@prospection-c.example</a>', '6 / 30', '10', badge('bleu', 'En montée', '▶')], ['<a href="boite.html">claire@prospection-a.example</a>', 'Faite', '40', badge('vert', 'Prête', '✓')],
                                                                              ['<a href="boite.html">will@prospection-b.example</a>', 'Faite', '20 (÷ 2)', badge('ambre', 'Ralentie', '▲')]], liens=['boite.html'] * 3)
    normal = haut + c + bloc('Toutes les boîtes', t, icone='boite')
    P['chauffe.html'] = page('chauffe', 'Chauffe', 'Montée en douceur : <strong>1 boîte</strong> en chauffe, jour 6 sur 30.', normal)


def _sante():
    haut = kpis(kpi('Boîtes prêtes', '3', 'boite', 'vert', '', 'boites.html', unite='/ 4', graph=jauge('Prêtes', 3, 4, 'vert', '75 %')),
                kpi('Volume du jour', '120', 'envoi', 'bleu', '', unite='possibles', graph=jauge('Envoyés', 68, 120, 'bleu', '68 envoyés')),
                kpi('Adresses refusées', '0,8 %', 'interdit', 'vert', 'limite : 2 %', graph=jauge('Part de la limite', 8, 20, 'vert', '40 %')),
                kpi('Plaintes', '0 %', 'alerte', 'vert', 'limite : 0,1 %', graph=jauge('Part de la limite', 0, 10, 'vert', '0 %')))
    feux_ = '<div class="feux">%s</div>' % ''.join(tuile_feu(d, e, s, chiffres([('5/5', 'DNS'), (dm, 'DMARC')]), 'domaine.html') for d, e, s, dm, ln in DOMS)
    rythme = bloc('Rythme par messagerie', tableau('Rythme', ['Messagerie', 'Envoyés', 'Rythme', 'État'], [['Messagerie grand public A', '28', '10 / heure', badge('vert', 'Normal', '●')], ['Messagerie opérateur B', '22', '6 / heure', badge('vert', 'Normal', '●')],
                                                                                                        ['Messagerie pro C', '18', '3 / heure', badge('ambre', 'Freinée', '▲')]]), icone='sante')
    alerte_ = bloc('Une boîte ralentie', '<p style="font-weight:700;margin-bottom:12px;overflow-wrap:anywhere">will@prospection-b.example</p>' + chiffres([('3 %', 'refus temp.'), ('÷ 2', 'volume'), ('09:30', 'depuis')]),
                   'ambre', 'alerte', mot='Attention', pied=btn('Voir ce qui s’est passé', 'plein', 'boite.html', 'oeil'))
    arret_ = bloc('Arrêt d’urgence', chiffres([('2 clics', 'pour tout couper'), ('0', 'message perdu')]), 'rouge', 'arret', mot='Sécurité', pied='<button type="button" class="btn btn-danger" data-ouvre="fen-arret">%sTout arrêter</button>' % ic('arret'))
    normal = (verdict_global('Envois normaux', '3 boîtes prêtes · 1 ralentie · test du matin réussi', 'vert', 'coche', badge('vert', 'Vérifié il y a 3 min', '✓'))
              + haut + mini_titre('Feux par domaine') + feux_ + '<div class="grille deux" style="margin-top:24px">%s%s</div>' % (alerte_, rythme)
              + '<div class="grille deux">%s%s</div>' % (bloc('Envoyés sur 14 jours', courbe([40, 52, 60, 64, 70, 0, 0, 78, 84, 102, 110, 118, 96, 68], ['19 oct.', '26 oct.', 'Aujourd’hui'], '', 'Envoyés par jour'), icone='stats'), arret_))
    P['sante.html'] = page('sante', 'Santé des envois', '%s <strong>Tout va bien.</strong> Une boîte ralentie.' % feu('vert'), normal,
                           etat_vide('sante', 'Aucun envoi pour l’instant', 'Ajoutez un domaine pour commencer.', btn('Ajouter un domaine', 'plein', 'domaines.html', 'plus')),
                           etat_erreur('Chiffres illisibles. Par prudence, pas de vert.', 'État des envois inconnu'),
                           actions=btn('Lancer un test', 'contour', icone='test', attrs='data-toast="Test lancé : résultat dans 2 min."'), onglets_haut=ONG_SANTE('sante.html'))


def _chercher():
    form = ('<form class="barre-outils" onsubmit="return false" role="search"><label class="champ-recherche" for="ce-adr">%s<span class="visuellement-cache">Adresse e-mail</span>'
            '<input type="search" id="ce-adr" value="yves@bois-forme.example"></label>%s</form>' % (ic('chercher'), btn('Chercher', 'plein', icone='chercher', attrs='data-toast="3 messages trouvés."')))
    res = tableau('Messages', ['Quand', 'Campagne', 'Boîte', 'Réponse du serveur', 'En clair'], [
        ['30 oct. 09:12', 'Organisateurs Rhône-Alpes · message 1', 'claire@prospection-a.example', '<span class="mono">550 5.1.1</span>', badge('rouge', 'Adresse inexistante', '■')],
        ['30 oct. 09:12', '—', '—', '—', badge('gris', 'Adresse mise en liste de suppression', '○')],
        ['12 sept. 10:40', 'Clubs d’entreprises Savoie · message 1', 'sophie@prospection-a.example', '<span class="mono">250 2.0.0</span>', badge('vert', 'Accepté', '✓')]], secondaires=(2,))
    fiche = bloc('Yves Roche · Atelier Bois & Forme', '<p>Fiche CRM : <a href="contact.html">ouvrir</a> · peut-on lui écrire ? <strong>Non</strong> (adresse inexistante).</p>', 'rouge', 'personne', mot='Ne plus écrire')
    normal = form + fiche + bloc('3 messages pour cette adresse', res, icone='journal', pied=btn('Exporter', 'petit', icone='export', attrs='data-toast="Historique exporté (CSV)."'))
    P['chercher-envoi.html'] = page('chercher-envoi', 'Chercher un envoi', 'Une adresse → <strong>tous ses messages</strong> et la raison en clair.', normal, onglets_haut=ONG_SANTE('chercher-envoi.html'), menu='sante')


def _feu_vert():
    C = [('Domaines : DNS au vert', True), ('DMARC publié', True), ('Retour (PTR) des adresses IP', True), ('Boîtes témoins reçues', True), ('Test du matin réussi 7 jours', True), ('Chauffe terminée (1 boîte au moins)', True),
         ('Page de désinscription en ligne', True), ('En-tête de désinscription en un clic', True), ('Bloc d’information art. 14', True), ('Identité de l’expéditeur remplie', True), ('Alertes par e-mail testées', True),
         ('Sauvegarde vérifiée', True), ('Tout arrêter testé', True), ('Boucles de retour des messageries', False), ('Inscription aux tableaux des messageries', False)]
    liste = '<ul class="controles">%s</ul>' % ''.join('<li%s><span class="p" aria-hidden="true"%s>%s</span>%s</li>' % ('' if ok else ' style="background:var(--ambre-fond);border-color:var(--ambre-filet);color:var(--ambre-texte)"', '' if ok else ' style="background:var(--ambre-filet)"', ic('coche' if ok else 'alerte'), E(n)) for n, ok in C)
    normal = '<div class="grille deux-un">%s%s</div>' % (bloc('15 critères', liste, icone='bouclier'), bloc('Avant le premier envoi', anneau(13, 15, 'ambre', '13/15', 'Presque prêt', '2 inscriptions à faire'), 'ambre', 'fusee', mot='13 / 15',
                                                                                                           pied=btn('Faire les 2 inscriptions', 'plein', 'reglages-envoi.html', 'fleche')))
    P['feu-vert.html'] = page('feu-vert', 'Feu vert', '<strong>13 critères sur 15</strong> avant le premier envoi.', normal, onglets_haut=ONG_SANTE('feu-vert.html'), menu='sante')


def _desinscriptions():
    verif = bloc('Puis-je écrire à… ?', '<form id="form-verifier" class="barre-outils" style="margin:0"><label class="champ-recherche" for="adresse-verif">%s<span class="visuellement-cache">Adresse ou domaine</span><input type="search" id="adresse-verif" placeholder="adresse@exemple.example ou domaine"></label><button type="submit" class="btn btn-plein">Vérifier</button></form><div id="resultat-verif" aria-live="polite" style="margin-top:12px"></div>' % ic('chercher'),
                 'bleu', 'interdit', mot='Vérifier')
    haut = kpis(kpi('Oppositions', '146', 'interdit', 'gris', 'jamais effacées'), kpi('Ce mois', '6', 'calendrier', 'bleu', 'dont 4 par le lien'), kpi('Domaines entiers', '3', 'domaine', 'ambre', 'toute l’organisation'))
    t = tableau('Registre des oppositions', ['Adresse ou domaine', 'Quand', 'Comment', 'Portée'], [
        ['yves@bois-forme.example', '31 oct. 2026', 'Réponse « STOP »', 'Adresse'], ['garage-saules.example', '12 oct. 2026', 'Lien de désinscription', badge('ambre', 'Toute l’organisation', '▲')],
        ['contact@salon-x.example', '02 oct. 2026', 'Demande RGPD', 'Adresse']])
    normal = verif + haut + bloc('Registre des oppositions', t, icone='journal', pied=btn('Exporter le registre (preuve)', 'petit', icone='export', attrs='data-toast="Registre exporté : CSV horodaté et signé."'))
    P['desinscriptions.html'] = page('desinscriptions', 'Désinscriptions', '<strong>146 oppositions</strong>, jamais effacées. Partagées avec le CRM.', normal)


def _alertes():
    def al(titre, quoi, fait, faire, teinte, icone, mot):
        return bloc(titre, '<p><strong>Ce qui se passe :</strong> %s</p><p style="margin-top:6px"><strong>Ce que le système a fait :</strong> %s</p><p style="margin-top:6px"><strong>Que faire :</strong> %s</p>' % (quoi, fait, faire), teinte, icone, mot=mot)
    haut = kpis(kpi('En cours', '2', 'alerte', 'ambre', ''), kpi('Réglées (7 j)', '5', 'coche', 'vert', ''), kpi('Canaux', '2', 'cloche', 'bleu', 'console + e-mail'))
    normal = haut + '<div class="pile">%s%s%s</div>' % (
        al('Boîte « will@ » ralentie', 'refus temporaires à 3 % depuis 09:30.', 'volume divisé par 2.', 'rien si ça baisse ; sinon <a href="boite.html">ouvrir la boîte</a>.', 'ambre', 'alerte', 'Attention'),
        al('DMARC : passer à « quarantaine »', 'prospection-c.example est prêt.', 'rappel posé au 15 nov.', '<a href="domaine.html">ouvrir le domaine</a>.', 'violet', 'etincelle', 'Nouveau'),
        al('Test du matin réussi', '4 témoins sur 4 à 07:05.', 'rien.', 'rien.', 'vert', 'test', 'Fait'))
    P['alertes.html'] = page('alertes', 'Alertes d’envoi', '<strong>2 alertes</strong> en cours. Console et e-mail seulement.', normal,
                             actions=btn('Régler les alertes', 'contour', 'reglages-alertes.html', 'reglages'))


# ======================= RÉGLAGES D'ENVOI =======================
def _reglages_envoi():
    cartes = '<div class="reglages-liens">%s</div>' % ''.join('<a href="%s">%s<span><strong>%s</strong><small>%s</small></span></a>' % (h, ic(i), t, s) for h, i, t, s in [
        ('regles-prudence.html', 'bouclier', 'Règles de prudence et horaires', 'Seuils, fenêtre d’envoi'), ('identite.html', 'personne', 'Identité de l’expéditeur', 'Bloc d’information art. 14'),
        ('reglages-alertes.html', 'cloche', 'Alertes et avis', 'Console et e-mail'), ('serveurs.html', 'reseau', 'Flux séparés', 'Prospection, lettre, codes'), ('desinscriptions.html', 'interdit', 'Désinscriptions', 'Registre et preuve')])
    absence = bloc('Mode absence', interrupteur('Je pars du 23 au 27 déc.', 'Les campagnes se mettent en pause ; les réponses attendent.', 'absence', False), 'violet', 'calendrier', mot='Nouveau')
    boucles = bloc('Boucles de retour des messageries', lignes(ligne('Signal Spam', 'Inscrit', '', badge('vert', 'Fait', '✓')), ligne('Messagerie pro C', 'À faire au premier envoi', '', badge('terracotta', 'À faire', '●')),
                                                               ligne('Messagerie grand public A', 'À faire au premier envoi', '', badge('terracotta', 'À faire', '●'))), 'terracotta', 'reponses', mot='2 à faire')
    normal = cartes + '<div class="grille deux" style="margin-top:24px">%s%s</div>' % (absence, boucles)
    P['reglages-envoi.html'] = page('reglages-envoi', 'Réglages d’envoi', 'Tout ce qui règle <strong>le produit Envoi</strong>, à part du CRM.', normal, onglets_haut=ONG_REG('reglages-envoi.html'))


def _regles():
    regles = bloc('Règles de prudence', lignes(*[ligne(t, s, ic('bouclier'), badge('vert', 'Active', '✓')) for t, s in [
        ('Si plus de 2 % d’adresses refusées : pause de la boîte', 'Seuil durcissable, jamais assoupli en V0'), ('Si une plainte sur 1 000 : pause de la campagne', ''), ('Si le test du matin échoue : rien ne part', '')]]), 'vert', 'bouclier', mot='3 actives')
    horaires = bloc('Fenêtre d’envoi', '<div class="ligne-champs">%s%s</div>' % (champ('De', 'h-de', 'time', '09:00'), champ('À', 'h-a', 'time', '17:00')) + interrupteur('Jours ouvrés seulement', 'Pas de week-end ni de jour férié.', 'h-ouv'),
                    icone='horloge', pied=btn('Enregistrer', 'plein', icone='coche', attrs='data-toast="Réglages enregistrés."'))
    normal = '<div class="grille deux">%s%s</div>' % (regles, horaires)
    P['regles-prudence.html'] = page('regles-prudence', 'Règles et horaires', 'Des règles en phrases. <strong>Durcir seulement.</strong>', normal, onglets_haut=ONG_REG('regles-prudence.html'), menu='reglages-envoi')


def _identite():
    ident = bloc('Qui écrit', champ('Entité', 'id-ent', valeur='Axion-IA (société factice)') + champ('Adresse postale', 'id-adr', valeur='1 rue de l’Exemple, 69000 Lyon') + champ('Lien de rendez-vous', 'id-rdv', 'url', 'https://rdv.example/will'),
                 icone='personne', pied=btn('Enregistrer', 'plein', icone='coche', attrs='data-toast="Identité enregistrée."'))
    bloc14 = bloc('Bloc d’information (art. 14)', '<div class="apercu-mail"><p class="petit">Vous recevez ce message car votre adresse professionnelle est publique. Données : nom, adresse, entreprise. Source : annuaires publics. Se désinscrire en un clic.</p></div>', 'vert', 'bouclier', mot='Présent')
    normal = '<div class="grille deux">%s%s</div>' % (ident, bloc14)
    P['identite.html'] = page('identite', 'Identité de l’expéditeur', 'Ce qui figure <strong>sous chaque message</strong>.', normal, onglets_haut=ONG_REG('identite.html'), menu='reglages-envoi')


def _reglages_alertes():
    t = tableau('Alertes', ['Alerte', 'Console', 'E-mail'], [[a, badge('vert', 'Oui', '✓'), badge('vert' if e else 'gris', 'Oui' if e else 'Non', '✓' if e else '○')] for a, e in
                                                              [('Boîte ralentie', True), ('Test du matin échoué', True), ('Domaine sur une liste noire', True), ('Réponse intéressée', False), ('Rappel DMARC', False)]])
    normal = '<div class="grille deux-un">%s%s</div>' % (bloc('Type × canal', t, icone='cloche'), bloc('Alerte de test', champ('Seconde adresse', 'ra-2', 'email', 'secours@axion-ia.example'), 'bleu', 'test', mot='Essai',
                                                                                                      pied=btn('Envoyer une alerte de test', 'plein', icone='envoi', attrs='data-toast="Alerte de test envoyée (console + e-mail)."')))
    P['reglages-alertes.html'] = page('reglages-alertes', 'Alertes et avis', 'Console et e-mail <strong>seulement</strong>.', normal, onglets_haut=ONG_REG('reglages-alertes.html'), menu='reglages-envoi')


def _publique():
    contenu = ('<div class="carte-seule" style="text-align:center"><p class="petit">Message de la part de <strong>Axion-IA</strong></p><h1 style="margin:10px 0">Se désinscrire</h1>'
               '<p style="margin-bottom:14px">p***@boulangerie-tilleuls.example ne recevra plus rien de notre part.</p><label class="case" style="justify-content:center"><input type="checkbox"> Toute mon organisation</label>'
               '<button type="button" class="btn btn-plein large" data-toast="C’est fait. Vous ne recevrez plus rien.">Confirmer la désinscription</button><p class="petit" style="margin-top:12px">Un clic suffit. Aucune connexion demandée.</p></div>')
    P['desinscription-publique.html'] = ecran_seul('Se désinscrire', contenu, cle='desinscription-publique', produit='envoi')


for _f in (_campagnes, _nouvelle, _suivi, _resultats, _messages_types, _editeur, _calendrier, _reponses, _rattacher, _boites, _boite, _domaines, _domaine, _serveurs,
           _configuration, _chauffe, _sante, _chercher, _feu_vert, _desinscriptions, _alertes, _reglages_envoi, _regles, _identite, _reglages_alertes, _publique):
    _f()
