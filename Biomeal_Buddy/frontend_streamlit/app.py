import streamlit as st
import requests
import time

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Biomeal Buddy",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 Biomeal Buddy")
st.caption("AI-powered personalized nutrition & ordering")

# -------------------------------------------------
# INPUTS
# -------------------------------------------------
sleep_hours = st.slider("😴 Sleep Hours", 0, 12, 7)
steps = st.slider("👟 Steps Today", 0, 20000, 6000)
heart_rate = st.slider("❤️ Avg Heart Rate", 50, 120, 75)

diet = st.selectbox(
    "🍽️ Diet Preference",
    ["Normal", "Vegetarian", "Vegan", "Keto", "Paleo", "Diabetic", "High Protein"]
)

time_of_day = st.selectbox(
    "⏰ Time of Day",
    ["Morning", "Afternoon", "Evening", "Night"]
)

diet_key = diet.lower().replace(" ", "_")

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
for k in [
    "meal", "choice", "restaurants",
    "selected_restaurant", "cart",
    "order_confirmed", "why_meal"
]:
    if k not in st.session_state:
        st.session_state[k] = [] if k == "cart" else None

# -------------------------------------------------
# HEALTH METRICS
# -------------------------------------------------
calories_burned = int((steps * 0.04) + (sleep_hours * 15))
activity_level = "Low" if steps < 4000 else "Moderate" if steps < 9000 else "Active"
wellness_score = min(
    100,
    int((sleep_hours * 10) + (steps / 200) - abs(75 - heart_rate))
)

# -------------------------------------------------
# MEAL IMAGE MAP
# -------------------------------------------------
MEAL_IMAGES = {
    "paneer keto bowl": "https://images.unsplash.com/photo-1604908177225-6c4b4c94e5c5",
    "protein bowl": "https://images.unsplash.com/photo-1604908554027-7a1e7c3c41c5",
    "veg thali": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46",
    "paneer curry": "https://images.unsplash.com/photo-1601050690597-df0568f70950",
    "veg fried rice": "https://images.unsplash.com/photo-1603133872878-684f208fb84b",
    "grilled meat plate": "https://images.unsplash.com/photo-1544025162-d76694265947",
    "tofu stir fry": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6",
    "balanced meal plate": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
    "idli sambar": "assets/idli_sambar.jpg",
    "default": "assets/default_image.png",
}

def get_meal_image(meal_name: str):
    key = meal_name.lower().strip()
    return MEAL_IMAGES.get(key, MEAL_IMAGES["default"])

# -------------------------------------------------
# WHY THIS MEAL LOGIC (UNCHANGED)
# -------------------------------------------------
def generate_why_meal(meal):
    reasons = []
    if sleep_hours < 6:
        reasons.append("supports energy recovery due to low sleep")
    if steps > 8000:
        reasons.append("helps muscle recovery after high activity")
    if heart_rate > 85:
        reasons.append("is light and heart-friendly")
    if diet:
        reasons.append(f"matches your {diet.lower()} diet preference")
    reasons.append(f"is suitable for {time_of_day.lower()} time consumption")

    return f"🍽️ **{meal}** was recommended because it " + ", ".join(reasons) + "."

# -------------------------------------------------
# GET MEAL RECOMMENDATION
# -------------------------------------------------
if st.button("✨ Get Meal Recommendation"):
    with st.spinner("Analyzing your health profile..."):
        res = requests.post(
            "http://127.0.0.1:8000/recommend",
            json={
                "sleep_hours": sleep_hours,
                "steps": steps,
                "heart_rate": heart_rate,
                "diet": diet_key,
                "time_of_day": time_of_day.lower()
            }
        )
        st.session_state.meal = res.json()["meal"]
        st.session_state.why_meal = generate_why_meal(st.session_state.meal)
        st.session_state.choice = None
        st.session_state.restaurants = []
        st.session_state.selected_restaurant = None
        st.session_state.cart = []
        st.session_state.order_confirmed = False

# -------------------------------------------------
# MEAL DISPLAY
# -------------------------------------------------
if st.session_state.meal:
    st.success("✅ Recommended Meal for You")
    st.image(get_meal_image(st.session_state.meal), use_container_width=True)
    st.markdown(f"## 🍽️ {st.session_state.meal}")

    # ✅ WHY THIS MEAL (SAFE UI ADDITION)
    with st.expander("🤖 Why this meal?"):
        st.markdown(st.session_state.why_meal)

    st.session_state.choice = st.radio(
        "How would you like to eat?",
        ["🍳 Eat at Home", "🏪 Order from Restaurant"]
    )

