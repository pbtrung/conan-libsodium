from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "pbtrung")


class LibsodiumTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libsodium/1.0.12@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure(self, source_dir=self.conanfile_directory, build_dir="./")
        cmake.build(self)

    def imports(self):
        self.copy("*.dll", "bin", "lib")
        self.copy("*.dylib", "bin", "lib")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
