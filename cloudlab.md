You can do your labs for CS 523 using CloudLab in case you don't have the environment.
CloudLab is a research facility which provides bare-metal access and control over a substantial set of computing, storage, and networking resources.
If you haven’t worked in CloudLab before, you need to register a CloudLab account.

This tutorial walks you through the CloudLab registration process and shows you how to start an experiment in CloudLab.

Most importantly, it introduces our policies on using CloudLab that will be enforced throughout the semester.

## Register A CloudLab Account
To register an account, please visit http://cloudlab.us and create an account using your UIUC email address as login.
Note that an SSH public key is required to access the nodes CloudLab assigns to you; if you are unfamiliar with creating and using ssh keypairs, we recommend taking a look at the first few steps in GitHub’s guide to generating SSH keys. (Obviously, the steps about how to upload the keypair into GitHub don’t apply to CloudLab.) 
Click on Join Existing Project and enter `cs523-uiuc-sp24` as the project name.
Then click on Submit Request.
The instructor/TA will approve your request.
If you already have a CloudLab account, simply request to join the `cs523-uiuc-sp24` project.

## Start An Experiment
To initiate a new experiment, navigate to your CloudLab dashboard.
Click on the "Experiments" tab located in the upper left corner, and then choose "Start Experiment."

Proceed by clicking "Next" to advance to the next panel.
At this stage, assign a name to your experiment using the format netid-ExperimentName.

The default "small-lan:37" profiles allows you to choose the number of machines, the OS image, and optionally the physical node type.
We recommend Ubuntu 22.04 as the OS image, and c8220/c6420/c6320/c220g5/c220g2/c220g1 depending on the resource availability.
For more details on the hardware provided by CloudLab, refer to this [resource](https://www.cloudlab.us/resinfo.php).

Once you've selected the cluster, proceed to instantiate the experiment.
Upon completion, you will receive the ssh login command.
Attempt to log in to the machine and verify the number of CPU cores and available memory on the node.

## Policies on Using CloudLab Resources
Since the machines assigned to you are shared research resources,
we ask you not to retain these nodes for extended periods.
CloudLab initially provides users with a 16-hour allocation, with the option to extend it further.
Effectively manage your time by holding nodes only when actively working on assignments.
Use private git repo to store your code and remember to terminate the nodes when not in use.
If an extension is necessary, limit it to no more than 7 days.

Please refer to the [CloudLab policy](https://www.cloudlab.us/aup.php)
