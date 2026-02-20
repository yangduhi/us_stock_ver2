# MarketFlow Design System Specification

**Theme Name:** Neo-Fintech Dark  
**Core Philosophy:** Data-Dense, High Contrast, immersive Dark Mode with Neon Accents.  
**Tech Stack:** Tailwind CSS, Lucide Icons, Shadcn UI (Customized).

## 1. 🌑 Color Palette (Tailwind Config)
Background is nearly absolute black, but with subtle levels for depth.

| 용도 | Hex Code | Tailwind Class | 설명 |
| :--- | :--- | :--- | :--- |
| Global Background | `#050505` | `bg-[#050505]` | 앱 전체 배경 (거의 완전한 블랙) |
| Card Background | `#0f0f10` | `bg-[#0f0f10]` | 대시보드 위젯/카드 배경 |
| Sidebar Background | `#0a0a0a` | `bg-[#0a0a0a]` | 좌측 네비게이션 바 |
| Border (Subtle) | `#27272a` | `border-zinc-800` | 카드 및 섹션 구분선 (Opacity 20% 느낌) |
| Brand Primary | `#3b82f6` | `text-blue-500` | 로고, 링크, 주요 강조색 |
| Accent Green (Bull) | `#22c55e` | `text-green-500` | 상승, 매수 신호 (Neon Green) |
| Accent Red (Bear) | `#ef4444` | `text-red-500` | 하락, 매도 신호, 리스크 (Neon Red) |
| Accent Yellow | `#eab308` | `text-yellow-500` | 중립, 경고 (Warning) |
| Text Primary | `#ffffff` | `text-white` | 주요 제목, 수치 |
| Text Secondary | `#a1a1aa` | `text-zinc-400` | 설명, 라벨, 보조 텍스트 |

## 2. 📐 Typography & Layout
- **Font Family:** Inter or Geist Sans (System UI Font).
- **Font Weights:**
  - **Headings:** Bold (700) or ExtraBold (800) for huge numbers.
  - **Body:** Regular (400).
  - **Labels:** Medium (500), Uppercase tracking-wider.
- **Corner Radius:**
  - **Cards:** `rounded-xl` (12px) - Modern & soft.
  - **Buttons:** `rounded-lg` (8px).
  - **Tags/Badges:** `rounded-full`.

## 3. 🧩 Component Instructions

### A. Sidebar (Navigation)
- **Width:** Fixed `w-64` (256px).
- **Styling:** `bg-[#0a0a0a]` with `border-r border-zinc-800`.
- **Menu Item:**
  - Default: `text-zinc-400 hover:text-white hover:bg-zinc-900`.
  - **Active State:** `bg-zinc-800/50 text-white border-l-2 border-green-500` (Green vertical bar on left).
- **Grouping:** Section headers use `text-xs font-bold text-zinc-500 uppercase tracking-widest`.

### B. Dashboard Cards (Widgets)
- **Container:** `bg-[#0f0f10] border border-zinc-800 rounded-xl p-6`.
- **Shadow:** Minimal `shadow-sm`. Depth provided by border contrast.
- **Header:** `text-lg font-semibold text-white`.

### C. Gradient Text (Hero Section)
Use for primary emphasis (e.g., "One-Stop Dashboard").
```html
<h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
  One-Stop Dashboard
</h1>
```

### D. Data Visualization
- **Gauges (Donut):**
  - Background Ring: `stroke-zinc-800`.
  - Data Ring: `stroke-green-500` or `stroke-yellow-500`.
  - Center Text: `text-3xl font-bold`.
- **Progress Bars:**
  - Background: `bg-zinc-800`.
  - Fill: `bg-green-500` (Bullish), `bg-red-500` (Bearish).
  - Height: `h-2` or `h-3`.

### E. Status Badges
- **Style:** Background at 10~20% opacity.
- **Example:**
```html
<span class="px-2 py-1 rounded-full text-xs font-medium bg-green-500/10 text-green-500 border border-green-500/20">
  Risk-On
</span>
```

## 4. 💡 Visual Effects
- **Hover Effect:** `hover:bg-zinc-800/50` for cards/items.
- **Skeleton Loading:** `animate-pulse bg-zinc-800 rounded` to prevent layout shift.
- **Glassmorphism:** Use `backdrop-blur-md bg-black/70` strictly for modals/tooltips.
