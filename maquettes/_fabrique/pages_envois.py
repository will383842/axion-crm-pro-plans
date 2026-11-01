# -*- coding: utf-8 -*-
"""Pages du groupe « Envois » et « Mesurer ». Données factices : domaines en .example, aucune IP réelle."""
from socle import *  # noqa: F401,F403

P = {}


def _boites():
    lignes = [['<strong>%s</strong><span class="sous">%s</span>' % (a, n), d, feu(e, m), '<span class="chiffre">%s</span>' % v, p, btn('Ouvrir', 'petit-discret', 'chauffe.html')] for a, n, d, e, m, v, p in [
        ('claire@prospection-a.example', 'Claire (équipe Axion)', 'prospection-a.example', 'vert', 'Bon', '24 / 40', 'Jour 30 · fini'),
        ('will@prospection-a.example', 'Will', 'prospection-a.example', 'vert', 'Bon', '24 / 40', 'Jour 30 · fini'),
        ('will@prospection-b.example', 'Will', 'prospection-b.example', 'ambre', 'Ralentie', '12 / 40', 'Jour 30 · fini'),
        ('paul@prospection-c.example', 'Paul (équipe Axion)', 'prospection-c.example', 'vert', 'En montée', '8 / 10', 'Jour 6 sur 30')]]
    normal = tableau('Boîtes d’envoi', ['Boîte', 'Domaine', 'État', 'Aujourd’hui', 'Montée en douceur', ''], lignes) + '<p class="petit" style="margin-top:12px">Plafond : 150 envois par boîte et par jour, atteint seulement après la montée en douceur.</p>'
    ajout = fenetre('fen-boite', 'Ajouter une boîte', champ('Prénom et nom', 'b-nom', valeur='') + champ('Adresse', 'b-adr', 'email', aide='Doit appartenir à un domaine prêt.') + champ('Signature', 'b-sig', 'textarea', aide='Sans numéro de téléphone.')
                    + champ('Mot de passe de relève', 'b-mdp', 'password', aide='Écrit une seule fois, jamais réaffiché.') + '<label class="case"><input type="checkbox"> La personne a donné son accord écrit pour envoyer à son nom.</label>',
                    '<button type="button" class="btn btn-contour" data-ferme>Annuler</button><button type="button" class="btn btn-plein" data-ferme data-toast="Connexion testée : boîte ajoutée, montée en douceur démarrée.">Tester et ajouter</button>')
    P['boites.html'] = page('boites', 'Boîtes d’envoi', '<strong>4 boîtes</strong> · 3 prêtes, 1 en montée en douceur · 68 envois sur 130 aujourd’hui.', normal,
                            etat_vide('boite', 'Aucune boîte d’envoi', 'Une boîte = une vraie personne, sur un domaine prêt. Elle commence doucement (20 par jour).', btn('Ajouter une boîte', 'plein', attrs='data-ouvre="fen-boite"')),
                            actions=btn('Ajouter une boîte', 'plein', icone='plus', attrs='data-ouvre="fen-boite"'), apres=ajout)


