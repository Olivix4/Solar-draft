# SolarDraft — Codemagic CI/CD + GitHub Pages

SolarDraft is a static, client-side solar PV diagram-generator prototype. This repository runs automated checks with Codemagic and publishes the site to the `gh-pages` branch after checks pass on `main`.

## Repository layout

- `site/index.html` — SolarDraft website
- `tests/check_site.py` — structural and JavaScript syntax checks
- `codemagic.yaml` — CI and GitHub Pages deployment workflows

## One-time setup

### 1. Connect Codemagic
1. Sign in at https://codemagic.io/ and add the GitHub repository `Olivix4/Solar-draft`.
2. Select YAML-based configuration. Keep `codemagic.yaml` in the repository root.
3. In the Codemagic app settings, create an environment variable group named exactly `github_pages`.
4. Add `GH_PAGES_TOKEN` to that group and mark it Secret.

### 2. Create the GitHub token
Create a fine-grained personal access token scoped only to this repository. Grant **Contents: Read and write**. Use an expiry date and rotate the token when needed. Add it only to Codemagic as the secret `GH_PAGES_TOKEN`; never commit it or share it in chat.

### 3. Enable GitHub Pages
After the first successful deployment creates `gh-pages`:
1. Open repository **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch `gh-pages` and folder `/(root)`, then Save.
4. Wait for GitHub Pages to publish.

The expected site URL is https://olivix4.github.io/Solar-draft/.

## How CI/CD works
- Pushes and pull requests targeting `main` run `solardraft-website-ci`.
- Pushes to `main` run `solardraft-pages-deploy`; it repeats the checks and pushes only the generated `site/index.html` to `gh-pages` if checks pass.
- The deploy job force-updates `gh-pages`, which must remain a generated-output branch.

## Run checks locally
Requires Python 3 and Node.js:
```bash
python3 tests/check_site.py
```

## Limitations and engineering safety
The checks cover HTML structure, required controls, duplicate IDs and JavaScript syntax. They do not replace real-browser end-to-end tests. SolarDraft outputs conceptual drafts, not certified construction documents. Validate equipment datasheets, string voltages/currents, protection coordination, conductor sizing, earthing, battery compatibility, local standards and utility requirements with a qualified electrical designer before installation.
