# Using Bulk in your formulas
Working with bulk a formula can be challenging. Bulk by nature is an asynchronous job, while Formulas are a synchronous procedure. The trick to getting them to work together is webhooks.

In this example, we will use two formulas--one creates the bulk job, specifying who to notify when the job completes, and one which recieves the 'job done' notification and consumes the results.  This configuration leverages our `Elements-Async-Callback-Url` header.

IMPORTANT NOTE: this repository contains two examples of consuming the results of a bulk job in a formula
* Example 1 - Bulk sync of records from one element to another element.  That is, create records for each item in the results of the bulk extract.  For this example, use [bulk_Step1.json](bulk_Step1.json) and [bulk_Step2.json](bulk_Step2.json).
* Example 2 - Bulk extract from one element, save the bulk file to an element in the docs hub (Google Drive).  For this example, use [bulk_Step1.json](bulk_Step1.json) and [bulk_step2_docshub.json](bulk_step2_docshub.json).  If you are interested in example 2, please replace `bulk_Step2.json` referenced below with [bulk_step2_docshub.json](bulk_step2_docshub.json).  This formula template is setup to work with Google Drive, if you are working with a different docs hub element, you will need to make adjustments based on the providers requirements (e.g. path, file name, etc).  Please note that the folder and filename are both configured in the step `generateMetadata`--adjust as needed for your use case.

IMPORTANT NOTE: for these formulas to work, you must use a common resource! You must be able to call GET `/MyCommonResource`, copy a payload that gets returned and call POST `/myCommonResource` to the other endpoint. Included are some example transformations.

## To Configure
1. Import both formulas [bulk_Step1.json](bulk_Step1.json) and [bulk_Step2.json](bulk_Step2.json)
2. Create the common resource by calling POST `/organizations/objects/MyContact/definitions` with this payload: [ObjectDefinition.json](ObjectDefinition.json)
3. Create transformations for Salesforce by calling POST `/organizations/elements/sfdc/transformations/MyContact` with: [MyContactSFDC.json](MyContactSFDC.json)
4. Create transformations for DynamicsCRM by calling POST `/organizations/elements/dynamicscrm/transformations/MyContact` with: [dynamicscrmMyContact.json](dynamicscrmMyContact.json)
5. Create a formula instance for Bulk Step 2 and capture the ID of the created formula instance.  You will need to give the Bulk Step 1 formula the instance ID for the second formula. This will let the webhook trigger the correct formula when the bulk job is completed.

### Additional Information
Flowcharts describing the formulas can be found [here](Flowchart-BulkStep1.html) and [here](Flowchart-BulkStep2.html).

For more information on how to use Cloud Elements, see our [help center](https://docs.cloud-elements.com) or our [support page](https://support.cloud-elements.com/hc/en-us).
