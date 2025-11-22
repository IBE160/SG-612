# Phase 0 – Research (AI-bibliotek og plattform)

## Problem
Hvilken AI-plattform og SDK bør vi bruke for MVP? (Chat, verktøy-kall, rimelige kostnader, enkel drift)

## Kandidater (kort)
- **OpenAI**: God dokumentasjon, bred støtte, god verktøy-kalling. Kost/bruk variabelt.
- **Gemini (Google)**: Sterk på multimodal, god CLI/SDK, enkle verktøy. Godt gratisnivå for studenter i perioder.
- **Anthropic**: Sterk på sikkerhet/long context. Noe færre eksempler for verktøy-kall i Python.

## Behov/krav for oss
- Python-backend (Flask).
- Verktøy-kall (klassifisere label/priority lokalt først, ev. AI fallback).
- Lav friksjon for teamet (enkelt å kjøre lokalt og demo).
- Kostnadskontroll (cache / lav token-bruk).

## Anbefaling (MVP)
- **Plattform:** Gemini (CLI + Python SDK) _eller_ OpenAI (hvis foreleser krever).
- **Begrunnelse:** Enkelt å komme i gang, gode dev-verktøy, sterk multimodal ved behov, fornuftig kost.
- **Fallback:** Bygg koden slik at leverandør kan byttes (en liten `ai_client.py`-adapter).

## Arkitektur (lite)


## Neste
- Lage `ai_client.py` med funksjon `classify(label, text)`.
- Først: heuristikk (regex/keywords).
- Hvis lav selvtillit: kall AI (rate-limit + cache).
