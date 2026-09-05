const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const vm = require('node:vm');
const source = readFileSync(join(__dirname, '../../assets/js/app.js'), 'utf8');
function block(marker) {
  const start = source.indexOf('(function () {', source.indexOf(marker));
  return source.slice(start, source.indexOf('}());', start) + 5);
}
let installed = false;
const analytics = {
  window: {}, localStorage: { getItem: () => null, setItem() {} },
  document: {
    readyState: 'complete', querySelector: () => installed,
    querySelectorAll: () => [], createElement: () => ({dataset: {}}),
    head: { appendChild() { installed = true; } },
  },
};
vm.runInNewContext(block('0. Optional'), analytics);
analytics.window.gleeAnalytics.enable();
analytics.window.gleeAnalytics.disable();
assert.equal(analytics.window['ga-disable-G-89W66VMGPB'], true);
analytics.window.gleeAnalytics.enable();
assert.equal(analytics.window['ga-disable-G-89W66VMGPB'], false);

for (const event of ['load', 'error', 'timeout']) {
  const listeners = {};
  let timer;
  const fallback = { hidden: true, classList: { add() {}, remove() {} } };
  const frame = { dataset: {}, getAttribute: () => '#fallback', addEventListener: (name, fn) => { listeners[name] = fn; } };
  vm.runInNewContext(block('8. External frame fallback'), {
    document: { readyState: 'complete', querySelectorAll: () => [frame], querySelector: () => fallback },
    window: { setTimeout: (fn) => { timer = fn; return 1; }, clearTimeout: () => { timer = null; } },
  });
  if (event === 'timeout') timer();
  else listeners[event]();
  assert.equal(timer, null);
  assert.equal(fallback.hidden, event === 'load');
}
console.log('Analytics toggling and iframe load/error/timeout regressions passed.');
