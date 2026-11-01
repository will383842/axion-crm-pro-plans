# -*- coding: utf-8 -*-
"""Réglages, sécurité, données, technique, connexion, écrans V1. Données factices."""
from socle import *  # noqa: F401,F403

P = {}
FIL = [('Réglages', 'reglages.html', 'reglages')]


def _hub():
    def g(titre, liens):
        return '<h2 class="mini-titre">%s</h2><div class="reglages-liens">%s</div>' % (titre, ''.join(
            '<a href="%s">%s<span><strong>%s</strong>%s<small>%s</small></span></a>' % (h, ic(i), t, ('<span class="repere-v1">%s</span>' % v) if v else '', s) for h, i, t, s, v in liens))
    normal = (g('Mon compte', [('compte.html', 'personne', 'Mon compte et sécurité', 'Codes de secours, appareils', ''), ('reglages-alertes.html', 'cloche', 'Alertes et avis', 'Console et e-mail', '')])
              + g('Envois', [('regles-prudence.html', 'bouclier', 'Règles de prudence', 'Seuils, horaires, pression', ''), ('identite.html', 'entreprise', 'Identité de l’expéditeur', 'Raison sociale, bloc d’information', ''), ('regles-prudence.html#automatismes', 'horloge', 'Automatismes', 'Interrupteurs', '')])
              + g('Équipe et traces', [('equipe.html', 'equipe', 'Équipe et rôles', '3 personnes', ''), ('journal.html', 'journal', 'Journal', 'Qui a fait quoi', '')])
              + g('Données', [('rgpd.html', 'bouclier', 'Demandes RGPD', '1 à traiter', ''), ('sauvegardes.html', 'sauvegarde', 'Sauvegardes', 'Cette nuit 03:00', ''), ('collectes.html', 'collecte', 'Collectes de données', 'Alimenter la base', ''), ('listes.html#etiquettes', 'etiquette', 'Étiquettes', '4 étiquettes', ''), ('v1-ecrans.html#exports', 'export', 'Exports', 'Réversibilité', 'V1')])
              + g('Technique', [('configuration.html', 'outil', 'Configuration technique', 'Version 8 prête', ''), ('technique.html', 'serveur', 'Outils techniques', 'IA, relais, santé', ''), ('v1-ecrans.html#mises-a-jour', 'rafraichir', 'Mises à jour', 'Par vagues', 'V1'), ('v1-ecrans.html#api', 'cle', 'Accès API', 'Clés par espace', 'V1')])
              + g('Clients (console)', [('v1-ecrans.html#clients', 'equipe', 'Clients', 'Tous les espaces', 'V1'), ('v1-ecrans.html#synchro', 'rafraichir', 'Synchro console', 'Envois bloqués', 'V1'), ('v1-ecrans.html#usage', 'stats', 'Usage', 'Compteurs du mois', 'V1')]))
    P['reglages.html'] = page('reglages', 'Réglages', 'Tout ce qui se règle une fois. <strong>1 point</strong> demande votre attention : une demande RGPD.', normal)


def _compte():
    normal = ('<div class="grille deux">'
              + bloc('Mon profil', champ('Nom', 'c-nom', valeur='Will') + champ('E-mail de connexion', 'c-mail', 'email', 'will@axion.example', aide='Changement validé par un code envoyé à l’ancienne adresse.'))
              + bloc('Codes de secours', '<p><strong>7 codes restants</strong> sur 10.</p><p class="petit" style="margin-top:6px">À utiliser si vous n’avez plus accès à votre e-mail.</p>', 'vert', 'cle', mot='En règle', pied='<button type="button" class="btn btn-plein" data-toast="Code e-mail demandé, puis 10 nouveaux codes affichés une seule fois.">Régénérer les codes</button>')
              + '</div>'
              + bloc('Appareils de confiance (30 jours)', tableau('Appareils', ['Appareil', 'Ville approximative', 'Dernière utilisation', ''], [
                  ['<strong>Ordinateur · navigateur</strong><span class="sous">Cet appareil</span>', 'Lyon', 'maintenant', ''],
                  ['<strong>Téléphone · navigateur</strong>', 'Lyon', 'hier', btn('Retirer', 'petit', attrs='data-toast="Appareil retiré." data-annulable')]]))
              + bloc('Confort', interrupteur('Raccourcis clavier', 'G puis A, R, C… et / pour chercher', 'rac', True) + interrupteur('Densité compacte', 'Lignes plus serrées dans les tableaux', 'dens', False)))
    P['compte.html'] = page('compte', 'Mon compte', 'Session de 12 h. Code par e-mail actif. <strong>2 appareils</strong> de confiance.', normal, fil=FIL)


