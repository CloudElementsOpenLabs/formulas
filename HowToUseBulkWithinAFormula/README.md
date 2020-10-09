# Using Bulk in your formulas
Working with bulk a formula can be challenging. Bulk by nature is an asynchronous job, while Formulas are a synchronous procedure. The trick to getting them to work together is webhooks.

In this example, we will use two formulas--one creates the bulk job, specifying who to notify when the job completes, and one which recieves the 'job done' notification and consumes the results.  This configuration leverages our `Elements-Async-Callback-Url` header.

### IMPORTANT NOTES:

1. This repository contains two examples for consuming the results of a bulk job in a formula:
    * Example 1 - Bulk sync of records from one element to another element. That is, create records for each item in the results of the bulk extract. For this example, use [BulkStep1.json](BulkStep1.json) and [BulkStep2.json](BulkStep2.json).
    * Example 2 - Bulk extract from an element that then saves the bulk file to an element in the docs hub (Google Drive).  For this example, use [BulkStep1.json](BulkStep1.json) and [Bulkstep2DocsHub.json](BulkStep2DocsHub.json). 

    If you are interested in Example 2, please replace `BulkStep2.json` referenced below with [BulkStep2DocsHub.json](BulkStep2DocsHub.json).  This formula template is setup to work with Google Drive. If you are working with a different docs hub element, you will need to make adjustments based on the provider's requirements (e.g. path, file name, etc).  Please note that the folder and filename are both configured in the step `generateMetadata`--adjust as needed for your use case.
2. For these formulas to work, you must use a VDR! You must be able to call GET `/NameOfVDR`, copy a payload that gets returned, and then call POST `/NameOfVDR` to the other endpoint. Included are some example transformations as well as instructions for how to use them.

## Options for Importing Resources:
You have two options for importing your resources. You can either import using the UI or the doctor (Cloud Element's cli tool). Follow the instructions below for the method you prefer, then move on to [Configure Your Bulk Formula](#configure-your-bulk-formula).

### Import in the UI:
1. Import both formulas from the Formulas UI page.
    * Click the `BUILD NEW FORMULA` button, then select `Import` from the dropdown.
    * Find the json file [BulkStep1.json](BulkStep1.json) in the GettingAllResultsFromLoop directory and use it to import the formula.
    * Repeat for the file [BulkStep2.json](BulkStep2.json) (or [BulkStep2DocsHub.json](BulkStep2DocsHub.json) depending on your use-case).
3. Create the VDR and transformations for Salesforce and Microsoft Dynamics CRM:
    * Create the VDR by calling POST `/organizations/objects/MyContact/definitions` with this payload: [ObjectDefinition.json](ObjectDefinition.json). You can find this API [here](https://my-staging.cloudelements.io/api-docs/platform/organizations).
    * Create the transformation for Salesforce by calling POST `/organizations/elements/sfdc/transformations/MyContact` with this payload: [MyContactSFDC.json](MyContactSFDC.json) (same page as above), where the keyOrId is `sfdc` and the objectName is `MyContact`.
    * Create the transformation for Microsoft Dynamics CRM by calling POST `/organizations/elements/dynamicscrm/transformations/MyContact` with the payload: [dynamicscrmMyContact.json](dynamicscrmMyContact.json) (same page and endpoint as the above), where the keyOrId is `dynamicscrm` and the objectName is `MyContact`.
4. Follow the steps below under [Configure Your Bulk Formula](#configure-your-bulk-formula).

### Import Using the doctor:
1. Insure you have the correct version of the doctor installed locally. Run the command:
    ```
    npm i -g ce-util
    ```
    This will install the latest, non-beta version of the doctor. You can find full instructions [here](https://www.npmjs.com/package/ce-util/v/2.2.5) as well.
2. Import both formulas:
    * In the terminal, from the TheDoctor/Formulas directory, run the command:
        ```
        doctor upload formulas <accountNickName> -f BulkStep1.json
        ```
    * Repeat for the BulkStep2 (or BulkStep2DocsHub, depending on your use-case) formula:
        ```
        doctor upload formulas <accountNickName> -f BulkStep2.json
        ```
3. Import the VDR and example transformations:
    * In the terminal, from the TheDoctor/MyContactVDR directory, run the command
        ```
        doctor upload vdrs <accountNickName> -d . -n MyContact
        ```
    This will import the VDR as well as the transformations into your account.
4. Follow the steps below under [Configure Your Bulk Formula](#configure-your-bulk-formula).

## Configure Your Bulk Formula
Follow the steps below to finish configuring your bulk formulas.
1. Authenticate Element Instances:
    * If using the example VDR for **Example 1**, you will need to authenticate an element instance of both `Salesforce` and `Microsoft Dynamics CRM`. You will not see any transformations loaded from your VDR until you have authenticated instances. You will use one instance as a source element and one as a destination (target) element when creating your formula instance below.
    * If using the example VDR for **Example 2**, you will need to authenticate an element instance of one of the above (`Salesforce` or `Microsoft Dynamics CRM`) as well as an instance of `Google Drive`. You will use one of either `Salesforce` or `Microsofrt Dynamics CRM` as a source element, and a Docs Hub element (Google Drive) as the destination (target) when creating your Formula instance below.
2. Create a formula instance for Bulk Step 2.
    * Make sure you remember which element you chose for CRM source. You will need to choose the same one in the next formula instance you create for Bulk Step 1.
    * For `object` under `Values`, enter: `MyContact` (or the name of your VDR).
    * Capture the ID of the created formula instance. You will need to give the Bulk Step 1 formula the instance ID for the second formula. This will let the webhook trigger the correct formula when the bulk job is completed. 
3. Create a formula instance for Bulk Step 1, using the same element for CRM source as you chose before. Under `Values`:
    * For `object`, enter `MyContact` (or the name of your VDR).
    * Enter a cron job schedule (`0 0/10 0 ? * * *` will poll every 10 minutes).
    * Enter the Formula Instnace Id you captured from BulkStep2.
4. Go to your BulkStep1 Formula and open it, then select the `TRY IT OUT` button. Choose the instance you created before and click `RUN`.
5. Go back to the main Formulas UI and find your BulkStep2 formula. Click `EXECUTIONS` (appears on hover).
6. See that the Exeution was successful!

### Additional Information
Flowcharts describing the formulas are linked below:
* Example 1 - [here](Flowchart-BulkStep1.html) and [here](Flowchart-BulkStep2.html) 
* Example 2 - [here](Flowchart-BulkStep1.html) and [here](Flowchart-BulkStep2-docs-hub.html) 

For more information on how to use Cloud Elements, see our [help center](https://docs.cloud-elements.com) or our [support page](https://support.cloud-elements.com/hc/en-us).
