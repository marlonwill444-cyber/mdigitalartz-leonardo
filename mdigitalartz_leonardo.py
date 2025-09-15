"""
MDigitalArtz Leonardo API helper
This script uses the user's Leonardo Production API key to generate images using
the Phoenix 1.0 and Anime XL models and optionally upscale them. It uses the
`requests` library to interact with the Leonardo REST endpoints.

Note: Internet access is disabled in this environment, so this script cannot
actually send requests from within this notebook. Use this script in an
environment with network access.
"""

import json
from typing import Dict, Any

import requests


API_KEY = "cd8d7691-5ec5-48e1-9c6b-7160900f59a5"
"""
Your Leonardo Production API key. Keep this value secret. You can also set
this value via an environment variable (e.g., LEONARDO_API_KEY) and read
`os.environ["LEONARDO_API_KEY"]` instead of hard‑coding it here.
"""

PHOENIX_MODEL_ID = "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3"
ANIME_XL_MODEL_ID = "e71a1c2f-4f80-4800-934f-2c68979d8cc8"


def _make_headers() -> Dict[str, str]:
    """Builds the authorization headers for API requests."""
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def generate_images_phoenix(prompt: str, width: int = 1216, height: int = 1520,
                             num_images: int = 4, contrast: float = 3.5,
                             style_uuid: str = "a5632c7c-ddbb-4e2f-ba34-8456ab3ac436",
                             alchemy: bool = True) -> Dict[str, Any]:
    """
    Generates images using the Phoenix 1.0 model with the specified prompt.

    :param prompt: The text prompt describing the image.
    :param width: Width of the image (512–1536, multiple of 8).
    :param height: Height of the image (512–1536, multiple of 8).
    :param num_images: Number of images to generate.
    :param contrast: Contrast parameter required for Phoenix (e.g. 1.0–4.5).
    :param style_uuid: Optional style UUID for stylistic control.
    :param alchemy: Whether to enable Alchemy (enables upscaling beyond input size).
    :return: The JSON response from the API with generation details.
    """
    payload = {
        "modelId": PHOENIX_MODEL_ID,
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_images": num_images,
        "contrast": contrast,
        "alchemy": alchemy,
        "styleUUID": style_uuid,
    }
    response = requests.post(
        "https://cloud.leonardo.ai/api/rest/v1/generations",
        headers=_make_headers(),
        data=json.dumps(payload),
    )
    response.raise_for_status()
    return response.json()


def generate_images_anime_xl(prompt: str, width: int = 1216, height: int = 1520,
                              num_images: int = 4, preset_style: str = "CINEMATIC",
                              alchemy: bool = True) -> Dict[str, Any]:
    """
    Generates images using the Anime XL (SDXL) model with a preset style.

    :param prompt: The text prompt describing the image.
    :param width: Width of the image (512–1536, multiple of 8).
    :param height: Height of the image (512–1536, multiple of 8).
    :param num_images: Number of images to generate.
    :param preset_style: Preset style name (e.g. "CINEMATIC").
    :param alchemy: Whether to enable Alchemy.
    :return: The JSON response from the API with generation details.
    """
    payload = {
        "modelId": ANIME_XL_MODEL_ID,
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_images": num_images,
        "alchemy": alchemy,
        "presetStyle": preset_style,
    }
    response = requests.post(
        "https://cloud.leonardo.ai/api/rest/v1/generations",
        headers=_make_headers(),
        data=json.dumps(payload),
    )
    response.raise_for_status()
    return response.json()


def fetch_generation(generation_id: str) -> Dict[str, Any]:
    """
    Fetches metadata for a specific generation by ID.

    :param generation_id: The generationId returned from a create generation call.
    :return: The JSON response containing generation details and image URLs.
    """
    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    response = requests.get(url, headers=_make_headers())
    response.raise_for_status()
    return response.json()


def upscale_image(generated_image_id: str, upscale_multiplier: float = 1.5,
                  ultra_upscale_style: str = "ARTISTIC", creativity_strength: int = 5,
                  detail_contrast: int = 5, similarity: int = 5) -> Dict[str, Any]:
    """
    Requests an upscale job for a generated image using the Universal Upscaler.

    :param generated_image_id: ID of the generated image to upscale.
    :param upscale_multiplier: Factor (e.g. 1.5) to upscale. Max output ~20MP.
    :param ultra_upscale_style: Style parameter for upscaler (ARTISTIC/PHOTOGRAPHIC).
    :param creativity_strength: Creativity parameter (1‑5).
    :param detail_contrast: Detail contrast parameter (1‑5).
    :param similarity: Similarity parameter (1‑5).
    :return: The JSON response with upscale job details.
    """
    payload = {
        "ultraUpscaleStyle": ultra_upscale_style,
        "creativityStrength": creativity_strength,
        "detailContrast": detail_contrast,
        "similarity": similarity,
        "upscaleMultiplier": upscale_multiplier,
        "generatedImageId": generated_image_id,
    }
    response = requests.post(
        "https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler",
        headers=_make_headers(),
        data=json.dumps(payload),
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Example usage: this will not run properly without network access.
    prompt_phoenix = (
        "Ultra-detailed cyberpunk anime female, adult 25-35, Bengus-style anatomy, "
        "crisp angular lines, neon teal/indigo/electric blue rim light, rain city bokeh, "
        "no pink, no rainbow, no logos, no text."
    )
    result = generate_images_phoenix(prompt_phoenix)
    print(json.dumps(result, indent=2))
