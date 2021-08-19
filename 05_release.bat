set tag=%DATE:~6,4%%DATE:~0,2%%DATE:~3,2%.%time:~0,2%%time:~3,2%
gh release create %tag% C:\Users\pvnn\Desktop\ToIR_Patch\toir_patch.zip --title "Tales of Innocence R - English Patch %date% %time%" --notes "Automated Release %date% %time% Story 62%%, Movie Subs 90%%, Skit 60%%, Menu 76%%, NPC 43%%"
pause