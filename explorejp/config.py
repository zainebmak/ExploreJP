"""Configuration for ExploreJP Streamlit app."""

# Color Palette
COLORS = {
    "burgundy": "#6C0820",
    "cherry_blossom_pink": "#F2AEBC",
    "misty_rose": "#F2DCDB",
    "silver_lake_blue": "#5A86CB",
    "lapis_lazuli": "#305D91",
}

# Typography
FONTS = {
    "heading": "Playfair Display",
    "body": "Montserrat",
}

# Page Configuration
PAGE_CONFIG = {
    "page_title": "ExploreJP - Discover Japan",
    "page_icon": "🌸",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Custom CSS
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Montserrat:wght@300;400;500;600&display=swap');

    /* Global styles */
    .stApp {
        font-family: '""" + FONTS['body'] + """', sans-serif;
        background-color: #fff5f7;
        color: #3b1f2d;
    }

    .css-1d391kg, .css-18e3th9 { 
        background-color: #fff5f7 !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: '""" + FONTS['heading'] + """', serif;
        color: """ + COLORS['burgundy'] + """ !important;
    }

    /* Buttons */
    .stButton>button {
        background: """ + COLORS['burgundy'] + """ !important;
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-family: '""" + FONTS['body'] + """', sans-serif;
        font-weight: 600;
        letter-spacing: 0.03em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(108, 8, 32, 0.2);
        font-size: 0.95rem;
    }

    .stButton>button:hover {
        background: """ + COLORS['lapis_lazuli'] + """ !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(108, 8, 32, 0.3);
    }

    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(108, 8, 32, 0.2);
    }

    /* Secondary button style */
    .stButton>button[kind="secondary"] {
        background: white !important;
        color: """ + COLORS['burgundy'] + """ !important;
        border: 2px solid """ + COLORS['burgundy'] + """ !important;
        box-shadow: 0 4px 16px rgba(108, 8, 32, 0.1);
    }

    .stButton>button[kind="secondary"]:hover {
        background: """ + COLORS['misty_rose'] + """ !important;
        border-color: """ + COLORS['cherry_blossom_pink'] + """ !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(108, 8, 32, 0.15);
    }

    .city-card {
        background-color: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.08);
        margin-bottom: 18px;
    }

    .section-title {
        color: """ + COLORS['lapis_lazuli'] + """ !important;
        font-weight: 700;
    }

    .logo-container {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 24px;
    }

    .logo-mark {
        width: 64px;
        height: 64px;
        border-radius: 18px;
        background: linear-gradient(135deg, """ + COLORS['burgundy'] + """ 0%, """ + COLORS['cherry_blossom_pink'] + """ 100%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.14);
    }

    .city-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 18px;
        margin-bottom: 16px;
        border: 1px solid rgba(0, 0, 0, 0.06);
    }

    .city-card {
        background-color: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.08);
        margin-bottom: 18px;
        overflow: hidden;
    }

    .city-card .city-meta {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 12px;
        flex-wrap: wrap;
    }

    .badge {
        display: inline-block;
        background-color: """ + COLORS['cherry_blossom_pink'] + """;
        color: """ + COLORS['burgundy'] + """;
        border-radius: 999px;
        padding: 6px 14px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .info-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 28px;
        border: 1px solid rgba(255, 255, 255, 0.7);
    }

    .button-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 18px;
    }

    .button-grid .stButton>button {
        width: 100%;
        min-height: 70px;
        text-align: left;
        border-radius: 20px;
        background: rgba(242, 174, 188, 0.16) !important;
        color: #3b1f2d !important;
        border: 1px solid rgba(108, 8, 32, 0.12) !important;
        box-shadow: 0 14px 36px rgba(198, 138, 154, 0.08);
        padding: 18px 20px;
        font-weight: 700;
    }

    .button-grid .stButton>button:hover {
        background: rgba(242, 174, 188, 0.28) !important;
        color: #6c0820 !important;
    }

    .button-grid .stButton>button span {
        display: inline-flex;
        align-items: center;
        gap: 12px;
    }

    .section-card {
        background: rgba(255, 249, 251, 0.92);
        border-radius: 28px;
        padding: 28px;
        box-shadow: 0 20px 50px rgba(198, 138, 154, 0.12);
        margin-bottom: 24px;
        border: 1px solid rgba(242, 174, 188, 0.24);
    }

    .page-hero {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 24px;
        background: linear-gradient(180deg, rgba(255, 247, 250, 0.96) 0%, rgba(242, 220, 219, 0.98) 65%);
        border-radius: 28px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 24px 80px rgba(198, 138, 154, 0.1);
        border: 1px solid rgba(242, 174, 188, 0.3);
    }

    .page-hero .hero-copy {
        flex: 1;
        min-width: 300px;
    }

    .page-hero .hero-copy h2 {
        font-size: 2.5rem;
        color: """ + COLORS['burgundy'] + """;
        margin: 0 0 16px;
        line-height: 1.05;
    }

    .page-hero .hero-copy p {
        color: #6d4050;
        font-size: 1.05rem;
        margin-bottom: 18px;
        max-width: 640px;
    }

    .page-hero .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 10px 18px;
        border-radius: 999px;
        background: rgba(242, 174, 188, 0.18);
        border: 1px solid rgba(242, 174, 188, 0.35);
        color: """ + COLORS['burgundy'] + """;
        font-weight: 700;
        margin-bottom: 20px;
    }

    .page-hero .hero-card {
        flex: 0 0 360px;
        background: white;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(198, 138, 154, 0.1);
        border: 1px solid rgba(242, 174, 188, 0.3);
    }

    .hero-card-image {
        display: block;
        width: 100%;
        height: auto;
    }

    .hero-card-body {
        padding: 22px;
    }

    .hero-card-body h4 {
        margin: 0 0 10px;
        color: """ + COLORS['burgundy'] + """;
    }

    .hero-card-body p {
        margin: 0;
        color: #6d4050;
        line-height: 1.6;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: """ + COLORS['misty_rose'] + """;
    }

    .css-1v0mbdj {
        background-color: """ + COLORS['burgundy'] + """;
    }

    /* Cards */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }

    /* Hero section */
    .hero-page {
        background: linear-gradient(180deg, #fff8fb 0%, #fce7ef 30%, #fff5f7 100%);
        color: #3b1f2d;
        padding: 44px;
        border-radius: 32px;
        box-shadow: 0 44px 100px rgba(198, 138, 154, 0.12);
        border: 1px solid rgba(242, 174, 188, 0.35);
        margin-bottom: 32px;
    }

    .top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 28px;
        margin-bottom: 42px;
        flex-wrap: wrap;
    }

    .brand {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        font-weight: 700;
        font-size: 1.08rem;
        letter-spacing: 0.08em;
        color: """ + COLORS['burgundy'] + """;
    }

    .brand-name {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .brand-mark {
        width: 42px;
        height: 42px;
        border-radius: 16px;
        background: linear-gradient(135deg, """ + COLORS['burgundy'] + """ 0%, """ + COLORS['cherry_blossom_pink'] + """ 100%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.05rem;
        font-weight: 800;
        box-shadow: 0 12px 30px rgba(198, 138, 154, 0.16);
    }

    .brand-logo {
        width: 54px;
        height: 54px;
        object-fit: contain;
        border-radius: 16px;
        box-shadow: 0 14px 34px rgba(198, 138, 154, 0.16);
        display: block;
    }

    .brand-logo-badge {
        width: 54px;
        height: 54px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        background: linear-gradient(135deg, """ + COLORS['burgundy'] + """ 0%, """ + COLORS['cherry_blossom_pink'] + """ 100%);
        box-shadow: 0 14px 34px rgba(198, 138, 154, 0.16);
        padding: 6px;
    }

    .brand-logo-badge svg {
        width: 100%;
        height: 100%;
        display: block;
    }

    .nav-links {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        align-items: center;
        justify-content: center;
    }

    .nav-link {
        color: #6d4050;
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 10px 16px;
        border-radius: 999px;
        transition: background-color 0.2s ease, color 0.2s ease, transform 0.2s ease;
    }

    .nav-link.active,
    .nav-link:hover {
        background-color: rgba(242, 174, 188, 0.22);
        color: """ + COLORS['burgundy'] + """;
        transform: translateY(-1px);
    }

    .nav-cta {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 24px;
        background: """ + COLORS['burgundy'] + """;
        color: white;
        border-radius: 999px;
        font-size: 0.95rem;
        font-weight: 700;
        text-decoration: none;
        box-shadow: 0 18px 35px rgba(198, 138, 154, 0.16);
    }

    .hero-title {
        margin: 0 0 22px;
        font-size: 3.6rem;
        line-height: 1.02;
    }

    .hero-copy {
        font-size: 1.15rem;
        max-width: 680px;
        color: #6d4050;
        margin-bottom: 32px;
        line-height: 1.8;
    }

    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
        color: """ + COLORS['burgundy'] + """;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-size: 0.85rem;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        margin-bottom: 36px;
    }

    .hero-actions .stButton>button {
        width: 100%;
        min-height: 54px;
        border-radius: 20px;
        border: none;
        font-weight: 700;
        padding: 14px 22px;
        transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease, opacity 0.2s ease;
    }

    .hero-actions .stButton>button:first-child {
        background: linear-gradient(135deg, """ + COLORS['burgundy'] + """ 0%, """ + COLORS['cherry_blossom_pink'] + """ 100%);
        color: white;
        box-shadow: 0 24px 68px rgba(198, 138, 154, 0.16);
    }

    .hero-actions .stButton>button:last-child {
        background: rgba(255, 255, 255, 0.92);
        color: """ + COLORS['burgundy'] + """;
        border: 1px solid rgba(108, 8, 32, 0.18);
        box-shadow: 0 18px 40px rgba(198, 138, 154, 0.1);
    }

    .hero-actions .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 28px 84px rgba(198, 138, 154, 0.2);
        opacity: 0.98;
    }

    .hero-banner {
        margin-top: 16px;
        background: rgba(255,255,255,0.84);
        border: 1px solid rgba(242, 174, 188, 0.35);
        border-radius: 24px;
        padding: 24px;
        display: flex;
        gap: 18px;
        flex-wrap: wrap;
        color: #6d4050;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.7);
    }

    .hero-banner div {
        flex: 1 1 220px;
        min-width: 180px;
    }

    .hero-banner strong {
        display: block;
        color: """ + COLORS['burgundy'] + """;
        font-weight: 700;
        margin-bottom: 6px;
        font-size: 1.05rem;
    }

    .hero-page .hero-content {
        max-width: 720px;
    }

    .hero-page .hero-inner {
        display: grid;
        grid-template-columns: 1.2fr 0.9fr;
        gap: 40px;
        align-items: center;
    }

    @media (max-width: 960px) {
        .hero-page {
            padding: 32px 28px;
        }

        .hero-page .hero-inner {
            grid-template-columns: 1fr;
        }

        .top-bar {
            flex-direction: column;
            align-items: stretch;
        }

        .nav-links {
            justify-content: center;
        }

        .hero-actions {
            justify-content: flex-start;
        }

        .hero-title {
            font-size: 2.6rem;
        }

        .hero-copy {
            margin-bottom: 28px;
        }
    }

    .hero-page img {
        border-radius: 26px;
        width: 100%;
        max-width: 540px;
        box-shadow: 0 24px 60px rgba(198, 138, 154, 0.14);
    }

    .hero-page .hero-content {
        max-width: 720px;
    }

    .hero-page .hero-inner {
        display: grid;
        grid-template-columns: 1.2fr 0.9fr;
        gap: 40px;
        align-items: center;
    }

    @media (max-width: 960px) {
        .hero-page {
            padding: 32px 28px;
        }

        .hero-page .hero-inner {
            grid-template-columns: 1fr;
        }

        .hero-title {
            font-size: 2.6rem;
        }
    }

    /* New Clean Home Page Styles - Enhanced Hero Section */
    .hero-container-main {
        background: linear-gradient(135deg, #fff8fb 0%, #fef5f7 50%, #fff 100%);
        border-radius: 32px;
        padding: 60px 48px;
        margin-bottom: 56px;
        box-shadow: 0 12px 48px rgba(108, 8, 32, 0.08);
        position: relative;
    }

    .top-nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 32px 56px;
        background: white;
        border-radius: 28px;
        margin-bottom: 48px;
        box-shadow: 0 8px 36px rgba(108, 8, 32, 0.12);
        position: relative;
        z-index: 10;
    }

    .nav-brand-main {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .nav-brand-main .brand-logo,
    .nav-brand-main .brand-logo-badge {
        width: 56px;
        height: 56px;
    }

    .brand-name-text {
        font-size: 1.6rem;
        font-weight: 700;
        color: """ + COLORS['burgundy'] + """;
        font-family: '""" + FONTS['heading'] + """', serif;
        letter-spacing: 0.02em;
    }

    .nav-menu-main {
        display: flex;
        gap: 40px;
        align-items: center;
    }

    .nav-item-main {
        font-size: 0.9rem;
        letter-spacing: 0.12em;
        color: """ + COLORS['lapis_lazuli'] + """;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s;
        position: relative;
        padding: 8px 4px;
    }

    .nav-item-main.active {
        color: """ + COLORS['burgundy'] + """;
    }

    .nav-item-main.active::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: """ + COLORS['cherry_blossom_pink'] + """;
        border-radius: 2px;
    }

    .nav-item-main:hover {
        color: """ + COLORS['burgundy'] + """;
        transform: translateY(-2px);
    }

    .nav-cta-main {
        background: """ + COLORS['burgundy'] + """;
        color: white;
        border: none;
        padding: 16px 36px;
        border-radius: 32px;
        font-size: 0.85rem;
        letter-spacing: 0.12em;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 8px 28px rgba(108, 8, 32, 0.25);
        text-transform: uppercase;
    }

    .nav-cta-main:hover {
        background: """ + COLORS['lapis_lazuli'] + """;
        transform: translateY(-3px);
        box-shadow: 0 12px 36px rgba(108, 8, 32, 0.3);
    }

    .hero-left-content {
        padding: 40px 48px 40px 0;
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .hero-eyebrow-text {
        font-size: 0.8rem;
        letter-spacing: 0.2em;
        color: """ + COLORS['burgundy'] + """;
        font-weight: 700;
        margin-bottom: 28px;
        display: inline-block;
        text-transform: uppercase;
    }

    .hero-title-main {
        font-size: 5.5rem;
        line-height: 0.92;
        color: """ + COLORS['burgundy'] + """;
        margin-bottom: 36px;
        font-family: '""" + FONTS['heading'] + """', serif;
        font-weight: 700;
        text-shadow: 0 2px 8px rgba(108, 8, 32, 0.05);
        letter-spacing: -0.02em;
    }

    .hero-desc-text {
        font-size: 1.15rem;
        line-height: 1.9;
        color: #5a5a5a;
        margin-bottom: 44px;
        max-width: 540px;
        font-weight: 400;
    }

    .hero-right-visual {
        position: relative;
        padding: 20px 0;
        z-index: 2;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-image-main {
        width: 100%;
        max-width: 620px;
        border-radius: 32px;
        box-shadow: 0 28px 80px rgba(108, 8, 32, 0.22);
        display: block;
        transition: all 0.4s ease;
        border: 8px solid white;
    }

    .hero-image-main:hover {
        transform: scale(1.02) translateY(-8px);
        box-shadow: 0 32px 96px rgba(108, 8, 32, 0.28);
    }

    .hero-eyebrow-text {
        font-size: 0.75rem;
        letter-spacing: 0.18em;
        color: """ + COLORS['burgundy'] + """;
        font-weight: 700;
        margin-bottom: 24px;
        display: inline-block;
    }

    .hero-title-main {
        font-size: 5rem;
        line-height: 0.95;
        color: """ + COLORS['burgundy'] + """;
        margin-bottom: 32px;
        font-family: '""" + FONTS['heading'] + """', serif;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(108, 8, 32, 0.05);
    }

    .hero-desc-text {
        font-size: 1.08rem;
        line-height: 1.85;
        color: #5a5a5a;
        margin-bottom: 40px;
        max-width: 520px;
    }

    .hero-right-visual {
        position: relative;
        padding: 20px;
    }

    .hero-image-main {
        width: 100%;
        border-radius: 28px;
        box-shadow: 0 24px 72px rgba(108, 8, 32, 0.18);
        display: block;
        transition: transform 0.3s;
    }

    .hero-image-main:hover {
        transform: scale(1.02);
    }

    .section-title-main {
        font-size: 2.2rem;
        color: """ + COLORS['burgundy'] + """;
        font-weight: 700;
        margin: 0 0 28px 0;
        font-family: '""" + FONTS['heading'] + """', serif;
    }

    /* Style for VIEW ALL button */
    .stButton>button[key="view_all_destinations"] {
        background: white !important;
        color: """ + COLORS['burgundy'] + """ !important;
        border: 2px solid """ + COLORS['burgundy'] + """ !important;
        border-radius: 24px !important;
        padding: 12px 28px !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.12em !important;
        font-weight: 700 !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 16px rgba(108, 8, 32, 0.1) !important;
    }

    .stButton>button[key="view_all_destinations"]:hover {
        background: """ + COLORS['burgundy'] + """ !important;
        color: white !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(108, 8, 32, 0.2) !important;
    }

    /* Style for Explore Now button */
    .stButton>button[key="explore_now_btn"] {
        background: linear-gradient(135deg, """ + COLORS['burgundy'] + """ 0%, """ + COLORS['lapis_lazuli'] + """ 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 32px !important;
        padding: 18px 48px !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.12em !important;
        font-weight: 700 !important;
        box-shadow: 0 12px 40px rgba(108, 8, 32, 0.25) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
    }

    .stButton>button[key="explore_now_btn"]:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 16px 48px rgba(108, 8, 32, 0.35) !important;
    }

    .stButton>button[key="explore_now_btn"]:active {
        transform: translateY(-2px) scale(1.02) !important;
    }

    .dest-card-main {
        background: white;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(108, 8, 32, 0.12);
        transition: all 0.3s;
        cursor: pointer;
        border: 1px solid rgba(242, 174, 188, 0.15);
    }

    .dest-card-main:hover {
        transform: translateY(-12px);
        box-shadow: 0 20px 48px rgba(108, 8, 32, 0.18);
        border-color: """ + COLORS['cherry_blossom_pink'] + """;
    }

    .dest-image-main {
        width: 100%;
        height: 240px;
        object-fit: cover;
        display: block;
        transition: transform 0.3s;
    }

    .dest-card-main:hover .dest-image-main {
        transform: scale(1.05);
    }

    .dest-info-main {
        padding: 24px;
    }

    .dest-name-main {
        font-size: 1.4rem;
        font-weight: 700;
        color: """ + COLORS['burgundy'] + """;
        margin: 0 0 10px 0;
        font-family: '""" + FONTS['heading'] + """', serif;
    }

    .dest-desc-main {
        font-size: 0.95rem;
        color: #666;
        margin: 0;
        line-height: 1.5;
    }

    .guide-item-main {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 22px;
        background: white;
        border-radius: 18px;
        margin-bottom: 14px;
        transition: all 0.3s;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(108, 8, 32, 0.1);
        border: 1px solid rgba(242, 174, 188, 0.12);
    }

    .guide-item-main:hover {
        background: """ + COLORS['misty_rose'] + """;
        transform: translateX(12px);
        box-shadow: 0 8px 28px rgba(108, 8, 32, 0.15);
        border-color: """ + COLORS['cherry_blossom_pink'] + """;
    }

    .guide-icon-main {
        font-size: 2rem;
        filter: drop-shadow(0 2px 4px rgba(108, 8, 32, 0.1));
    }

    .guide-content-main {
        flex: 1;
    }

    .guide-title-main {
        font-size: 1.1rem;
        font-weight: 700;
        color: """ + COLORS['burgundy'] + """;
        margin: 0 0 5px 0;
    }

    .guide-desc-main {
        font-size: 0.88rem;
        color: #666;
        margin: 0;
        line-height: 1.4;
    }

    .guide-arrow-main {
        font-size: 2rem;
        color: """ + COLORS['cherry_blossom_pink'] + """;
        font-weight: 300;
        transition: transform 0.3s;
    }

    .guide-item-main:hover .guide-arrow-main {
        transform: translateX(6px);
    }

    @media (max-width: 1200px) {
        .hero-title-main {
            font-size: 3.5rem;
        }
        
        .nav-menu-main {
            display: none;
        }
        
        .hero-container-main {
            padding: 28px;
        }
    }

    /* Enhanced Explore Cities Page Styles */
    .explore-page-header {
        text-align: center;
        padding: 48px 24px 32px;
        background: linear-gradient(135deg, #fff8fb 0%, #fef5f7 100%);
        border-radius: 28px;
        margin-bottom: 32px;
        box-shadow: 0 8px 32px rgba(108, 8, 32, 0.08);
    }

    .explore-title {
        font-size: 3rem;
        color: """ + COLORS['burgundy'] + """;
        margin: 0 0 16px 0;
        font-family: '""" + FONTS['heading'] + """', serif;
        font-weight: 700;
    }

    .explore-subtitle {
        font-size: 1.1rem;
        color: #666;
        margin: 0;
        line-height: 1.6;
    }

    .stats-container {
        margin-bottom: 32px;
    }

    .stat-card {
        background: white;
        border-radius: 20px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(108, 8, 32, 0.08);
        transition: all 0.3s;
        border: 2px solid transparent;
    }

    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(108, 8, 32, 0.15);
        border-color: """ + COLORS['cherry_blossom_pink'] + """;
    }

    .stat-card-highlight {
        background: linear-gradient(135deg, """ + COLORS['misty_rose'] + """ 0%, #fff 100%);
        border-color: """ + COLORS['cherry_blossom_pink'] + """;
    }

    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: """ + COLORS['burgundy'] + """;
        font-family: '""" + FONTS['heading'] + """', serif;
        margin-bottom: 8px;
    }

    .stat-label {
        font-size: 0.95rem;
        color: #666;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* Beautiful Action Menu Buttons */
    .stButton>button[key^="action_"] {
        background: linear-gradient(135deg, #ffffff 0%, #fffbfc 100%) !important;
        border: 2px solid rgba(242, 174, 188, 0.25) !important;
        border-radius: 20px !important;
        padding: 28px 20px !important;
        text-align: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 24px rgba(108, 8, 32, 0.08) !important;
        min-height: 160px !important;
        color: """ + COLORS['burgundy'] + """ !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        white-space: pre-line !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        letter-spacing: 0.01em !important;
    }

    .stButton>button[key^="action_"]:hover {
        background: linear-gradient(135deg, """ + COLORS['misty_rose'] + """ 0%, #ffffff 100%) !important;
        border-color: """ + COLORS['cherry_blossom_pink'] + """ !important;
        transform: translateY(-10px) !important;
        box-shadow: 0 16px 40px rgba(108, 8, 32, 0.15) !important;
    }

    .stButton>button[key^="action_"]:active {
        transform: translateY(-6px) !important;
        box-shadow: 0 10px 32px rgba(108, 8, 32, 0.12) !important;
    }

    /* Style for active action button */
    .stButton>button[key^="action_"][aria-pressed="true"] {
        background: linear-gradient(135deg, """ + COLORS['misty_rose'] + """ 0%, #ffffff 100%) !important;
        border: 3px solid """ + COLORS['cherry_blossom_pink'] + """ !important;
        box-shadow: 0 10px 36px rgba(242, 174, 188, 0.25) !important;
        transform: translateY(-6px) !important;
    }

    /* View Details Button */
    .stButton>button[key^="view_"] {
        background: linear-gradient(135deg, """ + COLORS['burgundy'] + """ 0%, """ + COLORS['lapis_lazuli'] + """ 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(108, 8, 32, 0.2) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button[key^="view_"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(108, 8, 32, 0.3) !important;
    }

    /* Favorite Button */
    .stButton>button[key^="fav_"] {
        background: white !important;
        color: """ + COLORS['burgundy'] + """ !important;
        border: 2px solid """ + COLORS['cherry_blossom_pink'] + """ !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-size: 1.3rem !important;
        box-shadow: 0 4px 16px rgba(242, 174, 188, 0.2) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button[key^="fav_"]:hover {
        background: """ + COLORS['cherry_blossom_pink'] + """ !important;
        transform: scale(1.1) !important;
        box-shadow: 0 8px 24px rgba(242, 174, 188, 0.4) !important;
    }

    /* Close Details Button */
    .stButton>button[key="close_details"] {
        background: """ + COLORS['misty_rose'] + """ !important;
        color: """ + COLORS['burgundy'] + """ !important;
        border: 2px solid """ + COLORS['burgundy'] + """ !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(108, 8, 32, 0.12) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button[key="close_details"]:hover {
        background: white !important;
        transform: translateX(-4px) !important;
        box-shadow: 0 8px 24px rgba(108, 8, 32, 0.2) !important;
    }

    /* Remove from favorites button */
    .stButton>button[key^="myjapan_remove_"], 
    .stButton>button[key^="detail_fav_"],
    .stButton>button[key^="discover_fav_"] {
        background: white !important;
        color: """ + COLORS['burgundy'] + """ !important;
        border: 2px solid """ + COLORS['cherry_blossom_pink'] + """ !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(108, 8, 32, 0.1) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button[key^="myjapan_remove_"]:hover,
    .stButton>button[key^="detail_fav_"]:hover,
    .stButton>button[key^="discover_fav_"]:hover {
        background: """ + COLORS['burgundy'] + """ !important;
        color: white !important;
        border-color: """ + COLORS['burgundy'] + """ !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(108, 8, 32, 0.2) !important;
    }

    .current-view-header {
        background: white;
        padding: 20px 32px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(108, 8, 32, 0.08);
        margin-bottom: 28px;
    }

    .view-label {
        color: #666;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .view-name {
        color: """ + COLORS['burgundy'] + """;
        font-size: 1.3rem;
        font-weight: 700;
        font-family: '""" + FONTS['heading'] + """', serif;
    }

    .filter-section {
        background: white;
        padding: 24px;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(108, 8, 32, 0.08);
    }

    .results-count {
        text-align: center;
        padding: 16px;
        background: """ + COLORS['misty_rose'] + """;
        border-radius: 16px;
        margin-bottom: 28px;
        font-size: 1.05rem;
        color: """ + COLORS['burgundy'] + """;
    }

    .enhanced-city-card {
        background: white;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(108, 8, 32, 0.1);
        transition: all 0.3s;
        margin-bottom: 24px;
        border: 2px solid transparent;
    }

    .enhanced-city-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(108, 8, 32, 0.18);
        border-color: """ + COLORS['cherry_blossom_pink'] + """;
    }

    .enhanced-city-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        transition: transform 0.3s;
    }

    .enhanced-city-card:hover .enhanced-city-image {
        transform: scale(1.05);
    }

    .enhanced-city-content {
        padding: 20px;
    }

    .enhanced-city-name {
        font-size: 1.5rem;
        color: """ + COLORS['burgundy'] + """;
        font-weight: 700;
        margin: 0 0 12px 0;
        font-family: '""" + FONTS['heading'] + """', serif;
    }

    .enhanced-city-badges {
        margin-bottom: 12px;
    }

    .enhanced-badge {
        display: inline-block;
        background: """ + COLORS['cherry_blossom_pink'] + """;
        color: """ + COLORS['burgundy'] + """;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .enhanced-city-info {
        font-size: 0.9rem;
        color: #666;
        margin: 8px 0;
    }

    .enhanced-city-desc {
        font-size: 0.95rem;
        color: #555;
        line-height: 1.6;
        margin-top: 12px;
    }

    .city-detail-modal {
        background: white;
        border-radius: 28px;
        padding: 32px;
        box-shadow: 0 12px 48px rgba(108, 8, 32, 0.15);
        border: 2px solid """ + COLORS['cherry_blossom_pink'] + """;
    }

    .modal-header {
        text-align: center;
        margin-bottom: 28px;
        padding-bottom: 20px;
        border-bottom: 2px solid """ + COLORS['misty_rose'] + """;
    }

    .detail-image {
        width: 100%;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(108, 8, 32, 0.12);
    }

    .detail-section {
        margin-bottom: 24px;
    }

    .detail-section h3 {
        color: """ + COLORS['burgundy'] + """;
        font-size: 1.5rem;
        margin-bottom: 16px;
    }

    .detail-section p {
        line-height: 1.8;
        color: #555;
        margin-bottom: 8px;
    }

    .known-for-list {
        list-style: none;
        padding: 0;
    }

    .known-for-list li {
        padding: 12px 16px;
        background: """ + COLORS['misty_rose'] + """;
        border-radius: 12px;
        margin-bottom: 10px;
        color: """ + COLORS['burgundy'] + """;
        font-weight: 600;
    }

    .search-result-card {
        background: white;
        padding: 24px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(108, 8, 32, 0.08);
        transition: all 0.3s;
    }

    .search-result-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 28px rgba(108, 8, 32, 0.12);
    }

    .result-city-name {
        color: """ + COLORS['burgundy'] + """;
        font-size: 1.6rem;
        margin: 0 0 12px 0;
    }

    .result-info {
        color: #666;
        margin-bottom: 12px;
    }

    .result-desc {
        color: #555;
        line-height: 1.7;
    }

    .region-city-card, .season-city-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(108, 8, 32, 0.08);
        transition: all 0.3s;
        margin-bottom: 16px;
    }

    .region-city-card:hover, .season-city-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(108, 8, 32, 0.12);
        background: """ + COLORS['misty_rose'] + """;
    }

    .region-city-card h4, .season-city-card h4 {
        color: """ + COLORS['burgundy'] + """;
        margin: 0 0 8px 0;
        font-size: 1.2rem;
    }

    .region-city-card p, .season-city-card p {
        color: #666;
        margin: 0;
        font-size: 0.9rem;
    }

    .empty-favorites {
        text-align: center;
        padding: 80px 40px;
        background: white;
        border-radius: 28px;
        box-shadow: 0 8px 32px rgba(108, 8, 32, 0.08);
    }

    .empty-icon {
        font-size: 5rem;
        margin-bottom: 24px;
        opacity: 0.6;
    }

    .empty-favorites h3 {
        color: """ + COLORS['burgundy'] + """;
        font-size: 2rem;
        margin-bottom: 16px;
    }

    .empty-favorites p {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.7;
    }

    .favorite-city-card {
        background: white;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(108, 8, 32, 0.1);
        transition: all 0.3s;
        margin-bottom: 24px;
        border: 2px solid """ + COLORS['cherry_blossom_pink'] + """;
    }

    .favorite-city-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(108, 8, 32, 0.18);
    }

    .favorite-city-image {
        width: 100%;
        height: 220px;
        object-fit: cover;
    }

    .favorite-city-content {
        padding: 24px;
    }

    .favorite-city-name {
        font-size: 1.6rem;
        color: """ + COLORS['burgundy'] + """;
        font-weight: 700;
        margin: 0 0 12px 0;
        font-family: '""" + FONTS['heading'] + """', serif;
    }

    .favorite-city-badges {
        margin-bottom: 12px;
    }

    .favorite-city-info {
        font-size: 1rem;
        color: #666;
        margin: 12px 0;
    }

    .favorite-city-desc {
        font-size: 1rem;
        color: #555;
        line-height: 1.7;
    }

    .chart-title {
        color: """ + COLORS['burgundy'] + """;
        font-size: 1.8rem;
        margin-bottom: 24px;
        font-family: '""" + FONTS['heading'] + """', serif;
        text-align: center;
    }

    .action-menu-container {
        margin: 32px 0;
    }

    .cities-grid {
        margin-top: 32px;
    }

    .discover-section,
    .region-section,
    .season-section,
    .compare-section,
    .analytics-header {
        background: white;
        padding: 32px;
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(108, 8, 32, 0.1);
        margin-bottom: 24px;
    }

    .region-header,
    .season-header,
    .favorites-header,
    .comparison-header {
        background: linear-gradient(135deg, """ + COLORS['misty_rose'] + """ 0%, #fff 100%);
        padding: 24px 32px;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(108, 8, 32, 0.08);
    }

    .region-header h3,
    .season-header h3,
    .favorites-header h3,
    .comparison-header h3 {
        color: """ + COLORS['burgundy'] + """;
        font-size: 1.8rem;
        margin: 0;
        font-family: '""" + FONTS['heading'] + """', serif;
    }

    /* Input field styling */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        border: 2px solid rgba(242, 174, 188, 0.3) !important;
        border-radius: 16px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }

    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: """ + COLORS['cherry_blossom_pink'] + """ !important;
        box-shadow: 0 0 0 3px rgba(242, 174, 188, 0.2) !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(108, 8, 32, 0.08) !important;
    }

    @media (max-width: 768px) {
        .action-menu-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .explore-title {
            font-size: 2rem;
        }
        
        .stat-card {
            padding: 20px 16px;
        }
        
        .stat-number {
            font-size: 2rem;
        }
    }
</style>
"""