def _domaines():
    lignes = [['<strong>%s</strong>' % d, feu(e, m), a, x, '<span class="chiffre">%s</span>' % b, '<button type="button" class="btn btn-discret petit-btn" data-ouvre="tir-dmarc">Qui envoie en votre nom ?</button>'] for d, e, m, a, x, b in [
        ('prospection-a.example', 'vert', 'Prêt', '4 mois', '12 août 2027', '2'),
        ('prospection-b.example', 'ambre', 'Ralenti', '3 mois', '3 sept. 2027', '1'),
        ('prospection-c.example', 'vert', 'En montée', '27 jours', '6 oct. 2027', '1')]]
    dns = ''.join('<li>%s<span class="quoi"><strong>%s</strong><small><span class="code-dns">%s</span></small></span><button type="button" class="btn btn-discret petit-btn" aria-label="Copier la valeur de la ligne %d" data-toast="Valeur copiée.">Copier</button></li>' % (feu(e, m), n, v, i + 1) for i, (n, v, e, m) in enumerate([
        ('Autorisation (SPF)', 'v=spf1 include:envoi.prospection-d.example -all', 'vert', 'Trouvé'),
        ('Signature du domaine (DKIM)', 'k1._domainkey → clé publique (générée sur le serveur)', 'vert', 'Trouvé'),
        ('Politique anti-usurpation (DMARC)', 'v=DMARC1; p=none; rua=mailto:rapports@prospection-d.example', 'ambre', 'Vérification…'),
        ('Nom inverse (PTR)', 'Réglé par l’hébergeur du serveur', 'gris', 'En attente')]))
    assistant = tiroir('tir-dns', 'Ajouter un domaine : prospection-d.example', '<ol class="etapes-com" style="margin-bottom:16px"><li class="passe">1. Nom</li><li aria-current="step">2. Réglages</li><li>3. Vérification</li></ol><p class="petit" style="margin-bottom:8px">Copiez chaque ligne chez votre hébergeur. On revérifie toutes les 2 minutes.</p><ul class="liste">%s</ul>' % dns,
                       '<button type="button" class="btn btn-plein" data-ferme data-toast="Vérification relancée.">Vérifier maintenant</button>')
    dmarc = tiroir('tir-dmarc', 'Qui envoie en votre nom ?', '<ul class="liste"><li>%s<span class="quoi"><strong>Votre serveur d’envoi</strong><small>412 messages · signés</small></span></li><li>%s<span class="quoi"><strong>Hébergeur des boîtes</strong><small>38 messages · signés</small></span></li><li>%s<span class="quoi"><strong>Source inconnue</strong><small>12 messages depuis une adresse inconnue</small></span></li></ul><h3 class="mini-titre">Listes noires</h3><p>%s Aucune liste sur 8 contrôlées · 06:00</p>'
                   % (feu('vert', 'Autorisé'), feu('vert', 'Autorisé'), feu('ambre', 'Inconnu'), feu('vert', 'Propre')), btn('Revérifier maintenant', 'contour', attrs='data-toast="Contrôle des listes noires lancé."'))
    normal = tableau('Domaines d’envoi', ['Domaine', 'État', 'Âge', 'Expire le', 'Boîtes', ''], lignes) + '<p class="petit" style="margin-top:12px">Jamais le domaine principal d’Axion. Au plus 2 domaines par adresse IP. Un nouveau domaine au plus tous les 15 jours ouvrés.</p>'
    P['domaines.html'] = page('domaines', 'Domaines', '<strong>3 domaines</strong> d’envoi · 2 prêts, 1 en montée en douceur. Aucune expiration avant 9 mois.', normal,
                              etat_vide('domaine', 'Aucun domaine d’envoi', 'Un domaine séparé protège votre adresse principale. L’assistant vous guide en 10 minutes.', btn('Ajouter un domaine', 'plein', attrs='data-ouvre="tir-dns"')),
                              actions=btn('Ajouter un domaine', 'plein', icone='plus', attrs='data-ouvre="tir-dns"'), apres=assistant + dmarc)


def _serveurs():
    carte = bloc('Serveur d’envoi n° 1', '<dl class="infos"><dt>État</dt><dd>%s</dd><dt>Service d’envoi</dt><dd>%s</dd><dt>Liaison privée</dt><dd>%s</dd><dt>Disque</dt><dd>31 %%</dd><dt>Mémoire</dt><dd>44 %%</dd><dt>File d’attente</dt><dd>12 messages</dd><dt>Dernier envoi</dt><dd>11:42</dd></dl>' % (feu('vert', 'Sain'), feu('vert', 'Actif'), feu('vert', 'Active')), 'vert', 'serveur', mot='Sain')
    test = bloc('Test du matin · 07:05', tableau('Boîtes témoins', ['Témoin', 'Arrivée', 'Signature'], [
        ['Témoin 1 (messagerie grand public)', feu('vert', 'Réception'), feu('vert', 'OK')], ['Témoin 2 (messagerie grand public)', feu('vert', 'Réception'), feu('vert', 'OK')],
        ['Témoin 3 (messagerie pro)', feu('vert', 'Réception'), feu('vert', 'OK')], ['Témoin 4 (messagerie pro)', feu('vert', 'Réception'), feu('vert', 'OK')]]))
    ips = tableau('Adresses IP', ['Adresse', 'Nom inverse', 'Listes noires', 'Palier', 'Aujourd’hui', 'État'], [
        ['<strong>Adresse IP n° 1</strong><span class="sous">valeur masquée dans la maquette</span>', feu('vert', 'OK'), feu('vert', 'Aucune'), '3 sur 5', '<span class="chiffre">68 / 200</span>', feu('vert')]])
    normal = onglets('Serveurs', [('machines', 'Serveurs', '<div class="grille deux">%s%s</div>' % (carte, test)), ('ips', 'Adresses IP', ips + '<div class="bloc-pied">%s</div>' % btn('Ajouter une adresse IP', 'contour', icone='plus', attrs='data-toast="Assistant d’adresse IP ouvert."')),
                                  ('ajout', 'Ajouter un serveur', bloc('Un serveur demande à rejoindre', '<p>Empreinte affichée : <span class="code-dns">AX-7F3E-91C2 (factice)</span>. Comparez-la avec le guide d’installation.</p>', 'violet', 'serveur', mot='Nouveau', pied=btn('Accepter ce serveur', 'petit', attrs='data-toast="Code e-mail demandé, puis serveur accepté."')))])
    P['serveurs.html'] = page('serveurs', 'Serveurs', '%s Serveur d’envoi sain. Dernier envoi 11:42. <strong>Test du matin réussi.</strong>' % feu('vert'), normal,
                              etat_vide('serveur', 'Aucun serveur relié', 'Installez le serveur d’envoi avec le guide, puis acceptez-le ici.', btn('Ouvrir le guide d’installation', 'plein', attrs='data-toast="Guide ouvert."')),
                              etat_erreur('Le serveur ne répond plus depuis 10 min. Les envois sont en pause automatique. Un e-mail d’alerte est parti.', 'Serveur injoignable'),
                              actions=btn('Relancer le test du matin', 'plein', icone='rafraichir', attrs='data-toast="Test lancé : résultat dans 5 min."'), fil=[('Santé des envois', 'sante.html', 'serveurs')])


