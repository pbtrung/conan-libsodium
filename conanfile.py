from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import download, unzip
import os


class LibsodiumConan(ConanFile):
    name = "libsodium"
    version = "1.0.12"
    src_dir = name + "-" + version
    description = "The Sodium crypto library"
    license = "https://raw.githubusercontent.com/jedisct1/libsodium/master/LICENSE"
    url = "https://github.com/pbtrung/conan-libsodium"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        zip_name = "libsodium-%s.tar.gz" % self.version
        url = "https://download.libsodium.org/libsodium/releases/%s"
        download(url % zip_name, zip_name, verify=False)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            configure_command = "./configure"
            configure_command += " --prefix=" + os.getcwd()
            with tools.chdir(self.src_dir):
                self.run(configure_command)
                self.run("make -j " + str(max(tools.cpu_count() - 1, 1)))
                self.run("make install")

    def package(self):
        self.copy("*.h", dst="include", src="include", keep_path=True)
        self.copy("*.so*", dst="lib", src="lib", keep_path=False)
        self.copy("*.la", dst="lib", src="lib", keep_path=False)
        self.copy("*.pc", dst="lib/pkgconfig", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["sodium"]
