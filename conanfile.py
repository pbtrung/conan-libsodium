from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import download, unzip
import os


class LibsodiumConan(ConanFile):
    name = "libsodium"
    version = " "
    if self.settings.os != "Windows":
        src_dir = "%s-%s" % (name, version)
    else:
        src_dir = "%s-%s-msvc" % (name, version)
    description = "The Sodium crypto library"
    license = "https://raw.githubusercontent.com/jedisct1/libsodium/master/LICENSE"
    url = "https://github.com/pbtrung/conan-libsodium"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        if self.settings.os != "Windows":
            zip_name = "libsodium-%s.tar.gz" % self.version
        else:
            zip_name = "libsodium-%s-msvc.zip" % self.version
            
        url = "https://download.libsodium.org/libsodium/releases/%s"
        download(url % zip_name, zip_name, verify=False)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        if self.settings.os != "Windows":
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                configure_command = "./configure"
                configure_command += " --prefix=" + os.getcwd()
                with tools.chdir(self.src_dir):
                    self.run(configure_command)
                    self.run("make -j " + str(max(tools.cpu_count() - 1, 1)))
                self.run("make install")
        else:
            pass
        
    def package(self):
        if self.settings.os != "Windows":
            self.copy("*.h", dst="include", src="include", keep_path=True)
            self.copy("*.so*", dst="lib", src="lib", keep_path=False)
            self.copy("*.la", dst="lib", src="lib", keep_path=False)
            self.copy("*.pc", dst="lib/pkgconfig", src="lib", keep_path=False)
            self.copy("*.a", dst="lib", src="lib", keep_path=False)
        else:
            self.copy("*.h", dst="include", src="include", keep_path=True)
            if self.settings.arch == "x86":
                if self.settings.compiler == "Visual Studio":
                    if self.settings.build_type == "Debug":
                        if self.settings.compiler.version == "10":
                            package_windows(self, "Win32", "Debug", "v100")
                        elif self.settings.compiler.version == "12":
                            package_windows(self, "Win32", "Debug", "v120")
                        elif self.settings.compiler.version == "14":
                            package_windows(self, "Win32", "Debug", "v140")
                    elif self.settings.build_type == "Release":
                        if self.settings.compiler.version == "10":
                            package_windows(self, "Win32", "Release", "v100")
                        elif self.settings.compiler.version == "12":
                            package_windows(self, "Win32", "Release", "v120")
                        elif self.settings.compiler.version == "14":
                            package_windows(self, "Win32", "Release", "v140")
            elif self.settings.arch == "x86_64":
                if self.settings.compiler == "Visual Studio":
                    if self.settings.build_type == "Debug":
                        if self.settings.compiler.version == "10":
                            package_windows(self, "x64", "Debug", "v100")
                        elif self.settings.compiler.version == "12":
                            package_windows(self, "x64", "Debug", "v120")
                        elif self.settings.compiler.version == "14":
                            package_windows(self, "x64", "Debug", "v140")
                    elif self.settings.build_type == "Release":
                        if self.settings.compiler.version == "10":
                            package_windows(self, "x64", "Release", "v100")
                        elif self.settings.compiler.version == "12":
                            package_windows(self, "x64", "Release", "v120")
                        elif self.settings.compiler.version == "14":
                            package_windows(self, "x64", "Release", "v140")
    
    def package_windows(self, arch, build_type, compiler_version):
        src_dir = "%s/%s/%s" % (arch, build_type, compiler_version)
        self.copy("*", dst="dynamic", src="%s/dynamic" % src_dir, keep_path=False)
        self.copy("*", dst="ltcg", src="%s/ltcg" % src_dir, keep_path=False)
        self.copy("*", dst="static", src="%s/static" % src_dir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["sodium"]
