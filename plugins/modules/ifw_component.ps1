#!powershell

#AnsibleRequires -CSharpUtil Ansible.Basic

### Input parameters
$spec = @{
    options = @{
        state = @{ type = "str"; choices = "absent", "present", "latest"; default = "present" }
        name = @{ type = "list"; elements = "str"; required = $true; aliases = "component" }
    }
    supports_check_mode = $true
}


### Module initilization
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)


### Make use of input parameters
$Changed = $false
$State = $module.Params.state
$Components = $module.Params.name


### Main code
# Check if IfW is installed
if (-Not (Get-Command | Where-Object -Property Name -EQ "Install-IcingaComponent")) {
    throw "Necessary command 'Install-IcingaComponent' was not found. Is IfW installed?"
}

# Get list of installed components
function Get-InstalledComponentList () {
    param(
    );

    $ComponentList = Get-IcingaInstallation
    return $ComponentList
}

# Get list of available components
function Get-AvailableComponentList () {
    param(
    );

    $AvailableComponents = (Get-IcingaComponentList).Components
    return $AvailableComponents
}


function Install-Component () {
    param(
        [String]$Component,
        [String]$Version,
        [Switch]$CheckMode
    );

    if ($CheckMode) {
        return
    }

    Install-IcingaComponent `
        -Name $Component `
        -Version $Version `
        -Confirm `
        -Force `
        | Out-Null
}


function Remove-Component () {
    param(
        [String]$Component,
        [Switch]$CheckMode
    );

    if ($Component -EQ "framework") {
        throw "Refusing to remove component '$($Component)'!"
    }

    if ($CheckMode) {
        return
    }

    Uninstall-IcingaComponent `
        -Name $Component `
        -Confirm `
        | Out-Null
}



$Added = @(
)
$Removed = @(
)

$InstalledComponents = Get-InstalledComponentList
$AvailableComponents = Get-AvailableComponentList

foreach ($Component in $Components) {
    $NeedsInstallation = $false

    # Set version to specified version or to latest if state == latest and no version is specified
    $Name, $Version = $Component.ToLower() -Split ":"

    $CurrentVersion = $InstalledComponents.$Name.CurrentVersion
    $LatestVersion = $AvailableComponents.$Name

    # Allow shorthand "<NAME>:" to mean "<NAME>:latest"
    if ($Version -EQ "latest" -Or $Version -EQ "") {
        $Version = $LatestVersion
    }

    switch ($State) {
        "present" {
            # If component is not installed or installed in wrong version
            if ($InstalledComponents.Keys -NotContains $Name)  {
                if ($Version -EQ $null) {
                    $Version = $LatestVersion
                }
                $NeedsInstallation = $true

            } elseif ($Version -NE $null -And $Version -NE $CurrentVersion) {
                $NeedsInstallation = $true
            }

        }
        "latest" {
            # Mark any component with lower current version than 'latest' for install, unless component has a version specified
            # If a version is specified, check if component is already installed in that version
            if ($Version -EQ $null) {
                $Version = $LatestVersion

            }
            if ($Version -NE $LatestVersion) {
                if ($Version -NE $CurrentVersion) {
                    $NeedsInstallation = $true
                }
            } elseif ($CurrentVersion -NE $LatestVersion) {
                $Version = $LatestVersion
                $NeedsInstallation = $true
            }
        }
        "absent" {
            if ($InstalledComponents.Keys -Contains $Name)  {
                Remove-Component `
                    -Component $Name `
                    -CheckMode:$CheckMode
                $Removed += @{
                    name = $Name
                    version = $CurrentVersion
                }
                $Changed = $true
            }
        }
    }
    # For states "present" and "latest"
    if ($NeedsInstallation) {
        Install-Component `
            -Component $Name `
            -Version $Version `
            -CheckMode:$CheckMode
        $Added += @{
            name = $Name
            version = $Version
        }
        $Changed = $true
    }
}



### Module return
$module.Result.added = $Added
$module.Result.removed = $Removed
$module.Result.changed = $Changed
$module.ExitJson()
