import LocationForm from "@/components/LocationForm"

export default function Home() {
  return (
    <div className="flex h-[70vh] w-full flex-col items-center justify-center bg-slate-200 px-4">
      <h2 className="black my-10 text-5xl font-extrabold md:text-7xl">
        Solarwise
      </h2>
      <LocationForm />
    </div>
  )
}
