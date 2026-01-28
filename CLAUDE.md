# Seven24 – CLAUDE.md

## 1. Project Overview & Goals

**Seven24** is a professional portfolio and lead-generation static website for a Kenya-based freelance Statistics Expert and Data & AI Consultant (X: @Datadetective10). The site targets SMEs, startups, researchers, and e-commerce businesses worldwide who need data cleaning, business intelligence dashboards, statistical modeling, predictive analytics, and workflow automation.

**Core positioning:** "Academic rigor meets business speed" — emphasizing statistically sound, mathematically validated work over black-box AI hype.

**Key authority phrase:** Always refer to solutions as "Statistics Expert-powered" to reinforce credibility.

**Tagline:** "Data, Analytics & AI for Better Business Decisions"

**Ideal client statement (use frequently):** "I help small businesses, startups, and researchers turn data into decisions using applied statistics, analytics, and machine learning."

**Success metrics:**
- MVP deployed with all 6 pages, 5 service descriptions, 3 live Streamlit demos
- Working Netlify contact form + Calendly integration
- Professional, trust-building brand voice throughout
- Zero console errors, mobile-first design, fast load times
- Long-term: Generate 3–5 qualified leads per month

---

## 2. Brand Voice, Tone & Key Phrases

**Voice characteristics:**
- **Professional** – no slang, casual abbreviations, or overly technical jargon
- **Confident** – authoritative without arrogance; you are the expert
- **Approachable** – warm, human, benefit-focused; no corporate coldness
- **Trust-building** – emphasize transparency, accuracy, validation, peer-reviewed methods

**Forbidden phrases:**
- "BSc in Statistics" or any degree-specific credentials
- "AI-powered" (use "Statistics Expert-powered" instead)
- Hype language like "revolutionary", "game-changing", "cutting-edge"

**Preferred phrases:**
- "Academic rigor meets business speed"
- "Statistics Expert-powered solutions"
- "Turn data into decisions"
- "Validated, peer-reviewed methods"
- "No jargon – I explain results in plain language"

---

## 3. Visual & Design Guidelines

**Colors:**
- Primary Blue: `#007BFF`
- Hover Blue: `#0d6efd`
- Success Green: `#198754` (CTAs, accents)
- Light Background: `#F8F9FA`
- White: `#FFFFFF`

**Typography:**
- Primary Font: Roboto (Google Fonts)
- Secondary Font: Open Sans
- Base Size: 16px, Line Height: 1.6

**Components:**
- Responsive navbar with logo ("Seven24" + "Data & AI" tagline)
- Bootstrap 5 cards with subtle hover effects (shadow, slight lift)
- Accordion for FAQ and Services
- CTA buttons: Primary (solid blue) and Outline (blue border)
- Footer: Dark text, social icons, copyright © 2026 Seven24

**Accessibility:**
- Alt text on all images
- ARIA labels on icon buttons
- Keyboard navigable
- WCAG AA color contrast

---

## 4. Technology & Architecture Rules

**Tech Stack (non-negotiable):**
- HTML5 + CSS3 + Vanilla JavaScript (minimal)
- Bootstrap 5 via CDN
- Google Fonts (Roboto, Open Sans) + Font Awesome 6
- Netlify hosting (free tier)
- Netlify Forms (`data-netlify="true"`)
- Calendly inline embed
- Streamlit Community Cloud for demos

**Prohibitions:**
- ❌ No React, Vue, Angular, or SPA frameworks
- ❌ No Tailwind, Sass, or CSS preprocessors
- ❌ No Node.js, npm, Webpack, or build tools
- ❌ No backend, databases, or APIs
- ✅ Keep it simple: static files deployable to Netlify instantly

---

## 5. File & Folder Structure (GitHub Repo Layout)

```
d:\Seven24\
├── index.html              # Home (hero, services teaser, process, demos)
├── services.html           # 5 services (accordion/cards)
├── portfolio.html          # Case studies + 3 Streamlit demo links
├── about.html              # Bio, skills, values, process
├── faq.html                # 8 FAQ accordion items
├── contact.html            # Netlify form + Calendly embed
├── css/
│   └── custom.css          # Brand colors, components, responsive styles
├── js/
│   └── custom.js           # Smooth scroll, navbar highlight (minimal)
├── images/                 # Placeholder images (Unsplash URLs initially)
├── README.md               # Deployment guide + project overview
└── CLAUDE.md               # This file (project context for AI)
```

