# Seven24 Portfolio Website

> **Data, Analytics & AI for Better Business Decisions**

Professional portfolio and lead-generation website for Seven24, a Statistics Expert and Data & AI Consultant based in Kenya. Built with pure HTML, CSS, and minimal JavaScript for fast performance and easy deployment.

## 🚀 Live Site

- **Production URL:** [https://mokaya.netlify.app/](https://mokaya.netlify.app/)
- **Demo Streamlit Apps:** Replace placeholder URLs in `portfolio.html` with actual Streamlit app URLs

## 📋 Project Overview

**Purpose:** Showcase data analytics services and generate leads for SMEs, startups, and researchers worldwide

**Target Audience:** Businesses worldwide needing data cleaning, dashboards, statistical modeling, predictive analytics, and automation

**Brand Voice:** Professional, confident, approachable, benefit-focused, no hype

**Key Positioning:** "Academic rigor meets business speed" — Statistics Expert-powered solutions

## 🛠️ Technology Stack

- **HTML5** - Semantic, accessible markup
- **CSS3** - Bootstrap 5 via CDN + custom styles
- **JavaScript** - Minimal vanilla JS (smooth scroll, navbar)
- **Fonts** - Google Fonts (Roboto, Open Sans)
- **Icons** - Font Awesome 6
- **Hosting** - Netlify (free tier)
- **Forms** - Netlify Forms
- **Integrations** - Calendly (scheduling), Streamlit (demos)

**No build tools, no frameworks, no React — just static HTML for maximum simplicity.**

## 📁 Project Structure

```
Seven24/
├── index.html              # Home page (hero, services teaser, process, demos)
├── services.html           # Detailed service descriptions
├── portfolio.html          # Case studies + Streamlit demo links
├── about.html              # Bio, skills, values, process
├── faq.html                # FAQ accordion (8 questions)
├── contact.html            # Netlify form + Calendly embed
├── css/
│   └── custom.css          # Brand colors, components, responsive styles
├── js/
│   └── custom.js           # Smooth scroll, navbar highlighting
├── images/                 # Placeholder images (using Unsplash URLs)
├── README.md               # This file
└── CLAUDE.md               # Project context for AI-assisted development
```

## 🎨 Design System

### Colors
- **Primary Blue:** `#007BFF`
- **Hover Blue:** `#0d6efd`
- **Success Green:** `#198754` (CTAs, accents)
- **Light Background:** `#F8F9FA`
- **White:** `#FFFFFF`

### Typography
- **Primary Font:** Roboto (Google Fonts)
- **Secondary Font:** Open Sans
- **Base Size:** 16px
- **Line Height:** 1.6

### Components
- Responsive navbar with hamburger menu
- Bootstrap 5 cards with hover effects
- Accordion for FAQ and services
- Netlify Forms with honeypot spam protection
- Calendly inline embed

## 🚀 Local Development

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A code editor (VS Code, Sublime Text, etc.)

### Setup
1. **Clone or download** this repository
2. **Open `index.html`** in your browser
3. **That's it!** No build process, no npm install, no dependencies.

### Testing
- Test responsive design using browser DevTools (F12 → Device Toolbar)
- Test at breakpoints: 320px (mobile), 768px (tablet), 1920px (desktop)
- Test all navigation links
- Test form validation (contact form)

## 📦 Deployment to Netlify

### Step 1: Prepare Repository

```bash
# Initialize Git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Seven24 portfolio website"

# Add remote repository (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/seven24.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy to Netlify

1. **Sign up** at [netlify.com](https://netlify.com) (free tier)

2. **Create new site:**
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub account
   - Select the `Seven24` repository

3. **Build settings:**
   - **Build command:** Leave blank (no build required)
   - **Publish directory:** `/` or `.` (root directory)
   - Click "Deploy site"

4. **Wait for deployment:**
   - Netlify will deploy your site in ~1 minute
   - You'll get a random URL like `random-name-12345.netlify.app`

### Step 3: Configure Netlify Forms

1. **Enable forms:**
   - Go to Site settings → Forms
   - Forms should be automatically detected
   - Set up email notifications for form submissions

2. **Test the form:**
   - Go to your live site
   - Navigate to Contact page
   - Fill out and submit the form
   - Check Netlify dashboard → Forms to see submission

### Step 4: Custom Domain (Optional)

1. **Add custom domain:**
   - Site settings → Domain management
   - Add custom domain (e.g., `seven24.co.ke`)
   - Follow DNS configuration instructions

2. **Enable HTTPS:**
   - Netlify automatically provisions SSL certificates
   - HTTPS is enabled within ~24 hours

## 🔧 Post-Deployment Configuration

### Update Streamlit Demo URLs

In `portfolio.html` and `index.html`, replace placeholder URLs with actual Streamlit app URLs:

```html
<!-- Current placeholder -->
<a href="https://demo1.streamlit.app" ...>

<!-- Replace with your actual Streamlit app URL -->
<a href="https://your-app.streamlit.app" ...>
```

**3 Demos to deploy on Streamlit Community Cloud:**
1. **Predictive Analytics Dashboard** (sales/demand forecasting)
2. **Business KPI Visualizer** (revenue/churn/growth metrics)
3. **Inference Engine** (regression/hypothesis testing)

### Update Calendly URL

In `contact.html`, replace the placeholder Calendly URL:

```html
<!-- Current placeholder -->
<div class="calendly-inline-widget" data-url="https://calendly.com/datadetective10" ...>

<!-- Replace with your actual Calendly URL -->
<div class="calendly-inline-widget" data-url="https://calendly.com/yourusername" ...>
```

### Update Social Links

In all HTML files (footer), update social media URLs:
- **X (Twitter):** `https://twitter.com/Datadetective10`
- **LinkedIn:** Update with actual profile URL
- **GitHub:** Update with actual profile URL

### Replace Placeholder Images

Currently using Unsplash placeholder images. Replace with:
- Your professional headshot ([about.html](about.html))
- Actual project screenshots ([portfolio.html](portfolio.html))
- Custom images for demos ([index.html](index.html))

## 📝 Content Updates

### Adding a New Case Study

1. Open `portfolio.html`
2. Copy an existing `.portfolio-card` div
3. Update:
   - Image URL
   - Project title
   - Problem/Solution/Results
   - Tools/badges
4. Save and redeploy

### Updating Pricing

1. Open `services.html`
2. Find `.service-price` spans
3. Update pricing text
4. Save and redeploy

### Adding FAQ Items

1. Open `faq.html`
2. Copy an existing `.accordion-item` div
3. Update:
   - `id` attributes (e.g., `headingNine`, `collapseNine`)
   - Question and answer content
4. Save and redeploy

## 🧪 Testing Checklist

Before going live, verify:

### Functionality
- [ ] All navigation links work
- [ ] Hamburger menu opens/closes on mobile
- [ ] Netlify form submits successfully
- [ ] Calendly widget loads and allows booking
- [ ] "View Live Demo" buttons open in new tabs
- [ ] All internal anchor links work (#services, #contact-form, etc.)

### Responsive Design
- [ ] Looks good on mobile (320px - 767px)
- [ ] Looks good on tablet (768px - 991px)
- [ ] Looks good on desktop (1200px+)
- [ ] Images scale properly
- [ ] Text is readable at all sizes

### Performance
- [ ] Page load time < 3 seconds
- [ ] Images optimized (< 200KB each)
- [ ] Lighthouse Performance score > 90
- [ ] Lighthouse Accessibility score > 90
- [ ] Lighthouse SEO score > 90

### SEO
- [ ] All pages have unique meta titles
- [ ] All pages have meta descriptions
- [ ] All images have alt text
- [ ] Proper heading hierarchy (one h1 per page)
- [ ] No broken links (use validator)

### Accessibility
- [ ] Screen reader can navigate site
- [ ] Keyboard navigation works (Tab key)
- [ ] Color contrast passes WCAG AA
- [ ] All buttons have aria-labels where needed

## 🔒 Security Notes

- **Netlify Forms:** Honeypot field (`bot-field`) included for spam protection
- **External Links:** All external links open in new tabs with `rel="noopener noreferrer"`
- **No Sensitive Data:** No API keys or credentials in code
- **HTTPS:** Netlify provides free SSL certificates

## 📊 Analytics (Optional)

To add Google Analytics:

1. Get your GA4 Measurement ID from Google Analytics
2. Add to `<head>` of all HTML files:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## 🐛 Troubleshooting

### Netlify Form Not Working
- Check that `data-netlify="true"` attribute is present
- Verify hidden field `<input type="hidden" name="form-name" value="contact">` exists
- Check Netlify dashboard → Forms to see if detected
- Test after deploying (forms don't work locally)

### Calendly Not Loading
- Verify Calendly script is included: `<script src="https://assets.calendly.com/assets/external/widget.js" async></script>`
- Check that `data-url` matches your Calendly username
- Test on live site (may not work locally)

### Responsive Issues
- Test using browser DevTools device emulator
- Check Bootstrap 5 grid classes (`col-lg-*`, `col-md-*`, `col-sm-*`)
- Verify viewport meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

### Images Not Loading
- Check file paths (case-sensitive on Linux servers)
- Verify Unsplash URLs are correct and accessible
- Replace with local images if needed

## 🚀 Future Enhancements

**Phase 2 (After MVP):**
- Add testimonials section to home page
- Create blog for SEO content marketing
- Add custom domain (e.g., `seven24.co.ke`)
- Implement live chat widget (e.g., Tawk.to)
- Add portfolio filtering by service type

**Phase 3 (Advanced):**
- Integrate Google Analytics for traffic tracking
- Add reCAPTCHA to contact form if spam increases
- Create downloadable lead magnet (e.g., "Data Analysis Checklist" PDF)
- Build email newsletter signup
- Add dark mode toggle

## 📞 Support

**Built by:** Seven24
**Contact:** [contact.html](https://yourdomain.com/contact.html)
**X (Twitter):** [@Datadetective10](https://twitter.com/Datadetective10)

---

## 📄 License

This is a personal portfolio website. All content and code are proprietary to Seven24.

---

**Built with ❤️ using pure HTML, CSS, and minimal JavaScript.**
