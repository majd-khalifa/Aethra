# AETHRA — Complete Brand Identity & Visual Design Guidelines

**Production Release:** Approved Identity Master (`06_Approved_Identity_Production`)  
**Brand Positioning:** Software Development & Digital Technology Services  
**Central Brand Idea:** *"From the unseen to the extraordinary."*

---

## 1. Brand Overview & Positioning

**AETHRA** is a software development and digital technology company that partners with startups, entrepreneurs, small and medium-sized businesses, and growing enterprises to design, architect, and engineer reliable digital systems.

### Core Service Capabilities
- **Custom Software Development:** Tailored operational platforms, core domain engines, and internal business tools.
- **Web Applications & Portals:** High-performance browser applications, customer portals, and administrative control planes.
- **Mobile Applications:** Native and cross-platform iOS and Android applications built for speed and clarity.
- **Backend Systems & Databases:** Resilient server architectures, relational database schemas, and cloud infrastructure.
- **APIs & System Integrations:** Versioned REST and GraphQL contracts connecting ERPs, payment gateways, and third-party services.
- **Workflow Automation:** Event-driven pipelines and background services that eliminate manual operational bottlenecks.

### Brand Personality Attributes
1. **Intelligent, inventive, and forward-thinking** — grounded in real engineering logic.
2. **Confident without being arrogant** — clear, direct, and plain-spoken.
3. **Youthful without looking childish** — contemporary geometric precision without gimmicks.
4. **Premium without looking pretentious** — editorial restraint and generous negative space.
5. **Minimal without feeling empty** — every line, plane, and token serves a structural purpose.

---

## 2. Brand Story & Philosophy

Inspired conceptually by the classical notion of *Aether*—the subtle upper element—**AETHRA** expresses the transition from unseen thought to tangible digital reality:

> **"From the unseen to the extraordinary."**

Every software product begins as an invisible concept: a business model, an operational bottleneck, or an architectural hypothesis. Through logic, software engineering, and disciplined design, AETHRA transforms unseen ideas into structured, reliable digital systems.

**Visual Discipline:** We never illustrate this story with literal outer-space clichés (stars, galaxies, planets, neon portals, or circuit-board clipart). Instead, we express it through **clean geometric construction, luminous light-first surfaces, and a rising diagonal trajectory**.

---

## 3. Approved Logo System & Concept Explanation

### 3.1 The Approved `A` Monogram
The canonical AETHRA symbol (`01_Logo/SVG/aethra_logo_symbol_color.svg`) is reconstructed directly from `00_Reference/APPROVED_LOGO_REFERENCE.png` inside a `1000 × 1000` master coordinate grid:

- **Outer Silhouette:** A symmetrical apex triangle spanning `x = 100.0 .. 900.0` (`width = 800u`) and `y = 140.0 .. 860.0` (`height = 720u`), with an exact `9 : 5` (`1.80`, `60.95°`) leg slope.
- **Uniform Geometric Stroke Weight:** All four structural members—the left leg, right leg, rising internal crossbar, and lower-right horizontal base terminal—share a uniform perpendicular stroke width of **`62.6u`** (`8.7%` of symbol height).
- **Rising Diagonal Crossbar (`21.03°`):** Instead of a static horizontal bar, the internal crossbar rises from the lower-left vertex `(100.0, 860.0)` to meet the inner right leg at `(696.2, 624.6)`, embodying forward momentum and the ascent from concept to system.
- **Open Lower Geometry & Base Terminal:** The lower base remains open between `x = 100.0` and `x = 549.2`, anchored on the right by a crisp horizontal foot (`x = 584.0 .. 900.0`, `y = 860.0`) with an angled `60.95°` inner bevel `(549.2, 797.4)`.

### 3.2 Custom Outlined `AETHRA` Wordmark
- Set in custom geometric uppercase letterforms (`Λ E T H R Λ`) where both `A` glyphs omit their horizontal crossbars to form open architectural chevrons that echo the `A` monogram's open lower geometry.
- **Tracking:** Generous `+0.26em` architectural letter-spacing.
- **Primary Color:** Deep Violet-Ink (`#171327`) on light backgrounds; Crisp Near-White (`#FCFBFF`) on dark backgrounds.
- **Legal Cleanliness:** Never append decorative `®` or `™` symbols.

---

## 4. Logo Clear Space, Minimum Size & Misuse Rules

### 4.1 Clear Space Rule
- Define `X` as `20%` (`0.20 × H`) of the symbol height `H`.
- Maintain a minimum clear-space zone of **`1X` (`0.20 × H`)** on all four sides of the stacked lockup, horizontal lockup, or standalone symbol.

