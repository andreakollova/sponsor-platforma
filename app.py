import os
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# ---- Selectors ----
CITIES = [
    "Bratislava", "Košice", "Prešov", "Žilina", "Nitra",
    "Banská Bystrica", "Trnava", "Trenčín", "Martin", "Poprad"
]

COUNTRIES = [
    "Slovensko", "Česko", "Poľsko", "Maďarsko", "Rakúsko",
    "Nemecko", "Slovinsko", "Chorvátsko", "Rumunsko", "Ukrajina"
]

# ---- Helpers for static paths ----
def cover(name): return f"covers/{name}"
def avatar(name): return f"profileimages/{name}"

# ---- Demo data ----
CLUB_CARDS = [
    {
        "title": "HKM Nová Dubnica",
        "location": "Trenčiansky kraj",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Logo na drese", "Stadión banner", "Community"],
        "price_from": 450,
        "reach": "35k/m",
        "er": 3.1,
        "verified": True,
        "desc": "Regionálny klub s aktívnou mládežou a lokálnou komunitou. Stabilná návštevnosť a pravidelné podujatia."
    },
    {
        "title": "Nabor Bratislava Invincibles",
        "location": "Bratislava",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Social posty", "Event aktivácia", "Livestream"],
        "price_from": 700,
        "reach": "62k/m",
        "er": 2.6,
        "verified": True,
        "desc": "Moderný tím s rastúcim dosahom a kvalitnou produkciou obsahu. Vhodné pre mestské značky."
    },
    {
        "title": "HC Trenčín Juniors",
        "location": "Trenčín",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Logo na prilbe", "LED board", "Meet & Greet"],
        "price_from": 550,
        "reach": "48k/m",
        "er": 2.9,
        "verified": False,
        "desc": "Mládežnícky program s prepojením na školy a rodičovské komunity. Možné B2C aj CSR aktivácie."
    }
]

INFLUENCER_CARDS = [
    {
        "title": "Mia Runner",
        "location": "Bratislava",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["IG Reels", "TikTok", "Bežecké tipy"],
        "price_from": 350,
        "reach": "120k",
        "er": 5.4,
        "verified": True,
        "desc": "Bežkyňa a trénerka, edukatívny obsah a produktové recenzie. Silné ženské publikum 18–34."
    },
    {
        "title": "TechGoalie",
        "location": "Žilina",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["YouTube", "Recenzie", "Livestream"],
        "price_from": 420,
        "reach": "98k",
        "er": 4.1,
        "verified": True,
        "desc": "Technológie pre šport: senzory, wearables, recovery. Prepojenie na e-shopové UTM kampane."
    },
    {
        "title": "FitMama Zuz",
        "location": "Trnava",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["IG Stories", "Workouts", "Komunita"],
        "price_from": 300,
        "reach": "85k",
        "er": 6.0,
        "verified": False,
        "desc": "Cvičenia doma a s deťmi, silná lokálna komunita a vysoká interakcia v stories."
    }
]

# Partners (logos – placeholders in static/covers)
PARTNERS = [
    cover("partner1.png"), cover("partner2.png"), cover("partner3.png"),
    cover("partner4.png"), cover("partner5.png"), cover("partner6.png")
]

# Case studies (simple demo)
CASE_STUDIES = [
    {
        "logo": cover("partner1.png"),
        "title": "Retail značka × Mládežnícky klub",
        "result": "+42% IG reach",
        "desc": "3-mesačná lokálna kampaň – balík logo na drese + reels. Bezpečné escrow, jasné reporty."
    },
    {
        "logo": cover("partner2.png"),
        "title": "Wellness brand × Influencer",
        "result": "3.8× ROAS",
        "desc": "UGC videá + kód s UTM. Nárast predajov a stabilné ER počas celej spolupráce."
    },
    {
        "logo": cover("partner3.png"),
        "title": "Fintech × Klub",
        "result": "+11k leads",
        "desc": "Stadión bannery + community event. Silná aktivácia mimo sociálnych sietí."
    }
]

FAQ = [
    {
        "q": "Ako fungujú platby a escrow?",
        "a": "Sponzor vloží prostriedky do escrow. Po splnení milníkov sa platba uvoľní športovcovi/klubu. Refundy a spory rieši admin."
    },
    {
        "q": "Odkiaľ sú metriky?",
        "a": "Z oficiálnych API sociálnych sietí (IG/FB/YouTube/TikTok). V reporte vidíš reach, impresie, ER a demografiu."
    },
    {
        "q": "Môžem získať kurátorské Top 5?",
        "a": "Áno. Po vyplnení onboarding dotazníka porovnáme hodnoty značky, publikum a lokalitu a navrhneme Top 5."
    }
]

@app.route("/")
def index():
    return render_template(
        "index.html",
        cities=CITIES,
        countries=COUNTRIES,
        clubs=CLUB_CARDS,
        influencers=INFLUENCER_CARDS,
        partners=PARTNERS,
        cases=CASE_STUDIES,
        faq=FAQ,
        year=datetime.now().year
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))  # 5001 lokálne, v deployi si Render/CleverCloud nastaví PORT
    app.run(host="0.0.0.0", port=port, debug=True)
