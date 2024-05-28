import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import subprocess
import shutil
import os



class BareboneBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Barebone Builder")

        # Janela amarela
        self.root.configure(bg='yellow')

        # Área de texto
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Botões
        self.build_button = tk.Button(self.root, text="Build", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="Run", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="unmount", command=self.copy_file)
        self.copy_button.pack(pady=5)

    def execute_command(self, command,show:bool):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            self.text_area.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            if show:
                self.text_area.insert(tk.END,f"Error executing command:\n{e.output}")

    def build_kernel(self):#filename = tk.filedialog.askdirectory(title="Select folder to build")
        self.text_area.delete(1.0, tk.END)
        f1=open("f1","w")
        
        f1.close()
        self.text_area.insert(tk.END,f"writing 8 mega...")
        self.execute_command('dd if=/dev/zero of="initrd.img" bs=1k count=8000',True)
        self.execute_command('sudo mke2fs "initrd.img" -F -m 0 -b "8000" ',True)
        self.execute_command('sudo chmod 777 "initrd.img"',True)
        self.execute_command('sudo chmod 777 "f1"',True)
        
    def run_kernel(self):
        self.text_area.delete(1.0, tk.END)
        self.execute_command("mkdir /mnt/isos",False)
        self.execute_command("sudo chmod 777 initrd.img",False)
        self.execute_command("sudo chmod 777 /mnt/isos",False)
        self.execute_command('sudo mount "initrd.img" /mnt/isos -t ext2 -o loop=/dev/loop0',True)
        
        self.execute_command('mkdir /mnt/isos/bin',True)
        self.execute_command('mkdir /mnt/isos/sys',True)
        self.execute_command('mkdir /mnt/isos/usr',True)
        self.execute_command('mkdir /mnt/isos/usr/bin',True)
        self.execute_command('mkdir /mnt/isos/proc',True)
        self.execute_command('mkdir /mnt/isos/tmp',True)
        self.execute_command('mkdir /mnt/isos/dev',True)
        
        
        
        self.execute_command('cp ./f1 /mnt/isos/dev/stdio',True)
        self.execute_command('cp ./f1 /mnt/isos/dev/stdout',True)
        self.execute_command('cp ./f1 /mnt/isos/dev/stdin',True)
        self.execute_command('cp ./f1 /mnt/isos/dev/tty2',True)
        self.execute_command('cp ./f1 /mnt/isos/dev/tty1',True)
        self.execute_command('cp ./f1 /mnt/isos/dev/console',True)
        self.execute_command('cp ./f1 /mnt/isos/dev/zero',True)
        self.execute_command('cp ./f1 /mnt/isos/dev/null',True)
        self.execute_command('cp /usr/bin/bash /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/sh /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/echo /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/mount /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/printf /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/cp /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/mkdir /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/ls /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/cat /mnt/isos/bin',True)
        self.execute_command('cp /usr/bin/ps /mnt/isos/bin',True)
        self.execute_command('cp /mnt/isos/bin/* /mnt/isos/usr/bin',True)
       
        self.execute_command("nautilus --browser /mnt/isos",False)


    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        
        if 0==0:
            self.execute_command("sudo umount /mnt/isos",True)
            


if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
