# Phase 0 – Brainstorm

## Problem / Goal (1–2 setninger)
Studenter og travle brukere mister oversikt over oppgaver på tvers av skole/arbeid/hjem. Vi vil lage en superenkel to-do som automatisk foreslår **etiketter** (School/Work/Home/Health/Finance/Shopping/Other) og **prioritet**, slik at viktigste oppgaver kommer først.

## Primærbrukere & behov
- Studenter: rask innregistrering, prioritering i eksamensperioder.
- Ansatte/foreldre: kategorisering på autopilot, dagens topp-3-liste.
- Alle: filter/søk, “due soon”, enkel mobil-vennlig UI.

## Kjernefunksjoner (MVP)
- Legg til oppgave (tittel + valgfri dato) → automatisk label + prioritet (AI).
- Listevisning med sortering (prioritet, dato).
- Filter på etiketter.
- Fullfør/slett.
- Lokal lagring (første versjon) – server senere.

## Sider/Views vi tror vi trenger
- **Home**: liste, filtrering, fullfør/slett.
- **Add/Edit**: enkel form (som i `index.html`).
- **Analytics (senere)**: enkle grafer (fullførte pr. uke).
- **Settings (senere)**: velge AI-leverandør og terskler for prioritet.

## AI-tech vurdering (kort)
Kriterier: pris, kvalitet, latency, SDK-støtte, enkel integrasjon, logging/telemetri.  
**Anbefaling for MVP:** Start med **Gemini** (vi har allerede CLI/telemetri i repoet). Lag et tynt interface så vi kan bytte modell senere.

## Åpne spørsmål / risiko
- Personvern: lagrer vi data lokalt eller i sky (MVP: lokalt).
- Kostnader ved API-bruk (MVP: begrens kall / caching).
- Kvalitet på auto-label/priority uten treningsdata.
- Offline-støtte vs. skyfunksjoner.

## Datamodell (minimum)
`Task { id, title, label, priority, due_date?, done }`

## Neste steg (konkrete oppgaver)
1. Definere prioritetsskala (f.eks. 1–5) og mapping fra tekst → prioritet.
2. Lage enkel “heuristikk først” (regex/keywords) + AI-fallback.
3. Skisse UX for Home + Add/Edit (wireframe).
4. Lage liste-/filterlogikk i `app.py` + oppdatere `templates/index.html`.
5. Velge SDK for Gemini (python) og lage et lite kall for “classify(label, priority)”.
