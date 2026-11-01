# -*- coding: utf-8 -*-
"""Contrôle visuel automatique des maquettes (lot U1bis).

Ouvre les pages dans Chromium (Playwright) à 1440, 1024, 768 et 360 px de large,
dans chaque état (normal, vide, erreur, chargement), chaque onglet et chaque étape
d'assistant, puis vérifie :
  1. CHEVAUCHEMENT : deux éléments frères visibles dont les rectangles se recouvrent ;
  2. DÉBORDEMENT : page plus large que l'écran, élément qui sort de l'écran,
     contenu qui dépasse de sa boîte, ou défilement horizontal interne imprévu ;
  3. CONTRASTE : texte sous 4,5:1 (3:1 pour le gros texte) sur son fond réel ;
  4. TAILLE : texte sous 16 px hors pastilles et étiquettes (jamais sous 14 px) ;
  5. BOUTON PLEIN : plus d'un bouton plein visible à la fois.
Sort avec le code 1 s'il reste un problème.

Usage :
    pip install playwright        (Chromium déjà présent : /opt/pw-browsers/chromium)
    python3 maquettes/_fabrique/controle.py               # 8 pages clés + captures légères
    python3 maquettes/_fabrique/controle.py --toutes      # toutes les pages (sans captures)
    option --largeur=1440 : une seule largeur (pour lancer les 4 largeurs en parallèle)
    python3 maquettes/_fabrique/controle.py index.html    # une page
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
MAQ = os.path.dirname(ICI)
CAPTURES = os.path.join(MAQ, 'captures')
REPERES = ['index.html', 'medias.html', 'entreprises.html', 'etiquettes.html', 'campagnes.html', 'campagne-suivi.html', 'reponses.html', 'domaine.html']
LARGEURS = [1440, 1024, 768, 360]
ETATS = ['normal', 'vide', 'erreur', 'chargement']

JS = r"""
() => {
  window.scrollTo(0, 0);  // l'en-tête collant (seul sticky permis) ne doit rien recouvrir en haut de page
  const pb = [];
  const W = window.innerWidth;
  const nom = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    const c = (typeof el.className === 'string' ? el.className : '').trim().split(/\s+/).filter(Boolean).slice(0, 2);
    if (c.length) s += '.' + c.join('.');
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 28);
    return t ? s + ' « ' + t + ' »' : s;
  };
  const ferme = (el) => { const d = el.closest('dialog'); return d && !d.open; };
  const visible = (el) => {
    if (ferme(el)) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1;
  };
  // Masqué pour l'œil mais lu par les lecteurs d'écran (boîte de 1 px qui coupe son contenu)
  const minuscules = Array.from(document.querySelectorAll('body *')).filter(e => { const r = e.getBoundingClientRect(); return r.width <= 1 && r.height <= 1 && getComputedStyle(e).overflow === 'hidden'; });
  const cache = (el) => el.classList.contains('visuellement-cache') || !!el.closest('.visuellement-cache') || minuscules.some(m => m.contains(el));
  const surgit = (el) => { const p = getComputedStyle(el).position; return p === 'fixed'; };
  const tous = Array.from(document.querySelectorAll('body *')).filter(el => !el.closest('svg') || el.tagName === 'svg');
  const vis = new Set(tous.filter(visible));
  const SAUTE = new Set(['SCRIPT', 'STYLE', 'OPTION', 'BR', 'TEMPLATE', 'LEGEND']);

  // 1. Chevauchements entre frères
  for (const parent of [document.body, ...tous]) {
    if (parent !== document.body && !vis.has(parent)) continue;
    if (parent.tagName === 'svg') continue;
    const kids = Array.from(parent.children).filter(k => vis.has(k) && !SAUTE.has(k.tagName) && !cache(k) && !surgit(k));
    if (kids.length < 2) continue;
    const rects = kids.map(k => Array.from(k.getClientRects()));
    for (let i = 0; i < kids.length; i++) for (let j = i + 1; j < kids.length; j++) {
      let trouve = false;
      for (const a of rects[i]) { for (const b of rects[j]) {
        const x = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const y = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (x > 1.5 && y > 1.5) { trouve = true; break; }
      } if (trouve) break; }
      if (trouve) pb.push(['chevauchement', nom(kids[i]) + '  ×  ' + nom(kids[j])]);
    }
  }

  // 2. Débordements
  const de = document.documentElement;
  if (de.scrollWidth > W + 1) pb.push(['débordement', 'page plus large que l’écran : ' + de.scrollWidth + ' px pour ' + W + ' px']);
  const coupe = (el) => {
    for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
      const o = getComputedStyle(a).overflowX;
      if (o !== 'visible') return true;
    }
    return false;
  };
  const DEFILE_PERMIS = '.onglets, .colonnes, .palette ul';
  for (const el of vis) {
    if (cache(el) || surgit(el) || el.closest('dialog')) continue;
    const r = el.getBoundingClientRect();
    if ((r.right > W + 1 || r.left < -1) && !coupe(el)) pb.push(['débordement', nom(el) + ' sort de l’écran (' + Math.round(r.left) + ' → ' + Math.round(r.right) + ')']);
    const cs = getComputedStyle(el);
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0 && !['INPUT', 'SELECT', 'TEXTAREA', 'svg'].includes(el.tagName)) {
      if (cs.overflowX === 'visible' && cs.display !== 'inline' && cs.display !== 'table-cell' && cs.display !== 'table') pb.push(['débordement', nom(el) + ' : contenu plus large que la boîte (' + el.scrollWidth + ' > ' + el.clientWidth + ')']);
      else if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && !el.matches(DEFILE_PERMIS)) pb.push(['débordement', nom(el) + ' : défilement horizontal interne (' + el.scrollWidth + ' > ' + el.clientWidth + ')']);
    }
  }

  // 3 et 4. Contraste et taille du texte
  const rgba = (s) => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return [0, 0, 0, 0]; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const melange = (haut, bas) => { const a = haut[3]; return [haut[0] * a + bas[0] * (1 - a), haut[1] * a + bas[1] * (1 - a), haut[2] * a + bas[2] * (1 - a), 1]; };
  const fond = (el) => {
    const pile = [];
    for (let a = el; a; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
      const c = rgba(cs.backgroundColor);
      if (c[3] > 0) { pile.push(c); if (c[3] >= 1) break; }
    }
    let f = [255, 255, 255, 1];
    for (let i = pile.length - 1; i >= 0; i--) f = melange(pile[i], f);
    return f;
  };
  const PETIT_PERMIS = '.badge, .compteur, kbd, .touche, .mot, .repere-v1, .pastille, .nb, thead, .sequence .jour, .groupe-titre, .selecteur-etat legend, .groupe-pal, .mini-titre, .etiquette-paire, .tag-produit, .operateur';
  for (const el of vis) {
    if (cache(el)) continue;
    const texte = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
    if (!texte) continue;
    const cs = getComputedStyle(el);
    const taille = parseFloat(cs.fontSize), gras = parseInt(cs.fontWeight, 10) >= 700;
    if (taille < 14 || (taille < 16 && !el.closest(PETIT_PERMIS))) pb.push(['taille', nom(el) + ' : ' + taille + ' px']);
    const f = fond(el);
    if (!f) continue;
    const c = melange(rgba(cs.color), f);
    const l1 = lum(c), l2 = lum(f);
    const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    const gros = taille >= 24 || (taille >= 18.66 && gras);
    if (ratio < (gros ? 3 : 4.5)) pb.push(['contraste', nom(el) + ' : ' + ratio.toFixed(2) + ':1']);
  }

  // 5. Un seul bouton plein visible
  const pleins = Array.from(document.querySelectorAll('.btn-plein')).filter(b => vis.has(b));
  if (pleins.length > 1) pb.push(['bouton plein', pleins.length + ' boutons pleins visibles : ' + pleins.map(nom).join(' | ')]);
  for (const b of pleins) { if (b.getBoundingClientRect().height < 47.5) pb.push(['bouton plein', nom(b) + ' : moins de 48 px de haut']); }
  return pb;
}
"""


def lancer(pages, captures):
    from playwright.sync_api import sync_playwright
    if captures:
        os.makedirs(CAPTURES, exist_ok=True)
    problemes = []
    nb_vues = 0
    chemin = '/opt/pw-browsers/chromium'
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=chemin if os.path.exists(chemin) else None)
        for largeur in LARGEURS:
            ctx = nav.new_context(viewport={'width': largeur, 'height': 900 if largeur >= 768 else 780}, reduced_motion='reduce')
            pg = ctx.new_page()
            erreurs_js = []
            pg.on('pageerror', lambda e: erreurs_js.append(str(e)))
            for fichier in pages:
                url = 'file://' + os.path.join(MAQ, fichier)
                for etat in ETATS:
                    pg.goto(url + ('' if etat == 'normal' else '?etat=' + etat))
                    pg.wait_for_timeout(60)
                    vues = [('%s' % etat, None)]
                    if etat == 'normal':
                        # chaque onglet (role=tab) et chaque étape d'assistant
                        nb_tabs = pg.locator('[role="tab"]:visible').count()
                        vues += [('onglet %d' % (i + 1), ('tab', i)) for i in range(1, nb_tabs)]
                        nb_et = pg.locator('[data-assistant] .frise button:visible').count()
                        vues += [('étape %d' % (i + 1), ('etape', i)) for i in range(1, nb_et)]
                    for libelle, action in vues:
                        if action:
                            pg.goto(url)
                            pg.wait_for_timeout(40)
                            sel = '[role="tab"]:visible' if action[0] == 'tab' else '[data-assistant] .frise button:visible'
                            pg.locator(sel).nth(action[1]).click(timeout=3000)
                            pg.wait_for_timeout(40)
                        nb_vues += 1
                        for sorte, detail in pg.evaluate(JS):
                            problemes.append((fichier, largeur, libelle, sorte, detail))
                    if captures and etat == 'normal':
                        pg.goto(url)
                        pg.wait_for_timeout(60)
                        cible = os.path.join(CAPTURES, '%s-%d.png' % (fichier[:-5], largeur))
                        pg.screenshot(path=cible, full_page=True)
                        alleger(cible)
            for e in erreurs_js:
                problemes.append(('(script)', largeur, '-', 'erreur JS', e))
            ctx.close()
        nav.close()
    return problemes, nb_vues


def alleger(chemin):
    """Réduit la capture à 48 couleurs (PNG léger) si Pillow est présent."""
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(chemin).convert('RGB')
    im.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(chemin, optimize=True)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    toutes = '--toutes' in sys.argv
    if toutes:
        pages = sorted(f for f in os.listdir(MAQ) if f.endswith('.html'))
    else:
        pages = args or REPERES
    captures = not toutes and not args and '--sans-captures' not in sys.argv
    global LARGEURS
    for a in sys.argv:
        if a.startswith('--largeur='):
            LARGEURS = [int(a.split('=')[1])]
    problemes, nb_vues = lancer(pages, captures)
    vus = set()
    par_sorte = {}
    for fichier, largeur, vue, sorte, detail in problemes:
        cle = (fichier, sorte, detail)
        par_sorte[sorte] = par_sorte.get(sorte, 0) + 1
        if cle in vus:
            continue
        vus.add(cle)
        print('%-24s %5d px  %-12s %-14s %s' % (fichier, largeur, vue, sorte, detail))
    print('---')
    print('%d pages, %d largeurs, %d vues contrôlées.' % (len(pages), len(LARGEURS), nb_vues))
    for s in ['chevauchement', 'débordement', 'contraste', 'taille', 'bouton plein', 'erreur JS']:
        print('  %-14s : %d' % (s, par_sorte.get(s, 0)))
    if captures:
        print('Captures : %s' % os.path.relpath(CAPTURES, os.path.dirname(MAQ)))
    sys.exit(1 if problemes else 0)


if __name__ == '__main__':
    main()
