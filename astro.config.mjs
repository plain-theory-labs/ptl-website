import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://plaintheory.org',
  output: "static",
  trailingSlash: "ignore",
  integrations: [
    starlight({
      title: 'Plain Theory Labs',
      description: 'Documentation for the PTL certification framework.',
      defaultLocale: 'en',
      customCss: ['./src/styles/docs.css'],
      sidebar: [
        {
          label: 'Getting Started',
          items: [
            { label: 'Overview', link: '/docs/' },
            { label: 'How certification works', link: '/docs/certification/' },
            { label: 'Start a pilot', link: '/docs/pilot/' },
          ],
        },
        {
          label: 'Engines',
          items: [
            { label: 'PROFILE', link: '/docs/engines/profile/' },
            { label: 'ACE', link: '/docs/engines/ace/' },
            { label: 'COOL', link: '/docs/engines/cool/' },
            { label: 'FLUX', link: '/docs/engines/flux/' },
            { label: 'PACE', link: '/docs/engines/pace/' },
            { label: 'CORE', link: '/docs/engines/core/' },
            { label: 'GRADE', link: '/docs/engines/grade/' },
            { label: 'ATLAS', link: '/docs/engines/atlas/' },
            { label: 'CLAW', link: '/docs/engines/claw/' },
          ],
        },
        {
          label: 'Methodology',
          items: [
            { label: 'Scoring', link: '/docs/methodology/scoring/' },
            { label: 'Tiers', link: '/docs/methodology/tiers/' },
            { label: 'Coefficients', link: '/docs/methodology/coefficients/' },
          ],
        },
      ],
    }),
  ],
});
