"""Outils communs du vérificateur : affichage, lecture du RENDU, accès à Git et GitHub."""
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DEPOT_ENSEIGNANT = "bstocker/DataOps"
ATTENDUS = json.loads((Path(__file__).parent / "attendus.json").read_text(encoding="utf-8"))

COULEUR = sys.stdout.isatty() or os.environ.get("GITHUB_ACTIONS") == "true"
if os.environ.get("NO_COLOR"):
    COULEUR = False


def _c(code, texte):
    return f"\033[{code}m{texte}\033[0m" if COULEUR else texte


def vert(t): return _c("32", t)
def rouge(t): return _c("31", t)
def jaune(t): return _c("33", t)
def gras(t): return _c("1", t)


def mode_ci():
    return os.environ.get("GITHUB_ACTIONS") == "true"


def mode_prof():
    return os.environ.get("VERIF_MODE") == "prof"


class Atelier:
    """Regroupe les vérifications d'un atelier et calcule ses points."""

    def __init__(self, numero, titre, bareme):
        self.numero, self.titre, self.bareme = numero, titre, bareme
        self.lignes = []  # (statut, message, indice, points, points_max)

    def ok(self, message, points=0):
        self.lignes.append(("ok", message, None, points, points))

    def ko(self, message, indice=None, points_max=0, points=0):
        self.lignes.append(("ko", message, indice, points, points_max))

    def info(self, message):
        self.lignes.append(("info", message, None, 0, 0))

    @property
    def points(self):
        return min(self.bareme, round(sum(l[3] for l in self.lignes) * 2) / 2)

    @property
    def reussi(self):
        return all(l[0] != "ko" for l in self.lignes)

    def afficher(self):
        print()
        print(gras(f"━━━ Atelier {self.numero} — {self.titre} ━━━"))
        for statut, message, indice, pts, pts_max in self.lignes:
            bareme = f"  ({fmt(pts)}/{fmt(pts_max)} pt)" if pts_max else ""
            if statut == "ok":
                print(f"  ✅ {message}{bareme}")
            elif statut == "ko":
                print(f"  ❌ {rouge(message)}{bareme}")
                if indice:
                    premiere, *suite = indice.splitlines()
                    print(f"     {jaune('💡 ' + premiere)}")
                    for ligne in suite:
                        print(f"        {jaune(ligne)}")
            else:
                print(f"  ℹ️  {message}")
        if self.bareme:
            print(gras(f"  Score : {fmt(self.points)} / {fmt(self.bareme)}"))
        if self.reussi:
            print(vert(f"  🎉 Atelier {self.numero} validé !"))


def fmt(x):
    return f"{x:g}"


def lire_rendu():
    """Lit les tableaux du RENDU.md : lignes de la forme  | 1.2 | question | réponse |"""
    chemin = RACINE / "RENDU.md"
    reponses = {}
    if not chemin.exists():
        return reponses
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(\d+\.\d+)\s*\|[^|]*\|(.*)\|\s*$", ligne)
        if m:
            reponses[m.group(1)] = m.group(2).strip()
    return reponses


def nombre(texte):
    m = re.search(r"-?\d+(?:[.,]\d+)?", texte or "")
    return float(m.group(0).replace(",", ".")) if m else None


def empreinte(cle, valeur):
    return hashlib.sha256(f"{cle}:{valeur}".encode()).hexdigest()[:16]


def git(*args):
    r = subprocess.run(["git", *args], cwd=RACINE, capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout.strip()


def depot_github():
    """Renvoie "proprietaire/depot" du dépôt de l'étudiant."""
    depot = os.environ.get("VERIF_DEPOT") or os.environ.get("GITHUB_REPOSITORY")
    if depot:
        return depot
    code, url = git("remote", "get-url", "origin")
    m = re.search(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$", url) if code == 0 else None
    return m.group(1) if m else None


def api_github(chemin):
    """Interroge l'API GitHub (avec le jeton s'il existe, sinon sans : le dépôt est public)."""
    jeton = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    for avec_jeton in ([True, False] if jeton else [False]):
        requete = urllib.request.Request(f"https://api.github.com{chemin}",
                                         headers={"Accept": "application/vnd.github+json"})
        if avec_jeton:
            requete.add_header("Authorization", f"Bearer {jeton}")
        try:
            with urllib.request.urlopen(requete, timeout=20) as reponse:
                return json.loads(reponse.read())
        except urllib.error.HTTPError as e:
            if not (avec_jeton and e.code in (401, 403, 404)):
                raise


def lancer(commande, timeout=300, env=None):
    """Lance une commande depuis la racine du dépôt. Renvoie (code_retour, sortie)."""
    env_complet = {**os.environ, **(env or {})}
    try:
        r = subprocess.run(commande, cwd=RACINE, capture_output=True, text=True,
                           timeout=timeout, env=env_complet)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return -1, f"Délai dépassé ({timeout} s)"
    except FileNotFoundError as e:
        return -2, str(e)


def derniere_erreur(sortie, n=4):
    lignes = [l if len(l) <= 160 else l[:157] + "..." for l in sortie.strip().splitlines() if l.strip()]
    return "\n".join(lignes[-n:])
