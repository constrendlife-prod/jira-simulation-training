"""
Main Streamlit application for Jira Ticketing Simulation System.
"""
import streamlit as st
from streamlit_option_menu import option_menu
from database import Database
from datetime import datetime
from constants import PRIORITIES, PRODUCTS, FUNDAMENTAL_SOLUTIONS, PRIORITY_COLORS, FS_DETAILS_PROMPTS

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
if 'viewing_ticket_id' not in st.session_state:
    st.session_state.viewing_ticket_id = None


def render_ticket_card(ticket, show_actions=False):
    """Render a ticket as a card."""
    # Status colors
    status_colors = {
        "Open": "#2196F3",
        "Assigned to CORE": "#9C27B0",
        "Escalated to RD": "#FF9800",
        "Assigned back to Reporter": "#FFC107",
        "Assigned back to CORE": "#9C27B0",
        "Resolved": "#4CAF50",
        "Closed": "#757575"
    }

    priority_color = PRIORITY_COLORS.get(ticket['priority'], "#757575")
    status_color = status_colors.get(ticket['status'], "#757575")
    product = ticket.get('product', 'Not Specified')

    with st.container():
        st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            height: 100%;
        ">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #1976D2; font-size: 16px;">{ticket['ticket_number']}</h4>
                <span style="
                    background-color: {priority_color};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 600;
                ">{ticket['priority']}</span>
            </div>
            <h5 style="margin: 0 0 8px 0; color: #333; font-size: 14px;">{ticket['title']}</h5>
            <p style="margin: 0 0 8px 0; color: #666; font-size: 13px; line-height: 1.4;">
                {ticket['description'][:100]}{'...' if len(ticket['description']) > 100 else ''}
            </p>
            <div style="margin-bottom: 12px;">
                <span style="
                    background-color: #E3F2FD;
                    color: #1976D2;
                    padding: 2px 8px;
                    border-radius: 8px;
                    font-size: 11px;
                    font-weight: 500;
                ">📦 {product}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                <span style="
                    background-color: {status_color};
                    color: white;
                    padding: 4px 10px;
                    border-radius: 10px;
                    font-weight: 500;
                ">{ticket['status']}</span>
                <span style="color: #999;">{ticket['created_at'][:10]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Details", key=f"view_{ticket['id']}", use_container_width=True):
            st.session_state.viewing_ticket_id = ticket['id']
            st.rerun()


def render_chat_message(full_name: str, role: str, message: str, timestamp: str):
    """Render a chat message with color-coded styling."""
    # Color scheme based on role
    if role == "Reporter":
        bg_color = "#FFF3E0"  # Light orange for reporter
        border_color = "#F57C00"  # Dark orange
        role_badge_color = "#F57C00"
    elif role == "RD":
        bg_color = "#E8F5E9"  # Light green for RD
        border_color = "#388E3C"  # Dark green
        role_badge_color = "#388E3C"
    elif role == "Admin":
        bg_color = "#E3F2FD"  # Light blue for admin
        border_color = "#1976D2"  # Dark blue
        role_badge_color = "#1976D2"
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


def view_ticket_admin_full(ticket_id):
    """Full page view of a ticket for admin."""
    ticket = db.get_ticket_by_id(ticket_id)
    if not ticket:
        st.error("Ticket not found!")
        if st.button("← Back to Tickets"):
            st.session_state.viewing_ticket_id = None
            st.rerun()
        return

    # Back button
    col_back, col_space = st.columns([1, 4])
    with col_back:
        if st.button("← Back to Tickets", use_container_width=True):
            st.session_state.viewing_ticket_id = None
            st.rerun()

    st.title(f"{ticket['ticket_number']} - {ticket['title']}")

    # Priority, Status, and Product badges
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown(f"**Priority:** `{ticket['priority']}`")
        st.markdown(f"**Status:** `{ticket['status']}`")
    with col2:
        product = ticket.get('product', 'Not Specified')
        st.markdown(f"**Product:** `{product}`")

    st.markdown("---")

    # Main content in two columns
    col_left, col_right = st.columns([3, 1])

    with col_left:
        st.subheader("📋 Details")
        st.write(f"**Description:** {ticket['description']}")
        st.write(f"**Scenario:** {ticket['scenario']}")

        # Show conversation
        st.markdown("---")
        st.markdown("### 💬 Conversation")

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

        admin_reply_as = st.selectbox(
            "Reply as:",
            ["Reporter", "RD"],
            key=f"admin_reply_as_{ticket['id']}",
            help="Reply as Reporter (case creator) or RD (advanced technical support)"
        )

        admin_reply = st.text_area(
            "Your message",
            placeholder="Provide guidance, ask for clarification, or share updates...",
            key=f"admin_reply_{ticket['id']}",
            height=100
        )

        if st.button("📤 Send Reply", key=f"admin_send_{ticket['id']}", use_container_width=True):
            if admin_reply:
                db.add_ticket_reply(ticket['id'], st.session_state.user['id'], admin_reply, reply_role=admin_reply_as)
                st.success(f"Reply sent as {admin_reply_as}!")
                st.rerun()
            else:
                st.error("Please enter a message!")

    with col_right:
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

        st.markdown("---")
        st.markdown("### ⚙️ Actions")

        # Always show assignment option for Admin
        if ticket['status'] not in ['Resolved', 'Closed']:
            st.markdown("**Assign/Reassign CORE Engineer:**")
            engineers = db.get_all_engineers()
            engineer_options = [f"{e['full_name']}" for e in engineers]

            # Get current engineer index if assigned
            current_index = 0
            if ticket.get('core_engineer_id'):
                core_eng = db.get_user_by_id(ticket['core_engineer_id'])
                if core_eng:
                    try:
                        current_index = engineer_options.index(core_eng['full_name'])
                    except ValueError:
                        current_index = 0

            selected = st.selectbox(
                "Select CORE Engineer:",
                engineer_options,
                index=current_index,
                key=f"assign_{ticket['id']}"
            )
            if st.button("✅ Assign/Reassign", key=f"assign_btn_{ticket['id']}", use_container_width=True):
                engineer_index = engineer_options.index(selected)
                new_status = 'Assigned to CORE' if ticket['status'] == 'Open' else ticket['status']
                db.update_ticket_status(
                    ticket['id'],
                    new_status,
                    st.session_state.user['id'],
                    f"Assigned to {selected}",
                    core_engineer_id=engineers[engineer_index]['id']
                )
                st.success(f"Assigned to {selected}!")
                st.rerun()

            st.markdown("---")

        # Status-specific actions
        if ticket['status'] == 'Escalated to RD':
            if st.button("↩️ Back to CORE", key=f"admin_backcore_{ticket['id']}", use_container_width=True):
                db.update_ticket_status(
                    ticket['id'],
                    'Assigned back to CORE',
                    st.session_state.user['id'],
                    "Admin sent back to CORE"
                )
                st.success("Sent back to CORE!")
                st.rerun()

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

        # History section
        st.markdown("---")
        with st.expander("📜 View History"):
            history = db.get_ticket_history(ticket['id'])
            for h in history:
                st.text(f"{h['created_at'][:16]} - {h['full_name']}: {h['action']}")
                if h['comment']:
                    st.text(f"  Comment: {h['comment']}")


def view_ticket_engineer_full(ticket_id):
    """Full page view of a ticket for engineer."""
    ticket = db.get_ticket_by_id(ticket_id)
    if not ticket:
        st.error("Ticket not found!")
        if st.button("← Back to My Tickets"):
            st.session_state.viewing_ticket_id = None
            st.rerun()
        return

    # Back button
    col_back, col_space = st.columns([1, 4])
    with col_back:
        if st.button("← Back to My Tickets", use_container_width=True):
            st.session_state.viewing_ticket_id = None
            st.rerun()

    st.title(f"{ticket['ticket_number']} - {ticket['title']}")

    # Priority, Status, and Product badges
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown(f"**Priority:** `{ticket['priority']}`")
        st.markdown(f"**Status:** `{ticket['status']}`")
    with col2:
        product = ticket.get('product', 'Not Specified')
        st.markdown(f"**Product:** `{product}`")

    st.markdown("---")

    # Details
    st.subheader("📋 Details")
    st.write(f"**Description:** {ticket['description']}")
    st.write(f"**Training Scenario:** {ticket['scenario']}")

    # Show conversation
    st.markdown("---")
    st.markdown("### 💬 Conversation")

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
    st.markdown("**📝 Add Your Reply (as CORE Engineer):**")

    reply_message = st.text_area(
        "Your message",
        placeholder="Provide details, ask questions, or share your findings...",
        key=f"reply_{ticket['id']}",
        height=100
    )

    # Action buttons - Row 1
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📤 Send Reply", key=f"send_{ticket['id']}", use_container_width=True):
            if reply_message:
                db.add_ticket_reply(ticket['id'], st.session_state.user['id'], reply_message, reply_role="Engineer")
                st.success("Reply sent!")
                st.rerun()
            else:
                st.error("Please enter a message!")

    with col2:
        if ticket['status'] == 'Assigned to CORE':
            if st.button("⬆️ Escalate to RD", key=f"escalate_{ticket['id']}", use_container_width=True):
                db.update_ticket_status(
                    ticket['id'],
                    'Escalated to RD',
                    st.session_state.user['id'],
                    "Escalated by CORE Engineer - needs RD/SEG assistance"
                )
                st.success("Escalated to RD/SEG!")
                st.rerun()

    with col3:
        if ticket['status'] == 'Assigned to CORE':
            if st.button("📮 To Reporter", key=f"assign_reporter_{ticket['id']}", use_container_width=True):
                db.update_ticket_status(
                    ticket['id'],
                    'Assigned back to Reporter',
                    st.session_state.user['id'],
                    "CORE Engineer assigned back to Reporter"
                )
                st.success("Assigned to Reporter!")
                st.rerun()
        elif ticket['status'] == 'Assigned back to Reporter':
            if st.button("↩️ Back to CORE", key=f"backtocore_{ticket['id']}", use_container_width=True):
                db.update_ticket_status(
                    ticket['id'],
                    'Assigned to CORE',
                    st.session_state.user['id'],
                    "Reassigned back to CORE"
                )
                st.success("Assigned back to CORE!")
                st.rerun()

    with col4:
        # Retract Case button
        if ticket['status'] in ['Escalated to RD', 'Assigned back to Reporter']:
            if st.button("🔙 Retract Case", key=f"retract_{ticket['id']}", use_container_width=True):
                db.retract_case(
                    ticket['id'],
                    st.session_state.user['id'],
                    f"CORE Engineer retracted case from {ticket['status']}"
                )
                st.success("Case retracted! Returned to CORE.")
                st.rerun()

    # Row 2 - Resolve button
    st.markdown("---")
    if ticket['status'] == 'Assigned to CORE':
        if st.button("✅ Resolve Case with Summary", key=f"resolve_modal_{ticket['id']}", use_container_width=True, type="primary"):
            st.session_state[f"show_resolve_modal_{ticket['id']}"] = True
            st.rerun()

    # Resolution Modal
    if st.session_state.get(f"show_resolve_modal_{ticket['id']}", False):
        st.markdown("### 📝 Resolution Summary")
        st.info("Please provide a summary of how this case was resolved")

        with st.form(key=f"resolve_form_{ticket['id']}"):
            resolution_summary = st.text_area(
                "Resolution Summary",
                placeholder="Describe how the issue was resolved...",
                height=150,
                help="Provide a detailed summary of the resolution"
            )

            fs_option = st.selectbox(
                "Fundamental Solution",
                list(FUNDAMENTAL_SOLUTIONS.keys()),
                format_func=lambda x: f"{x} - {FUNDAMENTAL_SOLUTIONS[x]}",
                help="Select the fundamental solution type"
            )

            # Conditional FS details fields
            fs_details_text = ""
            if fs_option in FS_DETAILS_PROMPTS:
                st.markdown(f"**{fs_option} Details:**")
                fs_fields = []
                for field in FS_DETAILS_PROMPTS[fs_option]['fields']:
                    value = st.text_input(field, key=f"fs_{fs_option}_{field}_{ticket['id']}")
                    fs_fields.append(f"{field}: {value}")
                fs_details_text = "\n".join(fs_fields)

            col_submit, col_cancel = st.columns(2)
            with col_submit:
                submit_resolve = st.form_submit_button("✅ Confirm Resolution", use_container_width=True)
            with col_cancel:
                cancel_resolve = st.form_submit_button("❌ Cancel", use_container_width=True)

            if submit_resolve:
                if not resolution_summary:
                    st.error("Please provide a resolution summary!")
                else:
                    db.resolve_ticket_with_summary(
                        ticket['id'],
                        st.session_state.user['id'],
                        resolution_summary,
                        fs_option,
                        fs_details_text if fs_details_text else None
                    )
                    st.session_state[f"show_resolve_modal_{ticket['id']}"] = False
                    st.success("Case resolved successfully!")
                    st.rerun()

            if cancel_resolve:
                st.session_state[f"show_resolve_modal_{ticket['id']}"] = False
                st.rerun()


def login_page():
    """Display login page."""
    st.markdown("<h1 style='text-align: center;'>CORE Engineer Training Portal</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Ticket Management System</h3>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("Quick Login (Testing Mode)")
        st.info("Click a button below to login instantly")

        st.markdown("---")

        # Admin login button
        if st.button("🔐 Login as Admin", use_container_width=True, type="primary"):
            user = db.authenticate_user("admin", "admin123")
            if user:
                st.session_state.user = user
                st.success(f"Welcome, {user['full_name']}!")
                st.rerun()

        st.markdown("")  # Spacer

        # Engineer login button
        if st.button("👨‍💻 Login as Engineer", use_container_width=True):
            user = db.authenticate_user("engineer1", "eng123")
            if user:
                st.session_state.user = user
                st.success(f"Welcome, {user['full_name']}!")
                st.rerun()

        st.markdown("---")
        st.caption("**Admin:** Controls Reporter & RD roles")
        st.caption("**Engineer:** CORE Engineer trainee (John Smith)")


def logout():
    """Logout current user."""
    st.session_state.user = None
    st.session_state.current_page = "Dashboard"
    st.rerun()


def admin_dashboard():
    """Admin dashboard view."""
    # Check if viewing a specific ticket
    if st.session_state.viewing_ticket_id:
        view_ticket_admin_full(st.session_state.viewing_ticket_id)
        return

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

    # Recent tickets in card layout
    st.subheader("Recent Tickets")

    if tickets:
        recent_tickets = tickets[:12]  # Show up to 12 tickets (4 rows of 3)

        # Display in 3-column grid
        for i in range(0, len(recent_tickets), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(recent_tickets):
                    ticket = recent_tickets[i + j]
                    with cols[j]:
                        render_ticket_card(ticket)
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
            # Priority dropdown with descriptions
            priority_options = list(PRIORITIES.keys())
            priority_labels = [f"{p} - {PRIORITIES[p]}" for p in priority_options]
            selected_priority_index = st.selectbox(
                "Priority",
                range(len(priority_options)),
                format_func=lambda x: priority_labels[x],
                index=2,  # Default to P2
                help="Select priority level for this case"
            )
            priority = priority_options[selected_priority_index]

        with col2:
            # Product dropdown
            product = st.selectbox(
                "Product",
                PRODUCTS,
                help="Select the Trend Micro product related to this case"
            )

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
                    product=product,
                    created_by=st.session_state.user['id'],
                    reporter_id=reporter_id,
                    core_engineer_id=core_engineer_id
                )

                st.success(f"Ticket {ticket_number} created successfully!")
                st.balloons()


def admin_manage_tickets():
    """Admin page to manage all tickets."""
    # Check if viewing a specific ticket
    if st.session_state.viewing_ticket_id:
        view_ticket_admin_full(st.session_state.viewing_ticket_id)
        return

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
        priority_filter = st.selectbox("Filter by Priority", ["All", "P0", "P1", "P2", "P3", "P4"])

    with col3:
        product_filter = st.selectbox("Filter by Product", ["All"] + PRODUCTS)

    tickets = db.get_all_tickets()

    # Apply filters
    if status_filter != "All":
        tickets = [t for t in tickets if t['status'] == status_filter]
    if priority_filter != "All":
        tickets = [t for t in tickets if t['priority'] == priority_filter]
    if product_filter != "All":
        tickets = [t for t in tickets if t.get('product', 'Not Specified') == product_filter]

    st.markdown(f"**Showing {len(tickets)} ticket(s)**")
    st.markdown("---")

    if tickets:
        # Display tickets in 3-column card layout
        for i in range(0, len(tickets), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(tickets):
                    ticket = tickets[i + j]
                    with cols[j]:
                        render_ticket_card(ticket)
    else:
        st.info("No tickets match the selected filters.")


def engineer_dashboard():
    """Engineer dashboard view."""
    # Check if viewing a specific ticket
    if st.session_state.viewing_ticket_id:
        view_ticket_engineer_full(st.session_state.viewing_ticket_id)
        return

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
    st.subheader("My Tickets")

    if tickets:
        # Display tickets in 3-column card layout
        for i in range(0, len(tickets), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(tickets):
                    ticket = tickets[i + j]
                    with cols[j]:
                        render_ticket_card(ticket)
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
