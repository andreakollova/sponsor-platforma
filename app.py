import os
from datetime import datetime
from flask import Flask, render_template, abort

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

# Ikonky k športom (Bootstrap Icons)
SPORT_ICONS = {
    "Pozemný hokej": "bi-flag",
    "Flag Football": "bi-flag",
    "Ľadový hokej": "bi-snow",
    "Beh": "bi-lightning-charge",
    "Esports & Tech": "bi-controller",
    "Fitness": "bi-activity",
}

# --- Demo listingy (ukážky) – rozšírené o slug + detail dáta ---
CLUB_CARDS = [
    {
        "slug": "hkm-nova-dubnica",
        "title": "HKM Nová Dubnica",
        "location": "Trenčiansky kraj",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Logo na drese", "Stadión banner", "Komunita"],
        "price_from": 450, "reach": "35k/m", "er": 3.1,
        "verified": True,
        "desc": "Regionálny klub s aktívnou mládežou a stabilnou návštevnosťou.",
        "sport": "Pozemný hokej",

        # detail (galéria, inventár, balíčky, publikum, metriky...)
        "gallery": [cover("cover.png"), "hero-photo.png", "influencer-cover.png"],
        "inventory": {
            "Viditeľnosť": [
                {"icon": "bi-badge-ad", "name": "Logo na drese"},
                {"icon": "bi-easel", "name": "Banner v hale"},
                {"icon": "bi-broadcast-pin", "name": "Livestream overlay"},
            ],
            "Digitál": [
                {"icon": "bi-instagram", "name": "IG Reels"},
                {"icon": "bi-youtube", "name": "YouTube highlights"},
                {"icon": "bi-tiktok", "name": "TikTok klipy"},
            ],
            "Komunita": [
                {"icon": "bi-people", "name": "Mládežnícky deň"},
                {"icon": "bi-building", "name": "CSR aktivácia"},
            ],
        },
        "packages": [
            {"name": "Starter", "price": "€450+", "incl": ["Logo na drese (rukáv)", "1× IG reel", "Report PDF"]},
            {"name": "Growth", "price": "€950+", "incl": ["Banner v hale", "2× IG reel + 3× story", "Livestream overlay"]},
            {"name": "Brand Max", "price": "€1 900+", "incl": ["Logo na hrudi", "YouTube highlight", "Lokálna aktivácia"]},
        ],
        "audience": {
            "male": 62, "female": 38,
            "age": {"13–17": 12, "18–24": 28, "25–34": 34, "35–44": 16, "45+": 10}
        },
        "metrics": {"posts_m": 22, "avg_views": "18k", "avg_cpm": "€6.8"},
        "social": {"instagram": "#", "youtube": "#", "tiktok": "#"},
        "upcoming": [
            {"date": "2025-10-12", "title": "HKM vs. MŠK – domáci zápas", "type": "Zápas"},
            {"date": "2025-10-20", "title": "Livestream derby", "type": "Stream"},
        ],
    },
    {
        "slug": "nabor-bratislava-invincibles",
        "title": "Nabor Bratislava Invincibles",
        "location": "Bratislava",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Social posty", "Event aktivácia", "Livestream"],
        "price_from": 700, "reach": "62k/m", "er": 2.6,
        "verified": True,
        "desc": "Moderný tím s kvalitným obsahom. Vhodné pre mestské značky.",
        "sport": "Flag Football",
        "gallery": [cover("cover.png"), "hero-photo.png"],
        "inventory": {
            "Viditeľnosť": [
                {"icon": "bi-badge-ad", "name": "Logo na prilbe"},
                {"icon": "bi-easel", "name": "LED board"},
            ],
            "Digitál": [
                {"icon": "bi-instagram", "name": "IG Reels"},
                {"icon": "bi-broadcast", "name": "Livestream preroll"},
            ],
            "Komunita": [
                {"icon": "bi-megaphone", "name": "Event aktivácia"},
            ],
        },
        "packages": [
            {"name": "City", "price": "€700+", "incl": ["Logo na prilbe", "1× reel", "Report PDF"]},
            {"name": "City Pro", "price": "€1 400+", "incl": ["LED board", "2× reel + 1× livestream"]},
        ],
        "audience": {"male": 58, "female": 42, "age": {"18–24": 24, "25–34": 41, "35–44": 23, "45+": 12}},
        "metrics": {"posts_m": 18, "avg_views": "22k", "avg_cpm": "€7.2"},
        "social": {"instagram": "#", "youtube": "#"},
        "upcoming": [{"date": "2025-10-05", "title": "Exhibícia v meste", "type": "Event"}],
    },
    {
        "slug": "hc-trencin-juniors",
        "title": "HC Trenčín Juniors",
        "location": "Trenčín",
        "cover": cover("cover.png"),
        "avatar": avatar("profile.png"),
        "tags": ["Logo na prilbe", "LED board", "Meet & Greet"],
        "price_from": 550, "reach": "48k/m", "er": 2.9,
        "verified": False,
        "desc": "Mládežnícky program s prepojením na školy a lokálne komunity.",
        "sport": "Ľadový hokej",
        "gallery": [cover("cover.png")],
        "inventory": {
            "Viditeľnosť": [{"icon": "bi-snow", "name": "Logo na prilbe"}],
            "Digitál": [{"icon": "bi-instagram", "name": "Stories balík"}],
            "Komunita": [{"icon": "bi-people", "name": "Meet & Greet"}],
        },
        "packages": [
            {"name": "Junior", "price": "€550+", "incl": ["Logo na prilbe", "3× stories", "Report PDF"]},
        ],
        "audience": {"male": 66, "female": 34, "age": {"13–17": 18, "18–24": 30, "25–34": 28, "35–44": 16, "45+": 8}},
        "metrics": {"posts_m": 14, "avg_views": "11k", "avg_cpm": "€5.9"},
        "social": {"instagram": "#"},
        "upcoming": [{"date": "2025-10-10", "title": "Turnaj juniorov", "type": "Zápas"}],
    }
]

