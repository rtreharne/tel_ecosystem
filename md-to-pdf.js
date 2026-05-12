#!/usr/bin/env node

/**
 * Convert README.md to PDF
 * Usage: node md-to-pdf.js
 * 
 * Install dependencies:
 * npm install markdown-pdf
 */

const markdownPdf = require('markdown-pdf');
const fs = require('fs');
const path = require('path');

const inputFile = 'README.md';
const outputFile = 'README.pdf';

if (!fs.existsSync(inputFile)) {
    console.error(`Error: ${inputFile} not found`);
    process.exit(1);
}

console.log(`Converting ${inputFile} to ${outputFile}...`);

const options = {
    paperFormat: 'A4',
    margin: '2cm',
    cssPath: path.join(__dirname, 'pdf-styles.css'),
    remarkable: {
        html: true,
        breaks: true
    }
};

const files = [inputFile];

markdownPdf(options).from.files(files).to(outputFile, function() {
    console.log(`✓ PDF generated: ${outputFile}`);
    process.exit(0);
}).catch(error => {
    console.error(`Error generating PDF: ${error.message}`);
    console.error('\nTo install markdown-pdf, run:');
    console.error('  npm install markdown-pdf');
    process.exit(1);
});
