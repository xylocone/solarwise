import { z } from "zod"

export const calculateFormSchema = z.object({
  roofArea: z.string().min(1, "Roof area is required"),
  pvTechnology: z.enum(["monocrystalline", "polycrystalline", "thinFilm"], {
    errorMap: () => ({ message: "PV technology is required" }),
  }),
  // azimuth: z.string(),
  // mountingSlope: z.string(),
})
