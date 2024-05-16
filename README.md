# zolibá
kedvenc játékaim (python)

**Az összes játékhoz kell a "pygame" csomag, és ha jól emlékszem semmi más**

### Archery
- bal klikkel tudsz célozni
- amíg nem találtad el a céltáblákat, addig nem tudsz pénzt felszedni
- amikor eltalálod az utolsót, eltűnik minden fal és céltábla csak a nyilak nem
- ilyenkor lehet csak felszednie a pénzeket a nyilaknak esés közben
- 1-es gombbal tudsz venni aim assist-et, de el kell használnod egyből (1 alkalmas)
- azért van tele pénzzel az első szint mert tesztelgettem 😂

ehhez a játékhoz nem néztem semmilyen tutorialt, magamtól jutott az eszembe még az ötlet is

### Balls
- jobb klikk letartásával tudsz interaktálni a golyókkal

ez volt a legelső projekt amit csináltam ezek közül. követtem egy tutorialt, de a videóban C++ ban volt minden írva, szóval át kellett fordítanom.
kipróbáltam több golyóval is, de szegény python nem annyira bírta el, nagyon lassú volt.
> [tutorial](https://youtu.be/lS_qeBy3aQI?si=sGYpwQNm229x54cd)

### Grenade
- csak akkor működik jól, ha 2 kontroller a géphez van csatlakoztatva
- bal joystick-kal mozogsz
- "a"-val ugrassz (legalábbis x-box kontrolleren az "a"-val)
- "x"-szel lövöd ki a gránátodat, arra amerre épp nézel a bal joystick-kel
- ha az ellenfél meglő, lemegy egy bizonyos mennyiség az életedből (minél közelebb vagy annál több)
- a saját gránátod nem sebez téged, de ellő maga felől a robbanás

ez tartott a legtöbb ideig az összes közül, mert tutorial és akármilyen "physics engine" nélkül csináltam.
de szerintem még így is több időt töltöttem el játszani vele a húgommal mint megcsinálni 😂

### Particle System
- jól néz ki

nem olyan nagy cucc, ehez is néztem tutorialt de go-ban volt írva, és csak egyszer néztem meg, megpróbáltam magamtól megcsinálni.
a videóban csak egy terminal alkalmazás volt, szóval a színeket én adtam hozzá
> [tutorial](https://youtu.be/zW6MEpa9LFo?si=bUmb5ioLp9gsRFXM)

### pygame 3D
- WASD-al tudsz mozogni, egérrel tudsz körbe nézni
- sok értelme nincs, csak tesztelgettem

ezt még 2 éve lemásoltam egy tutorialról, de nagyon lassú volt, és nem valami hatékony.
a kockák minden oldalát mindegyik frame-ben kirajzolta az ablakra, én most nemrég megcsináltam hogy csak azok látszódjanak amik képen vannak, és nincsenek elbújva egy másik oldal mögé.
(még így is nagyon lassú, de ilyen 3-4x gyorsabb lett)
> [tutorial](https://youtu.be/g4E9iq0BixA?si=sKbzhW8oZGnilYoL)

### Ray Caster
- WASD-al tudsz mozogni, egérrel tudsz körbe nézni

már rég óta akartam ezt csinálni, de mindig elakadtam valahol.
kb. egy hete láttam egy videót erről az algoritmusról, és megpróbáltam beprogramozni, hát ez sült ki belőle.
a felbontás nagyon rossz, mert amúgy nagyon szenved vele a python. arra is gondoltam hogy egyszer meg kéne csinálnom rust-ban ahol 1000x gyorsabb lenne.
> [tutorial](https://youtu.be/NbSee-XM7WA?si=ZYpLklArnHfFZuHN)

### Solitaire
- bal klikkel ki tudsz jelölni kártyákat
- bal klikkel le tudod őket rakni, de csak akkor ha szabályos

ezzel nagyon sokat szenvedtem, mert nem néztem semmi féle tutorialt nem akartam nézni.
egy telefonos solitaire appról jött meg a kedvem ehhez, és szerintem tök jó lett.

### Suika game
- bal klikkel le tudsz engedni egy golyót
- azonos méretű golyók összeolvadnak egy nagyobb golyóba (minél nagyobb a két golyó, annál több pontot kapsz)
- ha egy golyó kirepül a pohár tetején, meghalsz

ezt egyből a "balls" projekt után csináltam, hogy leteszteljem a képletet egy igazi játékban.
kicsit befejezetlen (mint az összes többi), de még így is tök jó.
