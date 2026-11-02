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
