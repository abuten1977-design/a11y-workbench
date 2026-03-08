#!/usr/bin/env node
/**
 * Simple axe-core runner using Puppeteer
 * Usage: node axe_runner.js <URL>
 */

const puppeteer = require('puppeteer');
const { AxePuppeteer } = require('@axe-core/puppeteer');
const fs = require('fs');

async function runAxe(url) {
    console.log(`🔍 Testing: ${url}`);
    console.log('⏳ Launching browser...\n');
    
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });
    
    console.log('⏳ Running axe-core analysis...\n');
    
    const results = await new AxePuppeteer(page).analyze();
    
    await browser.close();
    
    // Save results
    fs.writeFileSync('axe_results.json', JSON.stringify(results, null, 2));
    
    console.log('✅ Results saved to: axe_results.json\n');
    console.log('📊 Quick summary:');
    console.log(`   URL: ${results.url}`);
    console.log(`   Violations: ${results.violations.length}`);
    console.log(`   Passes: ${results.passes.length}`);
    console.log(`   Incomplete: ${results.incomplete.length}`);
    console.log(`   Inapplicable: ${results.inapplicable.length}\n`);
    
    if (results.violations.length > 0) {
        console.log('⚠️  Found violations:');
        results.violations.forEach((v, i) => {
            console.log(`   ${i+1}. [${v.impact}] ${v.help} (${v.nodes.length} elements)`);
        });
    }
    
    console.log('\n💡 Run: python3 parse_axe.py axe_results.json');
    console.log('   to see detailed report\n');
}

const url = process.argv[2];
if (!url) {
    console.log('Usage: node axe_runner.js <URL>');
    console.log('Example: node axe_runner.js https://example.com');
    process.exit(1);
}

runAxe(url).catch(console.error);
