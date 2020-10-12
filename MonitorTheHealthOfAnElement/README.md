# How to monitor the health of your elements
The recommended way to monitor the health of an element is to create a formula. Import [ElementHealthFormula.json](ElementHealthFormula.json) into your account and play around with it. It is designed to run every 15 minutes and make an API call against an instance and send an email if the request fails.

A flowchart describing the formula can be found [here](Flowchart-HealthCheck.html).

For more information on how to use Cloud Elements, see our [help center](https://docs.cloud-elements.com)
or our [support page](https://support.cloud-elements.com/hc/en-us).

## How do I use the formula?
### Import the formula into your Cloud Elements environment:
You have two options when choosing how to import this formula. You can use the Formulas UI or the doctor.
1. Using the Formulas UI:
  * Click the `BUILD NEW FORMULA` button [found on this page](https://my-staging.cloudelements.io/formulas) and select `Import` from the dropdown.
  * Find the file `ElementHealthFormula.json` in the MonitorTheHealthOfAnElement directory and import it.
2. Using the doctor:
  * Insure you have the correct version of the doctor installed locally. Run the command `npm i -g ce-util` to install the latest, non-beta version of the doctor. You can find full instructions [here](https://www.npmjs.com/package/ce-util/v/2.2.5) as well. You will need to upload the file from TheDoctor directory, as files uploaded with the doctor have a different structure than files imported via UI.
  * In the terminal, from the MonitorTheHealthOfAnElement/TheDoctor directory, run the command:
    ```
    doctor upload formulas <accountNickName> -f ElementHealthFormula.json
    ```
### Use your formula:
1. Create an instance of the formula and a source element instance (you can choose any element you'd like)! You will enter the email you'd like to be notified at here.
2. In the `test` step, notice that the `API` field has `/accounts`. If the element you chose does not have an `/accounts` endpoint, you will need to update this field first.
3. Now, if a failed call is made during one of the 15 minute polls, you will be sent an email.
3. Feel free to play around with the formula until it suits your specific needs.