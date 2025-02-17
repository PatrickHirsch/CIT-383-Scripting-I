# HirschP2
# Module 4: Assignment 1 -- Classes and Packages
# CIT 383 | Scripting I
# 2025/02/16

# Custom module, HelpDeskSystem, is imported from custom package, helpdesk, imported and an object created
from helpdesk import HelpDeskSystem
theHelpDesk=HelpDeskSystem()


# Main loop to prompt for an option and hand-off user to the appropriate function
#   If an invalid selection (non-int or not in range of [1-4]) simply prints an error message
def main():
    userChoice=input("Choose an option: ")
    try:
        userChoice=int(userChoice)
        if userChoice<1 or userChoice>4:
            raise Exception()
    except Exception as e:
        userChoice=-1
    
    if userChoice==1:
        createNewTicket()
    elif userChoice==2:
        viewAllTickets()
    elif userChoice==3:
        updateTicketStatus()
    elif userChoice==4:
        exit()
    else:
        print("Invalid selection.\n")


# Prompts for user's name and a description of the issue before creating the ticket
#   Ticket is created via the HelpDeskSystem's create_ticket() function returning the new ticket's ID
def createNewTicket():
    requester_name=input("Enter your name: ")
    issue=input("Describe your issue: ")
    ticket_id=theHelpDesk.create_ticket(requester_name,issue)
    print(f"\nTicket created successfully! Ticket ID: {ticket_id}\n")
    

# Simply calls the HelpDeskSystem's view_tickets() function to print a list of all tickets
def viewAllTickets():
    theHelpDesk.view_tickets()


# Prompts user for a ticket's ID and new status, updating the ticket if valid options are passed via HelpDeskSystem's update_ticket_status()
#   Validates ticket_id by ensuring its an int, then by HelpDeskSystem's ticket_exists() function.
#   Validates statuses by ensuring they exist in the list of valid statuses, `statuses`.
#   Function fails gracefully if an invalid input is given by printing a message corresponding to the issue encountered and returns -1.
def updateTicketStatus():
    ticket_id=input("Enter Ticket ID: ")
    try:
        ticket_id=int(ticket_id)
        if not theHelpDesk.ticket_exists(ticket_id):
            raise Exception()
    except Exception as e:
        print("Invalid Ticket ID.\n")
        return -1
    
    statuses=["Open","In Progress","Resolved"]
    new_status=input(f"Enter new status ({', '.join(statuses)}): ")
    if new_status not in statuses:
        print("Invalid Status.\n")
        return -1
    
    theHelpDesk.update_ticket_status(ticket_id,new_status)
    print("\nTicket updated successfully!\n")
    

# Prints an initial welcome message and menu of options before entering main loop until interrupted or an option of '4' is selected
print("""Welcome to the IT Help Desk System")
1. Create a new ticket
2. View all tickets
3. Update ticket status
4. Exit""")
while True:
    main()