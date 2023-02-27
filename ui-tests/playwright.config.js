var baseConfig = require('@jupyterlab/galata/lib/playwright-config');

module.exports = {
    ...baseConfig,
    use: {
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
  },
  timeout: 240000,
  retries: 1,
};
