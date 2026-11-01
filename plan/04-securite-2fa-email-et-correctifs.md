# 04 : 2FA par e-mail et correctifs de sécurité du CRM Pro (plan du 30/10/2026)

Version condensée du plan du concepteur sécurité (lecture seule, aucun code écrit, constats d'agent non rejoués). Chemins relatifs à `C:\Users\willi\Documents\Projets\Axion-CRM-Pro\`.

## URGENT hors mission (à décider par Will)

## Constats confirmés par le concepteur (avec chemins)
- Protection de main (lue le 30/10) : 4 contrôles exigés ; gitleaks/semgrep non exigés.

## Solution retenue

## Plan en PR courtes (tests Pest écrits d'abord, rouges avant le correctif) : RIEN N'EST CODÉ
- PR-0 : fermer C1 tout de suite (409 sur setup/confirm si la 2FA est active ; retirer les deux routes de la liste blanche ; anti-rejeu TOTP).
- PR-C : mailer `auth` isolé (variables MAIL_AUTH_*), test qui interdit toute dérive commerciale vers Mail::, MAIL_MAILER_AUTH=auth.
- PR-D : 2FA e-mail backend (migration additive two_factor_email_codes, service, contrôleur, routes avec limiteurs, middlewares, RGPD, commande de secours crm:2fa:reinitialiser, 16 tests).
- PR-E : front (page de saisie du code, renvoi, codes de secours une seule fois).
- PR-F (facultatif, 2 semaines plus tard) : retirer le code TOTP.
- Protection de main : exiger en plus Gitleaks et Semgrep (gratuit, dépôt public) ; ne pas exiger Trivy ni ZAP (jamais lancés sur une PR, ils bloqueraient tout).

## Pièges

## Décisions pour Will
1. Lien magique : l'éteindre quand la 2FA e-mail est active (recommandé) ou le garder.
2. Expéditeur : crm@axion-ia.com sur l'agent dédié (recommandé si le domaine est vérifié) ou noreply@axion-crm-pro.com (demande SPF/DKIM dans Cloudflare).
3. Garder les 10 codes de secours.
4. Garder les paramètres : 10 min, 5 essais, verrou 1 h après 15 échecs, 2FA valable 12 h.
6. Contrôles exigés sur main : Gitleaks et Semgrep seulement (recommandé) ou aussi les audits de dépendances.
