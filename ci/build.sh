#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../tex"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
