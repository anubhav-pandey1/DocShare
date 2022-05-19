# DocShare

As part of this challenge you will implement a sharing mechanism for documents. The output can be a simple backend application with no UI. API calls can be tested via terminal or postman.

We will consider a very simple document with its name being the only data it holds.

Every user has a unique email address and can create as many documents as they want. 
The document can be shared to others via mentioning their email address.
The document can be shared with either read only access or write access.

## How Document Access Works

### READ ACCESS

✅ Can read the document
🚫 Can’t write to the document
🚫 Can’t share the document
🚫 Can’t delete the document

### WRITE ACCESS

✅ Can read the document
✅ Can write to the document
✅ Can share the document using email address of the receiver
🚫 Can’t edit the access level of a user to the document
🚫 Can’t delete the document

### DOCUMENT OWNER

✅ Can read the document
✅ Can write to the document
✅ Can share the document using email address of the receiver
✅  Can edit the access level of a user to the document
✅ Can delete the document


## API

### Create Document: 
Document has only name as its data

### View Document: 
Fetches the name of the document

### Edit Document: 
Overrides the name of the document

### Give Access to the Document

### Edit Access to the Document

### Delete the Document

NOTE: 💡 Ignore the authentication of the users. Assume email of the user is passed along with the API calls.

Once you are done with the above and have time, you can tackle the below challenges

## Bonus Challenges:

- Write API for getting all the documents that a user has access to, the documents that they created and the ones that are shared with them.

- Implement publicly viewable documents. Public documents can be viewed by anyone even if they don’t have any access to the document. The access to private documents remains unchanged.

NOTE: The output can be a simple backend application with no UI. API calls can be tested via terminal or postman. Once you are done with the assignment, share the 1. Zip file of the code or github link  and  2. A screen recording of the working challenge. If you do not find time to finish the entire challenge, add inline comments in the code explaining how you would have implemented it.