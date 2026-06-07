# HarbourRWA

> **AI & RWA Track · Human-Driven RWA Infrastructure · Deployed on Mantle Network**

HarbourRWA is a Mantle-native RWA infrastructure stack that collapses the four broken steps of traditional asset issuance — compliance review, investor onboarding, token minting, and post-issuance coupon servicing — into one verifiable on-chain pipeline.

## One-Line Pitch

HarbourRWA is the first RWA infrastructure where AI compliance output becomes an on-chain permission primitive: the score gates minting, the prospectus hash is anchored on-chain, and investors claim USDY coupons through the contract — not a spreadsheet.

## Five Core Highlights

### 1. AI Output Is an On-Chain Permission Primitive

Most RWA projects use AI as a chatbot layer. HarbourRWA uses it as a permission source.

The AI engine analyses a prospectus and outputs a 0–100 compliance score plus a report hash. That score is written to `ComplianceOracle.sol` on Mantle via `submitScore(assetId, score, reportHash)`. `ComplianceModule.canMint(wallet, assetId)` reads the oracle before every mint. If the score is below threshold, the contract rejects the transaction — not the UI, the contract.

```
AI Engine  →  submitScore()  →  ComplianceOracle (Mantle)
                                       ↓
                             ComplianceModule.canMint()
                                       ↓
                             HarbourRWAToken.mintForAsset()  ← passes or reverts
```

This satisfies the hackathon's hard requirement: *"AI-powered function callable on-chain."*

### 2. The Only RWA Demo That Closes the Full Lifecycle

| Stage | Typical RWA Demo | HarbourRWA |
|-------|-----------------|------------|
| Compliance review | Off-chain PDF | AI score written to `ComplianceOracle` on Mantle |
| Investor onboarding | Centralised whitelist | `IdentityRegistry` — on-chain KYC state |
| Token minting | UI-controlled | `ComplianceModule.canMint()` — contract enforced |
| **Coupon funding** | **Not present** | **`fundDividend()` — issuer deposits USDY into contract** |
| **Investor claim** | **Not present** | **`claimDividend()` — pro-rata distribution, on-chain** |

A bond is only worth something if you can collect coupons. HarbourRWA is the only hackathon demo that makes post-issuance servicing an on-chain, verifiable act.

### 3. Five Critical RWA States Live on Mantle

Mantle is not the deployment chain — it is the execution layer for every state that matters:

| # | State | Contract | What it proves |
|---|-------|----------|---------------|
| 1 | Compliance score | `ComplianceOracle` | AI output is auditable, tamper-evident |
| 2 | Investor eligibility | `IdentityRegistry` | KYC is enforced at the contract layer |
| 3 | Mint permission | `ComplianceModule` | Policy lives in code, not in a dashboard |
| 4 | Coupon pool | `HarbourRWAToken.dividendFunding` | USDY is real, locked, and ring-fenced |
| 5 | Claim record | `dividendClaims` mapping | No double-claiming; fully auditable on-chain |

### 4. Prospectus Hash Binding — Regulatory Compliance by Design

Every registered asset stores a `prospectusCommitment` (`keccak256` of the full offering document) at the time of issuance. The AI engine reviews the same document and its hash is written alongside the compliance score. This means:

- The token is cryptographically bound to a specific legal document.
- Any document substitution is detectable on-chain.
- This mirrors the disclosure integrity requirement under SFC rules — implemented not as a process but as an immutable on-chain link.

### 5. Platform Architecture, Not a Single-Asset Demo

HIBT (infrastructure bond) and KCRT (commercial REIT) share identical contracts:

- Same `HarbourRWAToken.sol` — asset type distinguished by the `AssetType` enum (`Bond`, `REIT`, `GreenBond`, `TradeReceivable`)
- Same `ComplianceModule` — compliance policy is configurable per asset
- Same `ComplianceOracle` — scores are namespaced by `assetId`, supporting unlimited assets

Any Mantle-based issuer or intermediary can deploy this stack for their own asset class without modifying a single contract. That is what makes this infrastructure rather than a demo.

## What Is Live In The Demo

**Primary asset:**
- HIBT — Harbour Infrastructure Bond Token, Asia infrastructure bond with semi-annual USDY coupons

**Secondary asset:**
- KCRT — Kowloon Commercial REIT Token, demonstrates platform reusability across asset classes

**Live on-chain workflow:**

1. `/compliance` — AI reviews the prospectus, outputs a score + report hash, writes to `ComplianceOracle.submitScore(...)` on Mantle
2. `/kyc` — Investor onboarding writes eligibility to `IdentityRegistry` on Mantle
3. `/subscribe` — `ComplianceModule.canMint(...)` is called; HIBT is minted only if compliance and KYC pass
4. `/portfolio` — Reads live HIBT balance and coupon schedule from the contract; issuer funds coupon in USDY; investor claims on-chain
5. `/tokenize` — Issuer deploys a new `HarbourRWAToken` wired to the compliance and coupon infrastructure

**Adjacent capabilities (demo-scoped):**
- AI portfolio assistant driven by the investor's real on-chain holdings
- Prospectus drafting and sponsor inbox workflow
- Regulator-facing audit and compliance dashboard
- KCRT lane for asset-class breadth

## Why It Fits the Track

