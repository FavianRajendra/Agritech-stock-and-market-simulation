import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Adding custom CSS for fonts and emojis
st.markdown("""
    <style>
        body {
            font-family: 'Poppins', sans-serif;
        }
        h1, h2, h3 {
            color: #FF69B4;
        }
        .stButton>button {
            background-color: #FF69B4;
            color: white;
            font-size: 20px;
        }
        .stButton>button:hover {
            background-color: #FF1493;
        }
        .emoji {
            font-size: 30px;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Modul Negosiasi
class IoTDeviceSupplier:
    def __init__(self, name, initial_price, initial_stock):
        self.name = name
        self.initial_price = initial_price
        self.stock = initial_stock

    def negotiate_price(self, farmer_budget, messages):
        current_price = self.initial_price
        negotiation_rounds = []
        
        # Allow negotiations to continue as long as there's stock and the price is higher than the farmer's budget
        while self.stock > 0 and current_price > farmer_budget:
            messages.append(f"{self.name}: Offering price {current_price} 💸.")
            current_price -= 50  # Example price drop per round
            negotiation_rounds.append(current_price)
            messages.append(f"Farmer: Countering with budget {farmer_budget} 💰.")
        
        if self.stock > 0:  # After the negotiation, if stock is still available
            messages.append(f"{self.name}: Final agreed price {current_price} ✨.")
            self.stock -= 1  # Decrease stock after negotiation
        else:
            messages.append(f"{self.name}: No more stock available for negotiation 😢.")
        
        return current_price, negotiation_rounds

# Modul Koordinasi
class FertilizerDistributor:
    def __init__(self, name, initial_stock):
        self.name = name
        self.stock = initial_stock

    def deliver_fertilizer(self, messages):
        message = f"{self.name} is delivering fertilizer based on land needs 🌾."
        messages.append(message)
        self.stock -= 1  # Decrease stock after delivery
        return message

# Backend Simulation
class AgriTechSimulation:
    def __init__(self, farmer_budget, market_demand, seller_initial_price, buyer_initial_budget, supplier_stock, distributor_stock):
        self.farmer_budget = buyer_initial_budget
        self.market_demand = market_demand
        self.iot_suppliers = [
            IoTDeviceSupplier("IoT Supplier A", seller_initial_price, supplier_stock),
            IoTDeviceSupplier("IoT Supplier B", seller_initial_price - 50, supplier_stock)
        ]
        self.fertilizer_distributors = [
            FertilizerDistributor("Distributor 1", distributor_stock),
            FertilizerDistributor("Distributor 2", distributor_stock)
        ]
        self.messages = []

    def run_simulation(self):
        results = {}

        # Negotiation Module
        results["negotiation"] = {
            supplier.name: supplier.negotiate_price(self.farmer_budget, self.messages) for supplier in self.iot_suppliers
        }

        # Coordination Module
        results["coordination"] = [
            distributor.deliver_fertilizer(self.messages) for distributor in self.fertilizer_distributors
        ]

        return results, self.messages

# Streamlit App
st.title("🌱 AgriTech Solutions: Market Simulation 🌻")

# User Input for Simulation
st.sidebar.header("Market Simulation Inputs 🛒")
farmers_budget = st.sidebar.slider("Select Farmer's Budget 💸", 500, 1200, 850)
market_demand = st.sidebar.selectbox("Select Market Demand 📊", ["low", "high"], index=1)
seller_initial_price = st.sidebar.slider("Initial Seller Price 💰", 500, 1200, 1000)
buyer_initial_budget = st.sidebar.slider("Initial Buyer Budget 💸", 500, 1200, 850)

# Additional Inputs for Stock
supplier_stock = st.sidebar.slider("Remaining Stock of IoT Suppliers 📦", 1, 20, 10)
distributor_stock = st.sidebar.slider("Remaining Stock of Fertilizer Distributors 📦", 1, 20, 5)

# Run Simulation
if st.sidebar.button("Run Simulation 🚀"):
    simulation = AgriTechSimulation(farmers_budget, market_demand, seller_initial_price, buyer_initial_budget, supplier_stock, distributor_stock)
    results, messages = simulation.run_simulation()

    # Display Results
    st.header("Simulation Results 🎉")

    # Negotiation Results
    with st.expander("1. Negotiation Results 🏷️"):
        negotiation_data = {}
        max_rounds = 0

        for supplier, data in results["negotiation"].items():
            negotiation_data[supplier] = data[1]
            max_rounds = max(max_rounds, len(data[1]))

        for supplier in negotiation_data:
            negotiation_data[supplier] += [None] * (max_rounds - len(negotiation_data[supplier]))

        negotiation_df = pd.DataFrame(negotiation_data)
        negotiation_df.index = [f"Round {i+1}" for i in range(max_rounds)]
        st.line_chart(negotiation_df)

    # Coordination Results
    with st.expander("2. Coordination Results 🤝"):
        st.write("\n".join(results["coordination"]))

    # Communication and Negotiation Logs
    with st.expander("3. Communication and Negotiation Logs 📜"):
        st.text("\n".join(messages))

    # Stock Display
    with st.expander("4. Remaining Stock of Suppliers and Distributors 📉"):
        stock_info = {
            supplier.name: f"Stock: {supplier.stock}" for supplier in simulation.iot_suppliers
        }
        stock_info.update({
            distributor.name: f"Stock: {distributor.stock}" for distributor in simulation.fertilizer_distributors
        })
        st.write(stock_info)
