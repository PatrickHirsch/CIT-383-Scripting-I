# Simple class for a Ticket Object.
#   Maintains a Ticket ID, Requester Name, Description of Issue, and Status of Ticket
#   All fields are designed to be immutable post-creation except Status which may be updated via update_status(new_status)
#   Tickets may be printed as Strings, listing all fields.

class Ticket:
    def __init__(self,ticket_id,requester_name,issue,status):
        self.ticket_id=ticket_id
        self.requester_name=requester_name
        self.issue=issue
        self.status=status

    def update_status(self,new_status):
        self.status=new_status

    def __str__(self):
        return f"ID: {self.ticket_id} | Requester: {self.requester_name} | Issue: {self.issue} | Status: {self.status}"