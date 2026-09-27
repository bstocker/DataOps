#!/usr/bin/env bash
# Étudiant :    ./verifier.sh 2                  vérifie l'atelier 2
#               ./verifier.sh tout               vérifie tout et affiche la note automatique
# Enseignant :  ./verifier.sh etudiants          corrige tous les forks et crée prof/notes.csv
#               ./verifier.sh etudiant <pseudo>  corrige le fork d'un étudiant et affiche le détail
cd "$(dirname "$0")" || exit 1
export MLFLOW_DISABLE_AGENT_HINT=1

case "$1" in
  etudiants)
    shift
    python prof/noter_forks.py "$@"
    ;;
  etudiant)
    if [ -z "$2" ]; then
      echo "Précisez le pseudo GitHub de l'étudiant :  ./verifier.sh etudiant <pseudo>"
      exit 1
    fi
    pseudo="$2"
    shift 2
    python prof/noter_forks.py --etudiant "$pseudo" "$@" && \
      [ -f "prof/_forks/$pseudo.txt" ] && cat "prof/_forks/$pseudo.txt"
    ;;
  *)
    python -m verif "$@"
    ;;
esac
