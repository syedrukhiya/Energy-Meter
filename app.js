const express = require('express');

const app = express();
// Change this based on your astro.config.mjs, `base` option.
// They should match. The default value is "/".
const base = '/';
app.use(base, express.static('dist/client/'));

// Use dynamic import for ESM module
(async () => {
  const { handler: ssrHandler } = await import('./dist/server/entry.mjs');
  app.use(ssrHandler);

  app.listen(8080, () => {
    console.log('Server is running on port 8080');
  });
})();