# 25 : Documents de conformité : BROUILLONS (lot J2)

> **BROUILLON À VALIDER PAR WILL.** Aucun avocat n'a relu ces textes. Will les valide lui-même.
> Chaque texte cite ses sources. **Vérifiez chaque article sur Legifrance (droit français) et sur EUR-Lex (RGPD)** avant usage.
> Rien n'est en ligne. Aucun e-mail n'a été envoyé. Aucun serveur n'a été touché.

**Référence** : `plan/20-PLAN-CORRIGE-UNIQUE.md` (lot J2 du § 3.1, décisions du § 10). Voir aussi `plan/03-module-envoi-demarrage-petit.md` (§ 1.3, § 5) et `plan/05-clients-licence-et-multi-locataire.md` (§ B « Juridique »).

**Date du brouillon** : 01/11/2026. **Statut** : à relire par Will, puis à passer au contrôleur de contenu (lot C1).

---

## 0. Mode d'emploi

### 0.1 Les textes de loi à vérifier

| Texte | Où le lire | Ce qu'il dit, en bref |
|---|---|---|
| RGPD, règlement (UE) 2016/679 | EUR-Lex | Le cadre général. |
| Art. 5 RGPD | EUR-Lex | Grands principes (dont limitation de la conservation). |
| Art. 6.1.f RGPD + considérant 47 | EUR-Lex | Base légale « intérêt légitime ». Le considérant 47 cite la prospection. |
| Art. 12 RGPD | EUR-Lex | Délai de réponse (1 mois, + 2 mois si besoin), forme claire, vérification d'identité. |
| Art. 13 RGPD | EUR-Lex | Information quand les données viennent **de la personne** (formulaire, réponse). |
| Art. 14 RGPD | EUR-Lex | Information quand les données **ne viennent pas** de la personne. Délai : au plus tard au premier message (14.3.b), et au plus tard 1 mois (14.3.a). |
| Art. 15, 16, 17, 18, 21 RGPD | EUR-Lex | Droits : accès, rectification, effacement (et ses exceptions, 17.3), limitation, opposition (21.2 et 21.3 pour la prospection ; 21.4 : le droit doit être présenté clairement et à part). |
| Art. 28 RGPD | EUR-Lex | Contrat obligatoire avec un sous-traitant. Liste des clauses (28.3.a à h). |
| Art. 30 RGPD | EUR-Lex | Registre des traitements (30.1 responsable ; 30.2 sous-traitant). |
| Art. 32 RGPD | EUR-Lex | Sécurité. |
| Art. 33 et 34 RGPD | EUR-Lex | Violation de données : notifier la CNIL en 72 h si risque ; prévenir les personnes si risque élevé ; tout noter (33.5). |
| Art. 35 RGPD | EUR-Lex | Analyse d'impact (AIPD). |
| Art. L.34-5 du Code des postes et des communications électroniques (CPCE) | Legifrance | Prospection par e-mail. Dernier alinéa : identité de l'expéditeur visible, moyen simple et gratuit de s'opposer. |
| Loi n° 78-17 du 6 janvier 1978 « Informatique et Libertés » | Legifrance | Loi française qui complète le RGPD. |
| Art. 20 de la loi n° 2004-575 (LCEN) | Legifrance | Une publicité doit être reconnaissable comme telle et dire pour qui elle est faite. |

### 0.2 Les décisions de Will qui encadrent tous les textes

1. **Prospection en France seulement** au départ.
2. **Une opposition met la personne à l'écart des envois. Elle n'efface rien.** On garde une trace (empreinte) pour ne plus jamais écrire.
3. **Aucune suppression de données de personnes.** Une demande d'effacement = mise à l'écart immédiate + alerte à Will. **Will décide.**
4. **Entité d'envoi : la SAS française Axion-IA.**
5. **Interdits dans les messages** : « aucun gain garanti » et toute promesse de gain ; « agréé », « labellisé », « accrédité », « certifié », « Qualiopi » ; le nom de lieu interdit tenu dans la liste privée du contrôleur. Le contrôleur de contenu (lot C1) bloque ces mots.
6. **Aucun pixel de suivi**. Pas de mesure d'ouverture.

### 0.3 Les champs à remplir (jamais dans le dépôt public)

Les crochets `[...]` sont des champs. Ils seront remplis **dans le CRM** (réglages de l'espace), **pas dans ce fichier**.

| Champ | Exemple de forme |
|---|---|
| `[RAISON SOCIALE]` | Axion-IA SAS |
| `[ADRESSE POSTALE]` | adresse du siège |
| `[SIREN]` | 9 chiffres |
| `[E-MAIL RGPD]` | adresse dédiée aux demandes de droits |
| `[URL PAGE INFO]` | `https://go.[domaine-envoi]/vie-privee` |
| `[URL DÉSINSCRIPTION]` | `https://go.[domaine-envoi]/d/[jeton]` |
| `[SOURCE]` | la source réelle de l'adresse, pour ce contact précis |
| `[DURÉE]` | durée annoncée (voir point W-3 à la fin) |
| `[DATE]`, `[N° DEMANDE]` | remplis automatiquement |

---

## D1. Information article 14 RGPD (deux niveaux + variante sans offre)

**Pourquoi** : les adresses ne viennent pas des personnes. L'art. 14 RGPD impose de les informer, au plus tard au premier message (14.3.b). L'art. 21.4 impose de présenter le droit d'opposition **clairement et à part**.

**Comment** : niveau 1 court dans chaque e-mail ; niveau 2 complet sur une page web. Le niveau 1 renvoie au niveau 2. Le CRM refuse un premier message sans niveau 1 (lot J1).

### D1-a. Niveau 1 : bloc court dans chaque e-mail (`{bloc_information}`)

Version standard (≈ 60 mots) :

> Pourquoi ce message ? Nous avons trouvé votre adresse professionnelle dans [SOURCE]. Nous vous écrivons car notre offre concerne votre activité. [RAISON SOCIALE] traite ces données pour sa prospection, sur la base de son intérêt légitime. Vous pouvez vous opposer à tout moment : [lien « Ne plus recevoir de messages »]. Vos droits et le détail : [URL PAGE INFO].

Version encore plus courte (si le message est très court, ≈ 40 mots) :

> Votre adresse vient de [SOURCE]. [RAISON SOCIALE] l'utilise pour lui proposer ses services. Pour ne plus rien recevoir : [lien]. Vos droits (accès, opposition, réclamation à la CNIL) : [URL PAGE INFO].

Règles :
- `[SOURCE]` est la **vraie source de ce contact** (ex. « le répertoire public des entreprises », « le site internet de votre entreprise », « l'annuaire de [nom de l'annuaire] »). Jamais une formule vague comme « nos bases ».
- Le lien d'opposition est **à part**, visible, sans connexion, gratuit (art. 21.4 RGPD ; art. L.34-5 CPCE).
- Le bloc est placé **dans le corps** du message, pas seulement en tout petit dans le pied.

