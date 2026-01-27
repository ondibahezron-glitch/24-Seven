Seven24 – CLAUDE.md
Project Summary
Seven24 is a professional portfolio and lead-generation static website for a Kenya-based freelance Statistics Expert and Data & AI Consultant (X: @Datadetective10). The site targets SMEs, startups, researchers, and e-commerce businesses worldwide who need data cleaning, business intelligence dashboards, statistical modeling, predictive analytics, and workflow automation.

Core positioning: "Academic rigor meets business speed" — emphasizing statistically sound, mathematically validated work over black-box AI hype.

Key authority phrase: Always refer to solutions as "Statistics Expert-powered" to reinforce credibility.

Tagline: "Data, Analytics & AI for Better Business Decisions"

Ideal client statement (use frequently): "I help small businesses, startups, and researchers turn data into decisions using applied statistics, analytics, and machine learning."

Goals & Success Criteria
MVP Success Metrics:

Fully responsive, accessible static site deployed on Netlify
5 service pages clearly describing offerings
3 live Streamlit demo apps integrated and accessible
Working Netlify contact form
Professional, trust-building brand voice throughout
Zero console errors, mobile-first design, fast load times
Long-term (post-MVP):

Generate 3–5 qualified leads per month
Establish authority in global data/analytics freelance market
Demonstrate technical capability through interactive demos
Brand Voice & Tone Guidelines
Voice characteristics:

Professional – no slang, casual abbreviations, or overly technical jargon
Confident – authoritative without arrogance; you are the expert
Approachable – warm, human, benefit-focused; no corporate coldness
Trust-building – emphasize transparency, accuracy, validation, peer-reviewed methods
No hype – avoid buzzwords like "cutting-edge AI" or "revolutionary"; prefer "proven," "validated," "rigorous"
Writing rules:

Use second-person "you" when addressing potential clients
Lead with benefits, not features ("increase revenue by 15%" > "build predictive models")
Always tie services back to business outcomes: better decisions, cost savings, growth, efficiency
Avoid passive voice where possible
Use short paragraphs (2–4 sentences max) for scannability
Visual Design & UI Rules
Color Palette:

Primary Blue: #007BFF
Hover Blue: #0d6efd
Success Green: #198754 (CTAs, accents)
Light Backgrounds: #F8F9FA, white (#FFFFFF)
Text: Dark gray/black for body, blue for links
Typography:

Primary: Roboto (Google Fonts)
Secondary: Open Sans
Headings: bold, generous line-height
Body: 16px base, 1.6 line-height
Component Style:

