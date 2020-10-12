# Paging Example
Example of paging through results in a formula, without the use of a loop step.

Included in this folder:
- PagingExample.json, the example formula template
- Flowchart-PagingExample.html
- TheDoctor directory (use the file in this directory to upload via the doctor, Cloud Elements CLI tool)

## How do I use the formula?
### Import the formula into your Cloud Elements environment:
You have two options when choosing how to import this formula. You can use the Formulas UI or the doctor.
1. Using the Formulas UI:
  * Click the `BUILD NEW FORMULA` button [found on this page](https://my-staging.cloudelements.io/formulas) and select `Import` from the dropdown.
  * Find the file `PagingExample.json` in the PagingExample directory and import it.
2. Using the doctor:
  * Insure you have the correct version of the doctor installed locally. Run the command `npm i -g ce-util` to install the latest, non-beta version of the doctor. You can find full instructions [here](https://www.npmjs.com/package/ce-util/v/2.2.5) as well. You will need to upload the file from TheDoctor directory, as files uploaded with the doctor have a different structure than files imported via UI.
  * In the terminal, from the PagingExample/TheDoctor directory, run the command:
    ```
    doctor upload formulas <accountNickName> -f PagingExample.json
    ```
 
### Use your formula:
1. Create an instance of the formula and a source element instance (the template was built using Quickbooks Online)
2. Trigger the formula
  * In the Cloud Elements UI, toggle the formula to debugging mode, select your formula instance, add your trigger payload (example below), and click 'run'.
  * For ease of testing, the formula was configured with a manual trigger that expects a payload for querying:
    ```
    {
      "endDate": "2019-08-13",
      "startDate": "2015-07-30"
    }
    ```

### How does the formula page?
The `buildQuery` step checks if the `getInvoices` step has been executed before, if it has, it includes the nextPage token in the query, which is used in `getInvoices`.  The filter step `isLastPage` checks if the response body from the latest call to `getInvoices` is empty--if true the formula completes successfully, if false the formula goes back to `buildQuery` to start the process of fetching the next step.