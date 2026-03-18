# ptl-website

The public website and documentation for Plain Theory Labs,
built with Astro and Starlight.

Live at: [plaintheory.org](https://plaintheory.org)

[![Deploy](https://img.shields.io/badge/deployed-plaintheory.org-14532d)](https://plaintheory.org)
[![Built with Astro](https://img.shields.io/badge/built%20with-Astro-164e63)](https://astro.build)
[![Docs](https://img.shields.io/badge/docs-Starlight-134e4a)](https://plaintheory.org/docs)

## What this repo contains

The homepage at plaintheory.org and the full documentation
site at plaintheory.org/docs.

The homepage presents the PTL Score, the framework overview,
and the pilot contact. The documentation covers all nine
analytical engines with formulas, worked examples, CLI usage,
and input schemas.

## Structure

```
ptl-website/
├── src/
│   ├── pages/
│   │   └── index.astro        Homepage
│   ├── content/
│   │   └── docs/
│   │       ├── engines/       Nine engine pages
│   │       │   ├── ace.md
│   │       │   ├── cool.md
│   │       │   ├── flux.md
│   │       │   ├── pace.md
│   │       │   ├── core.md
│   │       │   ├── grade.md
│   │       │   ├── atlas.md
│   │       │   ├── claw.md
│   │       │   └── profile.md
│   │       └── methodology/   Scoring, tiers, coefficients
│   ├── styles/
│   │   ├── global.css         Homepage styles
│   │   └── docs.css           Starlight theme overrides
│   └── layouts/
│       └── Layout.astro       Homepage layout and header
├── astro.config.mjs           Astro + Starlight configuration
└── public/                    Static assets
```

## Design

Warm white background (#f0ede6). EB Garamond serif throughout.
JetBrains Mono for scores, code, and labels.

The PTL Score is the dominant visual element on the homepage.
Everything else supports it.

Reference: [Thinking Machines Lab](https://thinkingmachines.ai)

## Development

```bash
npm install
npm run dev      # localhost:4321
npm run build    # production build
npm run preview  # preview production build
```

## Related repositories

| Repository | Description |
|------------|-------------|
| [ptl-engines](https://github.com/plain-theory-labs/ptl-engines) | The nine analytical engines |
| [ptl-methodology](https://github.com/plain-theory-labs/ptl-methodology) | Scoring methodology — CC BY 4.0 |
| [ptl-context](https://github.com/plain-theory-labs/ptl-context) | Engineering context and session logs |

## Deployment

Deployed to GitHub Pages from the main branch automatically
on push. Build output is the `dist/` directory.

## License

MIT
