import Map from "@/components/Map";

export default function Calculator() {
    return (
        <div className="flex w-screen h-[80vh] bg-gray-300 justify-center items-center flex-col">
            <h3 className="text-5xl black font-extrabold my-5">
                Now Darg your exact location
            </h3>
            <Map />
        </div>
    );
}