def _chauffe():
    courbe = ('<figure style="margin:0"><svg class="courbe" viewBox="0 0 600 140" role="img" aria-labelledby="ch-t"><title id="ch-t">Montée prévue de 20 à 150 messages par jour en 30 jours ouvrés</title>'
              '<polyline fill="none" stroke="#dde2ea" stroke-width="3" stroke-dasharray="6 6" points="0,125 100,115 200,95 300,75 400,50 500,30 600,15"/><polyline fill="none" stroke="#b45309" stroke-width="3" points="0,125 60,121 120,117"/>'
              '<circle cx="120" cy="117" r="5" fill="#b45309"/></svg><figcaption class="petit">Jour 6 : 10 messages (prévu : 12). Objectif : 150 par jour au jour 30. <a href="#" data-toast="Tableau ouvert.">Voir en tableau</a></figcaption></figure>')
    normal = (bloc('paul@prospection-c.example', courbe, 'bleu', 'chauffe', mot='En cours')
              + tableau('Montée par boîte', ['Boîte', 'Jour', 'Aujourd’hui', 'Demain', 'État'], [
                  ['<strong>paul@prospection-c.example</strong>', '6 sur 30', '10', '12', feu('vert', 'Normal')],
                  ['<strong>claire@prospection-a.example</strong>', 'Fini', '40', '40', feu('vert', 'Fini')],
                  ['<strong>will@prospection-b.example</strong>', 'Fini', '20 (ralenti)', '40 si tout va bien', feu('ambre', 'Ralenti')]])
              + '<p class="petit" style="margin-top:12px">Les jours sans envoi ne comptent pas. Un problème fait redescendre d’un palier, jamais monter plus vite.</p>')
    P['chauffe.html'] = page('chauffe', 'Montée en douceur', 'Une boîte neuve envoie peu au début, puis un peu plus chaque jour. <strong>1 boîte en montée</strong>, jour 6 sur 30.', normal,
                             etat_vide('chauffe', 'Aucune boîte en montée', 'Toutes vos boîtes ont fini leur montée en douceur.', btn('Ajouter une boîte', 'plein', 'boites.html')),
                             fil=[('Santé des envois', 'sante.html', 'chauffe')])


