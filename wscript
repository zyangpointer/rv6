APPNAME = 'rv6'
VERSION = '0.0.1'

# Custom tasks

from waflib import Task, TaskGen
import re

def nasm_scan(task):
    deps = []
    node = task.inputs[0]

    include = re.compile('\A%include\s+"([a-zA-Z0-9_.]+)"')

    with open(node.abspath(), "r") as f:
        for line in f:
            match = include.match(line)
            if match:
                dep = node.parent.find_resource(match.group(1))
                if not dep:
                    raise "Bla"
                deps.append(dep)
    return (deps, [])

@TaskGen.taskgen_method
@TaskGen.feature('nasm')
def nasm_f(self):
    setattr(self, 'scan', nasm_scan)


# Allow to run scripts from the same folder via rule
@TaskGen.taskgen_method
@TaskGen.feature('local')
def local_f(self):
    setattr(self, 'rule', self.path.abspath()+'/'+getattr(self, 'rule', None))



# The build script

def options(opt):
    opt.load('compiler_c')

def configure(ctx):
    ctx.load('compiler_c')

    # Find other programs needed for the build process
    ctx.find_program('nasm', var='NASM')
    ctx.find_program('ld', var='LD')
    ctx.find_program('rustc', var='RUSTC')
    ctx.find_program('qemu-system-i386', var='QEMU')
    ctx.find_program('rustc', var='RUSTC')
    ctx.find_program('objcopy', var='OBJCOPY')

    ctx.env.NASMFLAGS = '-f elf32'
    ctx.env.RUSTFLAGS = '-O --target i386-intel-linux --lib -c'
    ctx.env.CFLAGS = '-fno-pic -static -fno-builtin -fno-strict-aliasing -Wall -MD -ggdb -m32 -Werror -fno-omit-frame-pointer -fno-stack-protector -O -nostdinc -I.'



    print('Successfully configured project')

def build(ctx):
    ctx.recurse("src")

def run(ctx):
    ctx(rule='${QEMU} ${SRC}', source='src/rv6.img',  always = True)

from waflib.Build import BuildContext
class runner(BuildContext):
        cmd = 'run'
        fun = 'run'

