#!powershell

#AnsibleRequires -CSharpUtil Ansible.Basic

### Input parameters
$spec = @{
    options = @{
        state = @{ type = "str"; choices = "absent", "present"; default = "present" }
        command = @{ type = "list"; elements = "str"; required = $true }
        list = @{ type = "str"; choices = "whitelist", "blacklist"; default = "whitelist" }
        endpoint = @{ type = "str"; choices = "apichecks", "checker"; default = "apichecks" }
        purge = @{ type = "bool"; default = $false }
    }
    supports_check_mode = $true
}


### Module initilization
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)


### Make use of input parameters
$Changed = $false
$State = $module.Params.state
$Commands = $module.Params.command
$List = $module.Params.list
$Endpoint = $module.Params.endpoint
$Purge = $module.Params.purge

$Blacklist = $false
if ($List -EQ "blacklist") {
    $Blacklist = $true
}


# Check if RESTApiCommand exists in given endpoint and list
function RESTApiCommand-Exists () {
    param(
        [String]$Command,
        [String]$Endpoint,
        [String]$List
    );

    $Exists = (Get-IcingaPowerShellConfig -Path "RESTApi.Commands.$($Endpoint).$($List)") -Contains $Command
    return $Exists
}

function Get-ExistingRESTApiCommand () {
    param(
        [String]$Endpoint,
        [String]$List
    );

    $ExistingCommands = Get-IcingaPowerShellConfig -Path "RESTApi.Commands.$($Endpoint).$($List)"
    return $ExistingCommands
}


### Main code
# Check if IfW is installed
if (-Not (Get-Command | Where-Object -Property Name -EQ "Add-IcingaRESTApiCommand")) {
    throw "Necessary command 'Add-IcingaRESTApiCommand' was not found. Is IfW installed?"
}

$Added = @()
$Removed = @()

$ExistingCommands = Get-ExistingRESTApiCommand -Endpoint $Endpoint -List $List

# Purge every command in endpoint and list
# Simply replace with given list of commands
if ($Purge) {
    if ($State -EQ "absent") {
        $Removed += $ExistingCommands
    } else {
        $Removed += ($ExistingCommands | Where-Object { $_ -Notin $Commands })
        $Added += ($Commands | Where-Object { $_ -Notin $ExistingCommands })
    }
    if (-Not $module.CheckMode) {
        if ($State -EQ "absent") {
            Set-IcingaPowerShellConfig -Path "RESTApi.Commands.$($Endpoint).$($List)" -Value @()
        } else {
            Set-IcingaPowerShellConfig -Path "RESTApi.Commands.$($Endpoint).$($List)" -Value $Commands
        }
    }
    if ($Removed -Or $Added) {
        $Changed = $true
    }
} else {
    foreach ($Command in $Commands) {
        $CommandExists = ($ExistingCommands -Contains $Command)

        # Update if needed
        if ($State -EQ "absent" -And $CommandExists) {
            if (-Not $module.CheckMode) {
                Remove-IcingaRESTApiCommand `
                    -Command $Command `
                    -Endpoint $Endpoint `
                    -Blacklist:$Blacklist
            }
            $Removed += $Command
            $Changed = $true
        } elseif ($State -EQ "present" -And (-Not $CommandExists)) {
            if (-Not $module.CheckMode) {
                Add-IcingaRESTApiCommand `
                    -Command $Command `
                    -Endpoint $Endpoint `
                    -Blacklist:$Blacklist
            }
            $Added += $Command
            $Changed = $true
        }
    }
}


### Module return
$module.Result.added = $Added
$module.Result.removed = $Removed
$module.Result.list = $List
$module.Result.endpoint = $Endpoint
$module.Result.changed = $Changed
$module.ExitJson()