def _alertes():
    ligne = lambda t, s, titre, quoi, fait, quand: '<li>%s<span class="quoi"><strong>%s</strong><small>%s</small><small>Ce que le système a fait : %s</small></span><span class="petit">%s</span></li>' % (badge(t, s[0], s[1]), titre, quoi, fait, quand)
    normal = (filtres(['Toutes', 'En cours (1)', 'Non lues (3)', 'Résolues'])
              + bloc('En cours', '<ul class="liste">%s</ul>' % ligne('ambre', ('Attention', '▲'), 'Boîte will@prospection-b.example ralentie', 'Refus temporaires : 3 % (seuil 2 %).', 'volume divisé par deux.', '09:42'), 'ambre', 'alerte',
                     pied='<button type="button" class="btn btn-plein" data-ouvre="tir-alerte">Voir ce qui s’est passé</button>')
              + bloc('Aujourd’hui', '<ul class="liste">%s%s</ul>' % (ligne('vert', ('Résolue', '✓'), 'Test du matin réussi', '4 témoins sur 4.', 'rien.', '07:05'), ligne('gris', ('Info', '○'), 'Sauvegarde faite', 'Copie hors site faite.', 'rien.', '03:00'))))
    tir = tiroir('tir-alerte', 'Boîte will@prospection-b.example ralentie', '<ol class="chronologie"><li><span class="rond">%s</span><strong>09:30</strong> · 3 refus temporaires sur 100 chez une messagerie.</li><li><span class="rond">%s</span><strong>09:42</strong> · Seuil de 2 %% franchi : volume divisé par deux.</li><li><span class="rond">%s</span><strong>09:42</strong> · Alerte affichée dans la console et envoyée par e-mail.</li></ol><p class="petit">Que faire ? Rien si cela redescend avant demain. Sinon, mettez la boîte en pause.</p>' % (ic('alerte'), ic('pause'), ic('cloche')),
                 btn('Mettre la boîte en pause', 'danger', attrs='data-ferme data-toast="Boîte en pause."') + btn('Marquer comme lue', 'contour', attrs='data-ferme data-toast="Alerte marquée comme lue." data-annulable'))
    P['alertes.html'] = page('alertes', 'Alertes', '<strong>1 alerte en cours</strong>, 3 non lues. Alertes envoyées dans la console et par e-mail seulement.', normal,
                             etat_vide('cloche', 'Aucune alerte', 'Tout va bien. Les alertes arrivent ici et par e-mail.', btn('Régler les alertes', 'plein', 'reglages-alertes.html')),
                             actions=btn('Régler les alertes', 'contour', 'reglages-alertes.html', 'reglages'), apres=tir)


def _desinscriptions():
    verif = ('<form id="form-verifier" class="bloc" role="search" aria-label="Puis-je écrire à… ?"><h2 style="margin-bottom:12px">Puis-je écrire à… ?</h2><div style="display:flex;gap:8px;flex-wrap:wrap"><label class="visuellement-cache" for="adresse-verif">Adresse e-mail ou domaine</label>'
             '<input id="adresse-verif" type="text" placeholder="paul@boulangerie-martin.example" style="flex:1 1 240px"><button type="submit" class="btn btn-plein">Vérifier</button></div><div id="resultat-verif" aria-live="polite" style="margin-top:12px"></div></form>')
    lignes = tableau('Ne plus écrire', ['Adresse ou domaine', 'Raison', 'Depuis', 'Portée'], [
        ['<strong>paul@boulangerie-martin.example</strong>', 'Désinscription (lien)', '12 oct. 2026', 'Personne'],
        ['<strong>garage-durand.example</strong>', 'Opposition « toute l’organisation »', '2 oct. 2026', 'Organisation'],
        ['<strong>l.bernard@atelier-bernard.example</strong>', 'STOP dans une réponse', 'hier', 'Personne'],
        ['<strong>ancienne@exemple.example</strong>', 'Adresse refusée', '20 sept. 2026', 'Technique']])
    normal = verif + '<h2 class="mini-titre">Liste « Ne plus écrire » (412)</h2>' + filtres(['Toutes', 'Désinscriptions', 'Oppositions', 'Plaintes', 'Refusées']) + lignes + '<div class="bloc-pied">%s %s</div>' % (btn('Ajouter une opposition', 'contour', icone='plus', attrs='data-toast="Fenêtre d’opposition ouverte."'), btn('Voir la page de désinscription', 'discret', 'desinscription-publique.html'))
    P['desinscriptions.html'] = page('desinscriptions', 'Désinscriptions', '<strong>412 adresses</strong> à qui on n’écrit plus jamais. Rien n’est jamais retiré de cette liste.', normal,
                                     etat_vide('interdit', 'Aucune désinscription', 'Les désinscriptions, oppositions et plaintes s’ajoutent ici toutes seules.', btn('Ajouter une opposition', 'plein', attrs='data-toast="Fenêtre d’opposition ouverte."')),
                                     fil=[('Santé des envois', 'sante.html', 'desinscriptions')])


