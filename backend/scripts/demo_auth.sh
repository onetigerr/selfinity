#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://127.0.0.1:8000}
EMAIL=${EMAIL:-demo_${RANDOM}@example.com}
PASS=${PASS:-secret12}

echo "Using BASE_URL=$BASE_URL"
echo "Registering user $EMAIL"

register() {
  curl -sS -X POST "$BASE_URL/auth/register" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}"
}

login() {
  curl -sS -X POST "$BASE_URL/auth/login" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}"
}

me() {
  local token="$1"
  curl -sS "$BASE_URL/auth/me" -H "Authorization: Bearer $token"
}

pretty() {
  if command -v jq >/dev/null 2>&1; then jq; else python3 -m json.tool; fi
}

REG=$(register)
echo "$REG" | pretty

TOK=$(login | { if command -v jq >/dev/null 2>&1; then jq -r .access_token; else python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])'; fi; })
echo "Token: ${TOK:0:20}..."

ME=$(me "$TOK")
echo "$ME" | pretty

echo "Done"

