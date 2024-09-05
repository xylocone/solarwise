"use client";

import { useEffect, useState, useRef } from "react";
import { useDebounceCallback } from "usehooks-ts";
import { OpenStreetMapProvider } from "leaflet-geosearch";
import "@/components/ui/form";
import { Button } from "./ui/button";
import { SearchResult } from "leaflet-geosearch/dist/providers/provider.js";
import { useRouter } from "next/navigation";

export default function LocationForm() {
    const [input, setInput] = useState("");
    const [results, setResults] = useState<SearchResult[]>([]);
    const [selectedIndex, setSelectedIndex] = useState(-1);
    const resultRefs = useRef<(HTMLLIElement | null)[]>([]);

    const debouncedSetInput = useDebounceCallback((value) => {
        setInput(value);
    }, 300);

    const router = useRouter();

    useEffect(() => {
        const provider = new OpenStreetMapProvider();
        const fetchResults = async () => {
            if (input) {
                const searchResults = await provider.search({ query: input });
                setResults(searchResults);
                setSelectedIndex(-1); // to make the selectedIndex -1 after search
            } else {
                setResults([]);
                setSelectedIndex(-1);
            }
        };
        fetchResults();
    }, [input]);

    const handleSelectResult = (index: number) => {
        setSelectedIndex(index);
        setInput(results[index].label);
        setResults([]);
        handleSubmit(index);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "ArrowDown") {
            e.preventDefault();
            setSelectedIndex((prevIndex) => {
                const newIndex = (prevIndex + 1) % results.length;
                resultRefs.current[newIndex]?.scrollIntoView({
                    behavior: "smooth",
                    block: "nearest",
                });
                return newIndex;
            });
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            setSelectedIndex((prevIndex) => {
                const newIndex =
                    (prevIndex - 1 + results.length) % results.length;
                resultRefs.current[newIndex]?.scrollIntoView({
                    behavior: "smooth",
                    block: "nearest",
                });
                return newIndex;
            });
        } else if (e.key === "Enter") {
            e.preventDefault();
            handleSubmit(selectedIndex);
        }
    };

    const handleSubmit = (index: number) => {
        const selectedLocation = results[index >= 0 ? index : 0]; // Pick the top result if nothing is selected
        if (selectedLocation) {
            console.log("Submitted Location:", selectedLocation);
            localStorage.setItem(
                "user-location",
                JSON.stringify(selectedLocation)
            );
            router.push("/calculator");
        }
    };

    return (
        <div className="w-full bg-slate-200 h-[70vh] flex items-center flex-col">
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    handleSubmit(selectedIndex);
                }}
            >
                <div className="flex justify-center items-center mb-2">
                    <input
                        type="text"
                        onChange={(e) => debouncedSetInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Search location"
                        className="pl-4 p-2 h-full "
                    />
                    <Button type="submit" className="rounded-none">
                        Check Your Roof
                    </Button>
                </div>
                <ul className="w-full md:max-w-1/2 md:mx-auto bg-white border border-gray-300 rounded shadow-lg max-h-[200px] overflow-y-auto">
                    {results.map((result: SearchResult, index: number) => (
                        <li
                            key={index}
                            ref={(el) => (resultRefs.current[index] = el)}
                            onClick={() => handleSelectResult(index)}
                            className={`p-2 border-b last:border-none hover:bg-gray-100 cursor-pointer ${
                                selectedIndex === index ? "bg-gray-200" : ""
                            }`}
                        >
                            {result.label}
                        </li>
                    ))}
                </ul>
            </form>
        </div>
    );
}