# -------------------------------------------------
# RESTAURANTS
# -------------------------------------------------
if st.session_state.choice == "🏪 Order from Restaurant":
    if st.button("🔍 Find Restaurants"):
        with st.spinner("Finding restaurants near you..."):
            res = requests.post(
                "http://127.0.0.1:8000/restaurants",
                json={"diet": diet_key}
            )
            data = res.json()

            if not data:
                data = [
                    {"name": "Healthy Hub", "rating": 4.5, "distance": 2.0, "time": 20},
                    {"name": "Smart Nutrition Kitchen", "rating": 4.6, "distance": 2.8, "time": 24}
                ]

            st.session_state.restaurants = data

# -------------------------------------------------
# RESTAURANT LIST
# -------------------------------------------------
if st.session_state.restaurants:
    st.markdown("## 🍴 Available Restaurants")
    for r in st.session_state.restaurants:
        with st.container(border=True):
            st.markdown(f"### 🏪 {r['name']}")
            st.caption(f"⭐ {r['rating']} | 📍 {r['distance']} km | ⏱️ {r['time']} mins")
            if st.button("View Menu", key=r["name"]):
                st.session_state.selected_restaurant = r["name"]
                st.session_state.cart = []

# -------------------------------------------------
# MENU LOGIC
# -------------------------------------------------
DIET_EXTRAS = {
    "vegetarian": [("Paneer Curry", 180, 410, 24, 22)],
    "vegan": [("Tofu Stir Fry", 200, 360, 22, 30)],
    "keto": [("Keto Paneer Plate", 240, 480, 35, 10)],
    "paleo": [("Grilled Meat Plate", 280, 560, 45, 12)],
    "diabetic": [("Low GI Veg Meal", 210, 350, 18, 40)],
    "high_protein": [("Protein Bowl", 260, 540, 42, 28)],
    "normal": [("Balanced Meal Plate", 200, 480, 25, 60)]
}

if st.session_state.selected_restaurant:
    st.markdown(f"## 📋 Menu – {st.session_state.selected_restaurant}")

    with st.container(border=True):
        st.image(get_meal_image(st.session_state.meal), use_container_width=True)
        st.markdown(f"### ⭐ {st.session_state.meal}")
        if st.checkbox("Add recommended meal to cart"):
            st.session_state.cart.append(250)

    st.markdown("### 🍽️ Other Options")
    for name, price, cal, protein, carbs in DIET_EXTRAS.get(diet_key, []):
        with st.container(border=True):
            st.image(get_meal_image(name), use_container_width=True)
            st.markdown(f"**{name}**")
            st.caption(f"₹{price}")
            if st.checkbox(f"Add {name}", key=name):
                st.session_state.cart.append(price)

# -------------------------------------------------
# CART & ORDER
# -------------------------------------------------
if st.session_state.cart:
    st.success(f"🧾 Total Bill: ₹{sum(st.session_state.cart)}")
    if st.button("✅ Confirm Order"):
        st.session_state.order_confirmed = True

if st.session_state.order_confirmed:
    st.markdown("## 🚚 Order Tracking")

    status_steps = [
        ("🧾 Order Confirmed", 25),
        ("👨‍🍳 Preparing Food", 50),
        ("🚴 Out for Delivery", 75),
        ("📦 Delivered", 100),
    ]

    progress_bar = st.progress(0)
    status_placeholder = st.empty()

    for status, value in status_steps:
        status_placeholder.info(status)
        progress_bar.progress(value)
        time.sleep(1)

    st.success("📦 Delivered! Enjoy your meal 🍽️")
    st.balloons()


# -------------------------------------------------
# HEALTH DASHBOARD
# -------------------------------------------------
st.markdown("---")
st.markdown("## 📊 Your Health Dashboard")
c1, c2, c3 = st.columns(3)
c1.metric("🔥 Calories Burned", f"{calories_burned} kcal")
c2.metric("💪 Activity Level", activity_level)
c3.metric("🧠 Wellness Score", f"{wellness_score}/100")
st.progress(wellness_score / 100)

st.caption("Biomeal Buddy • All rights reserved @ 2025")



