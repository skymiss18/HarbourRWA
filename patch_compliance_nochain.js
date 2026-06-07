const fs = require('fs');
const file = 'e:/Repos/TheTuringTestHackathon2026/app/src/app/compliance/page.tsx';
let c = fs.readFileSync(file, 'utf8');

// 1. Remove the on-chain txHash link block (lines 1206-1215 range)
const onchainBlock = `              {result.onChain && result.txHash && (\r\n\r\n                <a href={\`https://sepolia.mantlescan.xyz/tx/\${result.txHash}\`} target="_blank" rel="noopener noreferrer"\r\n\r\n                  className="text-[11px] font-mono text-blue-400 hover:text-blue-300 transition-colors">\r\n\r\n                  On-chain: {result.txHash.slice(0, 18)}...\r\n                </a>\r\n\r\n              )}\r\n\r\n            </div>`;
if (!c.includes(onchainBlock.slice(0, 40))) {
  console.log('ERROR: onchain block not found, trying alternate...');
  // Try without \r
  const alt = `              {result.onChain && result.txHash && (\n\n                <a href={\`https://sepolia.mantlescan.xyz/tx/\${result.txHash}\`} target="_blank" rel="noopener noreferrer"\n\n                  className="text-[11px] font-mono text-blue-400 hover:text-blue-300 transition-colors">\n\n                  On-chain: {result.txHash.slice(0, 18)}...\n                </a>\n\n              )}\n\n            </div>`;
  console.log('alt found:', c.includes(alt.slice(0, 40)));
}

const replacedBlock = `            </div>`;
c = c.replace(onchainBlock, replacedBlock);
console.log('txHash link removed:', !c.includes('result.onChain && result.txHash'));

// 2. Remove ComplianceOracle.sol reference in description
const oldDesc = `合规结果锚定至链上 ComplianceOracle.sol，不可篡改。`;
const newDesc = ``;
if (c.includes(oldDesc)) {
  c = c.replace(oldDesc, newDesc);
  console.log('ComplianceOracle reference removed from description');
} else {
  console.log('WARNING: ComplianceOracle description reference not found exactly');
}

fs.writeFileSync(file, c, 'utf8');
console.log('Done');
