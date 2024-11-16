"use client"

import Map from "@/components/component/Map"
import CalculateForm from "./common/CalculateForm"
import { useState } from "react"
import { EnergyEstimation } from "@/types"
import EstimationCarousel from "./common/EstimationCarousel"

export default function SavingEstimation() {
  const [production, setProduction] = useState<EnergyEstimation | null>(null)

  const scrollToSavings = () => {}

  return (
    <>
      <section className="flex h-[80vh] w-full flex-row items-center justify-around gap-10 bg-gray-300 md:px-10">
        <Map />
        <CalculateForm
          setProduction={setProduction}
          // scrollTrigger={scrollToSavings}
        />
      </section>
      <EstimationCarousel production={production} />
    </>
  )
}
