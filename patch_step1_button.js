const fs = require('fs');
const file = 'e:/Repos/TheTuringTestHackathon2026/app/src/app/tokenize/page.tsx';
let c = fs.readFileSync(file, 'utf8');

// 1. Add submittedToIntermediary state after sfcSubmitted
const stateTarget = '  const [sfcSubmitted, setSfcSubmitted] = useState(false);';
if (!c.includes(stateTarget)) { console.log('ERROR: state target not found'); process.exit(1); }
c = c.replace(
  stateTarget,
  stateTarget + '\n  const [submittedToIntermediary, setSubmittedToIntermediary] = useState(false);'
);

// 2. Replace button onClick to use setSubmittedToIntermediary(true) instead of setStep(2)
const btnOld = '          <button onClick={() => { if (form.assetName && form.description) { void submitToSponsorInbox(); setStep(2); } }}';
if (!c.includes(btnOld)) { console.log('ERROR: button target not found'); process.exit(1); }
c = c.replace(
  btnOld,
  '          <button onClick={() => { if (form.assetName && form.description) { void submitToSponsorInbox(); setSubmittedToIntermediary(true); } }}'
);

// 3. After the closing </button> of Step 1, add confirmation panel
// Replace the button + its closing </button> with conditional render
const buttonBlock = `          <button onClick={() => { if (form.assetName && form.description) { void submitToSponsorInbox(); setSubmittedToIntermediary(true); } }}

            disabled={!form.assetName || !form.description}

            className="w-full py-2.5 text-sm font-semibold text-white rounded-md disabled:opacity-40 transition-opacity hover:opacity-90"

            style={{ background: "#1d4ed8" }}>

            Submit for Intermediary Review \u2192
          </button>`;

const confirmPanel = `          {!submittedToIntermediary ? (
            <button onClick={() => { if (form.assetName && form.description) { void submitToSponsorInbox(); setSubmittedToIntermediary(true); } }}
              disabled={!form.assetName || !form.description}
              className="w-full py-2.5 text-sm font-semibold text-white rounded-md disabled:opacity-40 transition-opacity hover:opacity-90"
              style={{ background: "#1d4ed8" }}>
              Submit for Intermediary Review \u2192
            </button>
          ) : (
            <div className="rounded-lg p-4 space-y-3" style={{ background: "rgba(16,185,129,0.05)", border: "1px solid rgba(16,185,129,0.2)" }}>
              <div className="flex items-center gap-2">
                <span className="text-emerald-500 text-base">\u2713</span>
                <span className="text-sm font-semibold text-emerald-700">Submitted to Intermediary</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Asset information has been submitted to the Intermediary (Type\u00a06 LC / Sponsor) for compliance review.
                Await the intermediary\u2019s screening at <strong className="text-amber-700">/compliance</strong> and <strong className="text-amber-700">/audit</strong>,
                then SFC approval at <strong className="text-amber-700">/regulator/issuance</strong> before continuing.
              </p>
              <div className="flex items-center justify-between pt-2" style={{ borderTop: "1px solid rgba(16,185,129,0.2)" }}>
                <span className="text-[10px] text-slate-500">Return here after SFC approval to complete deployment.</span>
                <button onClick={() => setStep(2)}
                  className="ml-3 px-3 py-1.5 rounded text-xs font-semibold text-white transition-opacity hover:opacity-90"
                  style={{ background: "#6b7280" }}>
                  Resume Deployment \u2192
                </button>
              </div>
            </div>
          )}`;

// We need to undo the previous direct-onClick replacement and replace the whole block
// First restore the button onClick back to use setSubmittedToIntermediary, then replace full block
const singleBtnOld = `          <button onClick={() => { if (form.assetName && form.description) { void submitToSponsorInbox(); setSubmittedToIntermediary(true); } }}\r\n\r\n            disabled={!form.assetName || !form.description}\r\n\r\n            className="w-full py-2.5 text-sm font-semibold text-white rounded-md disabled:opacity-40 transition-opacity hover:opacity-90"\r\n\r\n            style={{ background: "#1d4ed8" }}>\r\n\r\n            Submit for Intermediary Review \u2192\r\n          </button>`;

if (!c.includes(singleBtnOld)) {
  console.log('ERROR: full button block not found');
  // Show what we have
  const idx = c.indexOf('Submit for Intermediary Review');
  console.log('context:', JSON.stringify(c.slice(idx-200, idx+200)));
  process.exit(1);
}

c = c.replace(singleBtnOld, confirmPanel);

console.log('submittedToIntermediary state added:', c.includes('const [submittedToIntermediary'));
console.log('confirmation panel added:', c.includes('Submitted to Intermediary'));
console.log('Resume Deployment button added:', c.includes('Resume Deployment'));

fs.writeFileSync(file, c, 'utf8');
console.log('Done');
