declare module "leaflet-geosearch" {
  import * as L from "leaflet"

  export class GeoSearchControl extends L.Control {
    constructor(options: any)
    addTo(map: L.Map): this
  }

  export class OpenStreetMapProvider {
    search(options: { query: string }): Promise<any[]>
  }

  export interface GeoSearchResultEvent extends L.LeafletEvent {
    location: {
      y: number
      x: number
    }
  }

  export interface MarkerDragEndEvent extends L.LeafletEvent {
    location: {
      lat: number
      lng: number
    }
  }
}
