"""
Main Streamlit application for Jira Ticketing Simulation System.
"""
import streamlit as st
from streamlit_option_menu import option_menu
from database import Database
from datetime import datetime

# Page config
st.set_page_config(
    page_title="CORE Engineer Training - Ticket System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def get_database():
    return Database()

db = get_database()

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Improve text area styling */
    .stTextArea textarea {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
    }

    /* Improve button styling */
    .stButton button {
        border-radius: 6px;
        font-weight: 500;
    }

    /* Improve expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 6px;
        font-weight: 500;
    }

    /* Chat container styling */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
        background-color: #fafafa;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"


def render_chat_message(full_name: str, role: str, message: str, timestamp: str):
    """Render a chat message with color-coded styling."""
    # Color scheme based on role
    if role == "Admin":
        bg_color = "#E3F2FD"  # Light blue for admin
        border_color = "#1976D2"  # Dark blue
        role_badge_color = "#1976D2"
    elif role == "RD":
        bg_color = "#E8F5E9"  # Light green for RD
        border_color = "#388E3C"  # Dark green
        role_badge_color = "#388E3C"
    else:  # Engineer
        bg_color = "#F3E5F5"  # Light purple for engineer
        border_color = "#7B1FA2"  # Dark purple
        role_badge_color = "#7B1FA2"

    # Format timestamp
    time_str = timestamp[:16] if len(timestamp) > 16 else timestamp

    # HTML for chat bubble
    chat_html = f"""
    <div style="
        margin-bottom: 15px;
        padding: 12px 16px;
        background-color: {bg_color};
        border-left: 4px solid {border_color};
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <div>
                <span style="
                    font-weight: bold;
                    color: #1a1a1a;
                    font-size: 14px;
                ">{full_name}</span>
                <span style="
                    margin-left: 8px;
                    padding: 2px 8px;
                    background-color: {role_badge_color};
                    color: white;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 600;
                ">{role}</span>
            </div>
            <span style="
                color: #666;
                font-size: 12px;
            ">{time_str}</span>
        </div>
        <div style="
            color: #2c2c2c;
            font-size: 14px;
            line-height: 1.5;
            white-space: pre-wrap;
        ">{message}</div>
    </div>
    """
    st.markdown(chat_html, unsafe_allow_html=True)


def login_page():
    """Display login page."""
    st.markdown("<h1 style='text-align: center;'>CORE Engineer Training Portal</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Ticket Management System</h3>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("Login")

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):
            user = db.authenticate_user(username, password)
            if user:
                st.session_state.user = user
                st.success(f"Welcome, {user['full_name']}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.markdown("---")
        st.info("**2 Login Types:**\n\n**Admin** (Controls Reporter & RD): admin / admin123\n\n**Engineer** (Trainee): engineer1 / eng123")


def logout():
    """Logout current user."""
    st.session_state.user = None
    st.session_state.current_page = "Dashboard"
    st.rerun()


def admin_dashboard():
    """Admin dashboard view."""
    col_title, col_refresh = st.columns([4, 1])

    with col_title:
        st.title("Admin Dashboard")

    with col_refresh:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    tickets = db.get_all_tickets()
    with col1:
        st.metric("Total Tickets", len(tickets))
    with col2:
        open_tickets = len([t for t in tickets if t['status'] in ['Open', 'Assigned to CORE']])
        st.metric("Active Tickets", open_tickets)
    with col3:
        escalated = len([t for t in tickets if t['status'] in ['Escalated to RD', 'Assigned to RD']])
        st.metric("Escalated to RD", escalated)
    with col4:
        resolved = len([t for t in tickets if t['status'] in ['Resolved', 'Closed']])
        st.metric("Resolved", resolved)

    st.markdown("---")

    # Recent tickets table
    st.subheader("Recent Tickets")

    if tickets:
        for ticket in tickets[:10]:
            with st.expander(f"**{ticket['ticket_number']}** - {ticket['title']} | Status: **{ticket['status']}**"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(f"**Description:** {ticket['description']}")
                    st.write(f"**Priority:** {ticket['priority']}")
                    st.write(f"**Created:** {ticket['created_at']}")

                with col2:
                    # Reporter
                    reporter = db.get_user_by_id(ticket['reporter_id']) if ticket.get('reporter_id') else None
                    if reporter:
                        st.write(f"**Reporter:** {reporter['full_name']}")
                    else:
                        st.write("**Reporter:** Unassigned")

                    # CORE Engineer
                    core_eng = db.get_user_by_id(ticket['core_engineer_id']) if ticket.get('core_engineer_id') else None
                    if core_eng:
                        st.write(f"**CORE Engineer:** {core_eng['full_name']}")
                    else:
                        st.write("**CORE Engineer:** Unassigned")

                    # Admin actions
                    if ticket['status'] == 'Escalated to RD':
                        if st.button(f"Back to CORE", key=f"reported_{ticket['id']}", use_container_width=True):
                            db.update_ticket_status(
                                ticket['id'],
                                'Assigned back to CORE',
                                st.session_state.user['id'],
                                "Admin sent back to CORE"
                            )
                            st.success("Sent back to CORE!")
                            st.rerun()
    else:
        st.info("No tickets yet. Create your first dispatch case!")


def admin_create_ticket():
    """Admin page to create new dispatch cases."""
    col_title, col_refresh = st.columns([4, 1])

    with col_title:
        st.title("Create Dispatch Case")

    with col_refresh:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    with st.form("create_ticket_form"):
        title = st.text_input("Ticket Title", placeholder="e.g., Network connectivity issue")

        description = st.text_area(
            "Description",
            placeholder="Describe the issue in detail...",
            height=100
        )

        scenario = st.text_area(
            "Training Scenario",
            placeholder="Provide the training scenario for the CORE engineer...",
            height=150,
            help="This is the scenario that engineers will work on for training purposes"
        )

        col1, col2 = st.columns(2)

        with col1:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])

        with col2:
            pass  # Spacing

        st.markdown("### 👥 Assignment")

        col1, col2 = st.columns(2)

        with col1:
            # Reporter assignment
            admins = db.get_all_admins()
            reporter_options = ["Unassigned"] + [f"{a['full_name']}" for a in admins]
            selected_reporter = st.selectbox("Reporter", reporter_options, help="Who reported this case")

        with col2:
            # CORE Engineer assignment
            engineers = db.get_all_engineers()
            engineer_options = ["Unassigned"] + [f"{e['full_name']}" for e in engineers]
            selected_engineer = st.selectbox("CORE Engineer", engineer_options, help="Assign to CORE Engineer for training")

        submitted = st.form_submit_button("Create Ticket", use_container_width=True)

        if submitted:
            if not title or not description or not scenario:
                st.error("Please fill in all required fields!")
            else:
                # Get IDs for assignments
                reporter_id = None
                if selected_reporter != "Unassigned":
                    reporter_index = reporter_options.index(selected_reporter) - 1
                    reporter_id = admins[reporter_index]['id']

                core_engineer_id = None
                if selected_engineer != "Unassigned":
                    engineer_index = engineer_options.index(selected_engineer) - 1
                    core_engineer_id = engineers[engineer_index]['id']

                ticket_number = db.create_ticket(
                    title=title,
                    description=description,
                    scenario=scenario,
                    priority=priority,
                    created_by=st.session_state.user['id'],
                    reporter_id=reporter_id,
                    core_engineer_id=core_engineer_id
                )

                st.success(f"Ticket {ticket_number} created successfully!")
                st.balloons()


def admin_manage_tickets():
    """Admin page to manage all tickets."""
    col_title, col_refresh = st.columns([4, 1])

    with col_title:
        st.title("Manage All Tickets")

    with col_refresh:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Open", "Assigned to CORE", "Escalated to RD", "Assigned to RD", "Assigned back to Reporter", "Assigned back to CORE", "Resolved", "Closed"]
        )

    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Critical"])

    tickets = db.get_all_tickets()

    # Apply filters
    if status_filter != "All":
        tickets = [t for t in tickets if t['status'] == status_filter]
    if priority_filter != "All":
        tickets = [t for t in tickets if t['priority'] == priority_filter]

    st.markdown(f"**Showing {len(tickets)} ticket(s)**")
    st.markdown("---")

    if tickets:
        for ticket in tickets:
            with st.expander(f"**{ticket['ticket_number']}** - {ticket['title']} | Priority: **{ticket['priority']}** | Status: **{ticket['status']}**"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**Description:** {ticket['description']}")
                    st.write(f"**Scenario:** {ticket['scenario']}")

                    # Show conversation in chat format
                    st.markdown("---")
                    st.markdown("### 💬 Conversation")

                    # Chat container
                    chat_container = st.container()
                    with chat_container:
                        replies = db.get_ticket_replies(ticket['id'])
                        if replies:
                            for reply in replies:
                                render_chat_message(
                                    full_name=reply['full_name'],
                                    role=reply.get('display_role', reply['role']),
                                    message=reply['message'],
                                    timestamp=reply['created_at']
                                )
                        else:
                            st.info("💬 No messages yet. Start the conversation below!")

                    # Admin reply section
                    st.markdown("---")
                    st.markdown("**📝 Add Your Reply:**")

                    # Add reply as dropdown for Admin too
                    admin_reply_as = st.selectbox(
                        "Reply as:",
                        ["Admin", "RD (Advanced Technical Guidance)"],
                        key=f"admin_reply_as_{ticket['id']}",
                        help="Choose Admin for normal responses, RD for advanced technical analysis"
                    )

                    admin_reply = st.text_area(
                        "Your message",
                        placeholder="Provide guidance, ask for clarification, or share updates...",
                        key=f"admin_reply_{ticket['id']}",
                        height=100
                    )
                    col_send, col_clear = st.columns([1, 4])
                    with col_send:
                        if st.button("📤 Send", key=f"admin_send_{ticket['id']}", use_container_width=True):
                            if admin_reply:
                                # Determine the role to save
                                admin_role_to_save = "RD" if "RD" in admin_reply_as else "Admin"
                                db.add_ticket_reply(ticket['id'], st.session_state.user['id'], admin_reply, reply_role=admin_role_to_save)
                                st.success(f"Reply sent as {admin_reply_as.split('(')[0].strip()}!")
                                st.rerun()
                            else:
                                st.error("Please enter a message!")

                with col2:
                    st.markdown("### 👥 People")

                    # Reporter
                    reporter = db.get_user_by_id(ticket['reporter_id']) if ticket.get('reporter_id') else None
                    if reporter:
                        st.write(f"**Reporter:** {reporter['full_name']}")
                    else:
                        st.write("**Reporter:** Unassigned")

                    # CORE Engineer
                    core_eng = db.get_user_by_id(ticket['core_engineer_id']) if ticket.get('core_engineer_id') else None
                    if core_eng:
                        st.write(f"**CORE Engineer:** {core_eng['full_name']}")
                    else:
                        st.write("**CORE Engineer:** Unassigned")

                    st.markdown("---")
                    st.write(f"**Created:** {ticket['created_at'][:16]}")
                    st.write(f"**Updated:** {ticket['updated_at'][:16]}")

                    st.info("💡 Admin can reply as 'RD' for technical guidance")

                    # Admin actions based on status
                    st.markdown("**Actions:**")

                    if ticket['status'] == 'Open':
                        engineers = db.get_all_engineers()
                        engineer_options = [f"{e['full_name']}" for e in engineers]
                        selected = st.selectbox(
                            "Assign to CORE:",
                            engineer_options,
                            key=f"assign_{ticket['id']}"
                        )
                        if st.button("Assign to CORE", key=f"assign_btn_{ticket['id']}", use_container_width=True):
                            engineer_index = engineer_options.index(selected)
                            db.update_ticket_status(
                                ticket['id'],
                                'Assigned to CORE',
                                st.session_state.user['id'],
                                f"Assigned to {selected}",
                                core_engineer_id=engineers[engineer_index]['id']
                            )
                            st.success("Assigned to CORE!")
                            st.rerun()

                    elif ticket['status'] == 'Escalated to RD':
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("↩️ Back to CORE", key=f"admin_backcore_{ticket['id']}", use_container_width=True):
                                db.update_ticket_status(
                                    ticket['id'],
                                    'Assigned back to CORE',
                                    st.session_state.user['id'],
                                    "Admin sent back to CORE"
                                )
                                st.success("Sent back to CORE!")
                                st.rerun()
                        with col_b:
                            if st.button("📮 Back to Reporter", key=f"admin_reporter_{ticket['id']}", use_container_width=True):
                                db.update_ticket_status(
                                    ticket['id'],
                                    'Assigned back to Reporter',
                                    st.session_state.user['id'],
                                    "Admin sent back to Reporter"
                                )
                                st.success("Sent back to Reporter!")
                                st.rerun()

                    elif ticket['status'] == 'Assigned to CORE':
                        if st.button("✅ Mark Resolved", key=f"resolve_{ticket['id']}", use_container_width=True):
                            db.update_ticket_status(
                                ticket['id'],
                                'Resolved',
                                st.session_state.user['id'],
                                "Admin marked as resolved"
                            )
                            st.success("Marked as resolved!")
                            st.rerun()

                # Show history
                with st.expander("View History"):
                    history = db.get_ticket_history(ticket['id'])
                    for h in history:
                        st.text(f"{h['created_at'][:16]} - {h['full_name']}: {h['action']}")
                        if h['comment']:
                            st.text(f"  Comment: {h['comment']}")
    else:
        st.info("No tickets match the selected filters.")


def engineer_dashboard():
    """Engineer dashboard view."""
    col_title, col_refresh = st.columns([4, 1])

    with col_title:
        st.title("My Assigned Tickets")

    with col_refresh:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    tickets = db.get_tickets_by_user(st.session_state.user['id'])

    # Statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Assigned", len(tickets))
    with col2:
        active = len([t for t in tickets if t['status'] == 'Assigned to CORE'])
        st.metric("Active", active)
    with col3:
        escalated = len([t for t in tickets if t['status'] == 'Escalated to SEG'])
        st.metric("Escalated", escalated)

    st.markdown("---")

    if tickets:
        for ticket in tickets:
            with st.expander(f"**{ticket['ticket_number']}** - {ticket['title']} | Priority: **{ticket['priority']}** | Status: **{ticket['status']}**"):
                st.write(f"**Description:** {ticket['description']}")
                st.write(f"**Training Scenario:** {ticket['scenario']}")
                st.write(f"**Priority:** {ticket['priority']}")
                st.write(f"**Status:** {ticket['status']}")

                st.markdown("---")

                # Show conversation in chat format
                st.markdown("### 💬 Conversation")

                # Chat container
                chat_container = st.container()
                with chat_container:
                    replies = db.get_ticket_replies(ticket['id'])
                    if replies:
                        for reply in replies:
                            render_chat_message(
                                full_name=reply['full_name'],
                                role=reply.get('display_role', reply['role']),
                                message=reply['message'],
                                timestamp=reply['created_at']
                            )
                    else:
                        st.info("💬 No messages yet. Start the conversation below!")

                # Reply form
                st.markdown("---")
                st.markdown("**📝 Add Your Reply:**")

                # Add reply as dropdown
                reply_as = st.selectbox(
                    "Reply as:",
                    ["Engineer", "RD (Advanced Technical Guidance)"],
                    key=f"reply_as_{ticket['id']}",
                    help="Choose Engineer for normal responses, RD for advanced technical analysis"
                )

                reply_message = st.text_area(
                    "Your message",
                    placeholder="Provide details, ask questions, or share your findings...",
                    key=f"reply_{ticket['id']}",
                    height=100
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("📤 Send Reply", key=f"send_{ticket['id']}", use_container_width=True):
                        if reply_message:
                            # Determine the role to save
                            role_to_save = "RD" if "RD" in reply_as else "Engineer"
                            db.add_ticket_reply(ticket['id'], st.session_state.user['id'], reply_message, reply_role=role_to_save)
                            st.success(f"Reply sent as {reply_as.split('(')[0].strip()}!")
                            st.rerun()
                        else:
                            st.error("Please enter a message!")

                with col2:
                    if ticket['status'] == 'Assigned to CORE':
                        if st.button("⬆️ Escalate to Admin/RD", key=f"escalate_{ticket['id']}", use_container_width=True):
                            db.update_ticket_status(
                                ticket['id'],
                                'Escalated to RD',
                                st.session_state.user['id'],
                                "Escalated by engineer - needs Admin/RD assistance"
                            )
                            st.success("Escalated to Admin/RD!")
                            st.rerun()

                with col3:
                    if ticket['status'] == 'Assigned back to Reporter':
                        if st.button("↩️ Back to CORE", key=f"backtocore_{ticket['id']}", use_container_width=True):
                            db.update_ticket_status(
                                ticket['id'],
                                'Assigned to CORE',
                                st.session_state.user['id'],
                                "Reassigned back to CORE"
                            )
                            st.success("Assigned back to CORE!")
                            st.rerun()
    else:
        st.info("You have no assigned tickets yet. Check back later!")


def main():
    """Main application."""
    # Show login page if not authenticated
    if st.session_state.user is None:
        login_page()
        return

    # Sidebar
    with st.sidebar:
        st.title("CORE Training Portal")
        st.markdown(f"**Logged in as:** {st.session_state.user['full_name']}")
        st.markdown(f"**Role:** {st.session_state.user['role']}")
        st.markdown("---")

        # Navigation based on role
        if st.session_state.user['role'] == 'Admin':
            selected = option_menu(
                "Navigation",
                ["Dashboard", "Create Dispatch Case", "Manage Tickets"],
                icons=['speedometer2', 'plus-circle', 'list-task'],
                menu_icon="cast",
                default_index=0
            )
        else:  # Engineer or RD (both use same dashboard)
            selected = option_menu(
                "Navigation",
                ["My Tickets"],
                icons=['ticket-perforated'],
                menu_icon="cast",
                default_index=0
            )

        st.session_state.current_page = selected

        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            logout()

    # Main content area
    if st.session_state.user['role'] == 'Admin':
        if st.session_state.current_page == "Dashboard":
            admin_dashboard()
        elif st.session_state.current_page == "Create Dispatch Case":
            admin_create_ticket()
        elif st.session_state.current_page == "Manage Tickets":
            admin_manage_tickets()
    else:  # Engineer or RD - both use same dashboard
        engineer_dashboard()


if __name__ == "__main__":
    main()
