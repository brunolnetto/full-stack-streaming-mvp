// playwright.config.js
// @ts-check
/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  testDir: './tests',
  use: {
    baseURL: 'http://localhost:5173',
    headless: true,
    browserName: 'chromium',
  },
};

export default config; 