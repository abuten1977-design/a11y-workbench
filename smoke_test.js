#!/usr/bin/env node
/**
 * Simple E2E smoke test for A11y Workbench
 */

const puppeteer = require('puppeteer');

const BASE_URL = process.env.TEST_URL || 'http://localhost:8000';

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function test() {
    console.log('🧪 A11y Workbench Smoke Test\n');
    console.log(`URL: ${BASE_URL}\n`);
    
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox']
    });
    
    const page = await browser.newPage();
    const errors = [];
    
    page.on('console', msg => {
        if (msg.type() === 'error') {
            errors.push(`Console: ${msg.text()}`);
        }
    });
    
    page.on('pageerror', error => {
        errors.push(`Page: ${error.message}`);
    });
    
    try {
        // Test 1: Dashboard loads
        console.log('✓ Loading dashboard...');
        await page.goto(`${BASE_URL}/dashboard`, { waitUntil: 'networkidle2', timeout: 10000 });
        await sleep(1000);
        
        // Test 2: Check key elements exist
        console.log('✓ Checking UI elements...');
        const elements = await page.evaluate(() => {
            return {
                hasProjects: !!document.querySelector('#projects-section'),
                hasTargets: !!document.querySelector('#targets-section'),
                hasSessions: !!document.querySelector('#sessions-section'),
                hasIssues: !!document.querySelector('#issues-section'),
                hasStats: !!document.querySelector('.stats-bar')
            };
        });
        
        console.log('  - Projects section:', elements.hasProjects ? '✅' : '❌');
        console.log('  - Targets section:', elements.hasTargets ? '✅' : '❌');
        console.log('  - Sessions section:', elements.hasSessions ? '✅' : '❌');
        console.log('  - Issues section:', elements.hasIssues ? '✅' : '❌');
        console.log('  - Stats bar:', elements.hasStats ? '✅' : '❌');
        
        // Test 3: Check API endpoints
        console.log('\n✓ Testing API endpoints...');
        
        const endpoints = [
            '/health',
            '/api/v1/projects',
            '/api/v1/statistics'
        ];
        
        for (const endpoint of endpoints) {
            const response = await page.goto(`${BASE_URL}${endpoint}`, { waitUntil: 'networkidle2' });
            const status = response.status();
            console.log(`  - ${endpoint}: ${status === 200 ? '✅' : '❌'} (${status})`);
        }
        
        // Summary
        console.log('\n' + '='.repeat(50));
        if (errors.length > 0) {
            console.log('⚠️  Errors detected:');
            errors.forEach(err => console.log(`  - ${err}`));
        } else {
            console.log('✅ No JavaScript errors detected');
        }
        console.log('='.repeat(50));
        
    } catch (error) {
        console.log('\n❌ Test failed:', error.message);
        process.exit(1);
    } finally {
        await browser.close();
    }
    
    console.log('\n🎉 Smoke test completed!\n');
}

test().catch(console.error);