def _alertes_reglages():
    lignes = [['<strong>%s</strong>' % t, '<input type="checkbox" checked aria-label="%s : console" style="width:20px;height:20px">' % t,
               '<input type="checkbox"%s aria-label="%s : e-mail" style="width:20px;height:20px">' % (' checked' if e else '', t), q] for t, e, q in [
        ('Alerte rouge', True, 'Immédiat'), ('Alerte ambre', True, 'Regroupé (15 min)'), ('Réponse intéressée', True, 'Regroupé (15 min)'),
        ('Réponse en attente plus de 24 h', True, 'Récapitulatif du matin'), ('Campagne à valider', False, 'Récapitulatif du matin'), ('Sauvegarde', False, 'Seulement si échec'), ('Synchro avec la console', False, 'Seulement si échec')]]
    normal = (tableau('Alertes par type et par canal', ['Type', 'Console', 'E-mail', 'Rythme'], lignes)
              + bloc('Adresses de réception', champ('Adresse principale', 'al-1', 'email', 'will@axion.example') + champ('Seconde adresse (hors domaine Axion)', 'al-2', 'email', 'secours@perso.example', aide='Reçoit les alertes rouges si l’adresse principale ne répond plus.'), pied=btn('M’envoyer une alerte de test', 'petit', icone='test', attrs='data-toast="Alerte de test envoyée : console et e-mail."'))
              + '<p class="petit" style="margin-top:12px">Deux canaux seulement : la console et l’e-mail. Jamais de téléphone ni de messagerie instantanée.</p>')
    P['reglages-alertes.html'] = page('reglages-alertes', 'Alertes et avis', 'Où et quand vous êtes prévenu. <strong>Console + e-mail</strong>, rien d’autre.', normal,
                                      actions=btn('Enregistrer', 'plein', attrs='data-toast="Réglages enregistrés."'), fil=FIL)


def _prudence():
    regle = lambda txt, sous: '<li><span class="quoi"><strong>%s</strong><small>%s</small></span>%s</li>' % (txt, sous, btn('Durcir', 'petit', attrs='data-toast="Fenêtre de réglage ouverte (seulement vers plus de prudence)."'))
    regles = (bloc('Règles en phrases', '<ul class="liste">%s%s%s%s%s</ul>' % (
        regle('Ralentir une boîte si les adresses refusées dépassent <b>2 %</b>', 'Sur les 100 derniers envois'),
        regle('Arrêter une boîte si les plaintes dépassent <b>0,1 %</b>', 'Arrêt immédiat + alerte rouge'),
        regle('Freiner les premiers messages si <b>15</b> réponses attendent', 'Le frein humain protège votre capacité à répondre'),
        regle('Au plus <b>150</b> envois par boîte et par jour', 'Après la montée en douceur'),
        regle('Au plus <b>2</b> domaines par adresse IP', 'Et une nouvelle ressource tous les 15 jours ouvrés')), 'gris', 'bouclier', mot='En V0 : durcir seulement')
              + '<p class="petit" style="margin-top:12px">En V0, une règle ne peut que devenir plus prudente. Chaque changement est écrit au journal.</p>')
    horaires = bloc('Horaires et pression', '<div class="ligne-champs">' + champ('Fenêtre d’envoi', 'h-fen', 'select', ['09:00 – 17:00', '10:00 – 16:00']) + champ('Jours', 'h-j', 'select', ['Jours ouvrés, fériés exclus', 'Lundi à jeudi']) + '</div>'
                    + '<p>Au plus <strong>1 message tous les 5 jours ouvrés</strong> par personne, et <strong>3 par organisation</strong> sur 30 jours.</p>')
    auto = bloc('Automatismes', interrupteur('Relève des boîtes', 'Toutes les 5 min · dernier passage 11:40', 'a1') + interrupteur('Construction des vagues', 'Chaque heure · dernier passage 11:00', 'a2')
                + interrupteur('Vérification planifiée des adresses', 'Chaque nuit · dernier passage 02:00', 'a3') + interrupteur('Rapport du matin par e-mail', 'Chaque jour 08:00', 'a4'))
    normal = onglets('Règles', [('prudence', 'Règles de prudence', regles), ('horaires', 'Horaires et pression', horaires), ('automatismes', 'Automatismes', auto)])
    P['regles-prudence.html'] = page('regles-prudence', 'Règles de prudence', 'Les garde-fous qui protègent vos domaines. <strong>5 règles</strong> actives.', normal,
                                     actions=btn('Enregistrer', 'plein', attrs='data-toast="Code e-mail demandé, puis règles enregistrées."'), fil=FIL)


