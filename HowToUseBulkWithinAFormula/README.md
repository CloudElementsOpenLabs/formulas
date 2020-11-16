# Using Bulk in your Formulas
Working with bulk a Formula can be challenging. Bulk by nature is an asynchronous job, while Formulas are a synchronous procedure. The trick to getting them to work together is bulk job callbacks.

In this example, we will use three Formulas--one creates the bulk job, specifying who to notify when the job completes, one which recieves the 'job done' notification and consumes the results and notifies you in the case that they occur. This configuration leverages our `Elements-Async-Callback-Url` header.

### IMPORTANT NOTES:

1. This repository contains two examples for consuming the results of a bulk job in a Formula:
    * Example 1 - Bulk sync of records from one Element to another Element. That is, create records for each item in the results of the bulk extract. For this example, use [BulkStep1.json](BulkStep1.json) and [BulkStep2.json](BulkStep2.json), as well as [BulkStep3.json](BulkStep3.json).
    * Example 2 - Bulk extract from an Element that then saves the bulk file to an Element in the docs hub (Google Drive).  For this example, use [BulkStep1.json](BulkStep1.json) and [Bulkstep2DocsHub.json](BulkStep2DocsHub.json), as well as [BulkStep3.json](BulkStep3.json).

    If you are interested in Example 2, please replace `BulkStep2.json` referenced below with [BulkStep2DocsHub.json](BulkStep2DocsHub.json).  This Formula template is setup to work with `Google Drive`. If you are working with a different docs hub Element, you will need to make adjustments based on the provider's requirements (e.g. path, file name, etc).  Please note that the folder and filename are both configured in the step `generateMetadata`--adjust as needed for your use case.

2. For these Formulas to work, you must use a VDR! You must be able to call GET `/NameOfVDR`, copy a payload that gets returned, and then call POST `/NameOfVDR` to the other endpoint. Included are some example transformations as well as instructions for how to use them.
3. The sample VDR in this repo was built using the VDR Engine V2. However, it **is** backwards compatible with the VDR Engine V1, so it does not matter which version you are running in your organization. If you'd like to check, you can follow the instructions [here](https://docs.cloud-Elements.com/home/introducing-v2-engine-feff13e-introducing-v2-engine) underneath `Determining your Current Engine`.

