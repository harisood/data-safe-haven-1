## Make a new deployment VM
### Deploy a new VM
- Go to the `secure_research_environment/azure-vms` directory
- Run `./deploy_azure_deployment_pool_vm.sh -s "<sh-management-subscription-name>" -i <shm-id> -n <number>` where `<number>` is a zero padded number one greater than largest one currently used by an existing deployment VM (eg. 01, 02, etc.)
- This will deploy a VM that you can use for deployment (ie. it has the necessary tools already installed)
- You will need to take the public keypair output at the end of deployment and add it to the `Settings > Deploy Keys` tab in the safe haven repo on GitHub. The keys **do not** need write access, so leave this box **unchecked**. 

### VM information
- The username is `atiadmin`
- The password is the `deployment-vm-admin-password` secret in the `kv-shm-<shm-id>` KeyVault in the `RG_SHM_SECRETS` resource group of the `<sh-management-subscription-name>` subscription
- Installed tools are:
    - mosh
    - azure-cli
    - powershell
    - pip
    - eternal terminal
- You will need to clone the safe haven repo via `git clone git@github.com:alan-turing-institute/data-safe-haven.git`. This will automatically authenticate using the VM's `id_rsa` SSH key you just added to the safe haven repo as a deploy key.


## Use a deployment VM to deploy to the Safe Haven
The VM(s) you want to use may be stopped to save money, so you may need to start the VM(s) you want to use from the Azure Portal
- Connect to the VM using `ssh atiadmin@sh-deployment-<shm-id>-<number>.westeurope.cloudapp.azure.com` (replacing `0X` with the zero padded number of the deployment VM you want to use; and using the password from the `deployment-vm-admin-password` secret in `kv-shm-<shm-id>` KeyVault in the `RG_SHM_SECRETS` resource group of the `<sh-management-subscription-name>` subscription)
- If you have not yet cloned the safe haven GitHub repository, run `git clone git@github.com:alan-turing-institute/data-safe-haven.git`
- Navigate to the folder in the safe haven repo with the deployment scripts using `cd data-safe-haven/secure_research_environment/sre_deploy_scripts/07_deploy_compute_vms`
- Checkout the master branch using `git checkout master` (or the deployment branch for the SHM environment you are deploying to - you may need to run `git fetch` first if not using `master`)
- Ensure you have the latest changes locally using `git pull`
- Ensure you are authenticated in the Azure CLI using `az login`
- Open a Powershell terminal with `pwsh`
- Ensure you are authenticated within the Powershell `Az` module by running `Connect-AzAccount` within Powershell
- Run `git fetch;git pull;git status;git log -1 --pretty="At commit %h (%H)"` to verify you are on the correct branch and up to date with `origin` (and to output this confirmation and the current commit for inclusion in the deployment record).
- Deploy a new VM into a SHM environment using the `Create_Compute_VM.ps1` script, entering the SRE ID, VM size (optional) and last octet of the desired IP address (next unused one between 160 and 199)
- After deployment, copy everything from the `git fetch;...` command and its output to the command prompt returned after the VM deployment and paste this into the deployment log (e.g. a Github issue used to record VM deployments for a DSG or set of DSGs)