INFLUENCER_CARDS = [
    {
        "slug": "mia-runner",
        "title": "Mia Runner",
        "location": "Bratislava",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["IG Reels", "TikTok", "Bežecké tipy"],
        "price_from": 350, "reach": "120k", "er": 5.4,
        "verified": True,
        "desc": "Bežkyňa a trénerka, edukatívny obsah a recenzie. Publikum 18–34.",
        "sport": "Beh",
        "gallery": [cover("influencer-cover.png"), "hero-photo.png"],
        "inventory": {
            "Digitál": [
                {"icon": "bi-instagram", "name": "IG Reel/Story"},
                {"icon": "bi-tiktok", "name": "TikTok video"},
                {"icon": "bi-youtube", "name": "YouTube review"},
            ],
            "Komunita": [{"icon": "bi-people", "name": "Workshop / meet-up"}],
        },
        "packages": [
            {"name": "Reel", "price": "€350+", "incl": ["1× IG Reel", "5× story frames", "Link/UTM"]},
            {"name": "Run Pack", "price": "€890+", "incl": ["Reel + TikTok", "Giveaway", "PDF report"]},
        ],
        "audience": {"male": 38, "female": 62, "age": {"18–24": 26, "25–34": 48, "35–44": 18, "45+": 8}},
        "metrics": {"posts_m": 12, "avg_views": "42k", "avg_cpm": "€7.8"},
        "social": {"instagram": "#", "tiktok": "#", "youtube": "#"},
        "upcoming": [{"date": "2025-10-03", "title": "Live beh – charita", "type": "Event"}],
    },
    {
        "slug": "techgoalie",
        "title": "TechGoalie",
        "location": "Žilina",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["YouTube", "Recenzie", "Livestream"],
        "price_from": 420, "reach": "98k", "er": 4.1,
        "verified": True,
        "desc": "Tech pre šport: senzory, wearables, recovery. Silná UTM atribúcia.",
        "sport": "Esports & Tech",
        "gallery": [cover("influencer-cover.png")],
        "inventory": {
            "Digitál": [
                {"icon": "bi-youtube", "name": "Video recenzia"},
                {"icon": "bi-broadcast", "name": "Livestream s product slotom"},
            ],
        },
        "packages": [
            {"name": "Review", "price": "€420+", "incl": ["1× YouTube video", "Link/UTM", "Pinned comment"]},
        ],
        "audience": {"male": 72, "female": 28, "age": {"18–24": 22, "25–34": 46, "35–44": 24, "45+": 8}},
        "metrics": {"posts_m": 6, "avg_views": "55k", "avg_cpm": "€6.1"},
        "social": {"youtube": "#", "instagram": "#"},
        "upcoming": [{"date": "2025-10-15", "title": "Live test senzorov", "type": "Stream"}],
    },
    {
        "slug": "fitmama-zuz",
        "title": "FitMama Zuz",
        "location": "Trnava",
        "cover": cover("influencer-cover.png"),
        "avatar": avatar("influencer.png"),
        "tags": ["IG Stories", "Workouts", "Komunita"],
        "price_from": 300, "reach": "85k", "er": 6.0,
        "verified": False,
        "desc": "Cvičenia doma a s deťmi, vysoká interakcia v stories.",
        "sport": "Fitness",
        "gallery": [cover("influencer-cover.png")],
        "inventory": {
            "Digitál": [
                {"icon": "bi-instagram", "name": "Story séria"},
                {"icon": "bi-camera-reels", "name": "IG Reel"},
            ],
            "Komunita": [{"icon": "bi-heart", "name": "Charitatívny tréning"}],
        },
        "packages": [
            {"name": "Stories", "price": "€300+", "incl": ["5× story", "Swipe-up link", "PDF report"]},
        ],
        "audience": {"male": 22, "female": 78, "age": {"18–24": 18, "25–34": 52, "35–44": 22, "45+": 8}},
        "metrics": {"posts_m": 16, "avg_views": "19k", "avg_cpm": "€5.4"},
        "social": {"instagram": "#"},
        "upcoming": [{"date": "2025-10-08", "title": "Live workout", "type": "Live"}],
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

def unique_sports(cards):
    return sorted({c["sport"] for c in cards})

def find_item(kind, slug):
    data = CLUB_CARDS if kind == "club" else INFLUENCER_CARDS
    for x in data:
        if x["slug"] == slug:
            return x
    return None

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

# --- DETAIL: klub / influencer ---
@app.route("/l/<kind>/<slug>")
def detail(kind, slug):
    if kind not in ("club", "influencer"):
        abort(404)
    item = find_item(kind, slug)
    if not item:
        abort(404)
    # labely do breadcrumb
    kind_label = "Kluby" if kind == "club" else "Športovci & Influenceri"
    return render_template(
        "detail.html",
        kind=kind,
        kind_label=kind_label,
        item=item,
        sport_icon=SPORT_ICONS.get(item["sport"], "bi-collection"),
        year=datetime.now().year
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
