"use client"

import React, { useState } from "react"
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select"
import {
  TooltipProvider,
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip"
import { Button } from "@/components/ui/button"
import { calculateFormSchema } from "@/schema/schema"
import { calculateAction } from "@/actions/actions"
import { EnergyEstimation } from "@/types"

type FormErrors = {
  roofArea?: string[]
  pvTechnology?: string[]
  azimuth?: string[]
  mountingSlope?: string[]
}

export default function CalculateForm({
  setProduction,
}: {
  setProduction: React.Dispatch<React.SetStateAction<EnergyEstimation | null>>
}) {
  // Get the position of the user stored from the local-storage
  const storedLocation = JSON.parse(
    localStorage.getItem("user-location") || "null"
  )

  const [position, setPosition] = useState<[number, number]>([
    storedLocation.y,
    storedLocation.x,
  ])

  const [errors, setErrors] = useState<FormErrors>({})

  const clientAction = async (formData: FormData) => {
    const newData = {
      roofArea: formData.get("roofArea"),
      pvTechnology: formData.get("pvTechnology"),
      // azimuth: formData.get("azimuth"),
      // mountingSlope: formData.get("mountingSlope"),
    }
    const result = calculateFormSchema.safeParse(newData)
    if (!result.success) {
      const fieldErrors = result.error.flatten().fieldErrors
      setErrors(fieldErrors)
      return
    }

    setErrors({})

    calculateAction({
      area: Number(result.data.roofArea),
      technology: result.data.pvTechnology,
      lat: position[0],
      lon: position[1],
    }).then(result => setProduction(result ? result.payload : null))
  }

  return (
    <Card className="max-w-md grow basis-1/2">
      <CardHeader>
        <CardTitle className="text-2xl">Solar Savings Calculator</CardTitle>
        <CardDescription>
          Discover how much you can save by installing solar panels.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form action={clientAction} className="space-y-4">
          <div className="grid gap-2">
            <Label htmlFor="roofArea">Roof Area</Label>
            <Input
              id="roofArea"
              name="roofArea"
              type="number"
              placeholder="Enter roof area (sq meters)"
            />
            {errors.roofArea && (
              <p className="text-sm text-red-500">{errors.roofArea}</p>
            )}
          </div>
          <div className="grid gap-2">
            <Label htmlFor="pvTechnology">PV Technology</Label>
            <Select name="pvTechnology">
              <SelectTrigger>
                <SelectValue placeholder="Select PV technology" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="monocrystalline">Monocrystalline</SelectItem>
                <SelectItem value="polycrystalline">Polycrystalline</SelectItem>
                <SelectItem value="thinFilm">Thin Film</SelectItem>
              </SelectContent>
            </Select>
            {errors.pvTechnology && (
              <p className="text-sm text-red-500">{errors.pvTechnology}</p>
            )}
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="grid gap-2">
              <Label htmlFor="azimuth">
                <TooltipProvider>
                  Azimuth
                  <Tooltip>
                    <TooltipTrigger>
                      <InfoIcon className="ml-2 h-4 w-4 text-muted-foreground" />
                    </TooltipTrigger>
                    <TooltipContent className="w-60">
                      <p>
                        The azimuth is the angle between the direction the solar
                        panels are facing and true south. A south-facing system
                        has an azimuth of 0 degrees.
                      </p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </Label>
              <Input
                required={false}
                disabled
                value={0}
                id="azimuth"
                name="azimuth"
                type="number"
                placeholder="Enter azimuth (degrees)"
              />
              {errors.azimuth && (
                <p className="text-sm text-red-500">{errors.azimuth}</p>
              )}
            </div>
            <div className="grid gap-2">
              <Label htmlFor="mountingSlope">
                <TooltipProvider>
                  Mounting Slope
                  <Tooltip>
                    <TooltipTrigger>
                      <InfoIcon className="ml-2 h-4 w-4 text-muted-foreground" />
                    </TooltipTrigger>
                    <TooltipContent className="w-60">
                      <p>
                        The mounting slope is the angle of the solar panels
                        relative to the horizontal. A flat roof has a mounting
                        slope of 0 degrees.
                      </p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </Label>
              <Input
                required={false}
                disabled
                value={15}
                id="mountingSlope"
                name="mountingSlope"
                type="number"
                placeholder="Enter mounting slope (degrees)"
              />
              {errors.mountingSlope && (
                <p className="text-sm text-red-500">{errors.mountingSlope}</p>
              )}
            </div>
          </div>
          <Button type="submit" className="w-full">
            Calculate
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}


function InfoIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <path d="M12 16v-4" />
      <path d="M12 8h.01" />
    </svg>
  )
}

