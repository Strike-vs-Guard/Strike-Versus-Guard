#!/usr/bin/env node
/** Claude Code SessionStart hook: prints the state a session must know and the first skill to run. */
import { execSync } from 'node:child_process';
const sh = (c) => {
  try {
    return execSync(c, { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
  } catch {
    return '';
  }
};
const branch = sh('git rev-parse --abbrev-ref HEAD') || '?';
const hooks = sh('git config core.hooksPath');
const warn = branch === 'development' ? '' : '  <-- run `git switch development` before editing';
console.log(
  `Strike vs Guard site. Branch: ${branch}${warn}. Node: ${sh('node -v') || '?'}. Git hooks: ${hooks || 'NOT INSTALLED (run npm ci)'}.\n` +
    'Process: run the svg-start skill first. Changes: svg-change. Bugs: svg-debug. Posts: svg-post. Layout decisions: svg-panel. Publishing: svg-release.\n' +
    'Rules: STANDARDS.md. Current state and open items: docs/claude/HANDOFF.md.',
);
