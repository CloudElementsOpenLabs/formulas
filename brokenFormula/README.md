# Formula Debugging Practice

## Problem this solves:
* This formula will give you a template that you can use to practice debugging formula issues.
* There are 3 errors that you will need to resolve before getting a successful formula instance execution.
* The intention of formula is to be able to receive an event for a customer record, retrieve the full record and then notify someone via email. 


## IMPORTANT NOTES:
* You will need an authenticated Element instance with a GET /customers API (endpoint) such as QBO or Sage Intacct V3. You can authenticate an Element instance in the UI.
* You will need to enable eventing for the /customers resource to be able to setup a proper formula execution. 

## Import Using the UI:
1. Go to the Formulas UI and click the `BUILD NEW FORMULA` button, then select `Import` from the dropdown.
2. Find the json file `brokenFormula.json` in the brokenFormula directory and use it to import the formula.
3. You can now interact with the formula in the UI. You can update the `aggregator` step as needed. Use the `TRY IT OUT` button to select (and/or create) a formula instance, as well as the Element instance (CRM) you want to use. Then run the formula.

## Import Using the doctor:
1. Insure you have the latest non-beta version of the doctor installed via npm. You can follow the directions found [here](https://www.npmjs.com/package/ce-util) or run the command `npm install -g ce-util`. You'll need a version of node that is >= v6.3.0. You will need to upload the file from TheDoctor directory, as files uploaded with the doctor have a different structure than files imported via UI.
2. From the TheDoctor directory, run the command:
  ```
  doctor upload formulas <acctNickName> -f brokenFormula.json
  ```
  This will upload the Broken Formula into the specified account.

3. You can now interact with the formula in the UI. You can update the `aggregator` step as needed. Use the `TRY IT OUT` button to select (and/or create) a formula instance, as well as the Element instance (CRM) you want to use. Then run the formula.


## Solution:
* The 1st error is in the `checkEventTrigger` step. This step has 2 `false` values that are being passed in the done function. This will force the formula to always go down the onFailure path. 
* The 2nd error is in the `retrieveEmployeeRecord` step, where you will notice that the selected element variable is missing the proper `{}` syntax. 
* The final error is in the `sendNotificationEmail` step where the javascript is missing an email to notify. 