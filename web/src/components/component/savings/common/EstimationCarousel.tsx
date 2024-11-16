import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"

import { EnergyEstimation } from "@/types"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

export interface EstimationCarouselProps {
  production: EnergyEstimation | null
}

export default function EstimationCarousel({
  production,
}: EstimationCarouselProps) {
  if (!production) return null

  return (
    <section className="flex h-screen basis-full flex-col self-end px-4 py-[10vh] sm:flex-row sm:justify-between sm:px-6">
      <div className="basis-full sm:basis-1/2">
        <h2>Your savings:</h2>
        <p></p>
      </div>

      <div className="basis-full sm:basis-1/2">
        <ChartContainer
          config={{
            energy: {
              label: "Energy",
            },
          }}
        >
          <BarChart accessibilityLayer data={production.months}>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="month"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              tickFormatter={value => value.slice(0, 3)}
            />
            <Bar
              dataKey="energy"
              fill="rgb(58, 181, 46)"
              gradientTransform=""
              radius={4}
            />
            <ChartTooltip content={<ChartTooltipContent />} />
          </BarChart>
        </ChartContainer>
      </div>
    </section>
  )
}

const Card: React.FC<EnergyEstimation["months"][0]> = ({
  energy,
  order,
  month,
}) => {
  return (
    <div className="flex aspect-square grow basis-[8%] flex-col items-center justify-center rounded-[50%] bg-green-700 text-white">
      <p>{month}</p>
      <h4>{energy.toFixed(0)}</h4>
    </div>
  )
}
