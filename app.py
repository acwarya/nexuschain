import streamlit as st
import json
import time

# --- INITIALIZATION & CONFIGURATION ---
st.set_page_config(page_title="NexusChain: Agentic Supply Chain Broker", layout="wide")

# Mock Enterprise Databases
LEGACY_ERP_INVENTORY = {"part_id": "CHIP-992", "current_stock": 12, "min_required": 100}
SUPPLIER_DB = [
    {"name": "Alpha Components", "part_id": "CHIP-992", "price_per_unit": 4.50, "lead_time_days": 4},
    {"name": "Beta Electronics", "part_id": "CHIP-992", "price_per_unit": 6.50, "lead_time_days": 1},
    {"name": "Gamma Tech", "part_id": "CHIP-992", "price_per_unit": 3.80, "lead_time_days": 7}
]

# Initialize session state for tracking agent workflows across page refreshes
if "workflow_state" not in st.session_state:
    st.session_state.workflow_state = {
        "step": "IDLE",
        "logs": [],
        "selected_vendor": None,
        "po_draft": None,
        "history": []
    }

def log_agent_action(agent_name, message):
    log_entry = f"🤖 [{agent_name}]: {message}"
    st.session_state.workflow_state["logs"].append(log_entry)

# --- APP LAYOUT ---
st.title("🔗 NexusChain — Agentic Supply Chain Tracker")
st.caption("Track 1 Prototype: Deterministic Multi-Agent Workflow with Human-in-the-Loop Safeguards")
st.write("---")

# Top Banner: Current Inventory Shortage Alert
st.error(f"🚨 **Legacy ERP Alert:** `{LEGACY_ERP_INVENTORY['part_id']}` is critically low! Current Stock: **{LEGACY_ERP_INVENTORY['current_stock']} units** (Minimum Required: {LEGACY_ERP_INVENTORY['min_required']})")

# Layout Columns
col_left, col_middle, col_right = st.columns([1, 1.2, 1.3])

# --- LEFT COLUMN: CONTROLS & CONSTRAINTS ---
with col_left:
    st.header("1. Chaos Controls")
    st.write("Set the operational guardrails. If the agents violate these, the workflow will intentionally self-terminate.")
    
    max_budget = st.number_input("Max Allowed Budget ($)", min_value=100, max_value=1000, value=500, step=50)
    max_lead_time = st.slider("Max Allowed Lead Time (Days)", min_value=1, max_value=10, value=5)
    
    st.write("---")
    if st.button("🚀 Trigger Agent Workflow", type="primary", use_container_width=True):
        # Reset State
        st.session_state.workflow_state["step"] = "PROCESSING"
        st.session_state.workflow_state["logs"] = []
        st.session_state.workflow_state["selected_vendor"] = None
        st.session_state.workflow_state["po_draft"] = None
        
        # Step 1: Inventory Verification
        log_agent_action("Inventory Agent", "Interrogating legacy ERP systems...")
        time.sleep(0.8)
        shortage = LEGACY_ERP_INVENTORY["min_required"] - LEGACY_ERP_INVENTORY["current_stock"]
        log_agent_action("Inventory Agent", f"Confirmed deficiency of {shortage} units for part CHIP-992.")
        
        # Step 2: Sourcing Alternative Vendors
        log_agent_action("Sourcing Agent", "Scanning verified external supply lines...")
        time.sleep(1.0)
        
        # Filter vendors who meet the timeline criteria
        viable_vendors = [v for v in SUPPLIER_DB if v["lead_time_days"] <= max_lead_time]
        
        if not viable_vendors:
            log_agent_action("Sourcing Agent", "❌ CRITICAL FAILURE: No vendors can fulfill requirements within specified lead time constraint.")
            st.session_state.workflow_state["step"] = "ESCALATED"
        else:
            # Sourcing algorithm: pick the cheapest option that met the timeline constraint
            best_vendor = min(viable_vendors, key=lambda x: x["price_per_unit"])
            total_cost = shortage * best_vendor["price_per_unit"]
            
            log_agent_action("Sourcing Agent", f"Identified optimal match: {best_vendor['name']} (Lead time: {best_vendor['lead_time_days']} days, Unit cost: ${best_vendor['price_per_unit']:.2f})")
            
            # Step 3: Enforcing Financial Guardrails
            log_agent_action("Contract Agent", f"Evaluating total expenditure: ${total_cost:.2f} against maximum ceiling limit of ${max_budget:.2f}...")
            time.sleep(0.8)
            
            if total_cost > max_budget:
                log_agent_action("Contract Agent", f"❌ CONSTRAINT BREACH: Calculated cost (${total_cost:.2f}) exceeds authorized threshold.")
                st.session_state.workflow_state["step"] = "ESCALATED"
            else:
                log_agent_action("Contract Agent", "Cost structures compliant. Synthesizing data payloads into strict JSON schema.")
                st.session_state.workflow_state["selected_vendor"] = best_vendor
                st.session_state.workflow_state["po_draft"] = {
                    "transaction_id": "PO-2026-889X",
                    "target_erp_node": "SAP-NODE-PROD4",
                    "vendor": best_vendor["name"],
                    "part_id": best_vendor["part_id"],
                    "quantity": shortage,
                    "total_amount_usd": total_cost,
                    "delivery_window_days": best_vendor["lead_time_days"],
                    "status": "AWAITING_HUMAN_SIGN_OFF"
                }
                st.session_state.workflow_state["step"] = "GATEWAY"
        st.rerun()