## Options for Importing Resources:
You have two options for importing your resources. You can either import using the UI or the doctor (Cloud Element's cli tool). Follow the instructions below for the method you prefer, then move on to [Configure Your Bulk Formula](#configure-your-bulk-Formula).

### Import in the UI:
1. Import both Formulas from the Formulas UI page.
    * Click the `BUILD NEW Formula` button, then select `Import` from the dropdown.
    * Find the json file [BulkStep1.json](BulkStep1.json) in the GettingAllResultsFromLoop directory and use it to import the Formula.
    * Repeat for the file [BulkStep2.json](BulkStep2.json) (or [BulkStep2DocsHub.json](BulkStep2DocsHub.json) depending on your use-case).
    * Repeat for the file [BulkStep3.json](BulkStep3.json).
3. Create the VDR and transformations for `Salesforce` and `Sugar CRM`:
    * Create the VDR by calling POST `/organizations/objects/MyContact/definitions` with this payload: [ObjectDefinition.json](ObjectDefinition.json). You can find this API [here](https://my-staging.cloudElements.io/api-docs/platform/organizations).
    * Create the transformation for `Salesforce` by calling POST `/organizations/Elements/sfdc/transformations/MyContact` with this payload: [MyContactSFDC.json](MyContactSFDC.json) (same page as above), where the keyOrId is `sfdc` and the objectName is `MyContact`.
    * Create the transformation for `Sugar CRM` by calling POST `/organizations/Elements/sugarcrmv2/transformations/MyContact` with the payload: [MyContactSugarCRM.json](MyContactSugarCRM.json) (same page and endpoint as the above), where the keyOrId is `sugarcrmv2` and the objectName is `MyContact`.
4. Follow the steps below under [Configure Your Bulk Formula](#configure-your-bulk-formula).

### Import Using the doctor:
1. Insure you have the correct version of the doctor installed locally. Run the command:
    ```
    npm i -g ce-util
    ```
    This will install the latest, non-beta version of the doctor. You can find full instructions [here](https://www.npmjs.com/package/ce-util) as well.
2. Import both Formulas:
    * In the terminal, from the TheDoctor/Formulas directory, run the command:
        ```
        doctor upload formulas <accountNickName> -f BulkStep1.json
        ```
    * Repeat for the BulkStep2 (or BulkStep2DocsHub, depending on your use-case) Formula:
        ```
        doctor upload formulas <accountNickName> -f BulkStep2.json
        ```
    * Repeat for the BulkStep3 Formula:
        ```
        doctor upload formulas <accountNickName> -f BulkStep3.json
        ```
3. Import the VDR and example transformations:
    * In the terminal, from the TheDoctor/MyContactVDR directory, run the command
        ```
        doctor upload vdrs <accountNickName> -d . -n MyContact
        ```
    This will import the VDR as well as the transformations into your account.
4. Follow the steps below under [Configure Your Bulk Formula](#configure-your-bulk-formula).

## Configure Your Bulk Formula
Follow the steps below to finish configuring your bulk Formulas.
1. Authenticate Element Instances:
    * If using the example VDR for **Example 1**, you will need to authenticate an Element instance of both `Salesforce` and `Sugar CRM`. You will not see any transformations loaded from your VDR until you have authenticated instances. You will use one instance as a source Element and one as a destination (target) Element when creating your Formula instance below.
    * **NOTE:** If you choose `Sugar CRM` as the source Element and `Salesforce` as the target, it's important to know that `Salesforce` does not allow for duplicate records to be created. Attempting to bulk upload records from `Sugar CRM` that already exist in `Salesforce` will result in an error for those records. If you'd like to test this direction and need new records created in your sandbox, consider checking out our example [SeedScript Repo](https://github.com/CloudElementsOpenLabs/scripts/tree/master/AddRecordsSeedScript), found in our OpenLabs [Scripts Repo](https://github.com/CloudElementsOpenLabs/scripts).
    * If using the example VDR for **Example 2**, you will need to authenticate an Element instance of one of the above (`Salesforce` or `Sugar CRM`) as well as an instance of `Google Drive`. You will use one of either `Salesforce` or `Sugar CRM` as a source Element, and a Docs Hub Element (Google Drive) as the destination (target) when creating your Formula instance below.
2. Create a Formula instance for Bulk Step 3.
    * Enter the email you would like to be notified at in case of an upload error.
    * Capture the ID of the created Formula instance. You will need to give the Bulk Step 2 Formula the instance ID for the third Formula. This will let the bulk job callback trigger the correct Formula if the bulk job runs into an error. 
3. Create a Formula instance for Bulk Step 2.
    * Make sure you remember which Element you chose for CRM source. You will need to choose the same one in the next Formula instance you create for Bulk Step 1.
    * For `object` under `Values`, enter: `MyContact` (or the name of your VDR).
    * For `thirdFormulaInstanceId`, enter the ID you captured from Step 2 when creating the Bulk Step 3 Formula.
    * Enter the email you would like to be notified at in case of an upload error.
    * Capture the ID of newly the created Formula instance for Bulk Step 2. You will need to give the Bulk Step 1 Formula the instance ID for the second Formula. This will let the bulk job callback trigger the correct Formula when the bulk job is completed. 
4. Create a Formula instance for Bulk Step 1, using the same Element for CRM source as you chose before. Under `Values`:
    * For `object`, enter `MyContact` (or the name of your VDR).
    * Enter the Formula instance Id you captured from BulkStep2.
5. Go to your BulkStep1 Formula and open it, then select the `TRY IT OUT` button. Choose the instance you created before and click `RUN`.
6. Go back to the main Formulas UI and find your BulkStep2 Formula. Click `EXECUTIONS` (appears on hover).
7. You might have to click the refresh icon next to `Formula Executions`, as it takes some time for the Formulas to communicate.
8. Lastly, you can always go to Bulk Step 3 to check for errors with the upload, but you will also be notified if any occur to the email you configured.

### Additional Information
Flowcharts describing the Formulas are linked below:
* BulkStep1 - [here](Flowchart-BulkStep1.html)
* BulkStep2 - [here](Flowchart-BulkStep2.html)
* BulkStep2DocsHub - [here](Flowchart-BulkStep2DocsHub.html)
* BulkStep3 - [here](Flowchart-BulkStep3.html)

For more information on how to use Cloud Elements, see our [help center](https://docs.cloud-Elements.com) or our [support page](https://support.cloud-Elements.com/hc/en-us).