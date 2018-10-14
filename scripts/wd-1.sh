#!/usr/bin/zsh
/usr/bin/rsync --delete -aAXv / \
    --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found","/swapfile"} \
    /mnt/WD-1/backups/root
