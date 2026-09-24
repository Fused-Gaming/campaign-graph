import fs from 'node:fs';

const fail = (message) => {
  console.error(`VERSION GATE FAILED: ${message}`);
  process.exit(1);
};

const version = fs.readFileSync('VERSION', 'utf8').trim();
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const pyproject = fs.readFileSync('pyproject.toml', 'utf8');
const init = fs.readFileSync('src/campaign_graph/__init__.py', 'utf8');

const pyprojectMatch = pyproject.match(/^version\s*=\s*"([^"]+)"/m);
const initMatch = init.match(/__version__\s*=\s*"([^"]+)"/);

if (!version) fail('VERSION is empty');
if (!pyprojectMatch) fail('pyproject.toml version not found');
if (!initMatch) fail('src/campaign_graph/__init__.py __version__ not found');

const observed = {
  VERSION: version,
  'package.json': packageJson.version,
  'pyproject.toml': pyprojectMatch[1],
  '__init__.py': initMatch[1],
};

for (const [source, value] of Object.entries(observed)) {
  if (value !== version) {
    fail(`${source}=${value} does not match VERSION=${version}`);
  }
}

console.log(`VERSION GATE OK: ${version}`);
