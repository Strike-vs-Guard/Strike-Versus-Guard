/** Logo plates, /plates/<name>.png: drawn by src/lib/plates.ts at build time (and on request in `astro dev`). */
import type { APIRoute, GetStaticPaths } from 'astro';
import { plateList, renderPlate, type Plate } from '../../lib/plates';

export const getStaticPaths = (async () =>
  (await plateList()).map((plate) => ({ params: { name: plate.name }, props: { plate } }))) satisfies GetStaticPaths;

export const GET: APIRoute = async ({ props }) =>
  new Response(new Uint8Array(await renderPlate((props as { plate: Plate }).plate)), {
    headers: { 'Content-Type': 'image/png' },
  });