def _identite():
    normal = ('<div class="grille deux">'
              + bloc('Entité qui écrit', '<div class="ligne-champs">' + champ('Raison sociale', 'i-rs', valeur='Axion-IA (SAS)') + champ('SIREN', 'i-siren', valeur='000 000 000 (factice)') + '</div>'
                     + champ('Adresse', 'i-adr', valeur='1 rue de l’Exemple, 00000 Ville') + champ('Contact RGPD', 'i-rgpd', 'email', 'rgpd@axion.example') + champ('Lien de rendez-vous', 'i-rdv', 'url', 'https://rdv.exemple.example/will', aide='Utilisé par le champ {lien_rdv} des messages.'))
              + bloc('Bloc d’information (art. 14)', champ('Texte ajouté à chaque premier message', 'i-bloc', 'textarea', 'Vous recevez ce message car votre organisation est publiquement référencée. Données conservées 3 ans sans échange. Pour ne plus rien recevoir : lien en un clic ou réponse « STOP ».')
                     + '<p class="petit">Aperçu tel qu’il part : sous la signature, en petit, sans lien vers le site d’Axion.</p>', 'bleu', 'bouclier', mot='Obligatoire')
              + '</div>')
    P['identite.html'] = page('identite', 'Identité de l’expéditeur', 'Qui écrit, et ce que la loi demande d’afficher. <strong>Complète.</strong>', normal,
                              actions=btn('Enregistrer l’identité', 'plein', attrs='data-toast="Identité enregistrée."'), fil=FIL)


def _equipe():
    lignes = [['<strong>%s</strong><span class="sous">%s</span>' % (n, m), badge(*r), c, feu('vert', 'Actif') if a else badge('gris', 'Invitée', '○'), e, btn('Changer le rôle', 'petit-discret', attrs='data-toast="Code e-mail demandé."')] for n, m, r, c, a, e in [
        ('Will', 'will@axion.example', ('violet', 'Propriétaire', '★'), 'maintenant', True, feu('vert', 'Actif')),
        ('Claire Roux', 'claire@axion.example', ('bleu', 'Envois', '◆'), 'hier', True, feu('vert', 'Actif')),
        ('Léa Bernard', 'lea@axion.example', ('gris', 'Commercial', '◆'), '—', False, badge('gris', 'En attente', '○'))]]
    roles = '<ul class="liste"><li>%s<span class="quoi">Tout, y compris valider les envois et les règles</span></li><li>%s<span class="quoi">Campagnes, boîtes, « Tout arrêter »</span></li><li>%s<span class="quoi">Contacts, réponses, tâches · pas de validation</span></li><li>%s<span class="quoi">Lecture seule</span></li></ul>' % (
        badge('violet', 'Propriétaire', '★'), badge('bleu', 'Envois', '◆'), badge('gris', 'Commercial', '◆'), badge('gris', 'Lecteur', '○'))
    normal = tableau('Équipe', ['Personne', 'Rôle', 'Dernière connexion', 'État', 'Code par e-mail', ''], lignes) + bloc('Ce que permet chaque rôle', roles, 'gris', 'bouclier', mot='Info')
    inv = fenetre('fen-inviter', 'Inviter une personne', champ('E-mail', 'inv-mail', 'email') + champ('Rôle', 'inv-role', 'select', ['Commercial', 'Envois', 'Lecteur']) + '<p class="petit">Un propriétaire ne peut être nommé que par un propriétaire.</p>',
                  '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Invitation envoyée.">Envoyer l’invitation</button>')
    P['equipe.html'] = page('equipe', 'Équipe et rôles', '<strong>3 personnes</strong> · 1 invitation en attente. Personne n’est jamais supprimé : on désactive.', normal,
                            etat_vide('equipe', 'Vous êtes seul', 'Invitez une personne pour partager le travail.', btn('Inviter une personne', 'plein', attrs='data-ouvre="fen-inviter"')),
                            actions=btn('Inviter une personne', 'plein', icone='plus', attrs='data-ouvre="fen-inviter"'), fil=FIL, apres=inv)


