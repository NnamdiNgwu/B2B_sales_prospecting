import React from 'react'
import {
  ResponsiveContainer, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend,
} from 'recharts'

export type ChartPoint = {
  date: string
  sent?: number
  opens?: number
  clicks?: number
  responses?: number
}

type Props = { data: ChartPoint[] }

export const PerformanceChart: React.FC<Props> = ({ data }) => {
  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 24, left: 8, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="sent" stroke="#3b82f6" strokeWidth={2} dot={false} name="Sent" />
          <Line type="monotone" dataKey="opens" stroke="#10b981" strokeWidth={2} dot={false} name="Opens" />
          <Line type="monotone" dataKey="clicks" stroke="#f59e0b" strokeWidth={2} dot={false} name="Clicks" />
          <Line type="monotone" dataKey="responses" stroke="#ef4444" strokeWidth={2} dot={false} name="Responses" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}