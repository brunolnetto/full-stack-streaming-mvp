import { test, expect } from '@playwright/test';

test('displays route hit counts', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('Route Hit Counts')).toBeVisible();
  // Optionally, check for table rows or loading state
  // await expect(page.locator('table')).toBeVisible();
}); 