def _journal():
    lignes = [[q, '<strong>%s</strong>' % a, o, badge(t, k, '●'), btn('Détail', 'petit-discret', attrs='data-toast="Détail affiché (avant / après)."')] for q, a, o, t, k in [
        ('11:42 · Will', 'A validé la campagne « Fédérations T1 »', 'Campagnes', 'bleu', 'Envoi'),
        ('10:05 · Claire Roux', 'A enregistré une opposition', 'Louis Bernard', 'terracotta', 'Opposition'),
        ('09:42 · Système', 'A ralenti une boîte', 'will@prospection-b.example', 'ambre', 'Pilotage'),
        ('08:01 · Will', 'S’est connecté', 'Ordinateur · Lyon', 'gris', 'Accès')]]
    normal = filtres(['Tout', 'Envois', 'Campagnes', 'Oppositions', 'Accès', 'Lectures', 'Réglages'], unique=False) + tableau('Journal', ['Quand · qui', 'Quoi', 'Sur', 'Sorte', ''], lignes)
    P['journal.html'] = page('journal', 'Journal', 'Chaque geste important est écrit ici, sans e-mail en clair. <strong>184 lignes</strong> aujourd’hui.', normal,
                             etat_vide('journal', 'Rien sur cette période', 'Élargissez la période ou retirez un filtre.', btn('Voir les 30 derniers jours', 'plein', attrs='data-toast="Période élargie."')),
                             actions=btn('Exporter le journal', 'contour', icone='export', attrs='data-toast="Code e-mail demandé, puis export prêt."'), fil=FIL)


def _sauvegardes():
    normal = (tuiles([('Dernière sauvegarde', '03:00', 'cette nuit'), ('Copie hors site', 'Faite', '03:20'), ('Place utilisée', '3,1 Go', 'sur 9 Go'), ('Dernier essai', '18 oct.', 'restauré en 14 min')])
              + tableau('Historique', ['Date', 'Sauvegarde', 'Copie hors site', 'Durée'], [['2 nov.', feu('vert', 'Faite'), feu('vert', 'Faite'), '6 min'], ['1er nov.', feu('vert', 'Faite'), feu('vert', 'Faite'), '6 min'], ['31 oct.', feu('vert', 'Faite'), feu('ambre', 'Refaite à 05:00'), '9 min']]))
    P['sauvegardes.html'] = page('sauvegardes', 'Sauvegardes', '%s Dernière sauvegarde cette nuit à 03:00. <strong>Copie hors site : faite.</strong>' % feu('vert'), normal,
                                 etat_vide('sauvegarde', 'Aucune sauvegarde encore', 'La première sauvegarde a lieu cette nuit à 03:00.', btn('Voir le réglage', 'plein', attrs='data-toast="Réglage affiché."')),
                                 actions=btn('Voir le dernier exercice', 'contour', attrs='data-toast="Exercice de restauration du 18 oct. : réussi en 14 min."'), fil=FIL)


def _rgpd():
    lignes = [['<strong>%s</strong>' % n, s, r, d, b] for n, s, r, d, b in [
        ('Demande d’accès', 'contact@exemple-asso.example', 'Reçue le 15 janv.', badge('terracotta', 'Avant le 14 févr.', '◷'), '<button type="button" class="btn btn-plein petit-btn" data-toast="Dossier préparé : données trouvées dans 3 tables.">Traiter la demande</button>'),
        ('Effacement', 'ancien@exemple.example', 'Reçue le 2 oct.', badge('vert', 'Faite', '✓'), btn('Voir', 'petit-discret'))]]
    normal = onglets('Conformité', [('demandes', 'Demandes', tableau('Demandes RGPD', ['Demande', 'Personne', 'Reçue', 'Délai', ''], lignes)),
                                    ('registre', 'Registre de l’IA', bloc('Registre de l’IA (existant)', '<p>2 usages déclarés : brouillon de message, tri des réponses. Aucune donnée client utilisée sans accord écrit.</p>', 'gris', 'journal', mot='Info')),
                                    ('traitements', 'Registre des traitements', '<p class="petit">Base légale par flux, sous-traitants, analyses d’intérêt légitime <span class="repere-v1">V1</span></p>')])
    P['rgpd.html'] = page('rgpd', 'Demandes RGPD', '<strong>1 demande</strong> à traiter avant le 14 févr. Effacement : l’empreinte d’opposition est gardée.', normal,
                          etat_vide('bouclier', 'Aucune demande', 'Les demandes d’accès, de rectification ou d’effacement arrivent ici.', btn('Enregistrer une demande', 'plein', attrs='data-toast="Fenêtre de demande ouverte."')),
                          fil=FIL)


