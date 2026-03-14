"""
Database models and helper functions for the Jira Ticketing Simulation System.
Supports both SQLite (local development) and Azure Cosmos DB (production).
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib


def get_database():
    """
    Factory function to get the appropriate database backend.
    Returns SQLite for local development or Cosmos DB for production.
    """
    backend = os.getenv("STORAGE_BACKEND", "sqlite").lower()

    if backend == "cosmosdb":
        try:
            from cosmos_db_handler import CosmosDBHandler
            print("Using Cosmos DB backend")
            return CosmosDBHandler()
        except ImportError as e:
            print(f"Warning: Could not import Cosmos DB handler: {e}")
            print("Falling back to SQLite")
            return DatabaseSQLite()
        except Exception as e:
            print(f"Warning: Could not initialize Cosmos DB: {e}")
            print("Falling back to SQLite")
            return DatabaseSQLite()
    else:
        print("Using SQLite backend")
        return DatabaseSQLite()


# Alias for backward compatibility
Database = get_database


class DatabaseSQLite:
    """Database handler for the ticketing system."""

    def __init__(self, db_path: str = "data/tickets.db"):
        """Initialize database connection."""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('Admin', 'Engineer', 'RD')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tickets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_number TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                scenario TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN (
                    'Open',
                    'Assigned to CORE',
                    'Escalated to RD',
                    'Assigned to RD',
                    'Assigned back to Reporter',
                    'Assigned back to CORE',
                    'Resolved',
                    'Closed'
                )),
                priority TEXT NOT NULL CHECK(priority IN ('P0', 'P1', 'P2', 'P3', 'P4')),
                reporter_id INTEGER,
                core_engineer_id INTEGER,
                rd_assignee_id INTEGER,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reporter_id) REFERENCES users(id),
                FOREIGN KEY (core_engineer_id) REFERENCES users(id),
                FOREIGN KEY (rd_assignee_id) REFERENCES users(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)

        # Ticket history/audit trail
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticket_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                old_status TEXT,
                new_status TEXT,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Ticket replies/comments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticket_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                reply_role TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.commit()
        conn.close()

        # Run migrations
        self.run_migrations()

    def run_migrations(self):
        """Run database migrations to add new columns."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Check if product column exists
        cursor.execute("PRAGMA table_info(tickets)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add product column if it doesn't exist
        if 'product' not in columns:
            cursor.execute("ALTER TABLE tickets ADD COLUMN product TEXT DEFAULT 'Not Specified'")

        # Add fundamental_solution column if it doesn't exist
        if 'fundamental_solution' not in columns:
            cursor.execute("ALTER TABLE tickets ADD COLUMN fundamental_solution TEXT DEFAULT 'FS:None'")

        # Add resolution_summary column if it doesn't exist
        if 'resolution_summary' not in columns:
            cursor.execute("ALTER TABLE tickets ADD COLUMN resolution_summary TEXT")

        # Add fs_details column if it doesn't exist (for storing FS-specific information)
        if 'fs_details' not in columns:
            cursor.execute("ALTER TABLE tickets ADD COLUMN fs_details TEXT")

        conn.commit()
        conn.close()

    def hash_password(self, password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str, full_name: str, role: str) -> bool:
        """Create a new user."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                (username, password_hash, full_name, role)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data."""
        conn = self.get_connection()
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            return dict(user)
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return dict(user)
        return None

    def get_all_engineers(self) -> List[Dict]:
        """Get all engineers."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role = 'Engineer' ORDER BY full_name")
        engineers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return engineers

    def get_all_rd(self) -> List[Dict]:
        """Get all RD users."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role = 'RD' ORDER BY full_name")
        rd_users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rd_users

    def get_all_admins(self) -> List[Dict]:
        """Get all admin users."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role = 'Admin' ORDER BY full_name")
        admins = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return admins

    def create_ticket(self, title: str, description: str, scenario: str,
                     priority: str, created_by: int, product: str = "Not Specified",
                     fundamental_solution: str = "FS:None", reporter_id: Optional[int] = None,
                     core_engineer_id: Optional[int] = None, rd_assignee_id: Optional[int] = None) -> str:
        """Create a new ticket and return ticket number."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Generate ticket number
        cursor.execute("SELECT COUNT(*) as count FROM tickets")
        count = cursor.fetchone()['count']
        ticket_number = f"CPDT-{count + 1:04d}"

        # Determine initial status
        if core_engineer_id:
            status = "Assigned to CORE"
        elif rd_assignee_id:
            status = "Assigned to RD"
        else:
            status = "Open"

        cursor.execute("""
            INSERT INTO tickets (ticket_number, title, description, scenario, status, priority,
                               product, fundamental_solution, reporter_id, core_engineer_id,
                               rd_assignee_id, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_number, title, description, scenario, status, priority,
              product, fundamental_solution, reporter_id, core_engineer_id, rd_assignee_id, created_by))

        ticket_id = cursor.lastrowid

        # Add to history
        cursor.execute("""
            INSERT INTO ticket_history (ticket_id, user_id, action, new_status)
            VALUES (?, ?, ?, ?)
        """, (ticket_id, created_by, "Ticket created", status))

        conn.commit()
        conn.close()

        return ticket_number

    def get_ticket_by_number(self, ticket_number: str) -> Optional[Dict]:
        """Get ticket by ticket number."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE ticket_number = ?", (ticket_number,))
        ticket = cursor.fetchone()
        conn.close()

        if ticket:
            return dict(ticket)
        return None

    def get_all_tickets(self) -> List[Dict]:
        """Get all tickets."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets ORDER BY created_at DESC")
        tickets = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return tickets

    def get_ticket_by_id(self, ticket_id: int) -> Dict:
        """Get a specific ticket by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_tickets_by_user(self, user_id: int) -> List[Dict]:
        """Get tickets assigned to a specific user (as CORE engineer or RD)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM tickets
               WHERE core_engineer_id = ? OR rd_assignee_id = ?
               ORDER BY created_at DESC""",
            (user_id, user_id)
        )
        tickets = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return tickets

    def get_tickets_by_reporter(self, user_id: int) -> List[Dict]:
        """Get tickets where user is the reporter."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tickets WHERE reporter_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        tickets = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return tickets

    def update_ticket_assignment(self, ticket_id: int, reporter_id: Optional[int] = None,
                                core_engineer_id: Optional[int] = None, rd_assignee_id: Optional[int] = None,
                                user_id: Optional[int] = None, comment: Optional[str] = None):
        """Update ticket assignments."""
        conn = self.get_connection()
        cursor = conn.cursor()

        updates = []
        values = []

        if reporter_id is not None:
            updates.append("reporter_id = ?")
            values.append(reporter_id)
        if core_engineer_id is not None:
            updates.append("core_engineer_id = ?")
            values.append(core_engineer_id)
        if rd_assignee_id is not None:
            updates.append("rd_assignee_id = ?")
            values.append(rd_assignee_id)

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(ticket_id)

            query = f"UPDATE tickets SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)

            if user_id:
                cursor.execute("""
                    INSERT INTO ticket_history (ticket_id, user_id, action, comment)
                    VALUES (?, ?, ?, ?)
                """, (ticket_id, user_id, "Assignment updated", comment))

        conn.commit()
        conn.close()

    def update_ticket_status(self, ticket_id: int, new_status: str, user_id: int,
                            comment: Optional[str] = None, reporter_id: Optional[int] = None,
                            core_engineer_id: Optional[int] = None, rd_assignee_id: Optional[int] = None):
        """Update ticket status and log to history."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get current status
        cursor.execute("SELECT status FROM tickets WHERE id = ?", (ticket_id,))
        result = cursor.fetchone()
        old_status = result['status'] if result else None

        # Build update query
        updates = ["status = ?", "updated_at = CURRENT_TIMESTAMP"]
        values = [new_status]

        if reporter_id is not None:
            updates.append("reporter_id = ?")
            values.append(reporter_id)
        if core_engineer_id is not None:
            updates.append("core_engineer_id = ?")
            values.append(core_engineer_id)
        if rd_assignee_id is not None:
            updates.append("rd_assignee_id = ?")
            values.append(rd_assignee_id)

        values.append(ticket_id)

        # Update ticket
        query = f"UPDATE tickets SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)

        # Add to history
        cursor.execute("""
            INSERT INTO ticket_history (ticket_id, user_id, action, old_status, new_status, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket_id, user_id, "Status changed", old_status, new_status, comment))

        conn.commit()
        conn.close()

    def resolve_ticket_with_summary(self, ticket_id: int, user_id: int, resolution_summary: str,
                                   fundamental_solution: str = "FS:None", fs_details: Optional[str] = None):
        """Resolve a ticket with summary and FS information."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get current status
        cursor.execute("SELECT status FROM tickets WHERE id = ?", (ticket_id,))
        result = cursor.fetchone()
        old_status = result['status'] if result else None

        # Update ticket
        cursor.execute("""
            UPDATE tickets
            SET status = 'Resolved',
                resolution_summary = ?,
                fundamental_solution = ?,
                fs_details = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (resolution_summary, fundamental_solution, fs_details, ticket_id))

        # Add to history
        cursor.execute("""
            INSERT INTO ticket_history (ticket_id, user_id, action, old_status, new_status, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket_id, user_id, "Ticket resolved", old_status, "Resolved", resolution_summary))

        conn.commit()
        conn.close()

    def retract_case(self, ticket_id: int, user_id: int, comment: str):
        """Retract a case - return it to 'Assigned to CORE' status."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get current status
        cursor.execute("SELECT status FROM tickets WHERE id = ?", (ticket_id,))
        result = cursor.fetchone()
        old_status = result['status'] if result else None

        # Update to Assigned to CORE
        cursor.execute("""
            UPDATE tickets
            SET status = 'Assigned to CORE',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (ticket_id,))

        # Add to history
        cursor.execute("""
            INSERT INTO ticket_history (ticket_id, user_id, action, old_status, new_status, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket_id, user_id, "Case retracted", old_status, "Assigned to CORE", comment))

        conn.commit()
        conn.close()

    def add_ticket_reply(self, ticket_id: int, user_id: int, message: str, reply_role: Optional[str] = None):
        """Add a reply/comment to a ticket."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ticket_replies (ticket_id, user_id, message, reply_role)
            VALUES (?, ?, ?, ?)
        """, (ticket_id, user_id, message, reply_role))

        # Update ticket timestamp
        cursor.execute("""
            UPDATE tickets SET updated_at = CURRENT_TIMESTAMP WHERE id = ?
        """, (ticket_id,))

        conn.commit()
        conn.close()

    def get_ticket_replies(self, ticket_id: int) -> List[Dict]:
        """Get all replies for a ticket."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tr.*, u.full_name, u.role,
                   COALESCE(tr.reply_role, u.role) as display_role
            FROM ticket_replies tr
            JOIN users u ON tr.user_id = u.id
            WHERE tr.ticket_id = ?
            ORDER BY tr.created_at ASC
        """, (ticket_id,))
        replies = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return replies

    def get_ticket_history(self, ticket_id: int) -> List[Dict]:
        """Get ticket history/audit trail."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT th.*, u.full_name
            FROM ticket_history th
            JOIN users u ON th.user_id = u.id
            WHERE th.ticket_id = ?
            ORDER BY th.created_at ASC
        """, (ticket_id,))
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return history
