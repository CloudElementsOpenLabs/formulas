# Combining All Results From a Formula Loop Step

## Problem this solves:**
* "How do you loop through something, get all the results from that loop and combine them?"

## Solution:**
You will need to use the last step of the loop as an aggregator
basically you will:
make a Javascript step called aggregator and then add the following Javascript:

  ```
  let arr = steps.aggregator ? steps.aggregator.arr : [];

  <insert custom logic>

  done({arr:arr})
  ```

This will look to see if the step has already run and if it has it will get the results from the step and you can add to them or if it has not run it will start with an empty array.

Included in this folder is [Loop_Step_Aggregation.json](Loop_Step_Aggregation.json), which is a formula json that can be imported and used to test with. With only a handful of steps, this formula will get contacts (from an Element Instance), loop through all those contacts, retrieve the contact name, and add it to an array. After is has finished looping through it will log an array of contact names. This formula uses a manual trigger for easy testing.

## IMPORTANT NOTES:
* You will need an authenticated Element instance with a GET /contacts API (endpoint). You can authenticate one in the UI.
* Your Element needs to return a field called **Name**. Alternatively, you can update the javascript step called `aggregator` to refer to a field that exists on the API you choose (i.e. for Zoho CRM v2, the field **Full_Name** could be used instead). You can update this step easily in the Formula UI.
* There is no paging in this formula. If you have over 200 contacts your final array will be an array of 200 names since the page size defaults to 200.
* The formula will be slow if you have a lot of contacts, and you might need to click the `CONTINUE POLLING` button in the steps pane after receiving a yellow warning message that the formula has stopped polling for results. This is expected as it is just a simple formula that you would need to edit and add your own logic to.

## Import Using the doctor:
1. Go to the Formulas UI and click the `BUILD NEW FORMULA` button, then select `Import` from the dropdown.
2. Find the json file `Loop_Step_Aggregation.json` in the GettingAllResultsFromLoop directory and use it to import the formula.
3. You can now interact with the formula in the UI. You can update the `aggregator` step as needed now. Use the `TRY IT OUT` button to select (and/or create) a formula instance, as well as the Element instance (CRM) you want to use. Then run the formula.

## Import Using the doctor:
1. Insure you have the latest non-beta version of the doctor installed via npm. You can follow the directions found here (https://www.npmjs.com/package/ce-util/v/2.2.5) or run the command `npm install -g ce-util`. You'll need a version of node that is >= v6.3.0
2. From the TheDoctor directory, run the command:
```
doctor upload formulas <acctNickName> -f loopStepAggregation.json
```
This will upload the Loop Step Aggregation Formula into the specified account.
3. You can now interact with the formula in the UI. You can update the `aggregator` step as needed now. Use the `TRY IT OUT` button to select (and/or create) a formula instance, as well as the Element instance (CRM) you want to use. Then run the formula.