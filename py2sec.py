import getopt
import os, sys
import subprocess
import shutil


class Task:
    def __init__(self):
        self.help_show = '''
py2sec is a Cross-Platform, Fast and Flexible tool to change the .py to .so(Linux and Mac) or .pdy(Win).
You can use it to hide the source code of py
It can be called by the main func as "from module import * "
py2sec can be used in the environment of python2 or python3

Usage: python py2sec.py [options] ...

Options:
  -v,  --version    Show the version of the py2sec
  -h,  --help       Show the help info
  -p,  --py         Python version, default value == 3
                    Example: -p 3  (means you tends to encrypt python3)
  -d,  --directory  Directory of your project (if use -d, you encrypt the whole directory)
  -f,  --file       File to be transfered (if use -f, you only encrypt one file)
  -m,  --maintain   List the file or the directory you don't want to transfer
                    Note: The directories should be surrounded by '[]', and must be the relative path to -d's value 
                    Example: -m __init__.py,setup.py,[poc/,resource/,venv/,interface/]
  -x,  --nthread    number of parallel thread to build jobs

Example:
  python py2sec.py -f test.py
  python py2sec.py -f example/test1.py
  python py2sec.py -d example/ -m test1.py,[bbb/]
        '''
        self.py_ver = '3'
        self.file_name = ''
        self.file_flag = 0
        self.file_list = []
        self.root_name = ''
        self.dir_flag = 0
        self.dir_list = []
        self.m_list = ''
        self.nthread = '1'


    def getOpt(self):       
        try:
            options,_ = getopt.getopt(sys.argv[1:],"vhp:d:f:m:x:",["version","help","py=","directory=","file=","maintain=", "nthread="])
        except getopt.GetoptError:
            print("Get options Error")
            print(self.help_show)
            sys.exit(1)

        for key, value in options:
            if key in ["-h", "--help"]:
                print(self.help_show)
            elif key in ["-v", "--version"]:
                print("py2sec version 0.2")
            elif key in ["-p", "--py"]:
                self.py_ver = value
            elif key in ["-d", "--directory"]:
                if self.file_name:
                    print("Error, don not use -d -f at the same time")
                    print(self.help_show)
                    sys.exit(1)
                if value[-1] == '/':
                    self.root_name = value[:-1]
                else:
                    self.root_name = value
            elif key in ["-f", "--file"]:
                if self.root_name:
                    print("Error, don not use -d -f at the same time")
                    print(self.help_show)
                    sys.exit(1)
                self.file_name = value
            elif key in ["-m", "--maintain"]:
                self.m_list = value
                if self.m_list.find(",[") != -1:
                    tmp = self.m_list.split(",[")
                    self.file_list = tmp[:-1]
                    self.dir_list = tmp[-1]
                    self.file_flag = 1
                    self.dir_flag = 1
                elif self.m_list.find("[") != -1:
                    self.dir_list = self.m_list[1:-1]
                    self.dir_flag = 1
                else:
                    self.file_list = self.m_list.split(",")
                    self.file_flag = 1
                if self.dir_flag == 1:
                    dir_tmp = self.dir_list.split(",")
                    self.dir_list=[]
                    for d in dir_tmp:
                        if d[-1] == ']':
                            d = d[:-1]
                        if d.startswith("./"):
                            self.dir_list.append(d[2:])
                        else:
                            self.dir_list.append(d)
            elif key in ["-x", "--nthread"]:
                self.nthread = value

    def getEncryptFileList(self):
        encrypt_fi_list = []
        if self.root_name != '':
            if not os.path.exists(self.root_name):
                print("No such Directory, please check or use the Absolute Path")
                sys.exit(1)

            try:
                for root, _, files in os.walk(self.root_name):
                    for fi in files:
                        if self.m_list != '':
                            skip_flag = 0
                            if self.dir_flag == 1:
                                for dir_c in self.dir_list:
                                    if (root+'/').startswith(self.root_name + '/' + dir_c):
                                        skip_flag = 1
                                        break
                                if skip_flag:
                                    continue
                            if self.file_flag == 1:
                                if fi in self.file_list:
                                    continue

                        if fi.endswith(".py"):
                            encrypt_fi_list.append("%s/%s" % (root,fi))
            except Exception as err:
                print(err)
        if self.file_name != '':
            if self.file_name.endswith(".py"):
                encrypt_fi_list.append(self.file_name)
            else:
                print("Make sure you give the right name of py file")

        return encrypt_fi_list

    def genSetup(self, encrypt_fi_list):
        if os.path.exists("setup.py"):
            os.remove("setup.py")
        with open("setup.py.template", "r") as f:
            template = f.read()
        cont = template % ('", "'.join(encrypt_fi_list), self.nthread, self.py_ver)
        with open("setup.py", "w") as f:
            f.write(cont)
    
    def pyEncrypt(self):
        if os.path.exists("build/"):
            shutil.rmtree("build/")
        if os.path.exists("tmp_build/"):
            shutil.rmtree("tmp_build/")
        p = subprocess.Popen("python setup.py build_ext > result/log.txt", shell=True, stderr=subprocess.PIPE)
        p.wait()
        err = p.stderr.readlines()
        if err:
            if self.py_ver == '3':
                p = subprocess.Popen("python3 setup.py build_ext > result/log.txt", shell=True, stderr=subprocess.PIPE)
                p.wait()
            else:
                p = subprocess.Popen("python2 setup.py build_ext > result/log.txt", shell=True, stderr=subprocess.PIPE)
                p.wait()
    

    def genProject(self):
        if not os.path.exists("result/"):
            os.mkdir("result/")
        if self.root_name:
            enc_root_name = "result/%s_encrypted"%self.root_name
            if os.path.exists(enc_root_name):
                shutil.rmtree(enc_root_name)
            shutil.copytree(self.root_name, enc_root_name)
            for root, _, files in os.walk("build/"):
                for fi in files:
                    if fi.endswith(".o"):
                        continue
                    else:
                        inner = '/'.join(root.split("/")[3:])
                        pure_root = "%s/%s" % (enc_root_name,inner)
                        tmp = fi.split(".")
                        pre_fi = "%s.py" % tmp[0]
                        pure_fi = "%s.%s" % (tmp[0],tmp[-1])
                        os.remove("%s/%s" % (pure_root, pre_fi))
                        shutil.copy("%s/%s"%(root, fi), "%s/%s"%(pure_root, pure_fi))
        if self.file_name:
            for root, _, files in os.walk("build/"):
                for fi in files:
                    if fi.endswith(".o"):
                        continue
                    else:
                        tmp = fi.split(".")
                        pure_fi = "%s.%s" % (tmp[0],tmp[-1])
                        shutil.copy("%s/%s"%(root, fi), "%s/%s"%("result", pure_fi))
                        break



if __name__ == "__main__": 
    task = Task()   
    task.getOpt()
    encrypt_fi_list = task.getEncryptFileList()
    task.genSetup(encrypt_fi_list)
    task.pyEncrypt()
    task.genProject()

