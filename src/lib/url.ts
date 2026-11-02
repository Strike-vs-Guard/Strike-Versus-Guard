/** Prefix a site-relative path with the configured base, e.g. url('partners/nus/'). */
export function url(path = ''): string {
  const base = import.meta.env.BASE_URL.replace(/\/?$/, '/');
  return base + path.replace(/^\//, '');
}

/** True when building a pull-request preview (set by .github/workflows/preview.yml). */
export const isPreview = !!import.meta.env.PREVIEW || !!process.env.PREVIEW;
export const previewPr = process.env.PREVIEW_PR || '';
