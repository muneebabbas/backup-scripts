#!/usr/bin/zsh
/usr/bin/rsync --delete -aAXvh / \
    --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found","/swapfile"} \
    -e "ssh -i /home/muneebabbas/.ssh/id_rsa -l muneebabbas" \
    muneebabbas@backup-server-1.local:/home/muneebabbas/backups/root
