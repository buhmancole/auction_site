## Alpha Auction Requirements

#### 1.	Introduction and Context
This project aims to build a system for running an auction at a school or church activity.
The auction system will be for managing a live event, not running an online auction like e-bay. It aims to replace paper voting with a mobile phone system so that people can know what they’ve spent so far and will also help tally the results at the end of the night. The system will support both a silent auction and a live auction and be capable of running on a PC (for an administrator) and iOS and Android mobile devices.


#### 2.	Users and their Goals

##### As a bidder: 
- As a bidder, I want to be able to see what items I've bid on. 
- As a bidder, I want to see what is up for bid (by category and search)
- As a bidder, I want to see the current highest bid
- As a bidder, I want to be able to see the time remaining in the auction
- As a bidder, I want to be able to bid (increments of admin specified)
- As a bidder, I want to get a notification when outbid
- As a bidder, I want to know when I win an item and how much I owe at the end of the auction
- As a bidder, I want to know how much I've spent (current winning high bids)

##### As an admin: 
- As an admin, I want to see all bids on an item
- As an admin, I want to add, delete, and edit an item
- As an admin, I want to set the starting bid for items and the bid increment per item
- As an admin, I want to set the auction start/end time
- As an admin, I want to look up a person by bidder number
- As an admin, I want to insert winning bids for live auction items (by bidder #)
- As an admin, I want to know who wins each item at the end of the auction
- As an admin, I want to know the total money raised

#### 3.	Functional Requirements
 - The user shall be able to place a bid on an item.
 - The user shall be able to view all available items to bid on, and narrow the scope down by category or by searching for a specific item.
 - The user shall see a timer at all times for how much time is left in the auction.
 - The user shall be notified when they are outbid.
 - The user shall be notified of all winning bids at the end of the auction and informed of the total amount owed.
 - Users shall be able to make accounts in order to bid on items.
 - Users shall enter a password upon creating an account that verifies that they are at the event.
 - Admins shall be able to add, edit, and delete items in the auction.
 - Admins shall be able to set a start and end time for the auction.
 - Admins shall be able to assign a winner to 'live' auction items.
 - Admins shall be able to print out a report for all items and the winning bidder.
 - Admins shall be able to print out a report for each item and the full list of bids.
 - Admins shall be able to impose a bid increment on each item.
 - Admins shall be able to view the total amount of money raised during the auction.
 - The system shall display the current auction to all visitors.
 - The system shall authenticate each user when placing a bid and ensure that only those with accounts can bid.

#### 4.	Non-functional Requirements
 - The system shall support 300 concurrent users.
 - The system shall be resistant to common hacking techniques - SQL injections, XSS, etc.
 - The system shall follow standard privacy procedures and never transmit passwords in cleartext.
 - The system shall be equally functional on iOS, Android, and PC devices.

#### 5.	Future Features
This section contains a list of ideas or features that are beyond the scope of the project.
 - Support simultaneous auctions
 - Support payment options
 - Allow for password requirements to participate in auction

#### 6.	Glossary
This section contains a list important terms and their definition.


