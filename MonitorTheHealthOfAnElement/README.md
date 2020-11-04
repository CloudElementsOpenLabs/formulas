# How to monitor the health of your elements
The recommended way to monitor the health of an element is to create a formula. Import [ElementHealthFormula.json](ElementHealthFormula.json) into your account and play around with it. It is designed to run every 15 minutes and make an API call against an instance and send an email if the request fails.

You can alternatively add these steps into a current Formula so that when an Element request step occurs, if an Element instance is not working it will automatically disable the Element instance and send an email notification to the email specified when setting up the instance.

**Note:** If you use the steps in this Formula to disable an Element instance, please be aware that:
1. If the request fails for any reason (ie the endpoint entered was incorrect, or the body was unable to be posted, or the vendor had an error, etc) the Element instance will be disabled and an email will be sent.
2. To re-enable the Element instance, you can make a `PUT` request to `/instances/enabled`.

For more information on how to use Cloud Elements, see our [help center](https://docs.cloud-elements.com)
or our [support page](https://support.cloud-elements.com/hc/en-us).

## How do I use the formula?
### Import the formula into your Cloud Elements environment:
You have two options when choosing how to import this formula. You can use the Formulas UI or the doctor.
1. Using the Formulas UI:
  * Find the file `ElementHealthFormula.json` in the MonitorTheHealthOfAnElement directory in github and download it locally.
  * Click the `BUILD NEW FORMULA` button [found on this page](https://my-staging.cloudelements.io/formulas) and select `Import` from the dropdown.
  * Find your Formula file and import it.
  
2. Using the doctor:
  * Ensure you have the correct version of the doctor installed locally. Run the command `npm i -g ce-util` to install the latest, non-beta version of the doctor. You can find full instructions [here](https://www.npmjs.com/package/ce-util) as well. You will need to upload the file from TheDoctor directory, as files uploaded with the doctor have a different structure than files imported via UI.
  * In the terminal, from the MonitorTheHealthOfAnElement/TheDoctor directory, run the command:
    ```
    doctor upload formulas <accountNickName> -f ElementHealthFormula.json
    ```
### Use your formula:
1. Create an instance of the formula.
  * Choose a source Element instance (you can choose any Element instance you'd like)!
  * Enter the email you'd like to be notified at here in the case of a failed and/or disabled instance.
  * Enter the object (the endpoint) you want the Formula to make a request to (it is configured for a GET request). The deafult is `ping`, which is an endpoint Cloud Elements natively supports for all Elements as a way to check the "heartbeat" of an Element instance. If you do not provide an endpoint, it will automatically choose ping.
2. Now, if a failed call is made during one of the 15 minute polls, you will be sent an email and the Element Instance will be disabled.
3. Feel free to play around with the formula until it suits your specific needs!