Bootstrap 5 utility classes preferred
Rounded corners: border-radius: 8px for cards
Shadows: subtle (box-shadow: 0 2px 8px rgba(0,0,0,0.1))
Buttons: solid green (#198754) with white text, hover darkens slightly
Icons: Font Awesome (CDN), use sparingly
Responsiveness:

Mobile-first breakpoints (Bootstrap defaults)
Test on 375px (mobile), 768px (tablet), 1200px (desktop)
Navbar collapses to hamburger on mobile
Cards stack vertically on small screens
Technology & Architecture Decisions
Strict Tech Stack (do NOT deviate):

HTML5 – semantic, accessible markup
CSS – Bootstrap 5 via CDN + /css/custom.css for overrides
JavaScript – minimal custom JS in /js/custom.js (navbar, smooth scroll only)
Icons – Font Awesome (CDN)
Fonts – Google Fonts (Roboto, Open Sans)
Hosting – Netlify (free tier), static deployment
Forms – Netlify Forms (data-netlify="true")
Demos – 3 separate Streamlit apps on Streamlit Community Cloud
Prohibited technologies (unless I explicitly request):

No React, Vue, Svelte, Angular
No Tailwind, Sass, PostCSS, build tools
No backend, databases, server-side rendering
No paid services, premium plugins, or third-party analytics at MVP stage
Why this stack:

Zero build complexity
Free hosting forever
Lightning-fast load times
Easy for me (client) to maintain HTML/CSS
Streamlit demos showcase technical skill without backend setup
File & Folder Structure

d:\Seven24\
├── index.html              # Home page
├── services.html           # 5 services overview
├── portfolio.html          # Case studies + demo links
├── about.html              # About me, credentials, process
├── faq.html                # Common objections, Q&A
├── contact.html            # Netlify form, email, social
├── css/
│   └── custom.css          # Custom styles, overrides
├── js/
│   └── custom.js           # Minimal JS (optional)
├── images/
│   └── (headshot, mockups, screenshots, icons)
├── README.md               # Deployment instructions
└── CLAUDE.md               # This file (your permanent context)
Naming conventions:

Use lowercase, hyphens for multi-word files (e.g., privacy-policy.html if added later)
Keep folder names simple: css, js, images (no assets/ or public/)
Important Content & Copy Rules
Services (exactly these five at MVP):

Python/R Data Cleaning & Analysis – transform messy data into analysis-ready datasets
Business Intelligence Dashboards – Power BI / Tableau / Python visualizations
Statistical Modeling & Hypothesis Testing – A/B tests, regression, ANOVA, p-values, confidence intervals
Predictive Machine Learning Models – sales forecasting, churn prediction, demand planning (emphasis on validation & explainability)
Workflow Automation & Applied AI – Python scripts, API integrations, simple AI agents
Each service must:

Open with a benefit-driven headline
Include a 2–3 sentence description
List 3–4 bullet points of deliverables or use cases
End with a soft CTA ("Let's discuss your project")
Homepage must include:

Hero section: tagline + ideal client statement + primary CTA
Services overview (summary of 5 services)
Social proof placeholder (testimonials or "Trusted by" section, even if minimal)
Demo preview section with links to Streamlit apps
Final CTA above footer
About page must cover:

Who I am (Statistics Expert, Kenya-based, X: @Datadetective10)
My philosophy: academic rigor meets business speed, no hype
Credentials (degrees, tools, methods)
Process overview (Discovery → Analysis → Delivery → Support)
Demo Integration Guidelines
Three Streamlit Apps (hosted on Streamlit Community Cloud):

Predictive Analytics Dashboard – sales/demand forecasting with interactive sliders
Business KPI Visualizer – revenue/churn/growth metrics with date range filters
Inference Engine – run regression/hypothesis tests, see p-values and confidence intervals
Integration options (choose per page):

Preferred: Hyperlink buttons ("View Live Demo" → opens in new tab)
Optional: Responsive iframe with ?embedded=true query param (test rendering first)
Fallback: Static screenshots with link overlay if iframe breaks on mobile
Placement:

Portfolio page: Dedicated section per demo with screenshot + description + link
Services page: Inline "See this in action" links within relevant service cards
Homepage: Brief teaser section with thumbnails + "Explore Demos" CTA
Copy for demos:

Emphasize interactivity: "Adjust parameters and see results in real-time"
Explain value: "This is how I deliver insights to clients"
Include disclaimer: "Demo uses synthetic data for privacy"
Netlify Deployment Checklist
Before first deploy:

 Create GitHub repo, push all files
 Sign up for Netlify (free tier)
 Connect repo to Netlify
 Build settings: Build command: (leave blank), Publish directory: / or .
 Set up contact form with data-netlify="true" attribute
 Test form submission (Netlify captures to dashboard)
Post-deploy verification:

 All pages load without 404s
 Images render correctly (check paths)
 Forms submit successfully (check Netlify dashboard under Forms)
 Links to Streamlit demos open in new tabs
 Mobile responsiveness confirmed (Chrome DevTools)
 No console errors (check browser inspector)
Deploy previews:

Enable branch deploys for testing changes before merging to main
Code Style & Best Practices
HTML:

Semantic HTML5 tags: <header>, <nav>, <section>, <article>, <footer>
Always include alt text on images
Use ARIA labels where Bootstrap doesn't provide implicit accessibility
Proper heading hierarchy (<h1> once per page, then <h2>, <h3>, etc.)
CSS:

Mobile-first: write base styles for small screens, use @media (min-width: ...) for larger
Prefer Bootstrap utility classes (mt-4, text-center, btn-success) over custom CSS
Custom CSS only for brand colors, typography overrides, or unique components
Consistent indentation (2 spaces)
JavaScript:

Keep to absolute minimum (navbar toggle, smooth scroll to anchor links)
No jQuery (Bootstrap 5 doesn't require it)
Vanilla JS ES6+ syntax
Comment any non-obvious logic
Accessibility:

Color contrast ratio ≥ 4.5:1 for body text
Focus states visible on all interactive elements
Form labels properly associated with inputs
Skip-to-content link for screen readers (optional but nice)
Performance:

Compress images (aim for <200KB per image)
Use CDN links for Bootstrap, Font Awesome, Google Fonts (faster than self-hosting)
Minimize custom CSS/JS file sizes
Lazy load images if page gets image-heavy (future optimization)
Prohibitions & Constraints
Never do these things (even if they seem helpful):

❌ Introduce React, Next.js, Astro, Tailwind, or any framework requiring a build step
❌ Add features I didn't request: blog, dark mode, animations (beyond simple hover effects), chatbots, cookie banners (not needed at MVP)
❌ Suggest paid tools, premium hosting, domain purchases, or email marketing platforms during MVP
❌ Weaken or remove "Statistics Expert" positioning in favor of generic "data scientist" language
❌ Generate code with fetch() API calls or assume server-side rendering exists
❌ Use Lorem Ipsum or placeholder copy—write real, benefit-driven content
❌ Add services beyond the five listed (clients often ask; politely explain scope is fixed at MVP)
When I ask for changes:

Always confirm you understand the change before coding
Show me the specific lines of code you'll modify (use file paths with line numbers when referencing code: index.html:42)
Explain trade-offs if my request conflicts with the stack (e.g., "Adding X requires a backend, which isn't part of the static architecture")
How to Use This File
For you (Claude) in future conversations:

Treat this as your system prompt for the Seven24 project
When I open a new conversation or return after a break, reference this file to recall project context, brand voice, tech stack, and constraints
If I ask you to "check CLAUDE.md" or "remember the project rules," reread this file
If I request something that contradicts this file, politely flag the conflict and ask if I want to override
For me (the client):

This is my single source of truth—I can update it as the project evolves
If I forget a design rule or tech choice, I'll refer back here
When working with other developers or tools, I can share this file for instant context
Updating this file:

I'll tell you explicitly: "Update CLAUDE.md to reflect [change]"
You'll edit this file and confirm what changed
Keep it under 1,200 words so it stays scannable