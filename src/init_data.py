"""
Initialize database with sample users and tickets for testing.
"""
from database import Database
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def initialize_sample_data():
    """Create sample users and tickets for the training system."""
    # Only delete SQLite database if using SQLite backend
    storage_backend = os.getenv("STORAGE_BACKEND", "sqlite")
    if storage_backend == "sqlite":
        db_path = "data/tickets.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Old SQLite database removed, creating new schema...")
    else:
        print(f"Using {storage_backend} backend - skipping file deletion...")

    db = Database()

    print("Initializing sample data...")

    # Create Admin users (controls both Reporter and RD roles)
    print("Creating admin users...")
    db.create_user("admin", "admin123", "System Administrator", "Admin")
    db.create_user("admin2", "admin123", "SEG Administrator", "Admin")

    # Create Engineer users (trainees)
    print("Creating engineer users...")
    db.create_user("engineer1", "eng123", "John Smith", "Engineer")
    db.create_user("engineer2", "eng123", "Sarah Johnson", "Engineer")
    db.create_user("engineer3", "eng123", "Mike Chen", "Engineer")
    db.create_user("engineer4", "eng123", "Emily Davis", "Engineer")

    # Get user IDs
    admin = db.authenticate_user("admin", "admin123")
    admin2 = db.authenticate_user("admin2", "admin123")
    engineer1 = db.authenticate_user("engineer1", "eng123")
    engineer2 = db.authenticate_user("engineer2", "eng123")

    # Create sample tickets
    print("Creating sample dispatch cases...")

    ticket1 = db.create_ticket(
        title="Customer Unable to Access Email",
        description="Customer reports they cannot log into their email account. Account appears active in system.",
        scenario="""
        **Training Scenario:**

        Customer: ABC Corporation
        Issue: Email access problems

        **Symptoms:**
        - User cannot log into Outlook
        - Password reset attempted, still fails
        - Account shows active in admin panel

        **Your Task:**
        1. Check account status
        2. Verify password reset functionality
        3. Check for any account locks or restrictions
        4. Verify MFA settings
        5. Provide resolution steps

        **Expected Actions:**
        - Investigate account logs
        - Check authentication service
        - Communicate findings clearly
        - Escalate if infrastructure issue suspected
        """,
        priority="P1",
        product="Maximum Security",
        created_by=admin['id'],
        reporter_id=admin2['id'],
        core_engineer_id=engineer1['id']
    )

    ticket2 = db.create_ticket(
        title="Network Connectivity Issues in Building 5",
        description="Multiple users in Building 5 reporting intermittent network connectivity.",
        scenario="""
        **Training Scenario:**

        Location: Building 5, Floor 3
        Affected Users: 15+

        **Symptoms:**
        - Intermittent connection drops
        - Slow network speeds
        - Some users completely offline

        **Your Task:**
        1. Determine scope of the issue
        2. Check network infrastructure
        3. Review recent changes
        4. Test connectivity from different points
        5. Provide timeline for resolution

        **Expected Actions:**
        - Systematic troubleshooting
        - Document findings
        - Clear communication with users
        - Escalate if hardware failure detected
        """,
        priority="P0",
        product="VPN Proxy One Pro",
        created_by=admin['id'],
        reporter_id=admin['id'],
        core_engineer_id=engineer2['id']
    )

    ticket3 = db.create_ticket(
        title="Software Installation Request - AutoCAD",
        description="Engineering department needs AutoCAD 2024 installed on 10 workstations.",
        scenario="""
        **Training Scenario:**

        Request Type: Software Installation
        Software: AutoCAD 2024
        Number of Licenses: 10

        **Requirements:**
        - Verify license availability
        - Check system requirements
        - Schedule installation time
        - Coordinate with users
        - Provide training resources

        **Your Task:**
        1. Verify we have available licenses
        2. Confirm workstation specs meet requirements
        3. Create installation plan
        4. Communicate timeline to requestor
        5. Document installation process

        **Expected Actions:**
        - Professional communication
        - Clear timeline
        - Risk assessment
        - Coordination with stakeholders
        """,
        priority="P2",
        product="Internet Security",
        created_by=admin['id'],
        reporter_id=admin2['id']
        # No engineer assigned initially
    )

    ticket4 = db.create_ticket(
        title="VPN Connection Failures for Remote Workers",
        description="Several remote employees unable to connect to company VPN.",
        scenario="""
        **Training Scenario:**

        Affected: Remote workers (5+ reports)
        Service: Company VPN

        **Symptoms:**
        - Connection timeout errors
        - Authentication failures
        - Some users connect but no network access

        **Your Task:**
        1. Identify common factors among affected users
        2. Check VPN server status
        3. Review VPN logs
        4. Test VPN from different locations
        5. Provide workarounds if available

        **Expected Actions:**
        - Systematic diagnosis
        - Check for patterns
        - Communicate status updates
        - Consider escalation if server-side issue
        """,
        priority="P1",
        product="VPN Proxy One Pro",
        created_by=admin['id'],
        reporter_id=admin['id']
        # No engineer assigned initially
    )

    # Add some sample replies to ticket 1
    db.add_ticket_reply(
        ticket_id=1,
        user_id=engineer1['id'],
        message="I've started investigating this issue. Checking the user's account status now."
    )

    db.add_ticket_reply(
        ticket_id=1,
        user_id=engineer1['id'],
        message="Account appears active. I've verified the password reset was successful. Checking MFA configuration next."
    )

    print("\nSample data initialized successfully!")
    print("\n" + "="*60)
    print("LOGIN CREDENTIALS - 2 ROLE SYSTEM:")
    print("="*60)
    print("\n** Admin Accounts (Controls Reporter & RD roles) **")
    print("  Username: admin  | Password: admin123 (System Administrator)")
    print("  Username: admin2 | Password: admin123 (SEG Administrator)")
    print("\n** CORE Engineer Accounts (Trainees) **")
    print("  Username: engineer1 | Password: eng123 (John Smith)")
    print("  Username: engineer2 | Password: eng123 (Sarah Johnson)")
    print("  Username: engineer3 | Password: eng123 (Mike Chen)")
    print("  Username: engineer4 | Password: eng123 (Emily Davis)")
    print("\n" + "="*60)
    print("NOTE: Admins can reply as 'Admin' or 'RD'")
    print("      Engineers can reply as 'Engineer' or 'RD'")
    print("="*60)


if __name__ == "__main__":
    initialize_sample_data()
