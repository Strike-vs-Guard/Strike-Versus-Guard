#!/usr/bin/env node
/**
 * Claude Code PreToolUse hook for Bash (wired in .claude/settings.json). Reads the tool call from
 * stdin and blocks commands that break STANDARDS §7 before they run, with a message that says
 * what to do instead. The git hooks in .githooks/ are the second line of defence.
 */
let input = '';
process.stdin.setEncoding('utf8');
for await (const chunk of process.stdin) input += chunk;
let cmd = '';
try {
  cmd = JSON.parse(input).tool_input?.command ?? '';
} catch {
  process.exit(0);
}
const allowMain = /SVG_ALLOW_MAIN=1/.test(cmd);
const block = (msg) => {
  console.error(`BLOCKED by scripts/claude/guard.mjs: ${msg}`);
  process.exit(2);
};

if (/\bgit\s+push\b/.test(cmd)) {
  if (/\bgit\s+push\b[^\n;&|]*\s(--force|-f|--force-with-lease)\b/.test(cmd)) block('force pushes are not allowed.');
  if (/\bgit\s+push\b[^\n;&|]*(\s--delete\b|\s:[\w\/-]+)/.test(cmd)) block('branch deletion is not allowed.');
  if (/\bgit\s+push\b[^\n;&|]*\bmain\b/.test(cmd) && !allowMain)
    block('pushing to main is not allowed. Push to development; main is updated only by merging a pull request (svg-release skill).');
}
if (
  /\bgit\s+(checkout|switch)\s+(-b|-c|--orphan)\b/.test(cmd) ||
  /\bgit\s+branch\s+(?!-)(?!(?:-d|-D|--delete|--list|--show-current|-a|-r|-v|-vv)\b)[\w\/.-]+/.test(cmd)
)
  block('creating branches is not allowed. Only development and main exist (STANDARDS §7).');
if (/\bgit\s+(checkout|switch)\s+main\b/.test(cmd) && !allowMain)
  block('do not work on main. Stay on development; publishing is a pull request (svg-release skill).');
if (/\bgit\s+merge\b/.test(cmd) && /\bmain\b/.test(cmd) && !allowMain)
  block('merging into main locally is not allowed. Open a pull request (svg-release skill).');
if (/\bgh\s+pr\s+merge\b/.test(cmd) && !allowMain)
  block("merging a pull request into main needs the site owner's go-ahead in this conversation. If given, prefix the command with SVG_ALLOW_MAIN=1.");
if (/\bplaywright\s+install\b/.test(cmd)) block('do not install browsers; npm run shots uses the Chrome already on the machine (or SVG_BROWSER).');
if (/\bgit\s+(reset\s+--hard|clean\s+-[a-z]*f)/.test(cmd)) block('destructive git commands are for the user to run.');
process.exit(0);
