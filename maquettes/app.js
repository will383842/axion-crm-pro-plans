/* Axion CRM Pro : comportements des maquettes (code maison, aucune bibliothèque). */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function lire(cle) { try { return window.sessionStorage.getItem(cle); } catch (e) { return null; } }
  function ecrire(cle, val) { try { if (val === null) { window.sessionStorage.removeItem(cle); } else { window.sessionStorage.setItem(cle, val); } } catch (e) { /* stockage indisponible : sans effet */ } }

  /* ---------- Toast (annoncé par aria-live) ---------- */
  var zoneToasts = $('#toasts');
  function toast(texte, annulable) {
    if (!zoneToasts) { return; }
    var t = document.createElement('div');
    t.className = 'toast';
    t.setAttribute('role', 'status');
    var s = document.createElement('span'); s.textContent = texte; t.appendChild(s);
    var duree = 6000;
    if (annulable) {
      duree = 8000;
      var b = document.createElement('button'); b.type = 'button'; b.textContent = 'Annuler';
      b.addEventListener('click', function () { t.remove(); toast('Action annulée.'); });
      t.appendChild(b);
    }
    zoneToasts.appendChild(t);
    var minuteur = setTimeout(function () { t.remove(); }, duree);
    // Le toast reste tant qu'il a la souris ou le focus (WCAG 2.2.1).
    t.addEventListener('mouseenter', function () { clearTimeout(minuteur); });
    t.addEventListener('focusin', function () { clearTimeout(minuteur); });
    t.addEventListener('mouseleave', function () { minuteur = setTimeout(function () { t.remove(); }, 3000); });
  }
  document.addEventListener('click', function (ev) {
    var el = ev.target.closest('[data-toast]');
    if (el) {
      if (el.tagName === 'A' && el.getAttribute('href') === '#') { ev.preventDefault(); }
      toast(el.getAttribute('data-toast'), el.hasAttribute('data-annulable'));
    }
  });

  /* ---------- Barre latérale : groupes repliables + tiroir mobile ---------- */
  /* Menu en accordéon, comme le vrai menu : une seule section ouverte à la fois. */
  var titres = $$('.groupe-titre');
  titres.forEach(function (b) {
    b.addEventListener('click', function () {
      var ouvrir = b.getAttribute('aria-expanded') !== 'true';
      titres.forEach(function (x) { x.setAttribute('aria-expanded', 'false'); $('#' + x.getAttribute('aria-controls')).hidden = true; });
      if (ouvrir) { b.setAttribute('aria-expanded', 'true'); $('#' + b.getAttribute('aria-controls')).hidden = false; }
    });
  });
  var barre = $('.barre'), boutonMenu = $('.bouton-menu'), voile = null;
  function fermerMenu() {
    if (!barre) { return; }
    barre.classList.remove('ouverte');
    if (voile) { voile.remove(); voile = null; }
    if (boutonMenu) { boutonMenu.setAttribute('aria-expanded', 'false'); boutonMenu.focus(); }
  }
  if (boutonMenu && barre) {
    boutonMenu.addEventListener('click', function () {
      barre.classList.add('ouverte');
      boutonMenu.setAttribute('aria-expanded', 'true');
      voile = document.createElement('div'); voile.className = 'voile';
      voile.addEventListener('click', fermerMenu);
      document.body.appendChild(voile);
      var premier = $('.nav-lien', barre); if (premier) { premier.focus(); }
    });
  }

  /* ---------- États de la maquette : normal / vide / erreur / chargement ---------- */
  var etats = ['normal', 'vide', 'erreur', 'chargement'];
  function appliquerEtat(etat) {
    if (etats.indexOf(etat) < 0) { etat = 'normal'; }
    var aDesEtats = $$('[data-etat]').length > 0;
    $$('[data-etat]').forEach(function (s) { s.hidden = (s.getAttribute('data-etat') !== etat); });
    $$('[data-seulement]').forEach(function (s) { s.hidden = s.getAttribute('data-seulement').split(' ').indexOf(etat) < 0; });
    var sq = $('#squelette'); if (sq) { sq.hidden = (etat !== 'chargement') || !aDesEtats; }
    var main = $('#contenu'); if (main) { main.setAttribute('aria-busy', String(etat === 'chargement')); }
    $$('.selecteur-etat input').forEach(function (i) { i.checked = (i.value === etat); });
    try {
      var url = new URL(window.location.href);
      if (etat === 'normal') { url.searchParams.delete('etat'); } else { url.searchParams.set('etat', etat); }
      window.history.replaceState(null, '', url.toString());
    } catch (e) { /* ouverture en fichier local sans URL modifiable : sans effet */ }
  }
  $$('.selecteur-etat input').forEach(function (i) { i.addEventListener('change', function () { appliquerEtat(i.value); }); });
  var etatDemande = 'normal';
  try { etatDemande = new URL(window.location.href).searchParams.get('etat') || 'normal'; } catch (e) { /* rien */ }
  appliquerEtat(etatDemande);
  document.addEventListener('click', function (ev) {
    var r = ev.target.closest('[data-reessayer]');
    if (r) { appliquerEtat('chargement'); setTimeout(function () { appliquerEtat('normal'); toast('Données rechargées.'); }, 900); }
  });

  /* ---------- Onglets (flèches gauche/droite, Début, Fin) ---------- */
  $$('[role="tablist"]').forEach(function (liste) {
    var tabs = $$('[role="tab"]', liste);
    function choisir(t, focus) {
      tabs.forEach(function (x) {
        var actif = x === t;
        x.setAttribute('aria-selected', String(actif));
        x.tabIndex = actif ? 0 : -1;
        var p = document.getElementById(x.getAttribute('aria-controls')); if (p) { p.hidden = !actif; }
      });
      if (focus) { t.focus(); }
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { choisir(t, false); });
      t.addEventListener('keydown', function (ev) {
        var j = null;
        if (ev.key === 'ArrowRight') { j = (i + 1) % tabs.length; }
        if (ev.key === 'ArrowLeft') { j = (i - 1 + tabs.length) % tabs.length; }
        if (ev.key === 'Home') { j = 0; }
        if (ev.key === 'End') { j = tabs.length - 1; }
        if (j !== null) { ev.preventDefault(); choisir(tabs[j], true); }
      });
    });
    var initial = tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0];
    if (initial) { choisir(initial, false); }
  });

  /* ---------- Puces de filtre ---------- */
  $$('.filtres').forEach(function (f) {
    $$('.puce', f).forEach(function (p) {
      p.addEventListener('click', function () {
        if (f.hasAttribute('data-unique')) { $$('.puce', f).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); p.setAttribute('aria-pressed', 'true'); }
        else { p.setAttribute('aria-pressed', String(p.getAttribute('aria-pressed') !== 'true')); }
      });
    });
  });

  /* ---------- Fenêtres et tiroirs (dialog natif : focus piégé, Échap) ---------- */
  document.addEventListener('click', function (ev) {
    var o = ev.target.closest('[data-ouvre]');
    if (o) {
      ev.preventDefault();
      var d = document.getElementById(o.getAttribute('data-ouvre'));
      if (d && typeof d.showModal === 'function') { d.showModal(); }
    }
    var f = ev.target.closest('[data-ferme]');
    if (f) { var dd = f.closest('dialog'); if (dd) { dd.close(); } }
  });
  $$('dialog').forEach(function (d) {
    d.addEventListener('click', function (ev) { if (ev.target === d) { d.close(); } });
  });

  /* ---------- Tout arrêter : bandeau rouge persistant pendant la visite ---------- */
  function majArret() {
    var b = $('#bandeau-arret'); if (!b) { return; }
    var actif = lire('arret') === 'oui';
    b.hidden = !actif;
    var feu = $('.feu-entete');
    if (feu) {
      feu.style.background = actif ? '#b91c1c' : '';
      feu.style.color = actif ? '#ffffff' : '';
      var mot = $('.mot-feu', feu); if (mot) { mot.textContent = actif ? 'Envois : arrêtés' : 'Envois : normaux'; }
      feu.setAttribute('aria-label', actif ? 'État des envois : arrêtés' : 'État des envois : normaux');
    }
  }
  document.addEventListener('click', function (ev) {
    if (ev.target.closest('[data-arreter]')) { ecrire('arret', 'oui'); majArret(); toast('Tous les envois sont arrêtés.'); }
    if (ev.target.closest('[data-reprendre]')) { ecrire('arret', null); majArret(); toast('Les envois reprennent.'); }
  });
  majArret();

  /* ---------- Centre d'alertes (cloche) ---------- */
  var cloche = $('#bouton-cloche'), panneau = $('#panneau-alertes');
  function fermerPanneau() { if (panneau && !panneau.hidden) { panneau.hidden = true; cloche.setAttribute('aria-expanded', 'false'); } }
  if (cloche && panneau) {
    cloche.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var ouvrir = panneau.hidden;
      panneau.hidden = !ouvrir;
      cloche.setAttribute('aria-expanded', String(ouvrir));
      if (ouvrir) { var l = $('a, button', panneau); if (l) { l.focus(); } }
    });
    document.addEventListener('click', function (ev) { if (!panneau.contains(ev.target)) { fermerPanneau(); } });
  }

  /* ---------- Palette (Ctrl K) ---------- */
  var palette = $('#palette'), champPal = $('#palette-champ');
  function ouvrirPalette() { if (palette && !palette.open) { palette.showModal(); champPal.value = ''; filtrer(''); champPal.focus(); } }
  function filtrer(q) {
    q = q.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    $$('#palette-liste li').forEach(function (li) {
      if (li.classList.contains('groupe-pal')) { return; }
      var t = li.textContent.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
      li.hidden = q !== '' && t.indexOf(q) < 0;
    });
  }
  if (champPal) {
    champPal.addEventListener('input', function () { filtrer(champPal.value); });
    champPal.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') { ev.preventDefault(); var a = $$('#palette-liste li:not([hidden]) a')[0]; if (a) { a.focus(); } }
    });
    $('#palette-liste').addEventListener('keydown', function (ev) {
      var liens = $$('#palette-liste li:not([hidden]) a');
      var i = liens.indexOf(document.activeElement);
      if (ev.key === 'ArrowDown' && i < liens.length - 1) { ev.preventDefault(); liens[i + 1].focus(); }
      if (ev.key === 'ArrowUp') { ev.preventDefault(); if (i > 0) { liens[i - 1].focus(); } else { champPal.focus(); } }
    });
  }
  $$('[data-palette]').forEach(function (b) { b.addEventListener('click', ouvrirPalette); });

  /* ---------- Raccourcis clavier (désactivables dans Mon compte) ---------- */
  var attenteG = false;
  document.addEventListener('keydown', function (ev) {
    if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === 'k') { ev.preventDefault(); ouvrirPalette(); return; }
    if (ev.key === 'Escape') { fermerPanneau(); if (barre && barre.classList.contains('ouverte')) { fermerMenu(); } return; }
    var cible = ev.target;
    if (cible.closest('input, textarea, select, [contenteditable]') || ev.ctrlKey || ev.metaKey || ev.altKey) { return; }
    if (lire('raccourcis') === 'non') { return; }
    if (attenteG) {
      attenteG = false;
      var dest = { a: 'index.html', r: 'reponses.html', c: 'campagnes.html', f: 'affaires.html', t: 'taches.html', s: 'sante.html', e: 'entreprises.html' }[ev.key.toLowerCase()];
      if (dest) { window.location.href = dest; }
      return;
    }
    if (ev.key.toLowerCase() === 'g') { attenteG = true; setTimeout(function () { attenteG = false; }, 1200); }
    if (ev.key === '/') { ev.preventDefault(); ouvrirPalette(); }
  });

  /* ---------- Lignes de tableau cliquables (le lien de la 1re cellule reste la voie clavier) ---------- */
  document.addEventListener('click', function (ev) {
    var tr = ev.target.closest('tr[data-href]');
    if (tr && !ev.target.closest('a, button, input, select, label, textarea')) { window.location.href = tr.getAttribute('data-href'); }
  });

  /* ---------- Assistant à étapes ---------- */
  var COCHE = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  $$('[data-assistant]').forEach(function (a) {
    var panneaux = $$('[data-etape]', a), boutons = $$('.frise button', a);
    function aller(n) {
      panneaux.forEach(function (p) { p.hidden = p.getAttribute('data-etape') !== String(n); });
      boutons.forEach(function (b, i) {
        if (i + 1 === n) { b.setAttribute('aria-current', 'step'); } else { b.removeAttribute('aria-current'); }
        b.classList.toggle('fait', i + 1 < n);
        var rond = $('.n', b);
        if (rond) { rond.innerHTML = i + 1 < n ? COCHE : String(i + 1); }
      });
      var titre = $('[data-etape="' + n + '"] h2', a); if (titre) { titre.setAttribute('tabindex', '-1'); titre.focus(); }
    }
    boutons.forEach(function (b, i) { b.addEventListener('click', function () { aller(i + 1); }); });
    a.addEventListener('click', function (ev) { var x = ev.target.closest('[data-aller]'); if (x) { aller(parseInt(x.getAttribute('data-aller'), 10)); } });
    panneaux.forEach(function (p, i) { p.hidden = i !== 0; });
  });

  /* ---------- Code à 6 chiffres : collage et avance automatique ---------- */
  $$('.cases-code').forEach(function (g) {
    var cases = $$('input', g);
    cases.forEach(function (c, i) {
      c.addEventListener('input', function () { c.value = c.value.replace(/\D/g, '').slice(0, 1); if (c.value && cases[i + 1]) { cases[i + 1].focus(); } });
      c.addEventListener('keydown', function (ev) { if (ev.key === 'Backspace' && !c.value && cases[i - 1]) { cases[i - 1].focus(); } });
      c.addEventListener('paste', function (ev) {
        var t = (ev.clipboardData || window.clipboardData).getData('text').replace(/\D/g, '').slice(0, 6);
        if (t.length) { ev.preventDefault(); t.split('').forEach(function (ch, k) { if (cases[k]) { cases[k].value = ch; } }); (cases[t.length] || cases[5]).focus(); }
      });
    });
  });

  /* ---------- Affaires : « Déplacer vers… » (alternative au glisser-déposer) ---------- */
  $$('select[data-deplacer]').forEach(function (s) {
    s.addEventListener('change', function () {
      if (!s.value) { return; }
      var carte = s.closest('.carte-affaire'), col = document.getElementById(s.value);
      if (carte && col) { $('.cartes-col', col).appendChild(carte); toast('Affaire déplacée vers « ' + $('h2 span', col).textContent + ' ».', true); }
      s.value = '';
      s.focus();
    });
  });

  /* ---------- Ne plus écrire : « Puis-je écrire à… ? » ---------- */
  var formVerif = $('#form-verifier');
  if (formVerif) {
    formVerif.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var v = $('#adresse-verif').value.trim().toLowerCase(), r = $('#resultat-verif');
      if (!v) { r.innerHTML = '<p class="petit">Saisissez une adresse e-mail ou un domaine.</p>'; return; }
      var non = /paul@boulangerie-tilleuls|garage-saules/.test(v);
      r.innerHTML = non
        ? '<div class="verdict teinte-terracotta bloc"><strong>Non.</strong> Désinscription le 12 oct. 2026 (lien dans le message). Définitif.</div>'
        : '<div class="verdict teinte-vert bloc"><strong>Oui.</strong> Aucune opposition, aucune désinscription, adresse vérifiée il y a 9 jours.</div>';
    });
  }
})();
