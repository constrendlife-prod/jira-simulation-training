"""
Azure Cosmos DB handler for production deployment.
This module provides Cosmos DB operations compatible with the SQLite interface.
"""
import os
from typing import Dict, List, Optional
from azure.cosmos import CosmosClient, exceptions, PartitionKey
from datetime import datetime
import hashlib


class CosmosDBHandler:
    """Cosmos DB handler with interface matching SQLite database."""

    def __init__(self):
        """Initialize Cosmos DB connection."""
        endpoint = os.getenv("COSMOSDB_ENDPOINT")
        key = os.getenv("COSMOSDB_KEY")
        database_name = os.getenv("COSMOSDB_DATABASE_NAME", "JiraTraining")

        if not endpoint or not key:
            raise ValueError("COSMOSDB_ENDPOINT and COSMOSDB_KEY must be set in environment variables")

        self.client = CosmosClient(endpoint, key)
        self.database = self.client.get_database_client(database_name)

        # Get container clients
        self.users_container = self.database.get_container_client("Users")
        self.tickets_container = self.database.get_container_client("Tickets")
        self.history_container = self.database.get_container_client("TicketHistory")
        self.replies_container = self.database.get_container_client("TicketReplies")

    def hash_password(self, password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str, full_name: str, role: str) -> bool:
        """Create a new user."""
        try:
            # Check if user exists
            query = f"SELECT * FROM Users u WHERE u.username = '{username}'"
            existing = list(self.users_container.query_items(query=query, enable_cross_partition_query=True))
            if existing:
                return False

            # Get next ID
            all_users = list(self.users_container.query_items(
                query="SELECT VALUE COUNT(1) FROM Users",
                enable_cross_partition_query=True
            ))
            next_id = str((all_users[0] if all_users else 0) + 1)

            user = {
                "id": next_id,
                "username": username,
                "password_hash": self.hash_password(password),
                "full_name": full_name,
                "role": role
            }
            self.users_container.create_item(body=user)
            return True
        except exceptions.CosmosHttpResponseError:
            return False

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user info."""
        password_hash = self.hash_password(password)
        query = f"SELECT * FROM Users u WHERE u.username = '{username}' AND u.password_hash = '{password_hash}'"

        users = list(self.users_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        return users[0] if users else None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID."""
        try:
            query = f"SELECT * FROM Users u WHERE u.id = '{str(user_id)}'"
            users = list(self.users_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return users[0] if users else None
        except:
            return None

    def get_all_engineers(self) -> List[Dict]:
        """Get all engineers."""
        query = "SELECT * FROM Users u WHERE u.role = 'Engineer'"
        return list(self.users_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

    def get_all_admins(self) -> List[Dict]:
        """Get all admin users."""
        query = "SELECT * FROM Users u WHERE u.role = 'Admin'"
        return list(self.users_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

    def create_ticket(self, title: str, description: str, scenario: str,
                     priority: str, created_by: int, product: str = "Not Specified",
                     fundamental_solution: str = "FS:None", reporter_id: Optional[int] = None,
                     core_engineer_id: Optional[int] = None, rd_assignee_id: Optional[int] = None) -> str:
        """Create a new ticket and return ticket number."""
        # Get next ticket number
        tickets = list(self.tickets_container.query_items(
            query="SELECT VALUE COUNT(1) FROM Tickets",
            enable_cross_partition_query=True
        ))
        count = tickets[0] if tickets else 0
        ticket_number = f"CPDT-{count + 1:04d}"

        # Determine initial status
        if core_engineer_id:
            status = "Assigned to CORE"
        elif rd_assignee_id:
            status = "Assigned to RD"
        else:
            status = "Open"

        # Create ticket
        ticket = {
            "id": ticket_number,
            "ticket_number": ticket_number,
            "title": title,
            "description": description,
            "scenario": scenario,
            "status": status,
            "priority": priority,
            "product": product,
            "fundamental_solution": fundamental_solution,
            "reporter_id": str(reporter_id) if reporter_id else None,
            "core_engineer_id": str(core_engineer_id) if core_engineer_id else None,
            "rd_assignee_id": str(rd_assignee_id) if rd_assignee_id else None,
            "created_by": str(created_by),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "resolution_summary": None,
            "fs_details": None
        }

        self.tickets_container.create_item(body=ticket)

        # Add to history
        history_id = f"{ticket_number}-history-1"
        history = {
            "id": history_id,
            "ticket_id": ticket_number,
            "user_id": str(created_by),
            "action": "Ticket created",
            "old_status": None,
            "new_status": status,
            "comment": None,
            "created_at": datetime.utcnow().isoformat()
        }
        self.history_container.create_item(body=history)

        return ticket_number

    def get_all_tickets(self) -> List[Dict]:
        """Get all tickets."""
        query = "SELECT * FROM Tickets ORDER BY Tickets.created_at DESC"
        tickets = list(self.tickets_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        # Convert string IDs back to integers for compatibility
        for ticket in tickets:
            ticket['id'] = ticket['ticket_number']
        return tickets

    def get_ticket_by_id(self, ticket_id) -> Optional[Dict]:
        """Get a specific ticket by ID (ticket_number)."""
        try:
            ticket = self.tickets_container.read_item(
                item=str(ticket_id),
                partition_key=str(ticket_id)
            )
            ticket['id'] = ticket['ticket_number']
            return ticket
        except exceptions.CosmosResourceNotFoundError:
            return None

    def get_tickets_by_user(self, user_id: int) -> List[Dict]:
        """Get tickets assigned to a specific user."""
        user_id_str = str(user_id)
        query = f"""
            SELECT * FROM Tickets t
            WHERE t.core_engineer_id = '{user_id_str}' OR t.rd_assignee_id = '{user_id_str}'
            ORDER BY t.created_at DESC
        """
        tickets = list(self.tickets_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        for ticket in tickets:
            ticket['id'] = ticket['ticket_number']
        return tickets

    def update_ticket_status(self, ticket_id: int, new_status: str, user_id: int,
                            comment: Optional[str] = None, reporter_id: Optional[int] = None,
                            core_engineer_id: Optional[int] = None, rd_assignee_id: Optional[int] = None):
        """Update ticket status."""
        try:
            # Get current ticket
            ticket = self.tickets_container.read_item(
                item=str(ticket_id),
                partition_key=str(ticket_id)
            )

            old_status = ticket['status']
            ticket['status'] = new_status
            ticket['updated_at'] = datetime.utcnow().isoformat()

            if reporter_id is not None:
                ticket['reporter_id'] = str(reporter_id)
            if core_engineer_id is not None:
                ticket['core_engineer_id'] = str(core_engineer_id)
            if rd_assignee_id is not None:
                ticket['rd_assignee_id'] = str(rd_assignee_id)

            # Update ticket
            self.tickets_container.replace_item(item=ticket['id'], body=ticket)

            # Add to history
            history_items = list(self.history_container.query_items(
                query=f"SELECT VALUE COUNT(1) FROM TicketHistory h WHERE h.ticket_id = '{str(ticket_id)}'",
                enable_cross_partition_query=True
            ))
            history_count = (history_items[0] if history_items else 0) + 1
            history_id = f"{str(ticket_id)}-history-{history_count}"

            history = {
                "id": history_id,
                "ticket_id": str(ticket_id),
                "user_id": str(user_id),
                "action": "Status changed",
                "old_status": old_status,
                "new_status": new_status,
                "comment": comment,
                "created_at": datetime.utcnow().isoformat()
            }
            self.history_container.create_item(body=history)

        except exceptions.CosmosResourceNotFoundError:
            pass

    def resolve_ticket_with_summary(self, ticket_id: int, user_id: int, resolution_summary: str,
                                   fundamental_solution: str = "FS:None", fs_details: Optional[str] = None):
        """Resolve a ticket with summary."""
        try:
            ticket = self.tickets_container.read_item(
                item=str(ticket_id),
                partition_key=str(ticket_id)
            )

            old_status = ticket['status']
            ticket['status'] = 'Resolved'
            ticket['resolution_summary'] = resolution_summary
            ticket['fundamental_solution'] = fundamental_solution
            ticket['fs_details'] = fs_details
            ticket['updated_at'] = datetime.utcnow().isoformat()

            self.tickets_container.replace_item(item=ticket['id'], body=ticket)

            # Add to history
            history_items = list(self.history_container.query_items(
                query=f"SELECT VALUE COUNT(1) FROM TicketHistory h WHERE h.ticket_id = '{str(ticket_id)}'",
                enable_cross_partition_query=True
            ))
            history_count = (history_items[0] if history_items else 0) + 1
            history_id = f"{str(ticket_id)}-history-{history_count}"

            history = {
                "id": history_id,
                "ticket_id": str(ticket_id),
                "user_id": str(user_id),
                "action": "Ticket resolved",
                "old_status": old_status,
                "new_status": "Resolved",
                "comment": resolution_summary,
                "created_at": datetime.utcnow().isoformat()
            }
            self.history_container.create_item(body=history)

        except exceptions.CosmosResourceNotFoundError:
            pass

    def retract_case(self, ticket_id: int, user_id: int, comment: str):
        """Retract a case - return it to 'Assigned to CORE' status."""
        try:
            ticket = self.tickets_container.read_item(
                item=str(ticket_id),
                partition_key=str(ticket_id)
            )

            old_status = ticket['status']
            ticket['status'] = 'Assigned to CORE'
            ticket['updated_at'] = datetime.utcnow().isoformat()

            self.tickets_container.replace_item(item=ticket['id'], body=ticket)

            # Add to history
            history_items = list(self.history_container.query_items(
                query=f"SELECT VALUE COUNT(1) FROM TicketHistory h WHERE h.ticket_id = '{str(ticket_id)}'",
                enable_cross_partition_query=True
            ))
            history_count = (history_items[0] if history_items else 0) + 1
            history_id = f"{str(ticket_id)}-history-{history_count}"

            history = {
                "id": history_id,
                "ticket_id": str(ticket_id),
                "user_id": str(user_id),
                "action": "Case retracted",
                "old_status": old_status,
                "new_status": "Assigned to CORE",
                "comment": comment,
                "created_at": datetime.utcnow().isoformat()
            }
            self.history_container.create_item(body=history)

        except exceptions.CosmosResourceNotFoundError:
            pass

    def add_ticket_reply(self, ticket_id: int, user_id: int, message: str, reply_role: Optional[str] = None):
        """Add a reply/comment to a ticket."""
        # Get count for unique ID
        reply_items = list(self.replies_container.query_items(
            query=f"SELECT VALUE COUNT(1) FROM TicketReplies r WHERE r.ticket_id = '{str(ticket_id)}'",
            enable_cross_partition_query=True
        ))
        reply_count = (reply_items[0] if reply_items else 0) + 1
        reply_id = f"{str(ticket_id)}-reply-{reply_count}"

        reply = {
            "id": reply_id,
            "ticket_id": str(ticket_id),
            "user_id": str(user_id),
            "message": message,
            "reply_role": reply_role,
            "created_at": datetime.utcnow().isoformat()
        }
        self.replies_container.create_item(body=reply)

        # Update ticket updated_at
        try:
            ticket = self.tickets_container.read_item(
                item=str(ticket_id),
                partition_key=str(ticket_id)
            )
            ticket['updated_at'] = datetime.utcnow().isoformat()
            self.tickets_container.replace_item(item=ticket['id'], body=ticket)
        except:
            pass

    def get_ticket_replies(self, ticket_id: int) -> List[Dict]:
        """Get all replies for a ticket."""
        query = f"SELECT * FROM TicketReplies r WHERE r.ticket_id = '{str(ticket_id)}' ORDER BY r.created_at"
        replies = list(self.replies_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        # Enrich with user information
        for reply in replies:
            user = self.get_user_by_id(reply['user_id'])
            if user:
                reply['full_name'] = user['full_name']
                reply['role'] = user['role']
                reply['display_role'] = reply.get('reply_role', user['role'])

        return replies

    def get_ticket_history(self, ticket_id: int) -> List[Dict]:
        """Get ticket history."""
        query = f"SELECT * FROM TicketHistory h WHERE h.ticket_id = '{str(ticket_id)}' ORDER BY h.created_at"
        history = list(self.history_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        # Enrich with user information
        for h in history:
            user = self.get_user_by_id(h['user_id'])
            if user:
                h['full_name'] = user['full_name']

        return history
