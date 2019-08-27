# General info
This formula synchronizes an unordered set of employee expenses into your ERP of choice.  Trigger the formula from your application with an expense payload
following the example file attached ('example_expense_payload.json').  The workflow results in creating an invoice per employee in the payload and adds each of the expenses as line items to the invoice.  


# Prerequisites 
Import the VDR "expenseInvoice" into your Cloud Elements account.  It is already setup with transformations into Netsuite, Quickbooks online and Xero holding all mandatory fields to create the invoice in the ERP system.

## Default settings
As this formula is an example, notice we included hard coded identifiers for some of the mandatory properties for invoice creation.  ie: vendor/entity/subsidiary identifier. Since the formula itself is generic, the better place to put the hardcoded values is in their respective VDR transformations.  
Make sure to alter the values to identifiers that work with your sandbox or extend the formula with object creations/ lookup queries to get the correct object id back.  


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

#Workflow step description
1. This formula is setup with a manual trigger taking in the attached payload
1. expenseSorter is a javascript step sorting the incoming payload into an employee dictionary holding all its expenses.
1. loopEmployee is the loop step that runs over the employee dictionary
1. handleEmployee is a javascript step constructing the invoice object.  Notice that this script holds some hardcoded values (dates as example). As described in "Default settings" you either find defaults on VDR level or in this JS step
1. submitInvoiceToERP submits the invoice object of the handleEmployee step into the ERP using the 'expenseInvoice' VDR.  The result is either an invoice ID or an error returned by the ERP.  Respectively addInvoiceId / addError.  Notice how this step has advanced configuration and accepts both 400 and 404 as acceptable HTTP response codes.  The example payload will run successfully on Netsuite apart for one expense that has a negative value. Netsuite will return with an appropriate error and response code.  We handle this error in the addError step
1. returnFullExpenseList in this example formula provides you the original payload back, including a "resultInvoice" or "resultError" property per expense in the list.  You can use this full result payload to send back to your own system or include this step in the loopEmployees loop to get intermediate updates back. 
