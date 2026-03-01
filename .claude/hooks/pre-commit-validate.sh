#!/bin/bash
# pre-commit hook — make validate 自動実行
# インストール: make hook-install

set -e
cd "$(git rev-parse --show-toplevel)"

echo "🔍 Running make validate (pre-commit) ..."
make validate

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ make validate 失敗。コミット前に問題を修正してください。"
    exit 1
fi
