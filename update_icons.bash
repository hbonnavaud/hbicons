#!/bin/bash

for dir in ~/.local/share/icons/*; do
    if [[ -d "$dir" ]]; then
        gtk-update-icon-cache -f -t "$dir"
    fi
done