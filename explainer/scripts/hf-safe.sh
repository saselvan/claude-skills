#!/usr/bin/env bash
# The way HyperFrames runs under the explainer skill: no vision or voice keys in the environment (the owner's rule is
# about Gemini and the API keys, 2026-10-26), no telemetry, no update check, the film's pinned version, and the
# subcommands that upload the project or a report refused. Package traffic (add, skills, upgrade, init, usage) is fine.
# Usage: hf-safe.sh [--with-heygen] <hyperframes subcommand> [args]   (run from the film folder; reads BRIEF.md)
set -euo pipefail

keep_heygen=0
if [[ "${1:-}" == "--with-heygen" ]]; then keep_heygen=1; shift; fi
sub="${1:-}"
case "$sub" in
  publish|cloud|lambda|cloudrun|feedback|"")
    echo "hf-safe: refusing 'hyperframes ${sub:-<none>}': it uploads the project or a report. Owner's call; run it by hand if approved." >&2
    exit 2 ;;
esac

pin=""
[[ -f BRIEF.md ]] && pin="$(sed -n 's/^hyperframes:[[:space:]]*\([0-9][0-9.]*\).*/\1/p' BRIEF.md | head -1)"
pkg="hyperframes${pin:+@$pin}"

extra=()
case "$sub" in
  snapshot) extra+=(--describe false) ;;
  capture)  extra+=(--skip-vision) ;;
esac

unset_keys=(-u GEMINI_API_KEY -u OPENAI_API_KEY -u ANTHROPIC_API_KEY -u ELEVENLABS_API_KEY)
[[ $keep_heygen -eq 1 ]] || unset_keys+=(-u HEYGEN_API_KEY)

exec env "${unset_keys[@]}" HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx "$pkg" "$@" ${extra[@]+"${extra[@]}"}
