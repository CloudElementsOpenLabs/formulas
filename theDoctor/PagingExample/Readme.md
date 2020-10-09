# Paging Example
Example of paging through results in a formula, without the use of a loop step.

Included in this folder:
- PagingExample.json, the example formula template

## How do I use the formula?
1. Insure you have the correct version of the doctor installed locally. Run the command `npm i -g ce-util` to install the latest, non-beta version of the doctor. You can find full instructions [here](https://www.npmjs.com/package/ce-util/v/2.2.5) as well.
2. Import the formula:
    * In the terminal, from the PagingExample directory, run the command `doctor upload formulas <accountNickName> -f PagingExample.json`.
3. Create an instance of the formula and a source element instance (the template was built using Quickbooks Online).
3. Trigger the formula
  - In the Cloud Elements UI, toggle the formula to debugging mode, select your `TRY IT OUT`, select (or create) a formula instance, add your trigger payload (example below), and click `RUN`.

For ease of testing, the formula was configured with a manual trigger that expects a payload for querying:
```
{
  "endDate": "2019-08-13",
  "startDate": "2015-07-30"
}
```

## How does the formula page?
The `buildQuery` step checks if the `getInvoices` step has been executed before, if it has, it includes the nextPage token in the query, which is used in `getInvoices`.  The filter step `isLastPage` checks if the response body from the latest call to `getInvoices` is empty--if true the formula completes successfully, if false the formula goes back to `buildQuery` to start the process of fetching the next step.

