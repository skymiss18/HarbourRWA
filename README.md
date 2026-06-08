# HarbourRWA

> **AI & RWA Track · Human-Driven RWA Infrastructure · Compliance-to-Claim RWA Lifecycle on Mantle**

HarbourRWA is a Mantle-native RWA infrastructure project that combines AI decision support with on-chain enforcement. It turns prospectus review, compliance scoring, investor onboarding, and portfolio guidance into verifiable workflow steps, then anchors the critical outcomes on Mantle so issuance, minting, and coupon servicing are enforced by contract state rather than screenshots or PDF approvals.

## One-Line Pitch

HarbourRWA is an end-to-end RWA workflow where AI produces usable compliance and investor-assistance outputs, and smart contracts turn those outputs into verifiable permissions, approvals, and post-issuance servicing on Mantle.

## Judge Takeaway

HarbourRWA is not presenting AI and RWA as two separate ideas placed side by side.

- AI is used to draft prospectus content, score compliance, assist KYC review, answer investor questions, and generate allocation suggestions.
- RWA infrastructure is used to make the important results of those steps enforceable on-chain.
- The combination matters because the project shows how AI can improve regulated asset workflows without replacing human oversight, while blockchain guarantees that the final compliance and issuance state cannot be silently overridden.

In short: **AI creates structured decision support, and Mantle turns the approved result into executable infrastructure.**

## Why The AI + RWA Combination Matters

Most projects only do one of these two things:

- use AI as a chat layer with no contract consequence
- use tokenization contracts without solving the real compliance workflow

HarbourRWA connects the two.

- AI reduces document friction, speeds up review, and makes compliance work machine-readable.
- Smart contracts convert that machine-readable output into mint gates, eligibility checks, and claimable servicing logic.
- Human actors remain in control: issuer, sponsor, regulator, compliance officer, and investor each keep their role.

That is the core product insight for judges: **the project is not only about tokenizing an asset, but about making regulated financial workflow programmable.**

## Why HarbourRWA Can Win The RWA Track

Most RWA demos stop at token creation or dashboard simulation. HarbourRWA proves the full regulated lifecycle and shows where AI adds operational value:

| Lifecycle Stage | Typical Hackathon Demo | HarbourRWA |
|---|---|---|
| Prospectus preparation | Static text or PDF upload | AI prospectus drafter with SFC-style sections, risk flags, and downloadable document flow |
| Sponsor review | Manual dashboard | Sponsor inbox receives issuer submissions from `/tokenize` and runs AI compliance review |
| Compliance evidence | Off-chain report | AI score and report hash written to `ComplianceOracle.sol` on Mantle |
| Regulator approval | Mock approval flag | `/regulator/issuance` handles issuance records, approval, and change-request branches |
| Smart contract audit | Not shown | `/audit` surfaces contract review and finding severity for the issuance stack |
| Investor onboarding | Centralised whitelist | `IdentityRegistry.sol` stores KYC and eligibility state used by mint and transfer checks |
| Subscription | UI-controlled mint button | `ComplianceModule.canMint()` gates `HarbourRWAToken.mintForAsset()` at contract level |
| Coupon servicing | Usually missing | Issuer funds the coupon pool in-contract; investor claims pro-rata coupon on-chain |
| Wealth management | Generic chatbot | AI advisor reads live holdings and coupon schedule, then generates a transparent rebalance plan |

The project is designed for the **Human-Driven RWA Infrastructure** path: issuer teams, licensed sponsors, compliance officers, regulators, and professional investors remain in the workflow, while AI makes the workflow faster and more structured, and smart contracts make the final state verifiable.

## Three On-Chain Proof Loops

### 1. AI Compliance Becomes On-Chain Permission

The AI engine analyses the prospectus against SFC-oriented rules, outputs a 0-100 score, and binds the result to a report hash. That result is written to `ComplianceOracle.sol` through `submitScore(assetId, score, reportHash)`.

```text
Issuer submission
	-> AI compliance engine
	-> score + reportHash
	-> ComplianceOracle.submitScore(...)
	-> ComplianceModule.canMint(...)
	-> HarbourRWAToken.mintForAsset(...) passes or reverts
```

The AI output is not a recommendation hidden inside the UI. It becomes a contract-readable state that directly affects whether issuance can proceed.

