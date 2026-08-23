# Nova Lab (Offline Clone)

Welcome to the Nova Lab offline clone! This project is a fully-functional, offline-capable mirror of a research peptide supply website, completely rebranded and customized.

## Overview
- **Original Brand:** Amino Club
- **New Brand:** Nova Lab
- **Features:**
  - 100% offline functionality
  - Bypassed age verification/researcher gate
  - High-quality, AI-processed transparent PNG images
  - Custom SVG logo featuring a chemical hexagon and gradient styling
  - Fully rewritten relative navigation links for offline browsing

## Directory Structure
- `clone/` - The root directory of the website clone.
  - `us.html` - The main homepage/landing page.
  - `assets/` - Contains all downloaded images and SVG logos. Backgrounds removed via AI to ensure transparency.
  - `us/` - Contains the internal pages of the website.

## Pages Index
Here are all the successfully cloned pages available in this archive:

### Main Catalog
- [Homepage](clone/us.html)
- [Products / Store](clone/us/store.html) - Main catalog of research peptides.
- [Build a Box](clone/us/subscription-box.html) - Custom subscription builder.
- [Bulk Orders](clone/us/bulk.html) - Wholesale and bulk purchasing.
- [Research Bundles](clone/us/bundles.html) - Curated peptide multipacks.

### Resources & Documentation
- [COAs (Certificates of Analysis)](clone/us/coa.html) - Third-party lab testing results.
- [Quality Standard](clone/us/quality.html) - Information on ISO 17025 lab testing and purity guarantees.
- [Research Use Only](clone/us/research-use.html) - Disclaimers on product usage.
- [FAQ](clone/us/faq.html) - Frequently asked questions.

### Account & Community
- [My Account](clone/us/account.html)
- [Membership](clone/us/membership.html)
- [Buy Points](clone/us/buy-points.html)
- [Partner / Affiliate Program](clone/us/affiliate.html)

### Policies & Support
- [Contact Us](clone/us/contact.html)
- [Shipping Policy](clone/us/shipping.html)
- [Returns Policy](clone/us/returns.html)
- [Terms of Service](clone/us/terms.html)
- [Privacy Policy](clone/us/privacy.html)
- [Disclaimer](clone/us/disclaimer.html)
- [Affiliate Terms](clone/us/affiliate-terms.html)

## Technical Details
This clone was created by bypassing the Next.js server-side verification using specific cookies (`amino_age_verified=1`), scraping the HTML, downloading all `_next/image` protected assets locally, removing solid backgrounds using the `rembg` AI model, and converting absolute routing paths into relative file paths for Windows Explorer compatibility.
