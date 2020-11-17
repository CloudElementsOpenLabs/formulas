# Creating a Loop Step Within Another Loop Step

## Problem this solves:
* "How should I setup a loopstep from within another loop and aggragate data from the nested loop?"

## Solution:
You will need to call the primary loop as the on failure branch of the nested loop. You will then need top use the standard aggregator approach to maintain the data from the nested loop. This approach is outlined below: 

  ```
  let arr = steps.aggregator ? steps.aggregator.arr : [];

  <insert custom logic>

  done({arr:arr})
  ```

This will look to see if the step has already run and if it has it will get the results from the step and you can add to them or if it has not run it will start with an empty array.

Included in this folder is [nestedLoops.json](nestedLoops.json), which is a formula json that can be imported and used to test with. With only a handful of steps, this formula will get invoices (from an Element Instance), loop through all those invoices and then through each invoice's line items, retrieve the line item's amount, and add it to an array. After is has finished looping through it will log an array of all of the line items' amount. This formula uses a manual trigger for easy testing.

## IMPORTANT NOTES:
* You will need an authenticated Element instance with a GET /invoices API (endpoint). Additionally, the invoices in the response will also need to have line items so that we could loop through those as well. This formula was built using Quickbooks Online as their inovice records have a line items array.  You can authenticate one in the UI.
* Your Element needs to return an array of line items that each contain a field called **Amount**. Alternatively, you can update the javascript step called `aggregator` to refer to a field that exists on the API you choose (i.e. for Zoho CRM v2, the field **Full_Name** could be used instead). You can update this step easily in the Formula UI.
* There is no paging in this formula. Additionally there is a pagination query in place to limit the number of invoices that get returned to 20. This extra step was added to make testing slightly easier as there are only a handful of records to work with. Please be mindful of this deliberate limitation as you test. 

## Import Using the UI:
1. Go to the Formulas UI and click the `BUILD NEW FORMULA` button, then select `Import` from the dropdown.
2. Find the json file `nestedLoops.json` in the nestedLLoops directory and use it to import the formula.
3. You can now interact with the formula in the UI. You can update the `aggregator` step as needed. Use the `TRY IT OUT` button to select (and/or create) a formula instance, as well as the Element instance (Finance System) you want to use. Then run the formula.

## Import Using the doctor:
1. Insure you have the latest non-beta version of the doctor installed via npm. You can follow the directions found [here](https://www.npmjs.com/package/ce-util) or run the command `npm install -g ce-util`. You'll need a version of node that is >= v6.3.0. You will need to upload the file from TheDoctor directory, as files uploaded with the doctor have a different structure than files imported via UI.
2. From the TheDoctor directory, run the command:
  ```
  doctor upload formulas <acctNickName> -f nestedLoops.json
  ```
  This will upload the Nested Loops Formula into the specified account.

3. You can now interact with the formula in the UI. You can update the `aggregator` step as needed. Use the `TRY IT OUT` button to select (and/or create) a formula instance, as well as the Element instance (Finance System) you want to use. Then run the formula.