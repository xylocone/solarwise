import Map from "@/components/Map"

export default function Calculator() {
  return (
    <div className="flex h-[80vh] w-screen flex-col items-center justify-center bg-gray-300">
      <h3 className="black my-5 text-5xl font-extrabold">
        Now Drag your exact location
      </h3>
      <Map />
    </div>
  )
}
