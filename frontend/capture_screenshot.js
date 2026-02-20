const { chromium } = require('playwright');
const path = require('path');

(async () => {
    console.log('Launching browser...');
    const browser = await chromium.launch();
    const page = await browser.newPage();

    console.log('Navigating to dashboard...');
    try {
        await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });

        // Set viewport to simulate desktop
        await page.setViewportSize({ width: 1920, height: 1080 });

        console.log('Taking screenshot...');
        const screenshotPath = path.resolve(__dirname, 'dashboard_audit.png');
        await page.screenshot({ path: screenshotPath, fullPage: true });

        console.log(`Screenshot saved to: ${screenshotPath}`);
    } catch (error) {
        console.error('Error taking screenshot:', error);
    } finally {
        await browser.close();
    }
})();