def _configuration():
    normal = (bloc('Version 8 prête', '<ul class="liste"><li>%s<span class="quoi"><strong>+ domaine prospection-d.example</strong></span></li><li>%s<span class="quoi"><strong>~ plafond de will@prospection-b.example : 40 → 20</strong></span></li></ul><p class="petit" style="margin-top:8px">Le serveur tire la version signée, la teste à blanc, puis l’applique. En cas d’échec : retour automatique à la version 7.</p>'
                    % (badge('vert', 'Ajout', '+'), badge('ambre', 'Changement', '~')), 'bleu', 'outil', mot='Prête',
                    pied='<button type="button" class="btn btn-plein" data-toast="Code e-mail demandé, puis version 8 appliquée.">Appliquer la version 8</button>')
              + tableau('Versions', ['Version', 'Appliquée le', 'Par', 'Résultat'], [['v7', '28 oct. 10:12', 'Will', feu('vert', 'Appliquée')], ['v6', '20 oct. 09:40', 'Will', feu('vert', 'Appliquée')], ['v5', '15 oct. 16:05', 'Will', feu('ambre', 'Retour automatique')]])
              + '<p class="petit" style="margin-top:12px">Contrôle de dérive toutes les 5 min : aucun écart. Rien ne se règle par connexion directe au serveur.</p>')
    P['configuration.html'] = page('configuration', 'Configuration technique', 'Configuration <strong>v8 prête</strong> : 1 domaine ajouté, 1 plafond changé.', normal,
                                   etat_vide('outil', 'Aucun changement en attente', 'Le serveur applique la version 7. Tout est à jour.', btn('Voir les versions', 'plein', attrs='data-toast="Historique affiché."')),
                                   etat_erreur('La version 8 a échoué au test à blanc. Le serveur reste en version 7. Détail : plafond hors bornes.', 'Version refusée'), fil=FIL)


def _technique():
    ligne = lambda n, s, e: '<li>%s<span class="quoi"><strong>%s</strong><small>%s</small></span>%s</li>' % (ic('outil'), n, s, e)
    normal = (bloc('Écrans existants repris', '<ul class="liste">%s%s%s%s%s%s</ul>' % (
        ligne('Santé du système', 'Services, files, erreurs', feu('vert')), ligne('Moteurs d’IA', 'Fournisseurs et règles de choix', feu('vert')),
        ligne('Serveurs relais', 'Pour les collectes de données', feu('vert')), ligne('Rotation des accès', 'Dernière rotation : 20 oct.', feu('vert')),
        ligne('Entreprises en Roumanie', 'Consultation seulement', badge('gris', 'Lecture', '○')), ligne('Vérification des adresses', 'Fournisseur, coût affiché pour information', feu('vert')))))
    P['technique.html'] = page('technique', 'Outils techniques', 'Réservé au propriétaire. <strong>Tout est au vert.</strong>', normal, fil=FIL)


