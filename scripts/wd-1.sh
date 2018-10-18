#!/usr/bin/zsh
/usr/bin/rsync --delete -aAXvh / \
    --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found","/swapfile"} \
    --rsync-path="sudo rsync" \
    /mnt/WD-1/backups/root
