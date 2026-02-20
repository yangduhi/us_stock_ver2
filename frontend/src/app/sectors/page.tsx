'use client'

import { SectorHeatmap } from '@/components/dashboard/SectorHeatmap'
import { useQuery } from '@tanstack/react-query'
import { fetchDashboardOverview } from '@/lib/api'

export default function SectorsPage() {
    const { data } = useQuery({
        queryKey: ['dashboard'],
        queryFn: fetchDashboardOverview,
        refetchInterval: 30000
    })

    return (
        <div className="min-h-screen p-8 text-white">
            <h1 className="mb-8 text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-300">
                섹터 퍼포먼스 (Sector Performance)
            </h1>
            <div className="h-[600px] w-full rounded-xl border border-zinc-800 bg-[#0f0f10] p-4">
                <SectorHeatmap sectors={data?.sectors} />
            </div>
        </div>
    )
}
