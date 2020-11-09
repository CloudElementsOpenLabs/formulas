# Stream An Image Between Two Elements Example
This Formula provides an example of streaming an image file from a storage/docs hub Element (the example uses `box`) and `Knowledge Owl`, a documentation management tool. The `box` Element can be found in our [Elements Catalog](https://docs.cloud-elements.com/home/catalog) while the `Knowledge Owl` Element is one of our Community Elements. You can easily import the `Knowledge Owl` Element in the UI under the Community Elements tab in the Elements UI.

Included in this folder:
- StreamImageBetweenElements.json, the example Formula template
- Flowchart-StreamImageBetweenElements.html
- TheDoctor directory (use the file in this directory to upload your Formula via the doctor, Cloud Element's CLI tool)

## How do I use the Formula?
### Import the Formula into your Cloud Elements environment:
You have two options when choosing how to import this Formula. You can use the Formulas UI or the doctor.
1. Using the Formulas UI:
  * Download the file [StreamImageBetweenElements.json](StreamImageBetweenElements.json) from the GitHub repo.
  * Click the `BUILD NEW FORMULA` button [found on this page](https://my-staging.cloudelements.io/formulas) and select `Import` from the dropdown.
  * Find the file `StreamImageBetweenElements.json` locally and import it.
2. Using the doctor:
  * Insure you have the correct version of the doctor installed locally. Run the command `npm i -g ce-util` to install the latest, non-beta version of the doctor. You can find full instructions [here](https://www.npmjs.com/package/ce-util) as well. You will need to upload the file from TheDoctor directory, as files uploaded with the doctor have a different structure than files imported via UI.
  * In the terminal, from the StreamImageBetweenElements/TheDoctor directory, run the command:
    ```
    doctor upload formulas <accountNickName> -f StreamImageBetweenElements.json
    ```

### Use your Formula:

#### Prerequisites
To use this Formula you will need an authenticated instance of both the `box` Element as well as the `Knowledge Owl` Element.
* Authenticate an instance of `box` in the Elements UI, ensuring events are enabled.
* Import the `Knowledge Owl` Element from the Elements UI under the Community tab.
* You will need a `Knowledge Owl` account to generate an API Key for authentication, as well as a first project for the required project_id. Creating and using an account in `Knowledge Owl` is free.
* Authenticate an instance of `Knowledge Owl` using your API Key and a dummy password (a default password is provided).

#### Steps
1. Create an instance of the Formula and a source element instance (the template was built using Quickbooks Online)
2. The trigger for this Formula is event-based, listening for the addition (creation) of a file in a `box` folder. Add an image file to your `box` folder that has events enabled.
3. In the Formula UI, open your Formula and toggle on `Debug Logging` so that all your steps appear.
4. Click `Try It Out`, selecting the event payload of the image that was just added to `box` as the trigger.
5. Create a Formula Instance by choosing the correct `box` and `Knowledge Owl` instances, and inputting the projectId (from `Knowledge Owl`) and the name for your image.
6. Click `Run`, then, once your Formula is complete, go login to `Knowledge Owl` to see that it now exists in your Files Library.

##### Customize
You can choose to customize this Formula in many ways. Currently, the Formula is streaming from `box` to `Knowledge Owl`, but you can easily change these two Elements. You will need to update the constructQueriesAndHeaders script so that your queries are consistent with the new Elements you choose.

If you decide to use a new Element to stream the file **to**, make sure the resource works in the Elements UI first. See this [image](ResourceImageConfiguration.png) as an example for how to set up your resource, or import the `Knowledge Owl` Element and checkout the `POST` `/files` endpoint. The `POST` `/files` resource in `Knowledge Owl` sends its data as multipart/form-data.