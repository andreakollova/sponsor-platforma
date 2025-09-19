import os
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# --- Selectory ---
CITIES = [
    "Bratislava", "Košice", "Prešov", "Žilina", "Nitra",
    "Banská Bystrica", "Trnava", "Trenčín", "Martin", "Poprad"
]

COUNTRIES = [
    "Slovensko", "Česko", "Poľsko", "Maďarsko", "Rakúsko",
    "Nemecko", "Slovinsko", "Chorvátsko", "Rumunsko", "Ukrajina"
]

def cover(name): return f"covers/{name}"
def avatar(name): return f"profileimages/{name}"

# --- Demo listingy (ukážky) ---
CLUB_CARDS = [
    {
        "title": "HKM Nová Dubnica",
        "location": "Trenčiansky kraj",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Logo na drese", "Stadión banner", "Komunita"],
        "price_from": 450, "reach": "35k/m", "er": 3.1,
        "verified": True,
        "desc": "Regionálny klub s aktívnou mládežou a stabilnou návštevnosťou.",
        "sport": "Pozemný hokej"
    },
    {
        "title": "Nabor Bratislava Invincibles",
        "location": "Bratislava",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Social posty", "Event aktivácia", "Livestream"],
        "price_from": 700, "reach": "62k/m", "er": 2.6,
        "verified": True,
        "desc": "Moderný tím s kvalitným obsahom. Vhodné pre mestské značky.",
        "sport": "Flag Football"
    },
    {
        "title": "HC Trenčín Juniors",
        "location": "Trenčín",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Logo na prilbe", "LED board", "Meet & Greet"],
        "price_from": 550, "reach": "48k/m", "er": 2.9,
        "verified": False,
        "desc": "Mládežnícky program s prepojením na školy a lokálne komunity.",
        "sport": "Ľadový hokej"
    }
]

INFLUENCER_CARDS = [
    {
        "title": "Mia Runner",
        "location": "Bratislava",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["IG Reels", "TikTok", "Bežecké tipy"],
        "price_from": 350, "reach": "120k", "er": 5.4,
        "verified": True,
        "desc": "Bežkyňa a trénerka, edukatívny obsah a recenzie. Publikum 18–34.",
        "sport": "Beh"
    },
    {
        "title": "TechGoalie",
        "location": "Žilina",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["YouTube", "Recenzie", "Livestream"],
        "price_from": 420, "reach": "98k", "er": 4.1,
        "verified": True,
        "desc": "Tech pre šport: senzory, wearables, recovery. Silná UTM atribúcia.",
        "sport": "Esports & Tech"
    },
    {
        "title": "FitMama Zuz",
        "location": "Trnava",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["IG Stories", "Workouts", "Komunita"],
        "price_from": 300, "reach": "85k", "er": 6.0,
        "verified": False,
        "desc": "Cvičenia doma a s deťmi, vysoká interakcia v stories.",
        "sport": "Fitness"
    }
]

# --- Partneri (Simple Icons slugs) ---
PARTNER_SLUGS = [
    "visa",
    "adidas", "nike", "puma", "underarmour",
    "redbull", "logitech",
    "cisco", "hp", "asus", "acer",
    "nvidia", "airbnb", "newbalance", "fila"
]

FAQ = [
    {"q": "Ako funguje portfólio pre veľké firmy?",
     "a": "Zadáš rozpočet a preferencie. My navrhneme diverzifikované portfólio klubov a športovcov. Pred investíciou ho vieš upraviť."},
    {"q": "Kto podpisuje zmluvy a rieši platby?",
     "a": "Platbu prijímame my a po telefonickom potvrdení uzatvárame zmluvy so športovcami/klubmi. Následne transparentne prerozdeľujeme financie."},
    {"q": "Čo uvidím v dashboards?",
     "a": "Najbližšie zápasy/streamy, odkazy na obsah a metriky – vrátane mesačných PDF/CSV reportov za každú položku portfólia."}
]

# --- Pomocné pre filter športov ---
def unique_sports(cards):
    return sorted({c["sport"] for c in cards})

SPORT_ICONS = {
    "Pozemný hokej": "bi-flag",
    "Flag Football": "bi-flag",
    "Ľadový hokej": "bi-snow",
    "Beh": "bi-lightning-charge",
    "Esports & Tech": "bi-controller",
    "Fitness": "bi-activity",
}

@app.route("/")
def index():
    club_sports = unique_sports(CLUB_CARDS)
    influencer_sports = unique_sports(INFLUENCER_CARDS)
    return render_template(
        "index.html",
        cities=CITIES, countries=COUNTRIES,
        clubs=CLUB_CARDS, influencers=INFLUENCER_CARDS,
        partners=PARTNER_SLUGS,
        faq=FAQ, year=datetime.now().year,
        club_sports=club_sports,
        influencer_sports=influencer_sports,
        sport_icons=SPORT_ICONS
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
