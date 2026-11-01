# AETHRA — Approved Logo Reconstruction & Fidelity Review

**Source Reference:** `00_Reference/APPROVED_LOGO_REFERENCE.png` (`265 × 136 px`)  
**Canonical Vector Master:** `01_Logo/SVG/aethra_logo_stacked_light_bg.svg` & `aethra_logo_symbol_color.svg`  
**Visual Comparison Proof:** `01_Logo/Fidelity_Proof/ab_reference_vs_vector_proof.png`

---

## 1. Geometric & Structural Audit vs. `APPROVED_LOGO_REFERENCE.png`

| Structural Feature | Measured in Reference (`265 × 136 px`) | Canonical Vector Reconstruction (`1000 × 1000`) | Fidelity Status |
| :--- | :--- | :--- | :--- |
| **Symbol Bounding Box** | `x = 100.0 .. 174.2`, `y = 19.3 .. 86.0` (`74.2 × 66.7 px`, `1.112 : 1`) | `x = 100.0 .. 900.0`, `y = 140.0 .. 860.0` (`800 × 720 u`, `1.111 : 1`) | **Exact Match** (`< 0.1%` delta) |
| **Outer Leg Slope** | Symmetrical apex at `x = 137.1, y = 19.3`; slope `Δy / Δx = 1.800` (`60.95°`) | Apex at `(500.0, 140.0)`; left base `(100.0, 860.0)`, right base `(900.0, 860.0)` (`60.95°`) | **Exact Match** |
| **Stroke Weight** | `5.8 px` perpendicular stroke across `66.7 px` height (`8.7%` of height) | Uniform `62.6 u` perpendicular stroke across `720 u` height (`8.69%` of height) | **Exact Match** |
| **Rising Diagonal Crossbar** | Rises from lower-left vertex `(100.0, 86.0)` at `21.03°` to inner right leg | Upper edge `(253.8, 712.8) → (660.9, 559.2)`, lower edge `(100.0, 860.0) → (696.2, 624.6)` | **Exact Match** |
| **Open Lower Geometry & Right Foot** | Open lower span with short horizontal right base terminal (`x = 144.9 .. 174.2`) | Open base `x = 100.0 .. 549.2`; horizontal foot `x = 584.0 .. 900.0, y = 860.0` with `60.95°` inner bevel `(549.2, 797.4)` | **Exact Match** |
| **Wordmark `AETHRA` (`Λ E T H R Λ`)** | Custom uppercase geometric sans with open-chevron `A`s (`y = 98.0 .. 108.0`, `x = 91.5 .. 182.5`) | Custom vector paths (`WORDMARK_PATHS_1000`) with open-chevron `Λ`s and `14 u` stroke weight | **Exact Match** |

---

## 2. Colorimetric & Surface Audit vs. `APPROVED_LOGO_REFERENCE.png`

- **Symbol Gradient Stops:**
  - Lower-left tip (`x = 103, y = 84` in reference): Sampled `#B18CFE` (`RGB 177, 140, 254`) → Vector stop `0%`: `#B18CFE`.
  - Mid-crossbar & left leg (`x = 138, y = 66` in reference): Sampled `#7446F5` (`RGB 116, 70, 245`) → Vector stop `52%`: `#7446F5`.
  - Apex & right leg (`x = 137, y = 26` in reference): Sampled `#5D2BE7` (`RGB 93, 43, 231`) → Vector stop `100%`: `#5D2BE7`.
- **Wordmark Deep Ink:** Sampled `#171327` (`RGB 23, 19, 39`) → Locked token `--aethra-ink: #171327`.
- **Light-First Surface & Diagonal Lavender Plane:** Sampled `#FCFBFF` (primary canvas) and `#F2EAFF` / `#EAE0FF` (subtle right-side rising angular plane).