### 2. Regulated Issuance Is Enforced By Contracts

HarbourRWA separates the regulated workflow into role-specific surfaces:

- `/tokenize` for issuer submission, approval-gated deployment, and token registration.
- `/compliance` for Type 6 sponsor review, AI scoring, report hashing, and submission to SFC.
- `/regulator/issuance` for SFC issuance approval or request-changes flow.
- `/audit` for smart contract technical due diligence.
- `/kyc` and `/admin/kyc` for investor submission and compliance officer approval.
- `/subscribe` for KYC, declaration, payment, and compliance-gated minting.

The important part is the gate: if oracle score, regulator status, or identity eligibility fails, the transaction is rejected at the contract layer. This is the point where AI-assisted review becomes RWA infrastructure rather than a front-end feature.

### 3. Post-Issuance Servicing Is Claimable

The demo bond asset is not a decorative asset card. The portfolio flow demonstrates the part most RWA demos omit: servicing after issuance.

- `/portfolio` reads live bond holdings, coupon schedule, and claim history.
- The issuer funds the coupon pool through `fundDividend()`.
- The investor claims a pro-rata coupon through `claimDividend()`.
- Claim records prevent double claiming and remain auditable on-chain.
- AI Wealth Advisor reads live holdings and schedule data before answering or rebalancing.

## What Is Live In The Demo

**Primary RWA:** a demo infrastructure bond asset with a 5.50% semi-annual coupon.

**Additional supported asset types:** Green bonds and trade receivables, using the same core contracts and compliance flow.

**Core demo pages:**

| Page | Role | What judges can verify |
|---|---|---|
| `/` | Overview | Live issuance card, role entry points, and headline bond economics |
| `/prospectus` | Issuer | AI draft generation, compliance check, document download, handoff to tokenization |
| `/tokenize` | Issuer | Submit asset, wait for sponsor/SFC approval, deploy `HarbourRWAToken` |
| `/compliance` | Sponsor / Type 6 LC | Sponsor inbox, AI SFC rule review, oracle score, report hash, SFC submission |
| `/audit` | Technical reviewer | Smart contract review surface and severity-based findings |
| `/regulator` | Regulator | Oversight dashboard reading issuance records and oracle-backed compliance state |
| `/regulator/issuance` | SFC reviewer | Approve issuance or request changes for dynamic applications |
| `/kyc` | Investor | Identity profile, professional investor classification, document upload, file hashing |
| `/admin/kyc` | Compliance officer | KYC review, AI document score, approve and whitelist investor |
| `/subscribe` | Investor | Pre-check, subscription, declarations, payment, compliance-gated mint |
| `/portfolio` | Investor / Issuer | Live holdings, coupon schedule, coupon fund and claim, AI Advisor, AI Rebalance |

## Five Critical States On Mantle

Mantle is not just a deployment badge. It is the verification layer for the states that matter in a regulated RWA lifecycle.

| # | State | Contract | Why It Matters |
|---|---|---|---|
| 1 | AI compliance score | `ComplianceOracle.sol` | Makes AI review tamper-evident and contract-readable |
| 2 | Compliance report hash | `ComplianceOracle.sol` | Binds the score to a specific review artifact |
| 3 | Investor eligibility | `IdentityRegistry.sol` | Turns KYC and PI classification into mint/transfer permissions |
| 4 | Mint and transfer gate | `ComplianceModule.sol` | Enforces policy in code rather than front-end logic |
| 5 | Coupon funding and claims | `HarbourRWAToken.sol` | Makes post-issuance servicing auditable and claimable |

## Architecture

```text
Frontend (Next.js 16 / React 19 / TypeScript)
	/prospectus          -> AI drafting + compliance check + document export
	/tokenize            -> issuer submission + approval-gated token deployment
	/compliance          -> sponsor inbox + AI review + oracle submission
	/audit               -> smart contract due diligence surface
	/regulator           -> oversight dashboard
	/regulator/issuance  -> SFC approval / request changes
	/kyc                 -> investor identity and document submission
	/admin/kyc           -> compliance officer KYC approval
	/subscribe           -> declaration + payment + compliance-gated mint
	/portfolio           -> live holdings + coupon funding/claim + AI advisor/rebalance

Smart Contracts (Mantle Sepolia / Mantle Mainnet, Solidity 0.8.24)
	ComplianceOracle.sol   -> AI score and reportHash per assetId
	IdentityRegistry.sol   -> KYC, jurisdiction, AML, and PI eligibility state
	ComplianceModule.sol   -> mint and transfer gate reading Oracle + Registry
	HarbourRWAToken.sol    -> ERC-3643-inspired asset token, coupon schedule, fundDividend, claimDividend
	YieldAggregator.sol    -> allocation surface for external settlement and yield assets used in the advisor demo
```

