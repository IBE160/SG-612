# Phase 1 – Priority & Heuristic MVP

## Mål (denne fasen)
1. Definere prioritetskala (1–5) og mapping fra tekst → prioritet.
2. Implementere heuristikk (regex/keywords) for {label, priority}.
3. Lage `ai_client.py` (adapter) med stub `classify(label, text)`.
4. Oppdatere `app.py` og `templates/index.html` med liste/filter + Add/Edit-flyt.
5. Kjør lokalt og verifiser flow: Home → Add/Edit → tilbake → filter/sort.

## Sjekkliste
- [ ] `priority_scale.md` med regler/mapping.
- [ ] `heuristics.py` (funksjoner for label/priority).
- [ ] `ai_client.py` (stub – returnerer heuristikk-resultat; klar for AI senere).
- [ ] `app.py` oppdatert (liste, filter, kall til heuristikk).
- [ ] `templates/index.html` oppdatert (filter/sort + Add/Edit).
- [ ] Testlogg (kort) i `docs/phase-1/test-notes.md`.
