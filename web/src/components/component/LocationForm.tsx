"use client"

import { useEffect, useState, useRef } from "react"
import { useDebounceCallback } from "usehooks-ts"
import { OpenStreetMapProvider } from "leaflet-geosearch"
import "@/components/ui/form"
import { Button } from "../ui/button"
import { SearchResult } from "leaflet-geosearch/dist/providers/provider.js"
import { useRouter } from "next/navigation"

export default function LocationForm() {
  const [input, setInput] = useState("")
  const [results, setResults] = useState<SearchResult[]>([])
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const resultRefs = useRef<(HTMLLIElement | null)[]>([])

  const debouncedSetInput = useDebounceCallback(value => {
    setInput(value)
  }, 300)

  const router = useRouter()

  useEffect(() => {
    const provider = new OpenStreetMapProvider()
    const fetchResults = async () => {
      if (input) {
        const searchResults = await provider.search({ query: input })
        setResults(searchResults)
        setSelectedIndex(-1) // to make the selectedIndex -1 after search
      } else {
        setResults([])
        setSelectedIndex(-1)
      }
    }
    fetchResults()
  }, [input])

  const handleSelectResult = (index: number) => {
    setSelectedIndex(index)
    setInput(results[index].label)
    setResults([])
    handleSubmit(index)
  }

  //handle dropdown navigation with arrows
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowDown") {
      e.preventDefault()
      setSelectedIndex(prevIndex => {
        const newIndex = (prevIndex + 1) % results.length
        resultRefs.current[newIndex]?.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
        })
        return newIndex
      })
    } else if (e.key === "ArrowUp") {
      e.preventDefault()
      setSelectedIndex(prevIndex => {
        const newIndex = (prevIndex - 1 + results.length) % results.length
        resultRefs.current[newIndex]?.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
        })
        return newIndex
      })
    } else if (e.key === "Enter") {
      e.preventDefault()
      handleSubmit(selectedIndex)
    }
  }

  const handleSubmit = (index: number) => {
    const selectedLocation = results[index >= 0 ? index : 0] // Pick the top result if nothing is selected
    if (selectedLocation) {
      console.log("Submitted Location:", selectedLocation)
      localStorage.setItem("user-location", JSON.stringify(selectedLocation))
      router.push("/calculate")
    }
  }

  return (
    <div className="flex h-[70vh] w-full flex-col items-center bg-slate-200">
      <form
        onSubmit={e => {
          e.preventDefault()
          handleSubmit(selectedIndex)
        }}
      >
        <div className="mb-2 flex items-center justify-center">
          <input
            type="text"
            onChange={e => debouncedSetInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search location"
            className="h-full p-2 pl-4"
          />
          <Button type="submit" className="rounded-none">
            Check Your Roof
          </Button>
        </div>
        <ul className="md:max-w-1/2 max-h-[200px] w-full overflow-y-auto rounded border border-gray-300 bg-white shadow-lg md:mx-auto">
          {results.map((result: SearchResult, index: number) => (
            <li
              key={index}
              ref={el => {
                resultRefs.current[index] = el
              }}
              onClick={() => handleSelectResult(index)}
              className={`cursor-pointer border-b p-2 last:border-none hover:bg-gray-100 ${
                selectedIndex === index ? "bg-gray-200" : ""
              }`}
            >
              {result.label}
            </li>
          ))}
        </ul>
      </form>
    </div>
  )
}
