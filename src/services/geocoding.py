import httpx


class GeocodingService:
    BASE_URL = "https://nominatim.openstreetmap.org"

    async def reverse_geocode(self, latitude: float, longitude: float) -> str | None:
        """Get address from coordinates using Nominatim."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/reverse",
                    params={
                        "lat": latitude,
                        "lon": longitude,
                        "format": "json",
                    },
                    headers={"User-Agent": "SpotDrop/1.0"},
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("display_name")
            except httpx.RequestError:
                pass
        return None

    async def geocode(self, address: str) -> tuple[float, float] | None:
        """Get coordinates from address using Nominatim."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/search",
                    params={
                        "q": address,
                        "format": "json",
                        "limit": 1,
                    },
                    headers={"User-Agent": "SpotDrop/1.0"},
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        return float(data[0]["lat"]), float(data[0]["lon"])
            except httpx.RequestError:
                pass
        return None


geocoding_service = GeocodingService()
