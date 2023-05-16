#!/usr/bin/env bash

set -Eeuo pipefail

source utils.sh

if [[ -f ~/.bashrc ]]; then
  cp ~/.bashrc ~/.bashrc.orig
  rm -rf ~/.bashrc
fi

if [[ -f ~/.condarc ]]; then
  rm -rf ~/.condarc
fi

git clone https://github.com/pmav99/newdot ~/.dotfiles
cd ~/.dotfiles
./init_home.sh
stow common

# Add symlink for bat
if [[ -x /usr/bin/batcat ]]; then
  if [[ ! -x ~/.local/bin/bat ]]; then
    ln -s /usr/bin/batcat ~/.local/bin/bat
  fi
fi
