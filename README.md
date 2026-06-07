# HarbourRWA

HarbourRWA is a Mantle-native RWA infrastructure project for regulated issuance, compliance-gated minting, investor onboarding, coupon servicing, and AI-assisted portfolio workflows.

This repository contains the application and smart contract code used for the HarbourRWA demo.

## What Is Included

- `app/src/app`: Next.js application routes for issuer, compliance, regulator, KYC, subscription, and portfolio flows
- `app/src/components`: shared UI components
- `app/src/lib`: app-side business logic and integrations
- `app/contracts/contracts`: Solidity contracts for oracle, identity, compliance, token, and yield flows

## Main Capabilities

- AI-driven prospectus and compliance workflow
- On-chain compliance scoring through `ComplianceOracle`
- Investor eligibility checks through `IdentityRegistry`
- Contract-level mint gating through `ComplianceModule`
- Coupon funding and claim flow through `HarbourRWAToken`
- AI Wealth Advisor and rebalance demo flow

## Run Locally

```bash
cd app
npm install

cd contracts
npm install
npm run compile

cd ..
npm run dev
```

## More Documentation

See `app/README.md` for the full project walkthrough, judging narrative, architecture, and demo flow.