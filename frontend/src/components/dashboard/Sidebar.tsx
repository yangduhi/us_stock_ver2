'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import {
    LayoutDashboard,
    TrendingUp,
    PieChart,
    Search,
    Settings,
    Bell,
    History,
    Activity,
    Zap,
    Shield,
    Briefcase,
    Globe
} from 'lucide-react'

const SIDEBAR_ITEMS = [
    {
        group: "개요", items: [
            { title: "대시보드", href: "/", icon: LayoutDashboard },
            { title: "시장 분석", href: "/analysis", icon: Activity },
            { title: "섹터 지도", href: "/sectors", icon: PieChart },
        ]
    },
    {
        group: "도구 및 정보", items: [
            { title: "종목 스크리너", href: "/screener", icon: Search },
            { title: "AI 시그널", href: "/signals", icon: Zap },
            { title: "리스크 모니터", href: "/risk", icon: Shield },
        ]
    },
    {
        group: "개인", items: [
            { title: "포트폴리오", href: "/portfolio", icon: Briefcase },
            { title: "기록", href: "/history", icon: History },
            { title: "알림", href: "/alerts", icon: Bell },
        ]
    },
    {
        group: "설정", items: [
            { title: "환경 설정", href: "/settings", icon: Settings },
        ]
    }
]

export function Sidebar() {
    const pathname = usePathname()

    return (
        <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-zinc-800 bg-[#0a0a0a] transition-transform">
            <div className="flex h-full flex-col overflow-y-auto px-3 py-4">
                {/* Logo */}
                <div className="mb-10 flex items-center gap-2 px-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500">
                        <TrendingUp className="h-5 w-5 text-white" />
                    </div>
                    <span className="text-xl font-bold tracking-tight text-white">MarketFlow</span>
                </div>

                {/* Navigation */}
                <nav className="flex-1 space-y-8">
                    {SIDEBAR_ITEMS.map((group) => (
                        <div key={group.group}>
                            <h2 className="mb-4 px-2 text-xs font-bold uppercase tracking-widest text-zinc-500">
                                {group.group}
                            </h2>
                            <div className="space-y-1">
                                {group.items.map((item) => {
                                    const isActive = pathname === item.href
                                    return (
                                        <Link
                                            key={item.href}
                                            href={item.href}
                                            className={cn(
                                                "group flex items-center rounded-lg px-2 py-2 text-sm transition-all duration-200",
                                                isActive
                                                    ? "bg-zinc-800/50 text-white border-l-2 border-green-500 rounded-l-none"
                                                    : "text-zinc-400 hover:bg-zinc-900 hover:text-white"
                                            )}
                                        >
                                            <item.icon className={cn(
                                                "mr-3 h-5 w-5",
                                                isActive ? "text-green-500" : "text-zinc-500 group-hover:text-white"
                                            )} />
                                            <span className="font-medium">{item.title}</span>
                                        </Link>
                                    )
                                })}
                            </div>
                        </div>
                    ))}
                </nav>

                {/* Bottom Section */}
                <div className="mt-auto border-t border-zinc-800 pt-4 px-2">
                    <div className="flex items-center gap-3 rounded-xl bg-zinc-900/50 p-3">
                        <div className="h-8 w-8 overflow-hidden rounded-full bg-zinc-700">
                            <div className="h-full w-full bg-gradient-to-br from-blue-500 to-cyan-400" />
                        </div>
                        <div className="flex flex-col">
                            <span className="text-xs font-bold text-white uppercase tracking-wider">Quant Alpha</span>
                            <span className="text-[10px] text-zinc-500">v2.5.0-S-Class</span>
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    )
}