---

## 6. Services & Demos Reference

**Services (exactly these five):**
1. **Python/R Data Cleaning & Analysis** – Data wrangling, outlier detection, validation
2. **Business Intelligence Dashboards** – Power BI, Tableau, Python (Plotly/Streamlit)
3. **Statistical Modeling & Hypothesis Testing** – A/B tests, regression, p-values, confidence intervals
4. **Predictive Machine Learning Models** – Forecasting, churn prediction, demand modeling
5. **Workflow Automation & Applied AI** – Python scripts, API integrations, agentic workflows

**Demos (exactly these three):**
1. **Predictive Analytics Dashboard** – Sales/demand forecasting with business recommendations (ARIMA, Prophet)
2. **Business KPI Visualizer** – CSV upload → revenue, churn, growth insights with visualizations
3. **Inference Engine** – CSV upload → regression analysis, p-values, confidence intervals, plain-language interpretation

**Demo Integration:**
- **Primary:** Hyperlink buttons opening in new tabs (`target="_blank" rel="noopener noreferrer"`)
- **Optional:** Iframes with `?embedded=true` (test first; fallback if broken)
- **Fallback:** Screenshots with "View Live Demo" buttons

---

## 7. Important Copy & Content Guidelines

**CTAs to use:**
- "Book Free Call" (links to Calendly)
- "View Live Demo" (links to Streamlit apps)
- "Get Started" / "Work With Me" (links to contact form)

**Contact details:**
- Email: ondibahezron@gmail.com
- WhatsApp: +254 712 200337
- X (Twitter): @Datadetective10
- LinkedIn: Hezron Mokaya
- Calendly: https://calendly.com/ondibahezron/30min

**SEO focus:**
- Keywords: "data analyst Kenya", "Power BI dashboards Nairobi", "statistics consultant", "machine learning Kenya"
- Every page has unique meta title + description
- All images have descriptive alt text

---

## 8. Netlify & Deployment Checklist

**Deploy steps:**
1. Push to GitHub: `git push origin main`
2. Connect repo to Netlify
3. Build settings: Build command = (blank), Publish directory = `/`
4. Enable Netlify Forms in dashboard
5. Test form submission after deploy
6. Verify Calendly embed loads correctly
7. Update Streamlit demo URLs with actual app links

**Post-deploy:**
- Replace Unsplash placeholder images with actual project screenshots
- Update profile photo in about.html
- Add custom domain (optional)
- Submit to Google Search Console

---

## 9. Code Style Preferences

**HTML:**
- Semantic tags (`<header>`, `<nav>`, `<section>`, `<article>`, `<footer>`)
- One `<h1>` per page
- Alt text on all images
- Consistent indentation (4 spaces)

**CSS:**
- Use CSS variables for colors (`:root`)
- Mobile-first responsive design
- Bootstrap classes where possible
- Custom classes in `custom.css` only when needed

**JavaScript:**
- Keep minimal (smooth scroll, form validation, navbar active state)
- Vanilla JS only, no jQuery
- No external libraries beyond Bootstrap bundle

---

## 10. Prohibitions (What Never to Do)

- ❌ Never suggest adding more pages beyond the 6 core pages until MVP has clients
- ❌ Never add services beyond the 5 locked services
- ❌ Never use Lorem Ipsum – always use real, benefit-driven copy
- ❌ Never mention "BSc" or specific degree credentials
- ❌ Never use AI hype language ("revolutionary", "game-changing")
- ❌ Never add backend, databases, or complex frameworks
- ❌ Never suggest time-consuming features before validating with real traffic

---

## 11. How to Use This File

**For me (project owner):**
When starting a new conversation with Claude Code about this project, reference or paste this file to provide full context. This ensures consistency across sessions and prevents scope creep.

**For Claude Code:**
Read this file completely before suggesting edits, new features, or copy changes. Prioritize simplicity, credibility, and benefit-focused language. When in doubt, ask before adding complexity.

**Updates:**
Keep this file synchronized with major project changes (new demos, pricing updates, tech stack changes). Treat it as the single source of truth.

---

**Live Site:** https://mokaya.netlify.app/
**GitHub Repo:** https://github.com/ondibahezron-glitch/24-Seven
**Last Updated:** 2026-01-28
