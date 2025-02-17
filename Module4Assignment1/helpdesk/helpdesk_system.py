# Simple Help Desk System object designed to maintain and manage a list of custom Ticket objects
#   Tickets may be created or have their statuses modified, though cannot be deleted.

from helpdesk.ticket import Ticket

class HelpDeskSystem:
    def __init__(self):
        self.tickets=[] # A list for all Ticket objects to be stored in
    
    # Function to create a ticket given the Requester's Name and a Description of the Issue
    #   Statuses of new tickets default to 'Open' and IDs are sequentially generated
    #   For this prototype, a ticket's ID corresponds with its index in the list `tickets`
    #      \_This is presumed safe since the list is never reordered nor any tickets deleted.
    # The newly created Ticket's ID is returned upon creation.
    def create_ticket(self,requester_name,issue):
        ticket_id=len(self.tickets)
        status='Open'
        self.tickets.append(Ticket(ticket_id,requester_name,issue,status))
        return ticket_id
    
    
    # Function to print all tickets in the system with a header and line breaks before and after
    #   This is done by the Ticket object's own defined string format.
    def view_tickets(self):
        print("\nTickets:")
        for ticket in self.tickets:
            print(str(ticket))
        print("")
    
    
    # Function to update a Ticket's Status given its ID.
    #   If the provided Ticket ID does not exist (as defined by ticket_exists)) throws an exception.
    def update_ticket_status(self,ticket_id,new_status):
        if self.ticket_exists(ticket_id):
            self.tickets[ticket_id].update_status(new_status)
        else:
            raise Exception(f"Nonexistant Ticket ID, {ticket_id}, provided in attempting to update status.")
    
    
    # Function to determine whether a provided Ticket ID exists returning a Boolean value
    #   Once again, this assumes ticket_id corresponds to index in array as explained in comments above create_ticket()
    def ticket_exists(self,ticket_id):
        if ticket_id<len(self.tickets):
            return True
        return False