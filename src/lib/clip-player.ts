/**
 * Click-to-play for the site's muted clips (browser only; imported from component <script>s).
 * Every clip registered here is exclusive: when one starts, any other playing clip pauses.
 */
const clips = new Set<HTMLVideoElement>();

/** Register a clip so that starting it pauses the others (works for native controls too). */
export function exclusive(video: HTMLVideoElement): void {
  if (clips.has(video)) return;
  clips.add(video);
  video.addEventListener('play', () => {
    for (const other of clips) if (other !== video && !other.paused) other.pause();
  });
}

interface Toggle {
  /** Element that gets `is-playing` while the clip plays. */
  root: HTMLElement;
  video: HTMLVideoElement;
  button: HTMLButtonElement;
  /** Accessible name for the button, given whether the clip is playing. */
  label: (playing: boolean) => string;
  /** Also set aria-pressed on the button (default true). */
  pressed?: boolean;
  /** Called just before a click starts the clip. */
  beforePlay?: () => void;
}

/** Wire a play/pause button to a clip: the button, its label and the root class follow the clip's state. */
export function bindToggle({ root, video, button, label, pressed = true, beforePlay }: Toggle): void {
  exclusive(video);
  const sync = () => {
    const on = !video.paused;
    root.classList.toggle('is-playing', on);
    if (pressed) button.setAttribute('aria-pressed', String(on));
    button.setAttribute('aria-label', label(on));
  };
  button.addEventListener('click', () => {
    if (video.paused) {
      beforePlay?.();
      video.play().catch(sync);
    } else {
      video.pause();
    }
  });
  video.addEventListener('play', sync);
  video.addEventListener('pause', sync);
  sync();
}

/**
 * Two (or more) runs of one clip, e.g. lit and lights off: each button carries `data-src` and `data-poster`.
 * Choosing a run swaps the source and poster and resets to the start; a clip that was playing keeps playing.
 * Buttons use aria-pressed; Left/Right arrows move between them (Enter/Space choose, as for any button).
 */
export function bindRuns(video: HTMLVideoElement, buttons: HTMLButtonElement[]): void {
  const choose = (pick: HTMLButtonElement) => {
    if (pick.getAttribute('aria-pressed') === 'true') return;
    const src = pick.dataset.src;
    if (!src) return;
    const playing = !video.paused;
    for (const b of buttons) b.setAttribute('aria-pressed', String(b === pick));
    video.pause();
    if (pick.dataset.poster) video.poster = pick.dataset.poster;
    else video.removeAttribute('poster');
    video.src = src;
    video.load();
    if (playing) video.play().catch(() => {});
  };
  buttons.forEach((b, i) => {
    b.addEventListener('click', () => choose(b));
    b.addEventListener('keydown', (e) => {
      const step = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!step) return;
      e.preventDefault();
      const next = buttons[(i + step + buttons.length) % buttons.length];
      next.focus();
      choose(next);
    });
  });
}
