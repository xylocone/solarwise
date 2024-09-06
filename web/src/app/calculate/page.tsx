import Map from "@/components/component/Map"
import CalculateForm from "@/components/component/CalculateForm"

export default function Calculator() {
  return (
    <div className="flex h-[80vh] w-screen flex-row items-center gap-10 bg-gray-300 md:px-10">
      <div className="w-1/2">
        <Map />
      </div>
      <div className="w-1/2 flex justify-center">
        <CalculateForm />
      </div>
    </div>
  )
}
