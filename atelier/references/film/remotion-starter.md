# Remotion starter for demo films

**Working template:** `/Users/samuel.selvan/repos/clinical-va-appkit/video/` (branch `step-2-identity-registry`). As of 2026-09-29 it is **untracked** in that repo, so check that it exists before relying on it. Copy it without `node_modules/`, `out/` or `public/captures/`, then `npm install`.

What it contains:
- `src/index.ts` (entry) → `src/Root.tsx` (compositions: `FilmA-16x9`, `FilmA-1x1`, `FilmB-16x9`, `FilmB-1x1`; fonts loaded here).
- `src/data/acts.json` (generated from the final script tables: shots with `startMs`, `durationTargetSec`, `narration[]`, `claimClass`, `claims`), `src/data/shot-crops.json` (one crop per shot), `src/data/code-shots.json` (`{id, file, startLine, endLine, code}`, byte-for-byte).
- `src/tokens.ts` (white ground, ink, one accent, DM Sans / DM Mono, calm ease-out, 200–300 ms fades). Take the values from the app's own CSS tokens and motion file, never from memory.
- `src/components/`: `Caption` (backticked nouns in mono), `TypeCard` (lines build), `DiagramCard` (native SVG, only what the demo runs), `ReviewCard` (ticked lines, each ≥ 2.5 s), `EndCard` (the one provenance line), `ScreenShot` (capture + crop + push-in 1.00→1.04), `CodeShot`.
- `scripts/check-*.js` (fix them first, see `checks.md`), `render-stills.js`, `render-all-stills.sh`, `final-deliver.sh`.
- `remotion.config.ts`: `h264`, `yuv420p`, CRF 23.

## The four setup bugs (each cost a render round)
1. **`registerRoot` goes in `src/index.ts`**, not in `Root.tsx`. `src/index.ts` is `import {registerRoot} from 'remotion'; import {RemotionRoot} from './Root'; registerRoot(RemotionRoot);`, and every CLI call points at it: `npx remotion still src/index.ts FilmA-16x9 out/x.png --frame=990`.
2. **The config import is `import {Config} from '@remotion/cli/config';`**, not from `remotion`.
3. **Font import paths are PascalCase without spaces:** `import {loadFont} from '@remotion/google-fonts/DMSans'` and `'@remotion/google-fonts/DMMono'`. Call `loadFont('normal', {weights, subsets: ['latin']})` at module level in `Root.tsx`. Remotion does no font fallback, so check a still before trusting the type.
4. **Public assets go through `staticFile()`:** `staticFile(\`captures/${name}.png\`)` resolves from `video/public/`. Raw relative paths don't resolve in the bundle.

`package.json` wires `check:lint`, `check:reading`, `check:chrome` and `check:pills`. Add `check:crop-text`, which the template runs by hand.

**Dependencies you must add:** `@remotion/cli` and `@remotion/google-fonts`, at the same version as `remotion` (the template uses `^4.0.527`), plus a `tsconfig.json` (the Remotion template default).

## Order of work
Captures from one real rehearsal run (GET-only capture script, free port, `<title>` checked, bearer token via `extraHTTPHeaders` for a live app) → `code-shots.json` pinned → crops → checks at 0 → one still per shot for every composition, and look at them → draft MP4s → visual gauntlet → final renders → `ffprobe`.

**The coordinator runs renders.** Subagents under the auto-mode classifier couldn't run them reliably (`lakebase-demo.md` field lessons).

**Licence:** Remotion is cleared for internal use only (D9). For customer use, clear the Company License through procurement, or re-render with HyperFrames (Apache 2.0). Keep the composition data (`acts.json`, crops, captures) tool-agnostic so a re-render is a port, not a rewrite.
