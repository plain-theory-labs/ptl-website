import { defineConfig } from "astro/config";

export default defineConfig({
  site: 'https://plaintheory.org',
  base: '/',
  output: "static",
  trailingSlash: "never"
});
