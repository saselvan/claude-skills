# Remotion starter for demo films

**Working template:** `/Users/samuel.selvan/repos/clinical-va-appkit/video/` (branch `step-2-identity-registry`). As of 2026-09-29 it is **untracked** in that repo, so check that it exists before relying on it. Copy it without `node_modules/`, `out/` or `public/captures/`, then `npm install`.

Conventions the file tree doesn't show (list the tree for the rest):
- The three data files drive everything: `src/data/acts.json` is **generated from the final script tables**, never hand-edited; `shot-crops.json` holds one crop per shot; `code-shots.json` holds code byte-for-byte at its pinned lines.
- `src/tokens.ts` takes its values from the app's own CSS tokens and motion file, read fresh.
- `EndCard` carries the one provenance line; `ReviewCard` lines hold ≥ 2.5 s each; `DiagramCard` draws only what the demo runs; `ScreenShot` push-ins run 1.00→1.04.
- `scripts/check-*.js` are defective until fixed (`checks.md`).

## The four setup bugs (each cost a render round)
1. **`registerRoot` goes in `src/index.ts`**, not in `Root.tsx`. `src/index.ts` is `import {registerRoot} from 'remotion'; import {RemotionRoot} from './Root'; registerRoot(RemotionRoot);`, and every CLI call points at it: `npx remotion still src/index.ts FilmA-16x9 out/x.png --frame=990`.
2. **The config import is `import {Config} from '@remotion/cli/config';`**, not from `remotion`.
3. **Font import paths are PascalCase without spaces:** `import {loadFont} from '@remotion/google-fonts/DMSans'` and `'@remotion/google-fonts/DMMono'`. Call `loadFont('normal', {weights, subsets: ['latin']})` at module level in `Root.tsx`. Remotion does no font fallback, so check a still before trusting the type.
4. **Public assets go through `staticFile()`:** `staticFile(\`captures/${name}.png\`)` resolves from `video/public/`. Raw relative paths don't resolve in the bundle.

`package.json` wires `check:lint`, `check:reading`, `check:chrome` and `check:pills`. Add `check:crop-text`, which the template runs by hand.

**Dependencies you must add:** `@remotion/cli` and `@remotion/google-fonts`, at the same version as `remotion` (the template uses `^4.0.527`), plus a `tsconfig.json` (the Remotion template default).

## Order of work
Captures from one real rehearsal run (`questions.md` "Screen source"; bearer token via `extraHTTPHeaders` for a live app) → `code-shots.json` pinned → crops → checks at 0 → one still per shot for every composition, and look at them → draft MP4s → visual gauntlet → final renders → `ffprobe`.

**The coordinator runs `remotion still` / `remotion render` and the checks itself.** Subagents under the auto-mode classifier couldn't run them reliably; they write code and data.

**Licence:** Remotion is cleared for internal use only (D9); customer use is a promotion trigger (`questions.md`). Keep the composition data (`acts.json`, crops, captures) tool-agnostic so a re-render is a port, not a rewrite.
