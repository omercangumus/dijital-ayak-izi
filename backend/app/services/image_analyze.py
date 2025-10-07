from typing import Any, Dict
import io
from PIL import Image
import imagehash
import exifread


def extract_exif_geotags(exif_tags: Dict[str, Any]) -> Dict[str, Any]:
    gps_lat = exif_tags.get('GPS GPSLatitude')
    gps_lat_ref = exif_tags.get('GPS GPSLatitudeRef')
    gps_lon = exif_tags.get('GPS GPSLongitude')
    gps_lon_ref = exif_tags.get('GPS GPSLongitudeRef')

    def to_deg(value):
        try:
            d = float(value.values[0].num) / float(value.values[0].den)
            m = float(value.values[1].num) / float(value.values[1].den)
            s = float(value.values[2].num) / float(value.values[2].den)
            return d + (m/60.0) + (s/3600.0)
        except Exception:
            return None

    lat = to_deg(gps_lat) if gps_lat else None
    lon = to_deg(gps_lon) if gps_lon else None
    if lat is not None and gps_lat_ref and gps_lat_ref.values in ['S']:
        lat = -lat
    if lon is not None and gps_lon_ref and gps_lon_ref.values in ['W']:
        lon = -lon
    return {"lat": lat, "lon": lon}


def analyze_image(file_bytes: bytes) -> Dict[str, Any]:
    # pHash
    with Image.open(io.BytesIO(file_bytes)) as img:
        img = img.convert('RGB')
        phash = str(imagehash.phash(img))

    # EXIF
    bio = io.BytesIO(file_bytes)
    bio.seek(0)
    tags = exifread.process_file(bio, details=False)
    gps = extract_exif_geotags(tags)

    return {
        "phash": phash,
        "exif": {
            "gps": gps,
            "has_exif": len(tags) > 0
        }
    }


