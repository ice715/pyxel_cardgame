#!/bin/bash

cd .. 
pyxel package cardgame_pyxel cardgame_pyxel/cardgame.py
mv cardgame_pyxel.pyxapp cardgame_pyxel/app3.pyxapp

cd cardgame_pyxel

git add app.pyxapp
git commit -m "Update app.pyxapp"

# git remote remove origin
# git remote add origin https://github.com/ice715/pyxel_cardgame.git

# git branch -M main  # メインブランチを 'main' に変更（必要なら）
git push -u origin main

# https://kitao.github.io/pyxel/wasm/launcher/?play=ice715.pyxel_cargdgame.app
