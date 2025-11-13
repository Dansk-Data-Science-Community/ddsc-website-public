# ddsc.io roadmap

## Indledning

Dette dokument gemmer oversigten over planerne for ddsc.io, herunder hvilken funktionalitet websitet skal understøtte.

## Nuværende features
- Websitet består pt. af en landing page med information og promoveringsmateriale af Dansk Data Science Community.
- Derudover findes der en eventside, hvor det er muligt via */admin* siden at oprette, slette og redigere et event. Dertil kan oploades et antal billeder til eventet som vises når man klikker ind på eventet.

## Nye features
De kommende features skal primært være med til at understøtte foreningens virke. Derfor lægges der vægt på brugeroprettelse og brugerstyring af sitet. De centrale features her er:

- Oprettelse af brugere.
    - inkl. aktivering af konto via email verificering.
- Fuld brugerstyring af konto, herunder 
    - *glemt password* (reset via email)
    - *nyt password* (rediger via log ind)
    - *log ind*
    - *log ud*
    - *redigering af profil*
- Bruger dashboard med:
    - Oversigt over tilmeldte events, herunder mulighed for afmelde event deltagelse
    - Oversigt over medlemsskab i foreningen, herunder kontigent beløb og mulighed for udmeldelse.
    - Redigering af brugeroplysninger.
- Mulighed for indmeldelse i foreningen.
    - Herunder blanket til indmeldelse.
    - Og oversigt over status på behandlingen af indmeldelsen.
- Mulighed for tilmelding til event.
    - Herunder tilmeldingsblanket.
    - Og email af "billet" til event med QR kode.
- Privacy/databeskyttelses policy side.
- Localization funktionalitet (dynamisk oversættelse af tekst på siden), herunder support for dansk og engelsk som primære sprog.

## Status på features

| Status | Feature | Status på funktionaliteter | Django app |
| :---: | :--- | --- | --- |
| ✔ | Oprettelse af brugere |`færdig`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web/users">users</a> |
| ✔ | Fuld brugerstyring af konto |`færdig`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web/users">users</a> |
| ✔ | Bruger dashboard |`færdig`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web/users">users</a> |
| ✔ | Blanket til indmeldelse |`færdig`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web/members">members</a> |
| ✔ | Tilmelding til event |`færdig`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web/events">events</a> |
| ❌ | Privacy/databeskyttelses |`klar`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web/members">members</a> |
| ❌ | Dansk/Engelsk localization |`klar`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web">global</a> |
| ❌ | Visning af bestyrelsesmedlemmer |`1 ud af 2`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web/members">members</a> |
| ❌ | Visning af vedtægter |`klar`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web">global</a> |
| ❌ | Visning af udvalg og organisering |`klar`| <a href="https://github.com/Dansk-Data-Science-Community/ddsc-website/tree/feature/users/ddsc_web/members">members</a> |
