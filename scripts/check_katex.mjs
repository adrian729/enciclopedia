#!/usr/bin/env node
// Render every \( … \) / \[ … \] math snippet through the SAME KaTeX version
// pinned in docs/index.html (downloaded once per version into the OS temp dir),
// with throwOnError — so TeX that would render red-or-broken in the browser
// fails here first. Extraction mirrors the katexMath plugin in index.html:
// raw markdown, display form matched before inline.
//
// Usage:
//   node scripts/check_katex.mjs                  # default scope: docs/software/procedural
//   node scripts/check_katex.mjs docs/foo docs/bar.md
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const indexHtml = readFileSync(join(repo, 'docs', 'index.html'), 'utf8');
const pin = indexHtml.match(/katex@([\d.]+)\/dist\/katex\.min\.js/);
if (!pin) {
  console.error('cannot find a pinned katex version in docs/index.html');
  process.exit(2);
}
const version = pin[1];
const cache = join(tmpdir(), `katex-${version}.min.js`);
if (!existsSync(cache)) {
  const res = await fetch(`https://cdn.jsdelivr.net/npm/katex@${version}/dist/katex.min.js`);
  if (!res.ok) {
    console.error(`katex@${version} download failed: HTTP ${res.status}`);
    process.exit(2);
  }
  writeFileSync(cache, await res.text());
}
const katex = createRequire(import.meta.url)(cache);

const targets = process.argv.slice(2);
const roots = targets.length ? targets : [join('docs', 'software', 'procedural')];
const files = [];
for (const t of roots) {
  const p = resolve(repo, t);
  if (statSync(p).isDirectory()) {
    for (const f of readdirSync(p, { recursive: true })) {
      if (f.toString().endsWith('.md')) files.push(join(p, f.toString()));
    }
  } else {
    files.push(p);
  }
}

let total = 0;
let failures = 0;
for (const f of files) {
  const md = readFileSync(f, 'utf8');
  for (const [re, display] of [[/\\\[([\s\S]+?)\\\]/g, true], [/\\\(([\s\S]+?)\\\)/g, false]]) {
    for (const m of md.matchAll(re)) {
      total++;
      try {
        katex.renderToString(m[1], { displayMode: display, throwOnError: true });
      } catch (e) {
        failures++;
        console.log(`FAIL ${f}: ${String(e.message).split('\n')[0]}\n  tex: ${m[1].trim().slice(0, 100)}`);
      }
    }
  }
}
console.log(`katex@${version}: ${total} snippets across ${files.length} file(s), ${failures} failure(s)`);
process.exit(failures ? 1 : 0);
