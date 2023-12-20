# yadf_bypass
Yet another disable_functions bypass. Nothing really new, just another way of doing the same thing. Tested in PHP 7.4/8.2 on x86_64 linux.

# Using
*You'll need to run **yadf** on the same arch as the target (or compile the shared object for the target's arch).*
- Edit the rev.sh file, or create yours
- Generate the malicious PHP file with:
```python
./yadf.py --input rev.sh --output malicious.php
```
- Upload the malicious.php file
- pwn

# Working logic
**yadf** uses a lockfile to determine if the shell has already been spawned, so that the webserver does not try to spawn a new one, preventing an unintentional DoS on the webserver. Without this, the webserver will be executing our shared object everytime and thus trying to spawn the reverse shell, leading to an infinite loop causing the unavailability of the webserver.
![image](https://github.com/0xbhsu/yadf_bypass/assets/152667761/6a2d1d0c-944f-479e-a978-8cf81ae75718)

The malicious PHP file generated starts by removing the lockfile and setting the **LD_PRELOAD** with our shared object file compiled earlier. It uses the /dev/shm directory to store the files, which is a "secure" and "no traces" directory.

# Functions dependency
That said, the target must not have blacklisted the **putenv()** function, since we need to update the **LD_PRELOAD** variable to be able to bypass the disable_function properly. In a cenario where the php.ini does not have the putenv() function in disable_functions option, **yadf** will work as expected; otherwise, it will not.

# TODO
- [ ] Test on different archs
- [ ] Test on different PHP versions
- [ ] Test on different distros
- [ ] Implement Windows support

# Reference & Help
[Chankro](https://github.com/TarlogicSecurity/Chankro/)

[Bshell](https://github.com/verctor/BShell/)

[Bypass_Disable_functions_Shell](https://github.com/l3m0n/Bypass_Disable_functions_Shell)

Boitatech

