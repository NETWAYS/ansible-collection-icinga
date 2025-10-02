#!powershell

#AnsibleRequires -CSharpUtil Ansible.Basic

### Input parameters
$spec = @{
    options = @{
        state = @{ type = "str"; choices = "absent", "present"; default = "present" }
        command = @{ type = "str"; required = $true }
        arguments = @{ type = "dict"; required = $false; default = @{} }
    }
    supports_check_mode = $true
}


### Module initilization
$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)


### Make use of input parameters
$Changed = $false
$State = $module.Params.state
$Command = $module.Params.command
$Arguments = $module.Params.arguments

# Sanetize $Arguments, prepend "-" to get "<COMMAND> -<FLAG> <VALUE>"
$TmpArguments = @{}
foreach ($Argument in $Arguments.Keys) {
    if (-Not $Argument.StartsWith("-")) {
        $TmpArguments."-$($Argument)" = $Arguments.$Argument
    }
}
$Arguments = $TmpArguments


### Main code
# Check if IfW is installed
if (-Not (Get-Command | Where-Object -Property Name -EQ "Show-IcingaRegisteredBackgroundDaemons")) { 
    throw "Necessary command 'Show-IcingaRegisteredBackgroundDaemons' was not found. Is IfW installed?"
}

# Check that $Command is valid and available
if (-Not (Get-Command | Where-Object -Property Name -EQ $Command)) { 
    throw "Necessary command '$($Command)' was not found."
}


# Check if BackgroundDaemon for given command exists
function BackgroundDaemon-Exists () {
    param(
        [String]$Command
    );

    $Exists = (Show-IcingaRegisteredBackgroundDaemons) -Contains $Command
    return $Exists
}

# Check if given command arguments are equal to existing command arguments
function ArgumentsAreEqual () {
    param(
        $Arguments,
        $ExistingArguments
    );

    $ArgumentsAreEqual = $true
    foreach ($Key in $Arguments.keys) {
        if ($Arguments.$Key -NE $ExistingArguments.$Key) {
            $ArgumentsAreEqual = $false
            break
        }
    }
    return $ArgumentsAreEqual
}

# Get existing arguments for given command
function Get-ExistingArguments () {
    param(
        [String]$Command
    );

    $Arguments = (Read-IcingaPowerShellConfig).BackgroundDaemon.EnabledDaemons."$($Command)".Arguments

    return $Arguments
}



$CommandIsRegistered = BackgroundDaemon-Exists -Command $Command
$ExistingArguments = Get-ExistingArguments -Command $Command
$ArgumentsAreEqual = ArgumentsAreEqual -Arguments $Arguments -ExistingArguments $ExistingArguments


# Update if needed
if ($State -EQ "absent" -And $CommandIsRegistered) {
    if (-Not $module.CheckMode) {
        Unregister-IcingaBackgroundDaemon `
            -BackgroundDaemon $Command | Out-Null
    }
    $Changed = $true

} elseif ($State -EQ "present" -And (-Not $CommandIsRegistered -Or -Not $ArgumentsAreEqual)) {
    if (-Not $module.CheckMode) {
        Register-IcingaBackgroundDaemon `
            -Command $Command `
            -Arguments $Arguments | Out-Null
    }
    $Changed = $true
}

$Before = @{
    command = (&{ if ($CommandIsRegistered) { $Command } else { $null } } )
    arguments = (&{ if ($CommandIsRegistered) { $ExistingArguments } else { $null } } )
}
$After = @{
    command = (&{ if ($State -EQ "present") { $Command } else { $null } } )
    arguments = (&{ if ($State -EQ "present") { $Arguments } else { $null } } )
}



### Module return
$module.Result.before = $Before
$module.Result.after = $After
$module.Result.changed = $Changed
$module.ExitJson()
