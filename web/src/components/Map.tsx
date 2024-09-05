"use client";
import "../app/globals.css";
import "leaflet/dist/leaflet.css";
import {
    MapContainer,
    Marker,
    Popup,
    TileLayer,
    useMap,
    useMapEvents,
} from "react-leaflet";
import { Icon, marker } from "leaflet";
import { useEffect, useState } from "react";
import { Button } from "./ui/button";
import { LocateFixed } from "lucide-react";
import { GeoSearchControl, OpenStreetMapProvider } from "leaflet-geosearch";
import "leaflet/dist/leaflet.css";
import "leaflet-geosearch/dist/geosearch.css";
import "./style.css";

const pinIcon = new Icon({
    iconUrl: "https://unpkg.com/leaflet@1.6/dist/images/marker-icon.png",
    iconSize: [25, 41],
});

export default function Map() {
    const storedLocation = JSON.parse(
        localStorage.getItem("user-location") || "null"
    );

    const [position, setPosition] = useState<[number, number]>([
        storedLocation.x,
        storedLocation.y,
    ]);
    const [error, setError] = useState<string | null>(null);

    const handleSuccess = (position: GeolocationPosition) => {
        const { latitude, longitude } = position.coords;
        setPosition([latitude, longitude]);
    };

    const handleError = (error: GeolocationPositionError) => {
        setError(error.message);
    };

    const handleLocationClick = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                handleSuccess,
                handleError
            );
        } else {
            setError("Geolocation is not supported by this browser.");
        }
    };

    const CenterMapOnPosition = () => {
        const map = useMap();
        map.setView(position, map.getZoom());
        return null;
    };
    const MapClickHandler = () => {
        useMapEvents({
            click(e) {
                setPosition([e.latlng.lat, e.latlng.lng]);
            },
        });
        return null;
    };

    function LeafletgeoSearch() {
        const map = useMap();
        useEffect(() => {
            const searchControl = new GeoSearchControl({
                provider: new OpenStreetMapProvider(),
                style: "bar",
                marker: {
                    draggable: true,
                },
            });
            map.addControl(searchControl);

            // Add event listener for geosearch/showlocation
            map.on("geosearch/showlocation", (result: any) => {
                const { location } = result;
                setPosition([location.y, location.x]);
            });

            // Add event listener for geosearch/marker/dragend
            map.on("geosearch/marker/dragend", (event) => {
                const { lat, lng } = event.location;
                setPosition([lat, lng]);
            });

            return () => {
                map.removeControl(searchControl);
                map.off("geosearch/showlocation");
                map.off("geosearch/marker/dragend");
            };
        }, [map]);

        return null;
    }

    console.log("User location: ", position);

    return (
        <div className="m-auto relative">
            <MapContainer center={position} zoom={15} scrollWheelZoom={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={position} icon={pinIcon}>
                    <Popup>
                        <h3>Your location</h3>
                    </Popup>
                </Marker>
                <CenterMapOnPosition />
                <MapClickHandler />
                <LeafletgeoSearch />
            </MapContainer>
            <Button
                onClick={handleLocationClick}
                className="space-x-2 py-2 absolute bottom-5 right-5 z-50"
            >
                <LocateFixed />
                <p>Use Current Location</p>
            </Button>
            {error && <div className="error">{error}</div>}
        </div>
    );
}