def _collectes():
    lignes = [['<strong>%s</strong>' % n, s, badge(*e), '<div class="barre-progression" role="progressbar" aria-label="Avancement %s" aria-valuenow="%d" aria-valuemin="0" aria-valuemax="100"><span style="width:%d%%"></span></div>' % (n, p, p), f, btn('Ouvrir', 'petit-discret')] for n, s, e, p, f in [
        ('Organisateurs d’événements · Rhône', 'Annuaire public', ('bleu', 'En cours', '▶'), 64, '412'), ('Clubs sportifs · Savoie', 'Annuaire public', ('vert', 'Terminée', '✓'), 100, '188'), ('Commerces · Lyon', 'Registre public', ('ambre', 'En pause', '❚❚'), 30, '96')]]
    normal = (tableau('Collectes', ['Collecte', 'Source', 'État', 'Avancement', 'Fiches trouvées', ''], lignes)
              + '<p class="petit" style="margin-top:12px">Ancien nom : « Campagnes » de collecte. Les liens anciens redirigent ici. L’historique est dans l’onglet suivant.</p>')
    P['collectes.html'] = page('collectes', 'Collectes de données', '<strong>1 collecte en cours</strong> · 696 fiches trouvées ce mois. Garde Sirene active.', normal,
                               etat_vide('collecte', 'Aucune collecte', 'Une collecte alimente la base à partir de sources publiques.', btn('Lancer une collecte', 'plein', attrs='data-toast="Assistant de collecte ouvert."')),
                               actions=btn('Lancer une collecte', 'plein', icone='plus', attrs='data-toast="Assistant de collecte ouvert."'), fil=FIL,
                               onglets_haut='<nav class="onglets" aria-label="Sections des collectes"><a href="collectes.html" aria-current="page">Collectes</a><a href="collectes.html#historique">Historique</a><a href="statistiques.html#carte">Carte de France</a></nav>')


def _v1():
    sec = lambda sid, titre, contenu: '<section id="%s" class="bloc" aria-labelledby="h-%s"><div class="bloc-tete"><h2 id="h-%s">%s</h2><span class="repere-v1">V1</span></div>%s</section>' % (sid, sid, sid, titre, contenu)
    normal = (bloc('Écrans de la phase V1 (console mutualisée)', '<p>Maquettes courtes. Elles seront détaillées avant le lot U13. Rien ici n’est en V0.</p>', 'violet', 'etincelle', mot='Plus tard')
              + sec('clients', 'Clients', tableau('Clients', ['Client', 'Repère', 'Version', 'Santé', 'Usage', ''], [
                  ['<strong>Axion-IA</strong>', '<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:#2346c8" role="img" aria-label="Repère bleu"></span>', 'v1.4', feu('vert'), '1 240 envois', ''],
                  ['<strong>Garage Durand (factice)</strong>', '<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:#b45309" role="img" aria-label="Repère ambre"></span>', 'v1.4', feu('vert'), '310 envois', btn('Demander un accès support', 'petit', attrs='data-toast="Accès support demandé : 2 h, tracé au journal."')]])
                    + '<p class="petit" style="margin-top:8px">Création d’un client en 3 étapes : identité, premier responsable, récapitulatif. Nom + couleur de repère, sans logo ni marque.</p>')
              + sec('synchro', 'Synchro console', '<p>%s 0 en attente · 0 abandonné · dernier passage 11:40.</p>' % feu('vert'))
              + sec('usage', 'Usage', '<p>Envois du mois : 1 240 / 3 000 (informatif, rien ne se bloque). Remise à zéro le 15 de chaque mois.</p>')
              + sec('exports', 'Exports', '<p>Sélection, liste, résultats de campagne, espace complet (réversibilité). Code e-mail redemandé.</p>')
              + sec('declenches', 'Messages déclenchés', '<p><strong>Quand</strong> [formulaire du site] <strong>envoyer</strong> [message type n° 3] <strong>après</strong> [10 minutes]. Pas de constructeur visuel.</p>')
              + sec('lettre', 'Lettre d’information', '<p>Abonnés consentants séparés de la prospection, double inscription, pages au nom légal du client.</p>')
              + sec('files', 'Files et sources', '<p>Messages en attente par client et par campagne ; état et âge de chaque source de mesure.</p>')
              + sec('mises-a-jour', 'Mises à jour', '<p>Version actuelle v1.4 · disponible v1.5 · vagues : Axion, pilote, tous · retour arrière.</p>')
              + sec('api', 'Accès API', '<p>Clés par espace, affichées une seule fois, révocables.</p>')
              + sec('champs', 'Champs personnalisés', '<p>Texte, liste ou date, utilisables dans le ciblage et les messages.</p>')
              + sec('taches-auto', 'Tâches automatiques', '<p>« Si pas de réponse 3 jours après le dernier message, créer une tâche « Appeler ». » Un interrupteur par règle.</p>')
              + sec('telephone', 'Appels', '<p>File d’appels, script validé, issues fermées, lien d’appel sans numérotation automatique.</p>')
              + sec('aide', 'Aide', '<p>Une page courte par entrée de menu, ouverte par « ? » au même endroit.</p>'))
    P['v1-ecrans.html'] = page('v1-ecrans', 'Écrans V1 et V2', 'Les écrans prévus après le premier envoi réel. <strong>13 écrans</strong> en aperçu.', normal, fil=FIL)