## Smart Contract Flow

```text
1. Issuer submits the bond issuance package
2. Sponsor AI review writes score + reportHash to ComplianceOracle
3. SFC approval unlocks deployment and issuance path
4. Investor KYC approval writes eligibility to IdentityRegistry
5. Subscribe calls ComplianceModule.canMint(...)
6. HarbourRWAToken.mintForAsset(...) executes only when checks pass
7. Issuer funds the coupon pool
8. Investor claims coupon from the contract
9. AI advisor reads live holdings and coupon state for portfolio guidance
```

## Judge Demo Flow

For a DoraHacks video or live judging session, show the highest-scoring path first:

1. `/prospectus` - Load demo data and generate the bond prospectus draft with AI.
2. `/tokenize` - Submit the bond application for intermediary review and show the Sponsor Inbox handoff.
3. `/compliance` - Run AI compliance review, show score/report hash, and submit to SFC.
4. `/audit` - Show technical due diligence for the smart contract stack.
5. `/regulator/issuance` - Approve the issuance and show that approval unlocks deployment.
6. `/kyc` - Submit investor profile and documents.
7. `/admin/kyc` - Approve the investor and write eligibility to the identity registry.
8. `/subscribe` - Mint 20 bond tokens only after oracle, SFC, and KYC checks pass.
9. `/portfolio` - Fund a coupon, claim it as the investor, then ask AI Wealth Advisor about the next coupon payment.
10. `/portfolio` - Click AI Rebalance to show an allocation plan based on live holdings and risk profile.

The core judging message: **HarbourRWA does not merely tokenize an asset. It uses AI to structure regulated workflow and uses Mantle contracts to enforce the approved result across issuance, eligibility, minting, servicing, and investor management.**

## Scoring Coverage

| Judging Dimension | HarbourRWA Advantage |
|---|---|
| Technical Depth | Multi-contract Mantle system; AI oracle write; ERC-3643-inspired compliance gate; live coupon funding and claims; role-based regulated workflow |
| Innovation | AI output becomes contract-relevant permission rather than a chatbot response; regulated approvals become executable infrastructure |
| Mantle Ecosystem Contribution | Core RWA lifecycle state lives on Mantle; coupon servicing and allocation logic are demonstrated with on-chain state |
| Product Completeness | Issuer, sponsor, regulator, investor, KYC admin, audit, subscription, portfolio, and AI advisor flows are all present |
| RWA Track Fit | Targets institutional RWA infrastructure, not a retail wrapper; the bond economics create a real need for post-issuance servicing |

## Submission Narrative

- **Asset on-chain:** a demo infrastructure bond with semi-annual on-chain coupon servicing.
- **AI role:** Prospectus drafting, SFC-oriented compliance review, structured scoring, report hashing, KYC document assistance, portfolio question answering, and allocation guidance.
- **Mantle realization:** `ComplianceOracle`, `IdentityRegistry`, `ComplianceModule`, `HarbourRWAToken`, and `YieldAggregator` anchor the workflow on Mantle.
- **Verifiable value:** Compliance evidence, investor eligibility, mint permission, coupon funding, and coupon claims are visible as contract-backed state.
- **Why it deserves first prize:** It turns RWA from a tokenization screen into a complete regulated issuance and servicing pipeline, and shows a credible way for AI to participate in that pipeline without removing human control.

## Local Setup

```bash
cd app
npm install

cd contracts
npm install
npm run compile
npm run deploy:testnet

cd ..
npm run dev
```

Required environment variables:

- `DEPLOYER_PRIVATE_KEY`
- `SILICONFLOW_API_KEY`
- `MANTLESCAN_API_KEY`
- `NEXT_PUBLIC_COMPLIANCE_ORACLE_ADDRESS`
- `NEXT_PUBLIC_IDENTITY_REGISTRY_ADDRESS`