<#
.Synopsis
   Discovers Raspberry Pi devices on hosts subnet
.DESCRIPTION
   This script checks local network interfaces and prompts the user for the one to use. Once the selection is made the script asynchronously pings the full
   1-254 range and collects the network addresses of devices that are active. The list is compared to the know mac addresses of Raspberry Pi. Any matches are
   highleghted in output.
   The asynchronous super fast ping sweep is based on https://gist.github.com/joegasper/93ff8ae44fa8712747d85aa92c2b4c78
.EXAMPLE
   Example of how to use this cmdlet
.EXAMPLE
   Another example of how to use this cmdlet
.NOTES
   Created by piTheWay
#>




#know mac addresses
$macs=@("28-CD-C1","3A-35-41","DC-A6-32","E4-5F-01")

#find local subnet
$localnics=@((Get-NetIPAddress -AddressFamily IPv4) |where {$_.InterfaceAlias -notmatch "loopback"} )
Write-Host "`nPlease choose the network adapter connected to the same network as Raspberry Pi:`n"
For ($i = 0; $i -lt $localnics.Count; $i++) {
    Write-Host "$($i+1):  $($localnics[$i].InterfaceAlias)  $($localnics[$i].IPAddress)`n" -ForegroundColor Yellow
}

[int]$number = Read-Host "Press the number to select store"
$selectednic = $localnics[$number - 1]
write-host "You selected $($selectednic.interfacealias) $($selectednic.ipaddress)`n" -ForegroundColor Green
$subnet=$selectednic.ipaddress -replace ".{3}$"

$ips = 1..254 | ForEach-Object {"$($SubNet).$_"}
$ps = foreach ($ip in $ips) {
        (New-Object Net.NetworkInformation.Ping).SendPingAsync($ip, 250)
}
[Threading.Tasks.Task]::WaitAll($ps)
$ps.Result | Where-Object -FilterScript {$_.Status -eq 'Success' -and $_.Address -like "$subnet*"} |
Select-Object Address,Status,RoundtripTime -Unique |
ForEach-Object {
    if ($_.Status -eq 'Success'-and $_.Address -notmatch $selectednic.ipaddress) {
        write-host $_.Address
        $neighbr=Get-NetNeighbor -IPAddress $_.Address
        Write-Host " `nDiscovered IP" $($_.Address) "with mac address" $neighbr.LinkLayerAddress -ForegroundColor Cyan
        foreach ($mac in $macs) {
            if (($neighbr.LinkLayerAddress -replace ".{9}$") -contains $mac) {
                write-host $_.Address "is likely a raspberry pi!" -ForegroundColor Green
            }
        }
    }
}