### 4.2 Minimum Size & Micro-Size Optimization
| Variant | Minimum Digital Size | Minimum Print Size | Usage Notes |
| :--- | :--- | :--- | :--- |
| **Stacked Lockup** | `120 px` width | `28 mm` width | Primary hero, cover, and profile lockup |
| **Horizontal Lockup** | `140 px` width | `32 mm` width | Website headers, app navbars, document headers |
| **Standalone Symbol** | `24 px × 24 px` | `6 mm × 6 mm` | Standard UI icons, avatars, social badges |
| **Micro Symbol (`aethra_logo_micro_small_size.svg`)** | `16 px × 16 px` | `4 mm × 4 mm` | Browser favicons (`16px`/`24px`) — features `+32%` optical stroke reinforcement (`82.6u`) |

### 4.3 Logo Misuse Rules (Strictly Prohibited)
1. **Do not** rotate, skew, or italicize the symbol or wordmark.
2. **Do not** replace the open-chevron `Λ` glyphs in `AETHRA` with standard closed-bar typeface `A`s.
3. **Do not** close the open lower base of the `A` monogram or flatten its rising diagonal crossbar.
4. **Do not** apply neon outer glows, heavy drop shadows, 3D extrusions, or cosmic/starfield effects.
5. **Do not** place the violet gradient mark on low-contrast mid-tone purple backgrounds.
6. **Do not** alter the proportion or spacing between the `A` symbol and the `AETHRA` wordmark.

---

## 5. Color System & Usage Proportions

AETHRA is a **light-first brand identity** with controlled dark-mode flexibility for software interfaces and technical diagrams.

| Role | Token Name | HEX | RGB | Usage Proportion & Function |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Light Surface** | `--aethra-surface-primary` | `#FCFBFF` | `252, 251, 255` | **65%** — Primary canvas background across web, docs, and social |
| **Soft Lavender Surface** | `--aethra-surface-tint` | `#F2EDFF` | `242, 237, 255` | **18%** — Secondary cards, pills, and subtle diagonal background planes (`#EAE0FF`) |
| **Deep Violet-Ink** | `--aethra-ink` | `#171327` | `23, 19, 39` | **10%** — Primary wordmark, headlines, body copy (`#615B73`), and dark-mode canvas |
| **Primary Brand Violet** | `--aethra-violet-primary` | `#7446F5` | `116, 70, 245` | **7%** — Canonical symbol gradient (`#B18CFE → #7446F5 → #5D2BE7`), CTAs, and active indicators |

### Verified WCAG 2.1 Contrast Ratios
- **Deep Ink (`#171327`) on Primary Light Surface (`#FCFBFF`):** `17.90 : 1` (**WCAG AAA**)
- **Deep Ink (`#171327`) on Soft Lavender (`#F2EDFF`):** `15.84 : 1` (**WCAG AAA**)
- **Muted Slate-Ink (`#615B73`) on Primary Light Surface (`#FCFBFF`):** `5.82 : 1` (**WCAG AA**)
- **Deep Accessible Violet (`#5D2BE7`) on Primary Light Surface (`#FCFBFF`):** `5.71 : 1` (**WCAG AA**)
- **Primary Light Surface (`#FCFBFF`) on Deep Ink (`#171327`):** `17.90 : 1` (**WCAG AAA**)

---

## 6. Typography System & Hierarchy

All brand typography uses open-source **SIL Open Font License 1.1** typefaces bundled in `05_Brand_Guidelines/fonts/`:

1. **Primary Display & Headlines — `Space Grotesk` (`600 SemiBold`, `700 Bold`)**
   - Engineered geometric sans-serif that complements the sharp linear geometry of the `A` monogram.
   - Line height: `1.05 – 1.15`; Tracking: `-0.03em` to `-0.02em`.
2. **Body Copy & UI Controls — `Inter` (`400 Regular`, `500 Medium`, `600 SemiBold`)**
   - Neutral, high-x-height grotesque for long-form readability and dense product interfaces.
   - Line height: `1.50 – 1.60`; Tracking: `0em`.
3. **Technical Labels, Tags & Specs — `IBM Plex Mono` (`400 Regular`, `500 Medium`, `600 SemiBold`)**
   - Used for section numbers (`01 // CAPABILITIES`), architecture tags, and API contract snippets.
   - Line height: `1.40`; Tracking: `+0.06em` to `+0.10em` (uppercase).

---

## 7. Graphic Language & Layout Grid

- **Subtle Angular Lavender Planes:** Echoing `APPROVED_LOGO_REFERENCE.png`, light canvases (`#FCFBFF`) feature subtle rising diagonal planes (`#F2EAFF` / `#EAE0FF`) parallel to the `60.95°` leg slope of the `A` monogram.
- **Hairline Architectural Frames:** Content is organized inside clean `1px–1.5px` structural borders (`#E2D9FA` in light mode, `#322A4D` in dark mode) with `12px–20px` corner radii.
- **12-Column Layout Grid:**
  - Desktop (`1440 px`): 12 columns, `80 px` outer margins, `24 px` gutters.
  - Mobile (`390 px`): 4 columns, `24 px` outer margins, `16 px` gutters.
  - Instagram Portrait (`1080 × 1350 px`): `48 px` outer structural frame, `88 px` content margin.
