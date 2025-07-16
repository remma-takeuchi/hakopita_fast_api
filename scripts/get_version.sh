#!/bin/bash

# Gitタグからバージョンを取得
if git describe --tags --always >/dev/null 2>&1; then
    git describe --tags --always
else
    echo "unknown"
fi 