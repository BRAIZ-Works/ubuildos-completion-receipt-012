export const STATUSES = Object.freeze({QUALIFIED:'QUALIFIED', DISQUALIFIED:'DISQUALIFIED', REVIEW:'REVIEW'});
const present = v => typeof v === 'string' ? v.trim().length > 0 : v !== null && v !== undefined;

export function qualifyProspect(p) {
  const evidence = {
    fit: p.fit,
    need: p.need,
    timing: p.timing,
    next_step: p.next_step
  };
  const missing = Object.entries(evidence)
    .filter(([k,v]) => k === 'next_step' ? !present(v) : !['yes','no','now','soon','later'].includes(v))
    .map(([k]) => k);
  if (missing.length) {
    return {status: STATUSES.REVIEW, reason: `Missing or invalid evidence: ${missing.join(', ')}`, evidence};
  }
  if (p.fit === 'no') return {status: STATUSES.DISQUALIFIED, reason:'Fit criteria not met', evidence};
  if (p.need === 'no') return {status: STATUSES.DISQUALIFIED, reason:'No demonstrated need', evidence};
  if (p.timing === 'later') return {status: STATUSES.DISQUALIFIED, reason:'Timing is outside the active qualification window', evidence};
  if (!['now','soon'].includes(p.timing)) return {status: STATUSES.REVIEW, reason:'Timing evidence is not actionable', evidence};
  if (present(p.disqualify_reason)) return {status: STATUSES.REVIEW, reason:'Contradictory explicit disqualification note requires review', evidence};
  return {status: STATUSES.QUALIFIED, reason:'Fit, need, timing, and next step are explicitly supported', evidence};
}

export function enrichProspects(rows) {
  return rows.map(row => ({...row, qualification: qualifyProspect(row)}));
}

export function csvFor(rows) {
  const esc = v => `"${String(v ?? '').replaceAll('"','""')}"`;
  const header = ['id','prospect','owner','fit','need','timing','next_step','status','reason'];
  const lines = [header.map(esc).join(',')];
  for (const row of enrichProspects(rows)) {
    lines.push([
      row.id,row.prospect,row.owner,row.fit,row.need,row.timing,row.next_step,
      row.qualification.status,row.qualification.reason
    ].map(esc).join(','));
  }
  return lines.join('\n') + '\n';
}
