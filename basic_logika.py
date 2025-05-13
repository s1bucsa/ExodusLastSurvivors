import random

# === KONSTANTY ===
POCET_HRACU = 6
VELIKOST_POSADKY = 3
MIN_SKORE_PRO_PREZITI = 25

JMENA = ["Alex", "Robin", "Morgan", "Kai", "Sam", "Chris", "Jordan", "Taylor", "Drew", "Jamie"]
PROFESI = [
    "technik", "medik", "vůdce", "voják", "učitel", "vědec", "zemědělec", "programátor",
    "fotbalista", "bartender", "influencer", "fotograf", "spisovatel", "klaun", "mechanik"
]
NEDOSTATKY = [
    "nemocný", "příliš starý", "mladý a nezkušený", "mentálně labilní", "zraněný",
    "egocentrik", "paranoidní", "klaustrofobik", "bez empatie", "žádná"
]
POZITIVA = [
    "silný", "technicky nadaný", "přírodní vůdce", "odolný", "empatický",
    "rychlý učitel", "disciplinovaný", "žádné"
]
SKRYTE_CILE = ["sabotér", "pomocník", "neutrální"]

# === TŘÍDA POSTAVA ===
class Postava:
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.vek = random.randint(18, 80)
        self.sila = random.randint(1, 10)
        self.profese = random.choice(PROFESI)
        self.dovednost_hodnota = random.randint(3, 10)
        self.nedostatek = random.choice(NEDOSTATKY)
        self.pozitivum = random.choice(POZITIVA)
        self.skryty_cil = random.choice(SKRYTE_CILE)

        nedostatky_moznosti = [n for n in NEDOSTATKY if n != "příliš starý" and n != "mladý a nezkušený"]
        if self.vek < 30:
            nedostatky_moznosti.append("mladý a nezkušený")
        elif self.vek > 65:
            nedostatky_moznosti.append("příliš starý")

        self.nedostatek = random.choice(nedostatky_moznosti)

    def info(self):
        return (f"{self.jmeno} (Věk: {self.vek}, Síla: {self.sila}, Profese: {self.profese} "
                f"(schopnost: {self.dovednost_hodnota}), Nedostatek: {self.nedostatek}, "
                f"Pozitivum: {self.pozitivum}, Cíl: {self.skryty_cil})")

    def ohodnotit(self, typ_katastrofy):
        score = self.dovednost_hodnota + self.sila
        score += {
            "nemocný": -5, "příliš starý": -3, "mladý a nezkušený": -2, "mentálně labilní": -4,
            "zraněný": -3, "egocentrik": -2, "paranoidní": -2, "klaustrofobik": -1, "bez empatie": -2
        }.get(self.nedostatek, 0)
        score += {
            "silný": +3, "technicky nadaný": +4, "přírodní vůdce": +3, "odolný": +2,
            "empatický": +2, "rychlý učitel": +1, "disciplinovaný": +2
        }.get(self.pozitivum, 0)
        if self.skryty_cil == "sabotér":
            score -= 10
        if typ_katastrofy == "meteorit" and self.profese in ["vůdce", "mechanik"]:
            score += 2
        elif typ_katastrofy == "potopa" and self.profese in ["technik", "zemědělec"]:
            score += 2
        elif typ_katastrofy == "mimozemstani" and self.profese in ["voják", "medik"]:
            score += 3
        elif typ_katastrofy == "ai" and self.profese in ["programátor", "vědec"]:
            score += 3
        elif typ_katastrofy == "virus" and self.profese in ["medik", "učitel"]:
            score += 2
        elif typ_katastrofy == "slunce" and self.profese in ["vědec", "technik"]:
            score += 2
        return max(0, score)

# === HERNÍ SVĚT ===
class HerniSvet:
    def __init__(self):
        self.typ_katastrofy, self.popis_katastrofy = self.nahodna_katastrofa()
        self.hraci = self.vytvor_hrace(POCET_HRACU)
        self.vybrani = []

    def nahodna_katastrofa(self):
        katastrofy = {
            "meteorit": "☄️ Země byla zasažena masivním meteoritem.",
            "potopa": "🌊 Celosvětová potopa zatopila kontinenty.",
            "mimozemstani": "👽 Invaze mimozemšťanů zničila infrastrukturu.",
            "ai": "🤖 Umělá inteligence se vymkla kontrole.",
            "virus": "🦠 Pandemický virus rozvrátil společnost.",
            "slunce": "🔥 Slunce umírá a planeta se přehřívá."
        }
        klic = random.choice(list(katastrofy.keys()))
        return klic, katastrofy[klic]

    def vytvor_hrace(self, pocet):
        random.shuffle(JMENA)
        return [Postava(jmeno) for jmeno in JMENA[:pocet]]

    def hlasovani(self):
        print("\n🗳️ HLASOVÁNÍ")
        kandidati = [h for h in self.hraci if h not in self.vybrani]
        hlasy = {}
        for hrac in self.hraci:
            volba = random.choice(kandidati)
            hlasy[volba] = hlasy.get(volba, 0) + 1
        max_hlasu = max(hlasy.values())
        moznosti = [k for k, v in hlasy.items() if v == max_hlasu]
        vybran = random.choice(moznosti)
        print(f"🔹 Zvolen: {vybran.jmeno} ({max_hlasu} hlasů)")
        return vybran

    def simulace_mise(self):
        print("\n🚀 VYHODNOCENÍ MISE")
        total = 0
        for p in self.vybrani:
            score = p.ohodnotit(self.typ_katastrofy)
            print(f"- {p.jmeno}: skóre = {score}")
            total += score
        print(f"\n📊 Celkové skóre posádky: {total}")
        if total >= MIN_SKORE_PRO_PREZITI:
            print("✅ Mise úěspěšná. Lidstvo má šanci!")
        else:
            print("❌ Mise selhala. Lidstvo bylo ztraceno.")

# === HLAVNÍ PROGRAM ===
def main():
    svet = HerniSvet()
    print("\n🌍 Exodus: Last Survivors")
    print("\n=== KATASTROFA ===")
    print(svet.popis_katastrofy)

    print("\n=== POSTAVY ===")
    for h in svet.hraci:
        print("-", h.info())

    while len(svet.vybrani) < VELIKOST_POSADKY:
        print(f"\n--- KOLO {len(svet.vybrani)+1} ---")
        vybran = svet.hlasovani()
        svet.vybrani.append(vybran)

    print("\n=== POSÁDKA ===")
    for p in svet.vybrani:
        print("-", p.info())

    svet.simulace_mise()

if __name__ == "__main__":
    main()