# General info
This formula synchronizes an unordered set of employee expenses into your ERP of choice.  Trigger the formula from your application with an expense payload
following the example file attached ('example_expense_payload.json').  The workflow results in creating an invoice per employee in the payload and adds each of the expenses as line items to the invoice.  


# Prerequisites 
Import the VDR "expenseInvoice" into your Cloud Elements account.  It is already setup with transformations into Netsuite, Quickbooks online and Xero holding all mandatory fields to create the invoice in the ERP system.


#Example payload
Find the example payload attached but in general follows the following structure 

{
  "expenseArr": [
    "Expense No": number,
    "Submission No": number,
    "Type": string,
    "Employee First Name": string,
    "Employee Last Name": string,
    "Employee No": string,
    "Department Name": string,
    "Department Code": number,
    "Nominal Code": number,
    "Project Name": string,
    "Project Code": string,
    "Description": string,
    "Expense Date": date (dd/mm/yyyy),
    "Submission Date": date (dd/mm/yyyy),
    "Gross Amount": number,
    "Tax Amount": number,
    "Net Amount": number,
    "Tax Code": number
  ];
}

Note that the current formula does not use all of the fields in this payload and can easily be altered once you imported everything into your account.  The "expenseArr" array the payload starts with is important to maintain as this allows to loop over the expense data.


