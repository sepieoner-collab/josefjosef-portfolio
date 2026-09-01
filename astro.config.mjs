import { defineConfig } from "astro/config";

// Full docs: https://docs.astro.build/en/reference/configuration-reference/
export default defineConfig({
  site: "https://josefjosef.cz",
  vite: {
    server: {
      watch: {
        // Claude edits these files through the Cowork bridge, which doesn't
        // trigger macOS file-change events. Polling makes the dev server
        // notice edits reliably, so the browser always shows current code.
        usePolling: true,
        interval: 300,
      },
    },
  },
});