def _connexion():
    c = ('<div class="carte-seule"><div style="display:flex;align-items:center;gap:12px;margin-bottom:24px"><span class="barre-logo" aria-hidden="true">A</span><strong>Axion CRM Pro</strong></div>'
         '<section data-etat="normal" aria-label="Connexion"><div data-assistant><ol class="frise" aria-label="Étapes de connexion" hidden><li><button type="button" aria-current="step"><span class="n">1</span></button></li><li><button type="button"><span class="n">2</span></button></li></ol>'
         '<div data-etape="1"><h1 style="font-size:24px">Se connecter</h1><p class="petit" style="margin:6px 0 20px">Un code vous sera envoyé par e-mail.</p>'
         + champ('E-mail', 'cx-mail', 'email', 'will@axion.example', attrs='autocomplete="username"') + champ('Mot de passe', 'cx-mdp', 'password', 'motdepasse-factice', attrs='autocomplete="current-password"')
         + '<button type="button" class="btn btn-plein" style="width:100%%" data-aller="2">Se connecter</button><p style="margin-top:16px;text-align:center"><a href="#" data-toast="Lien de réinitialisation envoyé (vous serez prévenu par e-mail).">Mot de passe oublié</a></p></div>'
         '<div data-etape="2"><h2 style="font-size:24px">Code reçu par e-mail</h2><p class="petit" style="margin:6px 0 20px">Envoyé à w•••@axion.example. Valable 10 min.</p>'
         '<fieldset style="border:0;padding:0;margin:0 0 16px"><legend class="lib" style="font-weight:600;margin-bottom:8px">Code à 6 chiffres</legend><div class="cases-code">%s</div></fieldset>'
         '<label class="case"><input type="checkbox" checked> Faire confiance à cet appareil 30 jours</label>'
         '<a class="btn btn-plein" style="width:100%%" href="index.html">Valider le code</a><p style="margin-top:16px;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap"><a href="#" data-toast="Nouveau code envoyé.">Renvoyer le code</a><a href="#" data-toast="Saisissez un de vos codes de secours.">Utiliser un code de secours</a></p></div></div></section>'
         '<section data-etat="vide" hidden aria-label="Session expirée"><h1 style="font-size:24px">Session terminée</h1><p style="margin:8px 0 20px">Par sécurité, une session dure 12 h. Reconnectez-vous.</p><a class="btn btn-plein" style="width:100%%" href="connexion.html">Se reconnecter</a></section>'
         '<section data-etat="erreur" hidden role="alert"><h1 style="font-size:24px">Code incorrect</h1><p style="margin:8px 0 20px">Ce code ne fonctionne pas ou a expiré. Il vous reste 4 essais.</p><a class="btn btn-plein" style="width:100%%" href="connexion.html">Recevoir un nouveau code</a></section></div>'
         % ''.join('<input type="text" inputmode="numeric" maxlength="1" aria-label="Chiffre %d"%s>' % (i + 1, ' autocomplete="one-time-code"' if i == 0 else '') for i in range(6)))
    P['connexion.html'] = ecran_seul('Connexion', c)


def _introuvable():
    c = '<div class="carte-seule" style="text-align:center">%s<h1 style="margin:12px 0 8px">Page introuvable</h1><p class="petit" style="margin-bottom:20px">Le lien est peut-être ancien. Les anciennes pages redirigent vers les nouvelles.</p><a class="btn btn-plein" href="index.html">Retour à Aujourd’hui</a></div>' % ic('chercher', 'grande')
    P['introuvable.html'] = ecran_seul('Page introuvable', c, selecteur=False)


for f in (_hub, _compte, _alertes_reglages, _prudence, _identite, _equipe, _journal, _sauvegardes, _rgpd, _configuration, _technique, _collectes, _v1, _connexion, _introuvable):
    f()
