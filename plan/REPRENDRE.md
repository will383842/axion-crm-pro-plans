# REPRENDRE : CRM Pro complet (envoi, campagnes, console) : mis à jour le 30/10/2026

## ÉTAT AU 01/11/2026 (lot W0) : à lire en premier
- Plans 20 à 29 consolidés : total **≈ 685,5 j** (plan 20 § 12), par famille : socle 157,5 ; CRM Pro 108,5 ; Envoi 419,5. Will a dit OUI aux 6 questions du plan 29 et « PARFAIT » aux maquettes M2.
- **Plan d'exécution : `plan/30-PLAN-FINAL-ET-LOTS-DE-CODE.md`** : démo frontend d'abord (19 lots DM0 à DM3), sécurité de l'existant en parallèle (R0, S1-S3, S5-S7, S9). Textes des routines prêts : `plan/lots/<id>.md` (+ `RELECTURE.md`).
- PROCHAINE ÉTAPE : lancer DM0-COL, DM0-DEMO, R0 ; puis DM0-COQ ; puis la vague 1. Lot W1 à écrire : textes de la chaîne serveur après la démo (P1 → T1, BR).
- ATTENDU DE WILL : `plan/30` § 6 (protection de `main`, S5 privé, tests de la démo, feu vert de publication, achats : jamais sans son feu vert).

## BLOC DU HAUT (relire avant d'agir)
- OBJECTIF : plan « CRM Pro complet » d'Axion-IA : d'abord CRM Pro + envoi d'e-mails pour Axion, puis version pour la console des automatisations (CRM = module de base, envoi = option, moteur partagé séparé par client, 8 règles de préparation dès le début, fichier 10 § 8).
- RIEN N'EST CODÉ. Will a demandé : aucun code tant qu'il ne donne pas son feu vert. Aucun e-mail envoyé, aucun serveur touché.
- FAIT (tout sur disque, dossier `_PLAN-CRM-PRO-COMPLET-2026-10-30\`) : 00 synthèse, 01 architecture, 02 ce qui manque, 03 module d'envoi, 04 sécurité/2FA e-mail, 05 clients/licence, 06 critique, 07 UX/UI 2027, 08 parité PowerMTA/MailWizz, 09 systeme.io (REJETÉ), 10 liste complète et équipe, 11 inventaire SOS-Expat. Audits : `_AUDIT-CRM-PRO-ENVOI-MASSE-2026-10-30\` et `_AUDIT-SOS-EXPAT-REPRISE-2026-10-30\`.
- EN COURS (6 responsables Opus lancés le 30/10, sessions locales, livrables à venir dans le même dossier) : 12 vérif UI écran par écran ; 13 envoi et infrastructure ; 14 sécurité et isolation ; 15 conformité ; 16 campagnes et CRM ; 17 exécution cloud et calendrier. Si un fichier manque au retour de session : relancer l'agent correspondant avec le même sujet (les consignes sont dans la conversation du 30/10 ; sinon refaire à partir du § ci-dessus).
- PROCHAINE ÉTAPE : quand 12 à 17 sont là : consolider un PLAN CORRIGÉ unique (un seul total de jours, calendrier, tous les ajouts), puis critique-completude, puis poser à Will les questions une à une avec une recommandation.
- DÉCISIONS DE WILL : commencer petit en VOLUMES seulement ; complet en fonctions ; campagnes au cœur ; KumoMTA (pas PowerMTA ni MailWizz), repli Postfix+rspamd ; 2FA par e-mail ; Axion d'abord puis console ; AUCUN lien avec systeme.io et les 6 ajouts rejetés ; UI parfaite, moderne, peu de texte, CTA clairs, début 2027 ; alertes console + e-mail, PAS de téléphone/Telegram (24/10 maintenu, ma lecture de sa phrase du 30/10 à reconfirmer) ; implémentation rapide en cloud, GitHub public par lots sans file ; pause si mémoire du PC sous 1 Go.
- ATTENDU DE WILL : décisions listées dans `10-liste-complete-et-equipe.md` et `06-critique-completude-du-plan.md` § 5 (15 questions) ; rotation des clés ; achats de domaines et comptes (fichier 10 § 10) ; confirmer mode sombre = non, Telegram éteint, licence du code, fin de contrat client.
- RÈGLES DE FER : relire `C:\Users\willi\Documents\Projets\Axion-IA\_OPTIM-CONSO\REGLES-SOCLE.md` et `REGLES-AXION.md`.
- MÉMOIRE PC : au 30/10 la mémoire libre était de 1,59 Go. Sous 1 Go : tout mettre en pause et prévenir Will. Sous 2 Go : rien de lourd.

## PAUSE du 30/10/2026 (ordre de Will : « mets en pause »)
Les 6 responsables (fichiers 12 à 17) ont été ARRÊTÉS avant d'écrire leur livrable : aucun des fichiers 12 à 17 n'existe. Rien n'est perdu côté plan (00 à 11 intacts). REPRISE : relancer les 6 agents Opus avec les consignes de la conversation du 30/10 (UI écran par écran ; envoi et infrastructure ; sécurité et isolation ; conformité ; campagnes et CRM ; exécution cloud et calendrier), puis consolider le plan corrigé. Rien n'est lancé tant que Will ne dit pas de reprendre.
