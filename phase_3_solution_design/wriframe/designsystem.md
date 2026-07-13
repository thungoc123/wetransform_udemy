---
name: EduInsight AI
colors:
  surface: '#fbf8fa'
  surface-dim: '#dcd9db'
  surface-bright: '#fbf8fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f4'
  surface-container: '#f0edef'
  surface-container-high: '#eae7e9'
  surface-container-highest: '#e4e2e3'
  on-surface: '#1b1b1d'
  on-surface-variant: '#45474c'
  inverse-surface: '#303032'
  inverse-on-surface: '#f3f0f2'
  outline: '#75777d'
  outline-variant: '#c5c6cd'
  surface-tint: '#545f73'
  primary: '#091426'
  on-primary: '#ffffff'
  primary-container: '#1e293b'
  on-primary-container: '#8590a6'
  inverse-primary: '#bcc7de'
  secondary: '#006591'
  on-secondary: '#ffffff'
  secondary-container: '#39b8fd'
  on-secondary-container: '#004666'
  tertiary: '#1e1200'
  on-tertiary: '#ffffff'
  tertiary-container: '#35260c'
  on-tertiary-container: '#a38c6a'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e3fb'
  primary-fixed-dim: '#bcc7de'
  on-primary-fixed: '#111c2d'
  on-primary-fixed-variant: '#3c475a'
  secondary-fixed: '#c9e6ff'
  secondary-fixed-dim: '#89ceff'
  on-secondary-fixed: '#001e2f'
  on-secondary-fixed-variant: '#004c6e'
  tertiary-fixed: '#fadfb8'
  tertiary-fixed-dim: '#ddc39d'
  on-tertiary-fixed: '#271902'
  on-tertiary-fixed-variant: '#564427'
  background: '#fbf8fa'
  on-background: '#1b1b1d'
  surface-variant: '#e4e2e3'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-mono:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-margin: 24px
  gutter: 16px
  section-gap: 32px
  card-padding: 20px
---

## Brand & Style
The design system is engineered for educators and course creators who require clarity amidst complex datasets. The brand personality is **Intellectual, Reliable, and Precise**. It balances the authority of traditional academia with the forward-leaning energy of artificial intelligence.

The visual style follows a **Modern Corporate Minimalism** approach. It prioritizes information density without sacrificing legibility. By utilizing expansive whitespace and a structured containment system, the UI transforms raw learning analytics into actionable insights. The aesthetic is clean and "quiet," allowing the data visualizations—the hero of the platform—to command attention through color and contrast.

## Colors
The palette is anchored by a deep **Slate Navy** (Primary) to establish professional trust and groundedness. This is contrasted by an **Electric Cyan** (Secondary) used for interactive elements and "AI-driven" moments, such as automated suggestions or predictive insights.

- **Primary (#1E293B):** Used for navigation, headers, and primary text to ensure high contrast.
- **Secondary (#0EA5E9):** Used for primary buttons, active states, and key data trend lines.
- **Neutral/Background:** A cool grayscale palette (Slate) is used to prevent visual fatigue during long analysis sessions.
- **Semantic Colors:** Applied strictly to data status. Success (green) for completion rates, Warning (amber) for at-risk students, and Danger (red) for immediate drop-out alerts.

## Typography
This design system utilizes **Inter** for its exceptional legibility in data-heavy environments and high x-height. It remains neutral while providing the structural clarity needed for dashboards.

To enhance the "data-driven" feel, **JetBrains Mono** is introduced selectively for numerical values, IDs, and timestamps within tables. This monospaced secondary font ensures that columns of numbers align perfectly, aiding in quick scanning and comparison.

- **Headlines:** Use tight letter spacing and semi-bold weights to create a strong visual anchor.
- **Labels:** Uppercase labels are used for small category headers to differentiate from body text.
- **Hierarchy:** Maintain a clear distinction between "Reading" (Body) and "Scanning" (Data/Labels).

## Layout & Spacing
The layout follows a **12-column fluid grid** for desktop, transitioning to a single-column stack for mobile.

- **The Dashboard Grid:** A fixed sidebar (240px) provides persistent navigation, while the main content area uses fluid percentage-based columns.
- **Rhythm:** An 8px linear scale (incremented by 4px for tight components) governs all padding and margins.
- **Grouping:** Related data cards should be grouped with a 32px gap, while internal card elements use 16px or 20px padding to maintain a "breathable" feel.
- **Mobile:** Margins reduce to 16px, and all multi-column data cards reflow vertically to ensure charts remain legible.

## Elevation & Depth
Depth is used functionally to indicate interactivity and information hierarchy rather than for decoration.

- **Base Layer:** The background uses a soft Slate-50 (#F8FAFC) to reduce glare.
- **Surface Layer (Cards):** Main content containers are pure white with a subtle 1px border (#E2E8F0) and a very soft, diffused shadow (0px 4px 12px rgba(0,0,0,0.03)).
- **Hover States:** Interactive cards slightly lift on hover, increasing shadow depth and changing the border color to the Secondary Cyan.
- **Overlays:** Modals and dropdowns use a more pronounced shadow to clearly separate them from the dashboard background, accompanied by a light background blur (8px) for the backdrop.

## Shapes
The shape language is **Rounded (Level 2)**.

- **Cards & Containers:** Use a 12px (rounded-lg) radius to soften the high-density data and make the interface feel more modern and accessible.
- **Buttons & Inputs:** Use an 8px radius to maintain a professional, sharp appearance that suggests precision.
- **Badges:** Small status indicators use a full pill shape to distinguish them from interactive buttons.
- **Graphs:** Chart elements (bars, area fills) should also utilize small 2px-4px corner radii where technically possible to align with the overall UI language.

## Components
- **Buttons:** Primary buttons use a solid Secondary Cyan fill with white text. Secondary buttons use an outline style with Primary Navy text.
- **Data Cards:** Every card must include a header (Title + Icon/Action) and a footer for "View Details" links. Cards are the primary vessel for all analytics.
- **Status Badges:** Use a "soft" background (10% opacity of the semantic color) with high-contrast text for status labels (e.g., a pale green background with dark green text for "Complete").
- **Input Fields:** Use a subtle Slate-100 fill that turns white on focus with a 2px Cyan border. Labels should always be visible above the field.
- **Data Visualizations:** Use a custom-curated palette of blues, purples, and teals for multi-series charts. Ensure line weights are 2px minimum for accessibility.
- **Empty States:** When no data is available, use light-line illustrations and a clear CTA to "Import Data" or "Sync Course."