# --- MIDDLE COLUMN: LIVE AGENT LOGGING LAYER ---
with col_middle:
    st.header("2. Agentic Trace Log")
    st.write("Watch the deterministic state execution window unfold below:")
    
    if not st.session_state.workflow_state["logs"]:
        st.info("System idle. Adjust parameters and click 'Trigger Agent Workflow' to begin testing.")
    else:
        for log in st.session_state.workflow_state["logs"]:
            if "❌" in log:
                st.error(log)
            elif "✅" in log or "Compliant" in log:
                st.success(log)
            else:
                st.code(log, language="text")

# --- RIGHT COLUMN: HUMAN INTERACTION GATEWAY ---
with col_right:
    st.header("3. Secure Gateway")
    
    current_step = st.session_state.workflow_state["step"]
    
    if current_step == "GATEWAY":
        st.warning("🚨 **Action Required:** An autonomous draft requires authorization before writing payload back to legacy databases.")
        st.json(st.session_state.workflow_state["po_draft"])
        
        col_approve, col_reject = st.columns(2)
        with col_approve:
            if st.button("👍 Confirm & Transmit", type="primary", use_container_width=True):
                st.session_state.workflow_state["step"] = "COMPLETE"
                st.rerun()
        with col_reject:
            if st.button("👎 Terminate Order", type="secondary", use_container_width=True):
                st.session_state.workflow_state["step"] = "REJECTED"
                st.rerun()
                
    elif current_step == "COMPLETE":
        st.balloons()
        st.success("🎉 **Success!** Purchase order processed and securely committed to legacy ERP data tables.")
        if st.button("Reset Simulation"):
            st.session_state.workflow_state["step"] = "IDLE"
            st.rerun()
            
    elif current_step == "REJECTED":
        st.error("❌ **Order Aborted:** The draft was terminated manually by the manager.")
        if st.button("Reset Simulation"):
            st.session_state.workflow_state["step"] = "IDLE"
            st.rerun()
            
    elif current_step == "ESCALATED":
        st.error("🚨 **System Lockout (Escalated to Leadership):** The automated system could not find a compliant pathway within your parameters. It chose to pause safely instead of hallucinating a broken decision.")
        if st.button("Reset Simulation"):
            st.session_state.workflow_state["step"] = "IDLE"
            st.rerun()
