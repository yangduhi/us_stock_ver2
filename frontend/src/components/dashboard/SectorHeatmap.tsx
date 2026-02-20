'use client'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Treemap, ResponsiveContainer, Tooltip } from "recharts"

interface SectorHeatmapProps {
    sectors?: Record<string, number>
}

const CustomizedContent = (props: any) => {
    const { root, depth, x, y, width, height, index, payload, colors, rank, name, change } = props;

    return (
        <g>
            <rect
                x={x}
                y={y}
                width={width}
                height={height}
                style={{
                    fill: change > 0 ? "#22c55e" : "#ef4444", // Neon Green or Neon Red
                    stroke: "#050505",
                    strokeWidth: 2,
                    fillOpacity: Math.min(0.2 + (Math.abs(change) / 10), 1), // Dynamic opacity based on change
                }}
            />
            {width > 40 && height > 30 && (
                <text
                    x={x + width / 2}
                    y={y + height / 2 - 4}
                    textAnchor="middle"
                    fill="#fff"
                    fontSize={12}
                    fontWeight="bold"
                    className="uppercase tracking-tighter"
                >
                    {name}
                </text>
            )}
            {width > 40 && height > 30 && (
                <text
                    x={x + width / 2}
                    y={y + height / 2 + 12}
                    textAnchor="middle"
                    fill={change > 0 ? "#4ade80" : "#f87171"}
                    fontSize={11}
                    fontWeight="bold"
                >
                    {change > 0 ? "+" : ""}{change}%
                </text>
            )}
        </g>
    );
};

export function SectorHeatmap({ sectors }: SectorHeatmapProps) {
    // Transform object to array
    const data = sectors
        ? Object.entries(sectors).map(([name, change]) => ({
            name,
            size: Math.abs(change) + 1, // Size based on magnitude of move (visual weight), +1 to avoid 0
            change
        }))
        : []

    return (
        <Card className="border-zinc-800 bg-[#0f0f10]">
            <CardHeader className="pb-2">
                <CardTitle className="text-white">Sector Performance</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="h-[280px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <Treemap
                            data={data}
                            dataKey="size"
                            aspectRatio={4 / 3}
                            stroke="#050505"
                            content={<CustomizedContent />}
                        >
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#0f0f10',
                                    borderColor: '#27272a',
                                    borderRadius: '12px',
                                    padding: '8px'
                                }}
                            />
                        </Treemap>
                    </ResponsiveContainer>
                </div>
            </CardContent>
        </Card>
    )
}
