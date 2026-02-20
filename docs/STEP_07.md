# Step 7: Frontend Architecture (S-Class)

**Objective:** specific Next.js 14 App Router Implementation with **Zero-Layout-Shift** and **Streaming Hydration**.

## 1. Architectural Standards (Strict)
*   **Rendering Strategy:**
    *   **Shell (Sidebar/Nav):** React Server Components (RSC) - *Zero Bundle Size*.
    *   **Interactive Widgets:** Client Components (`'use client'`) with `Suspense` boundaries.
*   **State Management:**
    *   **Global UI:** `nuqs` (URL Query Params) for shareable state (e.g., `?ticker=AAPL&interval=1d`).
    *   **Server Cache:** React Query (`@tanstack/react-query`) with `staleTime: 5000`.
*   **Styling:**
    *   **Tailwind CSS v4** using the Neo-Fintech Dark design system (see [design_system.md](file:///D:/vscode/us_stock_ver2/docs/design_system.md)).
    *   **Shadcn UI** for all primitives, customized for high-contrast dark mode.

## 2. Task Instructions

### A. Core Setup
1.  **Initialize:**
    ```bash
    npx create-next-app@latest frontend --typescript --tailwind --eslint
    npx shadcn-ui@latest init
    ```
2.  **Directory Structure (Feature-First):**
    ```text
    frontend/app/
    ├── (dashboard)/        # Route Group (Protected)
    │   ├── layout.tsx      # RSC Shell (Sidebar + Navbar)
    │   ├── page.tsx        # /dashboard (Overview)
    │   └── [ticker]/       # /dashboard/AAPL
    ├── api/                # Route Handlers (BFF)
    └── components/
        ├── ui/             # Shadcn Primitives
        └── dashboard/      # Business Widgets
    ```

### B. Config-Driven Navigation
*   **File:** `frontend/config/nav.ts`
    ```typescript
    export const SIDEBAR_ITEMS = [
      { title: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { title: "Sectors", href: "/dashboard/sectors", icon: PieChart },
      // ... map all 12 items here
    ];
    ```
*   **Implementation:** `<Sidebar />` component maps this config. **NO HARDCODING.**

### C. UX & Performance
1.  **Streaming Skeletons:**
    *   Create `<DashboardSkeleton />` matching the exact layout grid.
    *   Wrap widgets in `Suspense`:
        ```tsx
        <Suspense fallback={<ChartSkeleton />}>
          <PriceChart ticker={ticker} />
        </Suspense>
        ```
2.  **Font Optimization:**
    *   Use `next/font/google` with `Inter` (UI) and `JetBrains Mono` (Data/Numbers).

## 3. Verification
*   **Lighthouse:** Performance Score > 95.
*   **UX Check:**
    *   Refresh page -> Shell loads instantly (server static).
    *   Widgets stream in parallel (no waterfall).
    *   URL changes when selecting a ticker.