def _desinscription_publique():
    c = ('<div class="carte-seule"><section data-etat="normal"><p class="petit">prospection-a.example</p><h1 style="margin:8px 0 12px">Vous ne recevrez plus de messages d’Axion-IA.</h1><p>C’est fait, en un clic. Aucune autre démarche.</p>'
         '<label class="case" style="margin-top:16px"><input type="checkbox"> Pour toute mon organisation</label><button type="button" class="btn btn-plein" style="width:100%;margin-top:8px" data-toast="C’est noté pour toute votre organisation.">Confirmer</button>'
         '<p class="petit" style="margin-top:16px"><a href="#" data-toast="Page « Pourquoi ce message » ouverte.">Pourquoi ai-je reçu ce message ?</a></p></section>'
         '<section data-etat="vide" hidden><h1>Déjà fait</h1><p style="margin-top:8px">Cette adresse est déjà désinscrite. Vous ne recevrez plus rien.</p></section>'
         '<section data-etat="erreur" hidden role="alert"><h1>Lien incomplet</h1><p style="margin-top:8px">Répondez simplement « STOP » au message : c’est pris en compte de la même façon.</p></section></div>')
    P['desinscription-publique.html'] = ecran_seul('Désinscription', c)


def _statistiques():
    entonnoir = tableau('Entonnoir', ['Étape', 'Nombre', 'Part'], [['Envoyés', '<span class="chiffre">1 240</span>', '100 %'], ['Réponses', '<span class="chiffre">62</span>', '5,0 %'], ['Réponses positives', '<span class="chiffre">21</span>', '1,7 %'], ['Rendez-vous', '<span class="chiffre">8</span>', '0,6 %'], ['Gagnés', '<span class="chiffre">3</span>', '0,2 %']], cartes=False)
    camp = tableau('Résultats par campagne', ['Campagne', 'Envoyés', 'Réponses', 'Positives', 'Rendez-vous'], [['Commerces de Lyon', '92', '11', '4', '2'], ['Organisateurs Rhône-Alpes', '280', '9', '3', '1']])
    carte = bloc('Carte de France', '<svg viewBox="0 0 300 260" style="width:100%;max-width:360px;height:auto" role="img" aria-labelledby="cf-t"><title id="cf-t">Contacts par région : Auvergne-Rhône-Alpes en tête avec 640 fiches</title><path d="M120 10l60 20 40-10 10 50 30 30-30 50 10 40-60-10-50 10-30-40 10-50-30-30 40-20z" fill="#eaf0ff" stroke="#2346c8" stroke-width="2"/><circle cx="200" cy="170" r="18" fill="#2346c8" opacity=".75"/><circle cx="130" cy="90" r="10" fill="#2346c8" opacity=".5"/></svg><p class="petit">Auvergne-Rhône-Alpes : 640 fiches · Île-de-France : 210.</p>')
    normal = (filtres(['30 derniers jours', '3 mois', '12 mois'])
              + tuiles([('Envoyés', '1 240', '30 derniers jours'), ('Taux de réponse', '5,0 %', 'objectif 4 %'), ('Rendez-vous', '8', '+3 vs mois dernier'), ('Gagnés', '3', '5 400 € HT')])
              + onglets('Statistiques', [('resultats', 'Résultats', camp), ('entonnoir', 'Entonnoir', entonnoir), ('carte', 'Carte', carte), ('rapports', 'Rapports', '<ul class="liste"><li><span class="quoi"><strong>Rapport d’octobre</strong><small>Figé le 1er nov.</small></span>%s</li></ul>' % btn('Télécharger (PDF)', 'petit', icone='export', attrs='data-toast="Téléchargement factice."'))])
              + '<p class="petit" style="margin-top:12px">Aucune mesure d’ouverture : seules les réponses et les rendez-vous comptent.</p>')
    P['statistiques.html'] = page('statistiques', 'Statistiques', '<strong>5,0 % de réponses</strong> sur 30 jours · 8 rendez-vous · 3 affaires gagnées.', normal,
                                  etat_vide('stats', 'Pas encore de chiffres', 'Les résultats apparaissent après le premier envoi.', btn('Créer une campagne', 'plein', 'campagne-nouvelle.html')),
                                  actions=btn('Exporter', 'contour', icone='export', attrs='data-toast="Export prêt · Télécharger."'))


for f in (_boites, _domaines, _serveurs, _chauffe, _alertes, _desinscriptions, _desinscription_publique, _statistiques):
    f()
