import LocationForm from "@/components/LocationForm";

export default function Home() {
    return (
        <div className="w-full bg-slate-200 h-[70vh] flex justify-center items-center flex-col px-4">
            <h2 className="text-5xl md:text-7xl black font-extrabold my-10">
                Solarwise
            </h2>
            <LocationForm />
        </div>
    );
}
