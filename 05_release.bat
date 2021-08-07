set tag=%DATE:~6,4%.%DATE:~3,2%.%DATE:~0,2%
gh release create %tag% C:\Users\pvnn\Desktop\ToIR_Patch\toir_patch.zip --title "Tales of Innocence R - English Patch %date%" --notes "Automated Release %date% %time%"
pause