### D1-b. Niveau 2 : page complète « Pourquoi ce message ? » (`[URL PAGE INFO]`)

> **Pourquoi avez-vous reçu un message de [RAISON SOCIALE] ?**
>
> *Dernière mise à jour : [DATE].*
>
> **1. Qui sommes-nous ?**
> [RAISON SOCIALE], société par actions simplifiée, SIREN [SIREN], [ADRESSE POSTALE].
> Nous sommes responsables du traitement de vos données.
> Pour toute question sur vos données : [E-MAIL RGPD].
> [Si un délégué à la protection des données est désigné : « Notre délégué à la protection des données : [contact]. » Sinon, supprimer cette ligne.]
>
> **2. Pourquoi utilisons-nous vos données ?**
> Pour vous présenter nos services, qui concernent votre activité professionnelle.
> Nous écrivons à des professionnels : dirigeants et responsables de petites et moyennes entreprises, organisateurs d'événements, associations et fédérations.
> Nous ne vous écrivons qu'en France.
>
> **3. Sur quelle base légale ?**
> Notre intérêt légitime à faire connaître nos services aux professionnels (article 6.1.f du RGPD).
> Nous avons vérifié que cet intérêt ne passe pas avant vos droits : le message concerne votre métier, il est peu fréquent, et vous pouvez l'arrêter en un clic.
> La prospection par e-mail entre professionnels est encadrée par l'article L.34-5 du Code des postes et des communications électroniques.
>
> **4. Quelles données ?**
> - Votre nom et votre prénom, si nous les connaissons.
> - Votre adresse e-mail professionnelle.
> - Votre fonction et le nom de votre organisation.
> - Des informations publiques sur votre organisation (activité, ville, taille).
> - L'historique de nos échanges : messages envoyés, vos réponses, votre éventuelle opposition.
>
> Nous ne collectons **aucune** donnée sensible. Nous ne mesurons **pas** l'ouverture de nos messages (aucun pixel de suivi).
>
> **5. D'où viennent vos données ?**
> De sources accessibles au public : [liste réelle des sources, par exemple : le répertoire public des entreprises tenu par l'INSEE, les sites internet des organisations, des annuaires professionnels publics].
> Le message que vous avez reçu indique la source de votre adresse.
> Nous ne contactons jamais une entreprise qui a demandé à ne pas figurer dans la diffusion publique du répertoire des entreprises.
>
> **6. Qui reçoit vos données ?**
> Seules les personnes habilitées de [RAISON SOCIALE].
> Et nos prestataires techniques, qui agissent sur nos instructions :
> - hébergement des serveurs : [HÉBERGEUR, pays] ;
> - hébergement des boîtes e-mail : [PRESTATAIRE, pays] ;
> - vérification de la validité des adresses : [PRESTATAIRE, pays].
>
> Nous ne vendons pas vos données. Nous ne les donnons à aucun client.
>
> **7. Vos données sortent-elles de l'Union européenne ?**
> [Choisir : « Non. » / « Oui, vers [pays], encadré par [décision d'adéquation ou clauses contractuelles types]. »]
>
> **8. Combien de temps les gardons-nous ?**
> [DURÉE — texte à valider par Will, voir W-3. Proposition : « Nous gardons vos données tant que nous échangeons avec vous. Sans échange pendant 3 ans, nous cessons tout envoi. Si vous vous opposez, nous gardons seulement une trace de votre adresse, pour ne plus jamais vous écrire. »]
>
> **9. Vos droits**
> Vous pouvez à tout moment :
> - **vous opposer** à nos messages, sans donner de raison : [lien de désinscription] ou répondez « STOP » ;
> - **accéder** à vos données et en recevoir une copie ;
> - **faire corriger** des données fausses ;
> - **demander l'effacement** de vos données ;
> - **demander la limitation** de leur utilisation ;
> - **définir des directives** sur le sort de vos données après votre décès (loi Informatique et Libertés).
>
> Écrivez à [E-MAIL RGPD]. Nous répondons sous un mois au plus.
> Nous pouvons vous demander de confirmer que l'adresse vous appartient.
>
> **10. Réclamation**
> Vous pouvez déposer une réclamation auprès de la CNIL (www.cnil.fr), autorité de contrôle en France.
>
> **11. Décision automatique**
> Aucune décision vous concernant n'est prise de façon entièrement automatique.

### D1-c. Variante « information pure, sans offre »

**Usage** : pour un lot de contacts collectés **avant tout envoi**, qui doivent être informés dans le délai d'un mois (art. 14.3.a RGPD), avant toute prospection. **Ce message ne contient aucune offre, aucun lien commercial, aucun appel à rendez-vous.** Le contrôleur de contenu le classe en nature « information art. 14 ».

Objet proposé :
> Information sur vos données professionnelles

Corps :
> Bonjour,
>
> Nous sommes [RAISON SOCIALE], une société française ([ADRESSE POSTALE], SIREN [SIREN]).
>
> La loi nous demande de vous prévenir : votre adresse professionnelle figure dans notre fichier de contacts professionnels.
> Nous l'avons trouvée dans [SOURCE].
>
> Nous pourrions vous écrire plus tard pour vous présenter nos services, liés à votre activité. Notre base légale est notre intérêt légitime.
>
> **Vous ne voulez pas recevoir nos messages ?** Cliquez ici : [lien « Je m'oppose »]. C'est immédiat et gratuit. Vous pouvez aussi répondre « STOP ».
>
> Vos autres droits (accès, correction, effacement, limitation, réclamation à la CNIL) et le détail de nos pratiques : [URL PAGE INFO].
> Pour toute question : [E-MAIL RGPD].
>
> Ce message est une simple information. Il n'appelle aucune réponse.
>
> [RAISON SOCIALE]

Règles pour cette variante :
- Envoyée **une seule fois** par adresse. Le CRM pose la date d'information (`first_info_at`) **à la livraison** (plan 03, § 5).
- **Aucune prospection** vers ce contact avant [délai à fixer par Will, proposition : 7 jours] après l'information, pour laisser le temps de s'opposer.
- Le volume de ce lot suit la même chauffe que les autres envois (aucune exception de volume).
- Si l'information n'a pas pu être faite dans le mois (adresse invalide, rebond) : le contact est mis à l'écart, jamais prospecté.

---

## D2. Page publique de désinscription et d'opposition

**Pourquoi** : art. 21.2, 21.3 et 21.4 RGPD ; art. L.34-5 CPCE (moyen simple et gratuit). Désinscription en un clic (RFC 8058) prévue au lot E6.

**Adresse** : `[URL DÉSINSCRIPTION]`, sous le domaine d'envoi (jamais sous `axion-ia.com`). La page reste en ligne après la fin d'un domaine.

**Effet** : opposition inscrite en moins d'une minute dans l'espace concerné. **Mise à l'écart, sans effacement.**

### D2-a. Clic depuis le message (lien valide)

Titre :
> C'est fait : vous ne recevrez plus nos messages.

Texte :
> Votre adresse [adresse masquée, ex. j•••@exemple.fr] ne recevra plus de messages de prospection de [RAISON SOCIALE].
> C'est enregistré. Vous n'avez rien d'autre à faire.
>
> Un message déjà en route peut encore arriver dans les prochaines minutes. Il sera le dernier.

Option (bouton secondaire) :
> [Bouton] Arrêter aussi pour toute mon organisation ([domaine masqué])

Texte sous le bouton :
> Utilisez ce bouton seulement si vous pouvez parler au nom de votre organisation. Plus aucune adresse en [domaine] ne recevra nos messages.

Liens en bas :
> Pourquoi avez-vous reçu ce message ? [URL PAGE INFO]
> Vos autres droits (accès, effacement…) : écrivez à [E-MAIL RGPD].

### D2-b. Confirmation après « toute mon organisation »

> C'est fait : plus aucune adresse en [domaine] ne recevra nos messages.

### D2-c. Déjà désinscrit

> Vous êtes déjà désinscrit. Vous ne recevez plus nos messages depuis le [DATE].
> Rien d'autre à faire.

### D2-d. Lien abîmé ou incomplet

> Ce lien ne fonctionne pas. Il est peut-être coupé ou incomplet.
>
> Pas de souci : indiquez votre adresse ci-dessous. Nous arrêtons tout envoi vers elle.
> [Champ : votre adresse e-mail] [Bouton : Ne plus recevoir de messages]

### D2-e. Formulaire manuel : réponse unique

Après envoi du formulaire, **toujours le même message**, que l'adresse soit connue ou non (on ne révèle pas qui est dans le fichier) :

> C'est enregistré. Si cette adresse figure dans notre fichier, elle ne recevra plus nos messages.

Règle technique : l'adresse saisie est enregistrée en opposition **sans e-mail de confirmation** (on n'envoie rien à une adresse qui vient de s'opposer).

### D2-f. Erreur technique

> Un problème technique nous empêche d'enregistrer votre demande pour le moment.
> Réessayez dans quelques minutes, ou répondez simplement « STOP » à notre message, ou écrivez à [E-MAIL RGPD].
> Votre demande sera traitée.

Règle technique : en cas d'erreur, la demande est **mise en file et rejouée**. Une alerte part vers Will (console + e-mail).

### D2-g. Trop de demandes (protection contre les abus)

> Trop de demandes en peu de temps. Réessayez dans une minute.

### D2-h. Règles de la page

- Aucune connexion, aucun mot de passe, aucune question obligatoire.
- Aucun pixel, aucun traceur, aucun bandeau publicitaire.
- Aucune offre, aucune tentative de faire changer d'avis.
- Lisible sur téléphone, au clavier, avec un lecteur d'écran.
- Le clic « un clic » (POST RFC 8058) ne montre pas de page : il enregistre et répond « 200 ».
- Question facultative possible **après** la confirmation : « Pourquoi ? (facultatif) : trop de messages / pas concerné / autre ». Jamais avant.

---

## D3. Mention dans le pied de chaque e-mail

**Pourquoi** : identité de l'expéditeur non dissimulée et adresse valable pour s'opposer (art. L.34-5 CPCE, dernier alinéa) ; publicité identifiable (art. 20 LCEN) ; rappel des droits (art. 14 et 21.4 RGPD).

### D3-a. Pied standard (prospection)

> —
> [Prénom Nom de l'expéditeur réel], [fonction] — [RAISON SOCIALE], SAS, SIREN [SIREN], [ADRESSE POSTALE].
> Message de prospection professionnelle. Vous pouvez vous opposer à tout moment : [Ne plus recevoir de messages] ou répondez « STOP ».
> Vos données : [URL PAGE INFO] · Vos droits : [E-MAIL RGPD].

### D3-b. Pied pour la variante « information pure » (D1-c)

> —
> [RAISON SOCIALE], SAS, SIREN [SIREN], [ADRESSE POSTALE].
> Message d'information sur vos données. Pour vous opposer : [Je m'oppose] ou répondez « STOP ». Détail : [URL PAGE INFO].

### D3-c. Règles du pied

- Le nom de l'expéditeur est **une vraie personne** (décision 7 de Will : jamais de faux nom).
- Les en-têtes `List-Unsubscribe` et `List-Unsubscribe-Post` sont présents (lot E6).
- Le pied n'est pas une image. Il reste lisible en texte brut.
- Le pied ne remplace pas le bloc D1-a dans le corps du **premier** message.
- Pour un client de la console : identité **du client**, jamais celle d'Axion (plan 03, § 1.3).

### D3-d. Exemple complet d'un premier message (structure seulement)

> Objet : [objet validé]
>
> Bonjour [Prénom],
>
> [2 à 5 phrases de message, validées par Will, passées au contrôleur.]
>
> [Prénom de l'expéditeur]
>
> **Pourquoi ce message ?** [Bloc D1-a.]
>
> — [Pied D3-a.]

---

## D4. Modèles de réponse aux demandes de droits

**Délai** : un mois à compter de la réception, prolongeable de deux mois si la demande est complexe ; il faut alors prévenir la personne dans le premier mois (art. 12.3 RGPD).
**Gratuit** (art. 12.5). **Vérification d'identité** seulement en cas de doute raisonnable (art. 12.6) : en général, une réponse depuis l'adresse concernée suffit.
**Tout est noté** dans l'écran « Demandes RGPD » (lot U12) : date de réception, type, réponse, date de réponse.

### D4-a. Accusé de réception (toutes demandes)

> Objet : Votre demande sur vos données — n° [N° DEMANDE]
>
> Bonjour,
>
> Nous avons bien reçu votre demande du [DATE] concernant vos données.
> Nous vous répondrons au plus tard le [DATE + 1 mois].
>
> [Si doute sur l'identité :] Pour protéger vos données, merci de nous écrire depuis l'adresse concernée par la demande. Sans cette confirmation, nous ne pouvons pas vous communiquer vos données.
>
> [RAISON SOCIALE] — [E-MAIL RGPD]

### D4-b. Réponse à une demande d'accès (art. 15 RGPD)

> Objet : Vos données — n° [N° DEMANDE]
>
> Bonjour,
>
> Voici les informations que nous détenons sur vous.
>
> **Vos données** : [tableau ou fichier joint : nom, prénom, adresse, fonction, organisation, données publiques sur l'organisation, historique des messages envoyés et reçus, statut d'opposition].
> **Pourquoi** : prospection professionnelle de [RAISON SOCIALE].
> **Base légale** : notre intérêt légitime (article 6.1.f du RGPD).
> **Source** : [SOURCE].
> **Destinataires** : nos équipes habilitées et nos prestataires techniques ([liste]).
> **Transfert hors Union européenne** : [non / oui, vers [pays], encadré par [outil juridique]].
> **Durée de conservation** : [DURÉE].
> **Décision automatique** : aucune.
>
> Vous pouvez demander la correction, l'effacement ou la limitation de vos données, ou vous opposer à nos messages. Vous pouvez aussi saisir la CNIL (www.cnil.fr).
>
> [Si la personne n'est pas dans le fichier :] Nous ne détenons aucune donnée associée à cette adresse.
>
> [RAISON SOCIALE] — [E-MAIL RGPD]

### D4-c. Réponse à une opposition (art. 21.2 et 21.3 RGPD)

L'opposition à la prospection est **sans condition** : pas de motif à demander. Elle est appliquée **le jour même**, sans attendre la réponse écrite.

> Objet : Opposition enregistrée — n° [N° DEMANDE]
>
> Bonjour,
>
> C'est fait : depuis le [DATE], vous ne recevez plus aucun message de prospection de [RAISON SOCIALE].
>
> Pour respecter votre choix dans la durée, nous gardons seulement une trace de votre adresse dans notre liste d'opposition. Cette trace sert uniquement à ne plus vous écrire.
>
> Si vous souhaitez aussi l'effacement de vos autres données, dites-le-nous en réponse à ce message.
>
> [RAISON SOCIALE] — [E-MAIL RGPD]

> **Point W-5** : envoyer cet e-mail de confirmation est-il souhaitable ? Une personne qui s'oppose peut ne plus vouloir aucun message. Proposition : ne l'envoyer **que** si la personne a écrit (e-mail, courrier), jamais après un clic de désinscription.

### D4-d. Demande d'effacement (art. 17 RGPD) : procédure interne

Décision de Will : **aucune suppression automatique**. Le CRM fait :

1. **Tout de suite** : mise à l'écart de la personne (opposition dans tous les univers de l'espace ; plus aucun envoi ; fiche masquée des listes de travail).
2. **Tout de suite** : alerte à Will (console + e-mail), avec la date limite de réponse.
3. **Will décide** dans le délai d'un mois, et note sa décision et son motif dans le registre des demandes.
4. Réponse écrite à la personne (modèle D4-e ou D4-f).

> **ATTENTION, point W-4** : quand une personne s'est opposée à la prospection et demande l'effacement, l'art. 17.1.c RGPD prévoit en principe l'effacement. Les exceptions (art. 17.3) sont limitées (par exemple obligation légale, défense de droits en justice). Garder une **trace minimale** pour ne plus écrire est la pratique courante, mais garder **toute la fiche** sans motif valable peut être contraire au RGPD. Un refus doit être motivé, et la personne doit être informée qu'elle peut saisir la CNIL (art. 12.4). **Will doit vérifier ce point sur EUR-Lex et sur le site de la CNIL avant le premier envoi.**

### D4-e. Réponse « effacement accepté » (si Will décide d'effacer)

> Objet : Effacement de vos données — n° [N° DEMANDE]
>
> Bonjour,
>
> Nous avons effacé vos données le [DATE].
>
> Nous gardons seulement une trace technique de votre adresse (une empreinte, non lisible) dans notre liste d'opposition. Elle sert uniquement à ne jamais vous écrire à nouveau, même si votre adresse réapparaît dans une source publique.
>
> [RAISON SOCIALE] — [E-MAIL RGPD]

### D4-f. Réponse « mise à l'écart, effacement non réalisé » (si Will décide de ne pas effacer)

> Objet : Votre demande d'effacement — n° [N° DEMANDE]
>
> Bonjour,
>
> Depuis le [DATE], vous ne recevez plus aucun message de [RAISON SOCIALE]. Vos données ne sont plus utilisées pour la prospection.
>
> Nous ne les avons pas effacées pour la raison suivante : [MOTIF PRÉCIS, fondé sur l'article 17.3 du RGPD — à rédiger par Will au cas par cas].
>
> Vous pouvez contester cette décision auprès de la CNIL (www.cnil.fr) ou devant un juge.
>
> [RAISON SOCIALE] — [E-MAIL RGPD]

### D4-g. Demande de correction (art. 16) ou de limitation (art. 18)

> Objet : Votre demande — n° [N° DEMANDE]
>
> Bonjour,
>
> [Correction :] Nous avons corrigé vos données le [DATE] : [ancienne valeur → nouvelle valeur].
> [Limitation :] Depuis le [DATE], vos données sont conservées mais ne sont plus utilisées, en attendant [motif de la limitation].
>
> [RAISON SOCIALE] — [E-MAIL RGPD]

### D4-h. Prolongation du délai (art. 12.3)

> Bonjour,
>
> Votre demande n° [N° DEMANDE] demande plus de temps : [raison courte]. Nous vous répondrons au plus tard le [DATE + 3 mois au total].
>
> [RAISON SOCIALE] — [E-MAIL RGPD]

### D4-i. Demande reçue pour un client de la console

Axion est alors sous-traitant. On ne répond **pas** à la place du client.

> Bonjour,
>
> Votre demande concerne des messages envoyés par [NOM DU CLIENT]. Nous lui avons transmis votre demande le [DATE]. C'est lui qui vous répondra.
> Ses coordonnées : [contact RGPD du client].
>
> [RAISON SOCIALE]

Règle : transmission au client **sous 48 h** (clause D9, art. 8).

---

## D5. Fiche du registre des traitements (art. 30.1 RGPD) : prospection

| Rubrique (art. 30.1) | Contenu proposé |
|---|---|
| **Nom du traitement** | Prospection commerciale par e-mail auprès de professionnels |
| **Responsable** | [RAISON SOCIALE], SAS, SIREN [SIREN], [ADRESSE POSTALE] ; représentant légal : [fonction] |
| **Contact** | [E-MAIL RGPD] ; délégué à la protection des données : [oui, contact / non désigné — W-8] |
| **Date de création / mise à jour** | [DATE] / [DATE] |
| **Finalités** | 1. Présenter les services de la société à des professionnels. 2. Gérer les réponses, rendez-vous et suites. 3. Gérer les oppositions et les demandes de droits. 4. Informer les personnes (art. 14). 5. Mesurer les résultats sans suivi individuel des ouvertures. |
| **Base légale** | Intérêt légitime (art. 6.1.f RGPD), voir D6. Gestion des oppositions : obligation légale (art. 6.1.c, art. 21 RGPD). |
| **Personnes concernées** | Dirigeants et responsables de TPE et PME ; organisateurs d'événements ; responsables d'associations et fédérations ; en France. |
| **Données** | Identité (nom, prénom si connu), adresse e-mail professionnelle, fonction, organisation, données publiques de l'organisation, historique des échanges, statut d'opposition, provenance de chaque donnée. **Aucune donnée sensible (art. 9). Aucune donnée d'ouverture.** |
| **Sources** | [liste réelle : répertoire public des entreprises (diffusion publique seulement), sites des organisations, annuaires publics, …] |
| **Destinataires internes** | Personnes habilitées de la société (rôles du CRM) |
| **Sous-traitants** | [Hébergeur serveurs, pays] ; [hébergeur boîtes e-mail, pays] ; [vérificateur d'adresses, pays] ; [sauvegarde hors site, pays]. Contrat art. 28 signé avec chacun : [oui/non, date]. |
| **Transferts hors UE** | [Aucun / pays + garantie] |
| **Durée de conservation** | [DURÉE, voir W-3]. Proposition actuelle : données actives tant qu'il y a échange ; 3 ans sans échange = mise à l'écart (plus aucun envoi) ; opposition = trace d'opposition conservée ; aucune suppression sans décision de Will. |
| **Sécurité (art. 32)** | Connexion avec code e-mail (2FA) ; droits par rôle ; isolation par espace (RLS) ; chiffrement des échanges ; sauvegarde quotidienne chiffrée et restauration testée ; journal des accès ; adresses non affichées en clair dans la liste d'opposition ; serveur d'envoi séparé. |
| **AIPD** | [Faite le / à faire — voir D7] |
| **Analyse d'intérêt légitime** | D6, version [n°], validée par Will le [DATE] |
| **Information des personnes** | D1 (niveaux 1 et 2, variante D1-c) |

**Registre sous-traitant (art. 30.2 RGPD)** : quand Axion agit pour des clients de la console, une fiche par client : nom et contact du client ; catégories de traitements faits pour lui ; transferts ; mesures de sécurité. Ce registre est tenu **hors du dépôt public**.

---

## D6. Analyse d'intérêt légitime (test en trois étapes)

**Pourquoi** : l'art. 6.1.f RGPD exige que l'intérêt légitime ne passe pas avant les droits des personnes. Le considérant 47 indique que la prospection **peut** être un intérêt légitime. L'analyse doit être écrite et gardée.

### Étape 1 : l'intérêt est-il légitime ?

| Question | Réponse proposée |
|---|---|
| Quel est l'intérêt ? | Faire connaître les services d'une jeune société française à des professionnels qui peuvent en avoir besoin. |
| Est-il légal ? | Oui. La prospection B2B par e-mail est permise si le message concerne la profession de la personne et si elle peut s'opposer (art. L.34-5 CPCE ; doctrine de la CNIL à vérifier). |
| Est-il réel et actuel ? | Oui : activité commerciale en cours. |
| Est-il clair ? | Oui : finalité écrite dans D5. |

**Conclusion étape 1** : intérêt légitime **[à confirmer par Will]**.

### Étape 2 : le traitement est-il nécessaire ?

| Question | Réponse proposée |
|---|---|
| Peut-on atteindre le but autrement, avec moins de données ? | Les autres moyens (publicité, salons) touchent mal les petites structures. Le message direct reste le moyen le plus ciblé. |
| Les données sont-elles limitées au strict besoin ? | Oui : identité, adresse pro, fonction, organisation, historique. Pas de donnée sensible, pas de suivi d'ouverture, pas d'enrichissement sur la vie privée. |
| Les volumes sont-ils limités ? | Oui : démarrage à 20 messages par jour ; plafond par boîte ; séquence de 4 messages au plus ; arrêt dès une réponse. |
| Ciblage pertinent ? | Oui : seulement des professionnels dont l'activité est liée à l'offre (segments choisis, motif d'éligibilité vérifié par le CRM). |

**Conclusion étape 2** : nécessaire et proportionné **[à confirmer par Will]**.

### Étape 3 : mise en balance avec les droits des personnes

| Élément | Pour la personne | Mesure qui protège |
|---|---|---|
| Nature des données | Données professionnelles, souvent publiques | Aucune donnée sensible ; adresses de webmail personnel refusées en froid (lot C3) |
| Attentes raisonnables | Un professionnel s'attend à recevoir des offres liées à son métier ; moins s'il est une très petite structure où pro et perso se mêlent | Message lié à l'activité ; ton sobre ; source citée dans chaque message |
| Gêne | Messages non sollicités | 4 messages au plus ; arrêt à la première réponse ; pression limitée par organisation |
| Contrôle | Pouvoir arrêter facilement | Désinscription en un clic ; STOP par réponse ; opposition effective en moins d'une minute ; opposition pour toute l'organisation |
| Transparence | Savoir qui écrit et pourquoi | Bloc art. 14 dans le premier message ; page complète ; expéditeur réel nommé |
| Risques de sécurité | Fuite du fichier | Mesures D5 (2FA, isolation, chiffrement, sauvegarde) ; procédure D8 |
| Personnes fragiles | Entrepreneurs individuels | Entreprises en diffusion partielle du répertoire public jamais contactées ; pas de promesse de gain (mots interdits) |
| Durée | Être relancé sans fin | 3 ans sans échange = plus aucun envoi |

**Conclusion étape 3** : avec ces mesures, l'intérêt légitime ne passe pas avant les droits des personnes **[à valider par Will]**.

**Risques restants à suivre** : taux de plaintes et d'oppositions (seuils du lot E7) ; si les oppositions dépassent [seuil à fixer], revoir le ciblage et refaire cette analyse.

**Revoir cette analyse** : chaque année, et à chaque changement (nouvelle source, nouveau segment, sortie de France, nouveau canal comme le téléphone en V1).

Signature : Will, [DATE], version [n°].

---

## D7. Analyse d'impact (AIPD) : plan et points à remplir

**Pourquoi** : l'art. 35 RGPD impose une AIPD quand le risque est élevé. Les lignes directrices européennes donnent 9 critères ; si **2 critères ou plus** sont remplis, l'AIPD est en principe requise. La CNIL publie une liste des traitements concernés et un outil gratuit (PIA). **À vérifier sur le site de la CNIL.**

### 7.1 Faut-il une AIPD ? (première grille, à cocher par Will)

| Critère | Ici ? | Note |
|---|---|---|
| Évaluation ou notation | [ ] | Score de priorité des contacts ? |
| Décision automatique avec effet important | [ ] | Non prévu |
| Surveillance systématique | [ ] | Non (aucun pixel) |
| Données sensibles | [ ] | Non |
| Grande échelle | [ ] | Base d'entreprises à l'échelle de la France : à juger |
| Croisement de fichiers | [ ] | Oui probable : répertoire public + sites + annuaires |
| Personnes vulnérables | [ ] | Non |
| Technologie nouvelle | [ ] | Brouillon IA d'accroche (V1) : à juger |
| Exercice d'un droit empêché | [ ] | Non |

**Recommandation** : faire l'AIPD en V0 (version courte), puis compléter en V1 (lot J4, D12) pour la console.

### 7.2 Plan de l'AIPD (méthode CNIL)

1. **Contexte**
   - Description du traitement (reprendre D5).
   - Responsable, sous-traitants, flux de données (schéma : sources → CRM → serveur d'envoi → boîte du destinataire → réponses → CRM).
   - Supports : serveurs, logiciels, boîtes e-mail, sauvegardes.
2. **Principes fondamentaux**
   - Finalités déterminées et légitimes (D5, D6).
   - Base légale (D6).
   - Minimisation (liste des champs, justification de chacun).
   - Exactitude (vérification des adresses, lot E4 ; correction possible).
   - Durées de conservation (W-3).
   - Information (D1).
   - Droits : accès, rectification, effacement, limitation, opposition (D2, D4).
   - Sous-traitants et contrats (D9 et contrats avec nos propres prestataires).
   - Transferts hors UE.
3. **Risques** (pour chaque risque : sources, menaces, impacts, gravité, vraisemblance)
   - Accès illégitime aux données (vol du fichier, compte compromis, fuite entre espaces clients).
   - Modification non désirée (opposition perdue, fiche modifiée par erreur).
   - Disparition des données (perte de la liste d'opposition = envoi à des personnes opposées).
   - Risques propres : envoi à une personne opposée ; message trompeur ; envoi hors France ; envoi trop fréquent.
4. **Mesures**
   - Existantes et prévues : lots S1-S9, S7 (isolation), E6, E7, C3, J1, D8.
5. **Validation**
   - Avis du délégué à la protection des données s'il existe.
   - Avis des personnes concernées si possible (art. 35.9), par exemple un petit panel de professionnels.
   - Décision écrite de Will : risques acceptables, ou mesures à ajouter.
6. **Revue** : chaque année et à chaque changement important.

### 7.3 Points à remplir par Will

- [ ] Volume prévu de contacts la première année.
- [ ] Liste réelle des sources.
- [ ] Liste réelle des sous-traitants et pays.
- [ ] Usage d'un score ou de l'IA sur les contacts (oui/non, lequel).
- [ ] Gravité et vraisemblance de chaque risque (échelle CNIL : négligeable, limitée, importante, maximale).
- [ ] Décision finale et date.

---

## D8. Procédure générique en cas de violation de données

**Pourquoi** : art. 33 RGPD (notifier la CNIL au plus tard **72 heures** après en avoir pris connaissance, sauf si la violation n'entraîne pas de risque) ; art. 34 (prévenir les personnes si le risque est **élevé**) ; art. 33.5 (noter **toutes** les violations, même non notifiées). Pour un client de la console : art. 33.2 (le sous-traitant prévient le client sans délai).

**Définition simple** : une violation, c'est quand des données personnelles sont **perdues, détruites, modifiées, divulguées ou consultées** sans autorisation, par accident ou volontairement.

### Étape 1 : détecter (heure H)

- Sources possibles : alerte du CRM, alerte du serveur, message d'un prestataire, message d'un destinataire, constat d'un membre de l'équipe.
- **Toute personne** qui a un doute prévient Will immédiatement (console + e-mail + téléphone).
- Noter **l'heure exacte** où l'on a pris connaissance du problème : c'est le départ des 72 h.

### Étape 2 : contenir (le plus vite possible)

- Couper l'accès en cause (compte, clé, serveur, partage).
- Changer les mots de passe et clés concernés.
- Mettre l'envoi en pause si besoin (bouton « Tout arrêter »).
- **Garder les preuves** (journaux, captures). Ne rien effacer.

### Étape 3 : qualifier (avant H + 24 h si possible)

Remplir cette fiche :

| Question | Réponse |
|---|---|
| Qu'est-il arrivé ? | |
| Quand ? Depuis quand ? | |
| Type : confidentialité (divulgation), intégrité (modification), disponibilité (perte) ? | |
| Quelles données ? | |
| Combien de personnes, environ ? | |
| Quels espaces (Axion, clients de la console) ? | |
| Les données étaient-elles chiffrées et la clé sûre ? | |
| Conséquences possibles pour les personnes (hameçonnage, usurpation, gêne) ? | |
| Le risque est-il : **nul / présent / élevé** ? | |

### Étape 4 : décider par écrit (avant H + 48 h si possible)

Will écrit et signe sa décision dans le registre :

| Cas | Décision |
|---|---|
| Risque **improbable** pour les personnes | Pas de notification à la CNIL. **Motif écrit obligatoire.** Inscription au registre. |
| Risque **présent** | Notification à la CNIL **avant H + 72 h** (téléservice de la CNIL). |
| Risque **élevé** | Notification à la CNIL **et** message aux personnes concernées, sans délai excessif (art. 34). |
| Données d'un client de la console | Prévenir le client **sans délai** (objectif : sous [24 h — W-9]). C'est **le client** qui décide de notifier la CNIL. |

Si toutes les informations ne sont pas connues à H + 72 h : notifier quand même ce que l'on sait, puis **compléter** (art. 33.4). Si on dépasse 72 h : notifier quand même et **expliquer le retard**.

### Étape 5 : informer les personnes (si risque élevé)

Modèle :

> Objet : Information importante sur vos données
>
> Bonjour,
>
> Le [DATE], nous avons découvert un problème de sécurité qui concerne vos données : [description simple].
> Données concernées : [liste].
> Conséquences possibles : [ex. risque de messages frauduleux].
> Ce que nous avons fait : [mesures].
> Ce que nous vous conseillons : [ex. se méfier des messages qui demandent des informations personnelles].
>
> Pour toute question : [E-MAIL RGPD].
>
> [RAISON SOCIALE]

### Étape 6 : tenir le registre des violations (art. 33.5)

Une ligne par violation, **même sans notification** :

| N° | Date de découverte | Date de début | Faits | Données et personnes | Conséquences | Mesures | Risque | Notifiée CNIL (date) ou motif de non-notification | Personnes informées (date) | Décision signée par |
|---|---|---|---|---|---|---|---|---|---|---|

Le registre est tenu **hors du dépôt public**.

### Étape 7 : tirer les leçons (sous 30 jours)

- Pourquoi c'est arrivé ? Qu'est-ce qui empêche que cela recommence ?
- Mettre à jour D5, D7 et cette procédure si besoin.
- Faire un exercice une fois par an (scénario fictif).

---

## D9. Contrat de sous-traitance type (art. 28 RGPD) : client de la console

> **BROUILLON À VALIDER PAR WILL.** À joindre aux conditions générales de la console (lot J4). Les crochets sont à remplir pour chaque client, **hors dépôt public**.

**Entre** :
- [NOM DU CLIENT], [forme], SIREN [n°], [adresse], représenté par [fonction], ci-après « **le Client** » (responsable de traitement) ;
- [RAISON SOCIALE], SAS, SIREN [SIREN], [ADRESSE POSTALE], ci-après « **Axion** » (sous-traitant).

### Article 1 : Objet

Axion traite des données personnelles **pour le compte du Client** et **sur ses seules instructions**, pour fournir le module CRM Pro et, si le Client l'a choisi, l'option d'envoi d'e-mails.

### Article 2 : Description du traitement (art. 28.3 RGPD)

| Élément | Contenu |
|---|---|
| Nature | Hébergement, stockage, organisation, consultation, envoi d'e-mails, réception des réponses, gestion des oppositions |
| Finalité | Gestion de la relation commerciale du Client et, si choisi, ses campagnes d'e-mails |
| Durée | Durée du contrat principal |
| Personnes concernées | Prospects, clients et contacts professionnels du Client ; utilisateurs du Client |
| Données | Identité, coordonnées professionnelles, fonction, organisation, historique des échanges, statut d'opposition ; [autres données décrites par le Client] |
| Données sensibles | **Aucune**, sauf accord écrit spécifique |

### Article 3 : Instructions du Client

1. Axion agit uniquement sur instruction documentée du Client. Les réglages faits par le Client dans la console valent instructions.
2. Si une instruction semble contraire au RGPD, Axion prévient le Client sans délai (art. 28.3, dernier alinéa).
3. Axion n'utilise **jamais** les données du Client pour son propre compte, ni pour un autre client, sans accord écrit du Client (décision 32 de Will).
4. La base de prospection d'Axion n'est jamais fournie au Client.

### Article 4 : Obligations du Client

Le Client :
1. garantit qu'il a une base légale pour chaque fichier qu'il importe (case obligatoire à l'import) ;
2. rédige et valide son propre texte d'information (art. 13 et 14 RGPD) ; le CRM bloque tout envoi sans ce texte ;
3. respecte l'art. L.34-5 CPCE et la politique d'usage acceptable de la console ;
4. tient son propre registre (art. 30.1) ;
5. répond aux demandes de droits des personnes.

### Article 5 : Confidentialité

Les personnes d'Axion qui accèdent aux données sont tenues au secret. L'accès du support est limité, motivé et tracé.

### Article 6 : Sécurité (art. 32 RGPD)

Axion met en œuvre au moins : authentification à deux facteurs ; isolation des données de chaque client ; chiffrement des échanges ; sauvegarde chiffrée et restauration testée ; journal des accès ; droits par rôle ; serveur d'envoi séparé par client. Le détail figure en annexe « Sécurité ».

### Article 7 : Sous-traitants ultérieurs

1. Le Client donne une autorisation générale écrite pour les sous-traitants listés en annexe (hébergement, boîtes e-mail, vérification d'adresses, sauvegarde).
2. Axion prévient le Client **[30 jours — W-10]** avant tout ajout ou changement. Le Client peut s'y opposer pour un motif sérieux ; à défaut d'accord, il peut résilier sans frais.
3. Axion impose à chaque sous-traitant ultérieur les mêmes obligations (art. 28.4) et reste responsable envers le Client.

### Article 8 : Droits des personnes

1. Le CRM permet au Client de répondre lui-même : export, correction, opposition, mise à l'écart.
2. Si Axion reçoit une demande destinée au Client, il la lui transmet **sous 48 heures** et n'y répond pas lui-même.

### Article 9 : Aide au Client

Axion aide le Client, dans la mesure du possible, pour la sécurité, les violations, l'analyse d'impact et la consultation de la CNIL (art. 32 à 36 RGPD).

### Article 10 : Violation de données

Axion prévient le Client **sans délai excessif, et au plus tard [24 h — W-9]** après en avoir pris connaissance (art. 33.2), avec les informations utiles à la notification (art. 33.3). Axion complète ces informations dès qu'il les a. Le Client décide de notifier la CNIL et les personnes.

### Article 11 : Transferts hors Union européenne

[Choisir : « Aucun transfert hors UE. » / « Transferts vers [pays], encadrés par [garantie]. »]

### Article 12 : Audit

Axion met à disposition du Client les informations nécessaires pour prouver le respect du présent contrat. Le Client peut faire un audit, à ses frais, avec un préavis de [30 jours], au plus [une fois par an] sauf violation.

### Article 13 : Fin du contrat (art. 28.3.g RGPD)

1. À la fin du contrat, **Axion ne supprime aucune donnée de sa propre initiative.**
2. Axion fournit au Client un **export complet** de ses données, dans un format lisible et courant, dans les [30 jours] suivant la fin.
3. Axion demande au Client son choix **par écrit** : (a) suppression des données ; (b) restitution seule (l'export) puis suppression ; (c) [autre choix éventuel validé par Will].
4. **La suppression n'a lieu que sur ordre écrit du Client** (courrier signé ou e-mail du représentant légal ou du contact RGPD désigné). Axion confirme la suppression par écrit, avec la date.
5. En attendant cet ordre, les données sont **verrouillées** : plus aucun envoi, plus aucun accès utilisateur, plus aucun traitement, sauf conservation et restitution. Les sauvegardes suivent la même règle.
6. Si le droit de l'Union ou le droit français impose de garder certaines données, Axion les garde pour la durée imposée, verrouillées.
7. **Sans réponse du Client** après [deux relances écrites sur 90 jours — W-11] : [décision à prendre par Will : prolonger le verrouillage / autre]. Voir W-11 : garder sans fin des données sans instruction pose un problème de durée de conservation (art. 5.1.e RGPD).

### Article 14 : Responsabilité, durée, droit applicable

Le présent contrat suit la durée du contrat principal. Les articles 5, 10 et 13 restent applicables tant qu'Axion détient des données du Client. Droit français. [Tribunal compétent : à fixer.]

**Annexes** : 1. Sécurité ; 2. Liste des sous-traitants ultérieurs (nom, pays, rôle) ; 3. Contacts (RGPD et sécurité) des deux parties.

Fait le [DATE], en deux exemplaires. Signatures.

---

## Points que Will doit décider ou vérifier

**À vérifier sur Legifrance et EUR-Lex (avant le premier envoi)**

- **V-1** : art. 14 RGPD : la page D1-b contient bien toutes les mentions de 14.1 et 14.2 (dont l'intérêt légitime poursuivi et la source).
- **V-2** : art. 21.4 RGPD : le lien d'opposition est-il assez « clair et à part » dans D1-a et D3-a ?
- **V-3** : art. L.34-5 CPCE (dernier alinéa) : identité et moyen d'opposition, conformes dans D3.
- **V-4** : doctrine actuelle de la CNIL sur la prospection B2B par e-mail (message lié à la profession) et sur les durées de conservation des prospects.
- **V-5** : art. 12 RGPD : délais et vérification d'identité de D4.
- **V-6** : art. 28.3 RGPD, points a à h : tous présents dans D9.
- **V-7** : art. 33 et 34 RGPD : délais et contenu de D8 ; adresse du téléservice de notification de la CNIL.
- **V-8** : liste CNIL des traitements soumis à AIPD : la prospection d'Axion y est-elle ?
- **V-9** : loi Informatique et Libertés : mention des directives après décès (D1-b, point 9).
- **V-10** : art. 20 LCEN : la mention « Message de prospection professionnelle » suffit-elle ?

**À décider par Will**

- **W-1** : sources réelles à citer dans `[SOURCE]` et sur la page D1-b.
- **W-2** : délai entre l'information pure (D1-c) et le premier message de prospection (proposition : 7 jours).
- **W-3** : **durée de conservation annoncée**. La règle « aucune suppression » doit être dite honnêtement dans D1-b et D5. Texte proposé au point 8 de D1-b.
- **W-4** : **demandes d'effacement**. Quand l'effacement est dû (art. 17.1.c après une opposition), refuser peut être contraire au RGPD. Décider : effacer en gardant la seule empreinte d'opposition, ou refuser avec un motif de l'art. 17.3.
- **W-5** : envoyer ou non un e-mail de confirmation après une opposition (proposition : seulement si la personne a écrit).
- **W-6** : garder le bouton « opposition pour toute mon organisation » (D2-a).
- **W-7** : prestataires et pays de chaque sous-traitant ; transferts hors UE (oui/non).
- **W-8** : désigner ou non un délégué à la protection des données (probablement non obligatoire : à vérifier, art. 37 RGPD).
- **W-9** : délai d'alerte d'un client de la console en cas de violation (proposition : 24 h).
- **W-10** : préavis avant changement de sous-traitant ultérieur (proposition : 30 jours).
- **W-11** : fin de contrat d'un client **sans réponse** à la demande d'ordre écrit : que faire après les relances ?
- **W-12** : faire l'AIPD dès la V0 (recommandé) et remplir la grille 7.1.
- **W-13** : signer l'analyse d'intérêt légitime (D6) et fixer le seuil d'oppositions qui la fait revoir.
- **W-14** : adresse `[E-MAIL RGPD]` dédiée, et qui la lit chaque jour.

**Suite** : après validation de Will, ces textes passent au contrôleur de contenu (mots interdits), puis alimentent les lots J1 (bloc art. 14 par espace), E6 (page publique), C4 (séquences et page « pourquoi ce message »), U12 (écran des demandes RGPD) et J4 (D9 et AIPD complète en V1).
