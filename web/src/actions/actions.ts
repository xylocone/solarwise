import { EnergyEstimation, APIResponse } from "@/types"

const API_URI = "/api"

export const calculateAction = async ({
  area,
  lat,
  lon,
}: {
  area: number
  technology: string
  lat: number
  lon: number
}) => {
  try {
    // Send a request to the backend for the SDLR
    const response = await fetch(API_URI + "/data/energy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lat,
        lon,
        area,
        efficiency: 0.223,
      }),
    })
    console.log("response: ", response)

    if (!response.ok) return null
    const json = await response.json()
    return (await json) as APIResponse<EnergyEstimation>
  } catch (error) {
    console.error("Error: ", error)
  }

  return null
}
