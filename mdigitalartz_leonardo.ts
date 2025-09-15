/*
 * MDigitalArtz Leonardo API helper
 *
 * This script provides functions to generate images using Leonardo's Production
 * API (Phoenix 1.0 and Anime XL models) and to request an upscale of a
 * generated image. It uses the axios HTTP client library. Make sure you
 * install axios (e.g. `npm install axios`) before running this script.
 *
 * Note: Because this environment does not have network connectivity, this
 * script cannot be executed here. Use it in your own Node.js environment.
 */

import axios from 'axios';

// Your Leonardo Production API key. Keep it secret. You could also load it
// from an environment variable like process.env.LEONARDO_API_KEY.
const API_KEY: string = 'cd8d7691-5ec5-48e1-9c6b-7160900f59a5';

const PHOENIX_MODEL_ID = 'de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3';
const ANIME_XL_MODEL_ID = 'e71a1c2f-4f80-4800-934f-2c68979d8cc8';

/**
 * Sends a POST request to generate images with the Phoenix 1.0 model.
 *
 * @param prompt Description of the desired image.
 * @param width  Image width (multiple of 8, 512–1536).
 * @param height Image height (multiple of 8, 512–1536).
 * @param numImages Number of images to generate.
 * @param contrast Contrast parameter (1.0–4.5).
 * @param styleUUID Optional style UUID for stylistic control.
 * @param alchemy Whether to enable Alchemy (allows larger output).
 */
export async function generateImagesPhoenix(
  prompt: string,
  width = 1216,
  height = 1520,
  numImages = 4,
  contrast = 3.5,
  styleUUID = 'a5632c7c-ddbb-4e2f-ba34-8456ab3ac436',
  alchemy = true
): Promise<any> {
  const payload = {
    modelId: PHOENIX_MODEL_ID,
    prompt,
    width,
    height,
    num_images: numImages,
    contrast,
    alchemy,
    styleUUID,
  };
  const response = await axios.post(
    'https://cloud.leonardo.ai/api/rest/v1/generations',
    payload,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data;
}

/**
 * Sends a POST request to generate images with the Anime XL model.
 *
 * @param prompt Description of the desired image.
 * @param width  Image width (multiple of 8, 512–1536).
 * @param height Image height (multiple of 8, 512–1536).
 * @param numImages Number of images to generate.
 * @param presetStyle Preset style name (e.g. "CINEMATIC").
 * @param alchemy Whether to enable Alchemy.
 */
export async function generateImagesAnimeXL(
  prompt: string,
  width = 1216,
  height = 1520,
  numImages = 4,
  presetStyle = 'CINEMATIC',
  alchemy = true
): Promise<any> {
  const payload = {
    modelId: ANIME_XL_MODEL_ID,
    prompt,
    width,
    height,
    num_images: numImages,
    alchemy,
    presetStyle,
  };
  const response = await axios.post(
    'https://cloud.leonardo.ai/api/rest/v1/generations',
    payload,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data;
}

/**
 * Retrieves details about a specific generation by ID.
 *
 * @param generationId The ID returned from create generation.
 */
export async function fetchGeneration(generationId: string): Promise<any> {
  const response = await axios.get(
    `https://cloud.leonardo.ai/api/rest/v1/generations/${generationId}`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  return response.data;
}

/**
 * Requests an upscale job for a generated image.
 *
 * @param generatedImageId ID of the generated image to upscale.
 * @param upscaleMultiplier Multiplier (1.0–2.0) controlling output size (<=20MP).
 * @param ultraUpscaleStyle Style parameter (e.g. "ARTISTIC").
 * @param creativityStrength Creativity parameter (1‑5).
 * @param detailContrast Detail contrast parameter (1‑5).
 * @param similarity Similarity parameter (1‑5).
 */
export async function upscaleImage(
  generatedImageId: string,
  upscaleMultiplier = 1.5,
  ultraUpscaleStyle = 'ARTISTIC',
  creativityStrength = 5,
  detailContrast = 5,
  similarity = 5
): Promise<any> {
  const payload = {
    ultraUpscaleStyle,
    creativityStrength,
    detailContrast,
    similarity,
    upscaleMultiplier,
    generatedImageId,
  };
  const response = await axios.post(
    'https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler',
    payload,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data;
}

// Example usage: these calls will not execute in this environment due to lack of network access.
async function example() {
  const prompt =
    'Ultra-detailed cyberpunk anime female, adult 25-35, Bengus-style anatomy, crisp angular lines, neon teal/indigo/electric blue rim light, rain city bokeh, no pink, no rainbow, no logos, no text.';
  const result = await generateImagesPhoenix(prompt);
  console.log(result);
}

// Uncomment the following line to run the example when executing this script in a Node environment.
// example().catch(console.error);
