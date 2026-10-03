import assert from 'node:assert/strict';
import {qualifyProspect, csvFor, STATUSES} from '../src/qualification.js';

const base={id:'T',prospect:'Test',owner:'Owner',fit:'yes',need:'yes',timing:'now',next_step:'Call'};
assert.equal(qualifyProspect(base).status, STATUSES.QUALIFIED);
assert.equal(qualifyProspect({...base, fit:'no'}).status, STATUSES.DISQUALIFIED);
assert.match(qualifyProspect({...base, fit:'no'}).reason, /Fit criteria/);
assert.equal(qualifyProspect({...base, need:'no'}).status, STATUSES.DISQUALIFIED);
assert.equal(qualifyProspect({...base, timing:'later'}).status, STATUSES.DISQUALIFIED);
assert.equal(qualifyProspect({...base, timing:'unknown'}).status, STATUSES.REVIEW);
assert.equal(qualifyProspect({...base, next_step:''}).status, STATUSES.REVIEW);
assert.equal(qualifyProspect({...base, disqualify_reason:'manual conflict'}).status, STATUSES.REVIEW);
const csv=csvFor([base]);
assert.match(csv,/"QUALIFIED"/);
assert.match(csv,/"Fit, need, timing, and next step are explicitly supported"/);
console.log('qualification tests: PASS (9 assertions)');
