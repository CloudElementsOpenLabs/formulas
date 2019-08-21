# General info
This ExpenseToInvoice formula syncs a set of expenses for a set of employees, they are not ordered. 
 The formula creates multiple invoices in the ERP system of choice, one per employee and holds all 
 his/her expenses that are in the payload.  Each expense in the payload is updated with the invoiceId 
 or the error that occurred.

# Prerequisites 
 The included expenseInvoice VDR has transformations to Netsuite, Quickbooks Online and Xero.