HarbourRWA targets the Human-Driven RWA Infrastructure path. The intended users are licensed intermediaries, issuer operations teams, and regulated compliance desks — not retail consumers.

AI is applied at the two most expensive and manual points in the workflow: prospectus compliance review and post-issuance portfolio guidance. In both cases the AI output feeds a structured on-chain state rather than stopping at a text response.

Mantle already has a credible RWA and yield-asset foundation — USDY, mETH, and a growing institutional ecosystem. HarbourRWA fills the missing layer: a compliance oracle, an issuance gate, and a coupon servicing contract that any Mantle-native issuer can plug into.

## Architecture

```text
Frontend (Next.js 16 / React 19 / TypeScript)
  /compliance  →  AI prospectus review  →  ComplianceOracle.submitScore()  →  Mantle
  /kyc         →  investor onboarding   →  IdentityRegistry.register()     →  Mantle
  /tokenize    →  asset registration    →  HarbourRWAToken.registerAsset() →  Mantle
  /subscribe   →  ComplianceModule.canMint()  →  HarbourRWAToken.mintForAsset()
  /portfolio   →  live balance + coupon history  →  fundDividend() / claimDividend()

Smart Contracts (Mantle Sepolia / Mainnet — Solidity 0.8.24 / OpenZeppelin 5)
  ComplianceOracle.sol   →  AI score (uint8) + reportHash (bytes32) per assetId
  IdentityRegistry.sol   →  KYC / jurisdiction / AML state per investor
  ComplianceModule.sol   →  mint + transfer gate; reads Oracle + Registry
  HarbourRWAToken.sol    →  ERC-3643-inspired token; coupon schedule + fundDividend + claimDividend
  YieldAggregator.sol    →  USDY + mETH yield routing for idle capital
```

## Two-Minute Judge Demo

1. `/compliance` — Upload the HIBT submission package. Run AI review. Show the Mantle tx hash and report hash from the oracle write.
2. `/kyc` — Whitelist the investor wallet. Show the on-chain registry update.
3. `/subscribe` — Attempt to mint before KYC (expect revert). Mint after KYC passes. Show the HIBT balance.
4. `/portfolio` — Show live HIBT balance and coupon schedule read directly from the contract.
5. Click **Fund Demo Coupon** — Issuer deposits USDY into the contract. Show the tx.
6. Click **Claim USDY** — Investor claims their pro-rata share. Show the USDY balance increase.
7. Open the AI advisor — Show portfolio guidance derived from the investor's actual on-chain holdings.

> The core argument: this project does not stop at tokenization. It proves compliance, enforces issuance, and closes coupon servicing — three loops that are each independently verifiable on Mantle.

## Scoring Coverage

| Judging Dimension | Weight | How HarbourRWA Addresses It |
|-------------------|--------|----------------------------|
| Technical Depth | 30% | Five-contract system; AI oracle writes on-chain; ERC-3643 compliance gate; end-to-end coupon servicing |
| Innovation | 25% | AI output as on-chain permission primitive — a new AI × Web3 paradigm not seen in prior RWA tooling |
| Mantle Ecosystem Contribution | 25% | Five critical RWA states on Mantle; USDY as coupon currency; mETH yield routing; reusable public infrastructure |
| Product Completeness | 20% | Full lifecycle runnable demo; two asset classes; live frontend; deployable by any issuer |

## Submission Narrative

- **Asset on-chain:** Asia infrastructure bond (HIBT) primary; commercial REIT (KCRT) secondary
- **AI role:** Compliance review → structured score + report hash → on-chain oracle; post-issuance portfolio guidance from real holdings
- **Mantle realization:** `ComplianceOracle`, `IdentityRegistry`, `ComplianceModule`, `HarbourRWAToken`, `YieldAggregator` — all deployed on Mantle; USDY for coupon settlement
- **Verifiable value:** Every critical step produces a Mantle contract call visible on MantleScan
- **Ecosystem fit:** Built on Mantle's existing RWA and yield-asset foundation; adds the missing compliance, issuance, and servicing layer

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
- `NEXT_PUBLIC_COMPLIANCE_MODULE_ADDRESS`
- `NEXT_PUBLIC_HARBOUR_RWA_TOKEN_ADDRESS`
- `NEXT_PUBLIC_YIELD_AGGREGATOR_ADDRESS`
- `NEXT_PUBLIC_USDY_ADDRESS`

The deploy script writes an `.env.deployed` snippet you can copy into your local environment.

## Before Open-Sourcing Or Submitting

- Remove all private keys and secrets from `.env.local` and any committed files.
- Make sure deployed addresses and MantleScan links are included in the final submission.
- Capture one compliance tx, one HIBT mint tx, one coupon funding tx, and one coupon claim tx for the demo video.
- Publish a public frontend URL instead of relying on localhost.

## Submission Checklist

- Open-source repo with setup instructions
- Public demo URL
- Mantle deployment addresses
- MantleScan verified contracts
- Demo video longer than 2 minutes
- DoraHacks submission that clearly states the project is Human-Driven RWA Infrastructure

## Tech Stack

- Next.js 16 + React 19 + TypeScript
- viem + wagmi + RainbowKit
- Solidity 0.8.24 + Hardhat + OpenZeppelin 5
- Mantle Sepolia / Mantle Mainnet
- SiliconFlow + Qwen models for AI analysis
- USDY and mETH integrations for yield and settlement demos
