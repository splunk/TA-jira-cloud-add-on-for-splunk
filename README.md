# JIRA Clound Add-on for Splunk

> The **JIRA Clound Add-on for Splunk** uses the _Jira REST API_ to fetch audit records from Jira and ingest them into Splunk.

## Getting Started
This is a TA to pull in data from Jira REST API. 
The [auditing](https://developer.atlassian.com/cloud/jira/platform/rest/v3/#api-group-Audit-records) endpoint is being hit to fetch data for the audit records. 

### Getting Jira API Token
- Get the proper permission: `Jira Administrators` global permission.
Please follow the instruction [here](https://confluence.atlassian.com/adminjiracloud/managing-global-permissions-776636359.html) to setup the proper permission.
- Get your API token
Please follow the instruction [here](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) to create an API token. Copy it to clipboard, then paste the token to elsewhere to save.

#### Installation and Configuration Steps
This application can be installed on-prem and cloud. 

##### Installation Steps for `on-prem`
Install the TA on one of the Heavy Forwarder(s).

##### Installation Steps for `cloud`
Create a support ticket with `APP-CERT` reference to get it installed on the Cloud instance *OR* follow the cloud-ops steps to install non-published applications.

#### Configuration steps
The configuration steps are common for `on-prem` and `cloud`. Please follow the following steps in order:
1. Open the Web UI for the Heavy Forwarder (or IDM).
2. Access the TA from the list of applications.
3. Create an input.
- Click on `Inputs` button on the top left corner.
- Click on `Create New Input` button on the top right corner.
- Enter the following details in the pop up box:
    - **Name** (_required_): Unique name for the data input.
    - **Interval** (_required_): Time interval of input in seconds. 
    - **Index** (_required_): Index for storing data.
    - **Base URL** (_required_): The Base URL. Must start with "https". For example, `https://your-domain.atlassian.net`
    - **username** (_required_): Jira account Email Address.
    - **API Token** (_required_): Jira API Token.
    - **Start Time** (_required_): The date and time on or after which returned audit records must have been created. Format: YYYY-MM-DDThh:mm:ss
- Click on the `Add` green button on the bottom right of the pop up box.

## Versions Supported

  - Tested for installation and basic ingestion on Splunk 8.0.1, 8.0.0, 7.3, 7.2, and 7.1 based on Jira test account.


> Built by Splunk's FDSE Team (#team-fdse).

## Reference 
- This Add-on was built via [Splunk Add-On Builder](https://docs.splunk.com/Documentation/AddonBuilder/3.0.1/UserGuide/Thirdpartysoftwarecredits).

## Credits & Acknowledgements
* Yuan Ling
* Mayur Pipaliya