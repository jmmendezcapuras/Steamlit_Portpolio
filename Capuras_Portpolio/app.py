import io
import os
import random
from datetime import date, datetime

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(
    page_title="John Miklos Capuras | Portfolio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Autobiography and portfolio built with Streamlit for CSIT 349."},
)


import base64

def img_b64(im: Image.Image) -> str:
    buf = io.BytesIO(); im.convert("RGB").save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@500;800&family=JetBrains+Mono:wght@400;700&display=swap');
.stApp{background:radial-gradient(circle at 10% 0%,#3a1a66 0%,#0E0818 50%),#0E0818;}
h1,h2,h3{font-family:'Unbounded',sans-serif!important;font-weight:800!important;letter-spacing:-.01em}
.mono{font-family:'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;font-size:.75rem;color:#B57BFF}
.topbar{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;letter-spacing:.08em;font-size:.72rem;color:#9a8bb8}
.topbar b{color:#EFE8FF}
.hero-name{font-family:'Unbounded',sans-serif;font-weight:800;font-size:clamp(2.6rem,6vw,5rem);line-height:1.02;margin:.3rem 0 .6rem;
  background:linear-gradient(90deg,#EFE8FF 0%,#C79BFF 55%,#8E5BC9 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.typed{font-size:1.25rem;font-weight:600;margin-bottom:.6rem}
.typed span{color:#C79BFF;border-right:3px solid #FF5C8A;padding-right:4px;animation:blink 1s step-end infinite}
@keyframes blink{50%{border-color:transparent}}
.portrait{position:relative;border-radius:50% 50% 24px 24px / 38% 38% 24px 24px;overflow:hidden;border:3px solid #9D5CFF;box-shadow:0 0 0 8px #9D5CFF22,0 0 60px #9D5CFF66}
.portrait img{width:100%;display:block}
.portrait .cap{position:absolute;left:50%;transform:translateX(-50%);bottom:12px;background:#0E0818cc;padding:4px 12px;border-radius:999px;font-family:'JetBrains Mono',monospace;font-size:.65rem;letter-spacing:.1em;white-space:nowrap}
.badge{position:absolute;top:-10px;left:-10px;z-index:2;background:#1A1030;border:2px solid #FF5C8A;border-radius:18px;padding:6px 12px;font-size:1.6rem;box-shadow:0 4px 18px #0008;animation:float 3s ease-in-out infinite}
@keyframes float{50%{transform:translateY(-6px)}}
.card{border:1px solid #3a2766;background:linear-gradient(160deg,#1A1030,#120A22);border-radius:20px;padding:18px 20px}
.card .k{font-family:'JetBrains Mono',monospace;letter-spacing:.1em;font-size:.65rem;color:#9a8bb8;text-transform:uppercase}
.card .v{font-family:'Unbounded';font-weight:800;font-size:1.9rem;line-height:1.3;color:#C79BFF}
.card .s{font-family:'JetBrains Mono',monospace;font-size:.68rem;color:#9a8bb8}
.chip{display:inline-block;border:1px solid #9D5CFF88;color:#D9BEFF;border-radius:8px;padding:2px 10px;margin:2px 4px 2px 0;font-size:.75rem;font-family:'JetBrains Mono',monospace}
[data-testid="stSidebar"]{background:#0b0614;border-right:1px solid #2a1a4a}
[data-testid="stButtonGroup"]{background:#1A1030;border:1px solid #3a2766;border-radius:14px;padding:6px}
div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:20px}
.stButton>button,.stDownloadButton>button,.stLinkButton>a{border-radius:999px}
</style>
"""
CALM = "<style>*{animation:none!important;transition:none!important}</style>"
st.markdown(CSS, unsafe_allow_html=True)

PROFILE = {
    "name": "John Miklos M. Capuras",
    "section": "CSIT 349 · GO1",
    "program": "Bachelor of Science in Information Technology (BSIT)",
    "year": "4th Year",
    "tagline": "Giving up is never the answer. I make mistakes, learn from them, and keep building.",
    "github": "https://github.com/jmmendezcapuras",
    "email": "capurasjohnmiklos@gmail.com",
    "bio": (
        "I am John Miklos M. Capuras, a person who believes that giving up is never the answer. "
        "I love to explore, discover new things, and learn from every experience. I know that making "
        "mistakes is part of life, but I believe every mistake is an opportunity to grow, improve, and "
        "become a better version of myself. Even when things get difficult, I always find a way to "
        "overcome challenges and keep moving forward. I may not know everything, and I may fail "
        "sometimes, but I will never stop trying, learning, and believing in myself. My goal is not "
        "to be perfect but to become better every day."
    ),
}

MILESTONES = {
    "Starting BSIT": "Chose Information Technology and wrote my first real programs. "
                     "This is where I learned that debugging is most of programming.",
    "First group web app": "Joined a team building an e-commerce site in Django. I owned the "
                           "Inventory and Warehouse modules while a groupmate handled Products and Categories.",
    "Going mobile": "Built an Android Kotlin module using Retrofit/OkHttp and Material Design, "
                    "my first time connecting a phone app to a real backend.",
    "Capstone: StudyMate": "Working with a team on StudyMate: Spring Boot API, React web client "
                           "and an Android app, with Auth, Subject, Session and Admin features.",
    "Writing features from scratch": "Preparing for a practical skills test where I write the "
                                     "Auth, Subject, Session and Admin features on my own, which pushed me to "
                                     "really understand patterns like JWT registration flows.",
}

SKILLS = pd.DataFrame(
    {
        "Skill": ["Python", "Java", "JavaScript", "React", "Spring Boot", "Django",
                  "Kotlin (Android)", "SQL / PostgreSQL", "Git & GitHub"],
        "Category": ["Language", "Language", "Language", "Frontend", "Backend", "Backend",
                     "Mobile", "Database", "Tools"],
        "Level": [75, 80, 70, 65, 70, 70, 60, 70, 75],
        "Years": [2, 3, 2, 1, 1, 1, 1, 2, 2],
    }
)

WEEKLY_HOURS = pd.DataFrame(
    {
        "Week": [f"W{i}" for i in range(1, 11)],
        "Coding": [6, 8, 7, 10, 12, 9, 14, 16, 13, 18],
        "Studying": [5, 6, 6, 7, 6, 8, 9, 8, 10, 9],
    }
).set_index("Week")

PROJECTS = [
    {
        "title": "StudyMate (Capstone)",
        "emoji": "📚",
        "role": "Full-stack developer: Auth, Subject, Session and Admin features, plus the Android module",
        "tools": ["Spring Boot", "React", "Kotlin", "PostgreSQL", "Retrofit", "JWT"],
        "outcome": "Working web + mobile study-session app with role-based admin tools and JWT login.",
        "link": "https://github.com/",
        "status": "In progress",
    },
    {
        "title": "E-Commerce Market App",
        "emoji": "🛒",
        "role": "Module owner: Inventory and Warehouse (group project)",
        "tools": ["Django", "Python", "SQLite", "HTML/CSS"],
        "outcome": "Delivered inventory tracking and warehouse management that plug into the Products/Categories modules.",
        "link": "https://github.com/",
        "status": "Completed",
    },
    {
        "title": "System Integration Study Guide",
        "emoji": "🧩",
        "role": "Solo author and developer",
        "tools": ["HTML", "CSS", "JavaScript"],
        "outcome": "Interactive exam reviewer covering integration types, levels, middleware and challenges, with answer keys.",
        "link": "https://github.com/",
        "status": "Completed",
    },
    {
        "title": "Iponko (IT332 Team Project)",
        "emoji": "💰",
        "role": "Team member: literature review (RRL sources 16-20) and software proposal",
        "tools": ["Research", "RRL", "Software Proposal"],
        "outcome": "Proposed a lightweight record-keeping system for informal savings pools (paluwagan) with two-sided payment confirmation and automatic dispute flagging.",
        "link": "https://github.com/",
        "status": "In progress",
    },
]

INTERESTS = ["Web development", "Mobile apps", "Backend design", "System integration",
             "Teamwork", "Learning by building"]

def make_avatar(initials: str, size: int = 400, accent: str = "#7C9CFF") -> Image.Image:
    img = Image.new("RGB", (size, size), accent)
    d = ImageDraw.Draw(img)
    for i in range(0, size, 40):
        d.line([(0, i), (i, 0)], fill="#FFFFFF22", width=6)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size // 3)
        small = ImageFont.truetype("DejaVuSans.ttf", size // 18)
    except OSError:
        font = small = ImageFont.load_default()
    w = d.textlength(initials, font=font)
    d.text(((size - w) / 2, size / 2 - size / 6), initials, fill="white", font=font)
    label = "stand-in photo"
    lw = d.textlength(label, font=small)
    d.text(((size - lw) / 2, size - size / 9), label, fill="white", font=small)
    return img


@st.cache_data
def build_resume_text(name: str, program: str, bio: str) -> str:
    lines = [f"# {name}", f"{program}", "", "## About", bio, "", "## Skills"]
    lines += [f"- {r.Skill}: {r.Level}/100" for r in SKILLS.itertuples()]
    lines += ["", "## Projects"]
    lines += [f"- {p['title']}: {p['role']} ({', '.join(p['tools'])})" for p in PROJECTS]
    return "\n".join(lines)


st.session_state.setdefault("likes", {p["title"]: 0 for p in PROJECTS})
st.session_state.setdefault("messages", [])
st.session_state.setdefault("visits", 0)
st.session_state.visits += 1

NAV = ["Prologue", "1 · Story", "2 · Skills", "3 · Projects", "Final · Contact"]

def go_to(page: str):
    st.session_state["nav"] = page

st.session_state.setdefault("visited", {"Prologue"})

with st.sidebar:
    uploaded = st.file_uploader("Swap the photo", type=["png", "jpg", "jpeg"],
                                help="Or place your picture at assets/photo.jpg")
    accent = "#B57BFF"
    standin = False
    if uploaded:
        photo = Image.open(uploaded)
    elif os.path.exists("assets/photo.jpg"):
        photo = Image.open("assets/photo.jpg")
    else:
        photo = make_avatar("JC", accent=accent)
        standin = True
    sc1, sc2 = st.columns([1, 2.4])
    sc1.image(photo, width="stretch")
    sc2.markdown(f"### {PROFILE['name'].upper()}")
    sc2.markdown(f"<span class='mono' style='color:#8b8b99'>{PROFILE['section']}</span>", unsafe_allow_html=True)
    st.divider()
    st.markdown("**Rounds cleared**")
    prog_slot = st.empty()
    st.divider()
    st.markdown("**Comfort**")
    calm = st.toggle("Calm mode", help="Turns off animations")
    compact = st.toggle("Compact project cards")
    show_chart = st.checkbox("Show skills chart", value=True)
    chart_kind = st.radio("Skills chart", ["Bar", "Area (hours)"], horizontal=True)
    st.divider()
    st.download_button("⬇️ Download résumé", build_resume_text(PROFILE["name"], PROFILE["program"], PROFILE["bio"]),
                       "John_Miklos_Capuras_resume.md", "text/markdown", width="stretch")
    st.download_button("📄 Download my story (.md)", "# My story\n\n" + "\n\n".join(f"## {k}\n{v}" for k, v in MILESTONES.items()),
                       "my_story.md", "text/markdown", width="stretch")
    st.link_button("‹› GitHub", PROFILE["github"], width="stretch")
    st.link_button("✉️ Email me", f"mailto:{PROFILE['email']}", width="stretch")
    st.caption(f"Page views this session: {st.session_state.visits}")

if calm:
    st.markdown(CALM, unsafe_allow_html=True)

st.markdown(f"<div class='topbar'><span>● <b>{PROFILE['name']}</b></span>"
            f"<span>CSIT 349 · Applied AI · <b>{PROFILE['section']}</b></span></div>", unsafe_allow_html=True)
st.session_state.setdefault("nav", "Prologue")
nav = st.segmented_control("Navigate", NAV, label_visibility="collapsed", key="nav") or "Prologue"
st.session_state.visited.add(nav)
done = len(st.session_state.visited)
prog_slot.progress(done / len(NAV), text=f"{done} of {len(NAV)} explored")

if nav == "Prologue":
    st.markdown("<div class='mono'>👻 Autobiography &amp; Portfolio</div>", unsafe_allow_html=True)
    R, L = st.columns([1, 1.7], gap="large")
    with R:
        st.markdown(f"<div style='position:relative'><div class='portrait'><img src='data:image/jpeg;base64,{img_b64(photo)}'>"
                    f"<div class='cap'>{PROFILE['name']}</div></div></div>", unsafe_allow_html=True)
        if standin:
            st.caption("Stand-in photo: replace via sidebar or assets/photo.jpg")
    with L:
        st.markdown("<div class='hero-name'>John Miklos<br>Capuras</div>", unsafe_allow_html=True)
        st.markdown("<div class='typed'>I build <span>full-stack apps.</span></div>", unsafe_allow_html=True)
        st.write(f"**{PROFILE['program']}, {PROFILE['year']}**")
        st.write(PROFILE["bio"])
        b1, b2, b3 = st.columns(3)
        b1.button("Read my story", type="primary", width="stretch", on_click=go_to, args=("1 · Story",))
        b2.button("See projects", width="stretch", on_click=go_to, args=("3 · Projects",))
        b3.link_button("‹› GitHub", PROFILE["github"], width="stretch")

    st.write("")
    tools = {t for p in PROJECTS for t in p["tools"]}
    stats = [("Featured projects", len(PROJECTS), "capstone + 3 more"),
             ("Technologies", len(tools), "Spring · Django · React"),
             ("Top skill", SKILLS.loc[SKILLS.Level.idxmax(), "Skill"], "my strongest"),
             ("Avg. skill", f"{SKILLS.Level.mean():.0f}/100", "self-rated")]
    for col, (k, v, sub) in zip(st.columns(4), stats):
        col.markdown(f"<div class='card'><div class='k'>{k}</div><div class='v'>{v}</div><div class='s'>{sub}</div></div>", unsafe_allow_html=True)

    st.write("")
    a, b = st.columns([1.3, 1], gap="large")
    with a:
        st.markdown("<div class='mono'>♥ Why this site looks like this</div>", unsafe_allow_html=True)
        st.write("TODO: one or two sentences in your own words about your design inspiration.")
        picked = st.pills("Interests", INTERESTS, selection_mode="multi", default=INTERESTS[:3], key="interest_pills")
    with b:
        st.subheader("Fast facts")
        st.dataframe(pd.DataFrame({"": ["Name", "Program", "Year", "Section", "Focus"],
                                   " ": [PROFILE["name"], PROFILE["program"], PROFILE["year"], PROFILE["section"], "Full-stack"]}),
                     hide_index=True, width="stretch")

elif nav == "1 · Story":
    st.markdown("<div class='mono'>👻 Round 1</div>", unsafe_allow_html=True)
    st.header("My story")
    length = st.radio("How much detail?", ["Short", "Full"], horizontal=True)
    if length == "Short":
        st.info("I'm a BSIT student who went from small class exercises to building full-stack web and mobile apps with a team. I learn by shipping things and fixing what breaks.")
    else:
        st.markdown("I started in Information Technology curious about how apps work behind the screen. Each semester added a layer: databases, web frameworks, then mobile and system integration. Group projects taught me as much about communication as code, because owning a module means other people depend on your work.")
    keys = list(MILESTONES)
    picked = st.select_slider("Slide through my journey", options=keys, value=keys[0])
    idx = keys.index(picked)
    st.progress((idx + 1) / len(keys), text=f"Milestone {idx + 1} of {len(keys)}")
    with st.container(border=True):
        st.markdown(f"### {picked}")
        st.write(MILESTONES[picked])
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**🎓 Education**"); st.write(f"{PROFILE['program']}, {PROFILE['year']}")
    with c2, st.container(border=True):
        st.markdown("**💡 Currently**"); st.write("Building my capstone, StudyMate, and sharpening backend fundamentals.")
    with st.expander("🎯 What I want to do next"):
        st.write("Grow into a backend-leaning full-stack developer and ship something people outside my class use.")
    with st.expander("🎨 Interests outside code"):
        st.write("TODO: add a few hobbies in your own words.")

elif nav == "2 · Skills":
    st.markdown("<div class='mono'>👻 Round 2</div>", unsafe_allow_html=True)
    st.header("Skills")
    f1, f2 = st.columns([2, 1])
    cats = f1.multiselect("Filter by category", sorted(SKILLS.Category.unique()), default=sorted(SKILLS.Category.unique()))
    min_level = f2.slider("Minimum level", 0, 100, 0, step=5)
    view = SKILLS[SKILLS.Category.isin(cats) & (SKILLS.Level >= min_level)]
    t_col, c_col = st.columns([3, 2], gap="large")
    with t_col:
        st.dataframe(view, hide_index=True, width="stretch", column_config={
            "Level": st.column_config.ProgressColumn("Level", min_value=0, max_value=100, format="%d"),
            "Years": st.column_config.NumberColumn("Years", format="%d yr")})
        st.caption("Levels are my own self-ratings, out of 100.")
    with c_col:
        if not show_chart:
            st.info("Chart hidden. Toggle it in the sidebar.")
        elif chart_kind == "Bar":
            st.bar_chart(view.set_index("Skill")["Level"], color=accent, horizontal=True)
        else:
            st.area_chart(WEEKLY_HOURS, color=[accent, "#FF5C8A"])
            st.caption("Weekly hours coding vs. studying.")
    with st.expander("Static table"):
        st.table(view[["Skill", "Category", "Level"]].reset_index(drop=True))

elif nav == "3 · Projects":
    st.markdown("<div class='mono'>👻 Round 3</div>", unsafe_allow_html=True)
    st.header("Projects")
    all_tools = sorted({t for p in PROJECTS for t in p["tools"]})
    tool_filter = st.multiselect("Filter by tool", all_tools, placeholder="Show all projects")
    status_filter = st.segmented_control("Status", ["All", "In progress", "Completed"], default="All")
    shown = [p for p in PROJECTS if (not tool_filter or set(tool_filter) & set(p["tools"]))
             and (status_filter in (None, "All") or p["status"] == status_filter)]
    if not shown:
        st.warning("No projects match those filters.")
    grid = st.columns(2)
    for i, p in enumerate(shown):
        with grid[i % 2], st.container(border=True):
            st.markdown(f"### {p['emoji']} {p['title']}")
            st.badge(p["status"], color="green" if p["status"] == "Completed" else "orange")
            if not compact:
                st.markdown(f"**Role:** {p['role']}")
                st.markdown("".join(f"<span class='chip'>{t}</span>" for t in p["tools"]), unsafe_allow_html=True)
                st.markdown(f"**Outcome:** {p['outcome']}")
            b1, b2 = st.columns(2)
            if b1.button(f"👍 {st.session_state.likes[p['title']]}", key=f"like_{p['title']}"):
                st.session_state.likes[p["title"]] += 1; st.rerun()
            b2.link_button("Repo", p["link"])
            with st.popover("Details"):
                st.write(p["role"]); st.write(p["outcome"])
    st.subheader("Project effort")
    st.bar_chart(pd.DataFrame({"Project": [p["title"] for p in PROJECTS], "Hours": [120, 60, 25, 30]}).set_index("Project"), color=accent)
    st.caption("Estimated hours per project (replace with your own numbers).")

else:
    st.markdown("<div class='mono'>👻 Final round</div>", unsafe_allow_html=True)
    st.header("Contact & feedback")
    form_col, info_col = st.columns([3, 2], gap="large")
    with form_col:
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Your name")
            email = st.text_input("Email")
            topic = st.selectbox("Topic", ["Feedback on this site", "Project collaboration", "Just saying hi"])
            when = st.date_input("Preferred reply date", min_value=date.today())
            rating = st.feedback("stars")
            message = st.text_area("Message", height=140, max_chars=500)
            agree = st.checkbox("I'm okay with John replying by email")
            sent = st.form_submit_button("Send message", type="primary")
        if sent:
            if not (name.strip() and message.strip() and agree):
                st.error("Please add your name, a message, and tick the checkbox.")
            else:
                with st.spinner("Sending..."):
                    pass
                st.session_state.messages.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "name": name,
                    "email": email, "topic": topic, "rating": (rating + 1) if rating is not None else None, "message": message})
                st.success(f"Thanks, {name}! Your message was received.")
                st.toast("Message sent 🎉"); st.balloons()
    with info_col:
        with st.container(border=True):
            st.markdown("**Find me**")
            st.write(f"📧 {PROFILE['email']}"); st.write(f"🏷️ {PROFILE['section']}")
        if st.session_state.messages:
            st.subheader("Messages this session")
            msgs = pd.DataFrame(st.session_state.messages)
            st.dataframe(msgs[["time", "name", "topic", "rating"]], hide_index=True, width="stretch")
            st.download_button("Download messages (CSV)", msgs.to_csv(index=False), "messages.csv", "text/csv")

st.divider()
st.caption(f"© {date.today().year} {PROFILE['name']} · {PROFILE['section']} · Built with Streamlit")
