# Product Brief — Smart To-Do (MVP)

## 1) Problem & mål
Folk glemmer eller utsetter små oppgaver. Vi vil gi en enkel to-do-app som automatisk:
- setter **etikett** (School/Work/Home/…)
- foreslår **prioritet** (1–5)
Mål: rask registrering, “bra nok” auto-klassifisering, og lav friksjon.

## 2) Primærbrukere
Studenter + foreldre/ansatte (enkle lister, lite tid, mobil/laptop).

## 3) Jobs-to-be-done
- “Jeg vil raskt legge inn en oppgave med ett felt og få forslag til label/prioritet.”
- “Jeg vil se kun det viktigste i dag.”
- “Jeg vil endre forslagene hvis de ikke stemmer.”

## 4) Scope (MVP)
- Legg til oppgave (tittel) → heuristikk (keywords/regex) → foreslå {label, priority}.
- Listevisning med filter/søk (by label, by priority).
- Rediger/slett oppgaver.
- Lokal lagring (fil/minne) i MVP. (Sky og konto senere.)

**Ikke med (Non-goals nå):**
- Deling/brukere, mobil-app, kalender-sync, notifikasjoner, avansert AI-kost.

## 5) Suksesskriterier (MVP)
- ≤ 2 klikk for å legge inn oppgave.
- ≥ 70% av forslagene føles “riktige nok” for brukeren.
- Ingen kost til skyleverandør for normal bruk (AI kun ved behov/caching).

## 6) Datamodell (minimum)
`task { id, title, label, priority, due_date?, done? }`
- **label** ∈ {School, Work, Home, Health, Finance, Shopping, Other}
- **priority** ∈ {1..5} (5 = høyest)

## 7) Heuristikk først (fallback AI)
- Regex/keyword-tabell pr. label og enkel mapping tekst→prioritet.
- Hvis heuristikk er usikker: valgfri AI-kall (rate-limit + cache).

## 8) Teknisk valg
- **Backend:** Python + Flask.
- **Frontend:** Enkle templates (Jinja2) + litt CSS.
- **AI-SDK:** Gemini (Google) først for enkel dev-flyt; design koden slik at leverandør kan byttes via `ai_client.py` (adapter).
- **Lagring:** In-memory / JSON-fil i MVP.

## 9) Enkle skisser (tekst)
**Home:** liste + filter (label/prio) + “Add”.  
**Add:** ett inputfelt (tittel). Etter submit vises forslag {label, priority} som kan endres før lagring.

## 10) Risikoer & tiltak
- **Treffrate lav:** start med manuell overstyring + lær av bruk (later).
- **AI-kost:** cache og begrens kall; heuristikk default.
- **Personvern:** lokalt i MVP; ingen PII.

## 11) Milepæler for neste fase
1. Definer prioritetsskala og mapping (1–5).
2. Implementer heuristikk (regex/keywords).
3. Lag `ai_client.py` med `classify(label, text)` (stub først).
4. Oppdater `app.py` (liste/filter) + `templates/index.html`.
5. Minimal UX-tråd: Home → Add/Edit → tilbake til Home.# Product Brief – Smart To-Do (auto labels & priority)

## 1. Problem
Folk bruker for mye tid på å skrive, sortere og prioritere to-dos. Vanskelig å se hva som er viktig nå.

## 2. Primærbrukere
Studenter og ansatte/foreldre som vil raskt fange oppgaver og få enkel prioritering.

## 3. Verdiforslag (IVP)
Skriv én setning (“Kjøpe bleier i morgen”), appen foreslår automatisk label (f.eks. Home) og prioritet (1–5). Mindre friksjon, bedre fokus.

## 4. Mål (MVP)
- Fange oppgave (tittel) → forslag {label, priority} → bruker kan justere → lagre.
- Vise liste med filter på label og sort etter priority.
- Lokal lagring (ingen PII i MVP).

## 5. Must-haves (MVP)
- Input-felt for tittel
- Auto-forslag for label/priority (heuristikk først, AI fallback)
- Lister + filter/sortering
- Enkel, rask UI (Home → Add/Edit → tilbake)

## 6. Nice-to-haves (senere)
- Due-date og påminnelser
- Synk (sky)
- Flere språk
- Statistikk/innsikt

## 7. Ikke-mål nå
- Team/deling
- Kompleks prosjektstyring
- Full mobilapp

## 8. Tekniske valg (MVP)
- Stack: Flask (Python) + enkel HTML/CSS
- Heuristikk (regex/keywords) → ev. AI via Gemini/OpenAI med rate-limit + cache
- Bygg `ai_client.py` som adapter slik at leverandør kan byttes

## 9. Risikoer & tiltak
- API-kost: bruk cache og begrens kall; heuristikk = default
- Personvern: lokal lagring i MVP; ingen PII
- Tidsrisiko: hold scope stramt (kun must-haves)

## 10. Suksessmål (MVP)
- T(90): < 5 sek fra åpning til lagret oppgave
- ≥ 70% av autolabel treffes riktig (kan overstyres)
- 80% av testbrukere opplever “mindre friksjon” vs. vanlig notat


