# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GccArmNoneEabiInstallerConan(ConanFile):
    name = "gcc-arm-none-eabi_installer"
    version = "8-2018-q4-major"
    description = "GNU ARM Embedded Toolchain"
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "gcc-arm-none-eabi_installer")
    url = "https://github.com/bincrafters/conan-gcc-arm-none-eabi_installer"
    homepage =
    "https://github.com/matt1795/conan-gcc-arm-none-eabi_installer"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os_build"

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    extension_lookup = {
        "Linux": "tar.bz2",
        "Macos": "tar.bz2",
        "Windows": "zip"
    }

    os_lookup = {
        "Linux": "linux",
        "Macos": "mac",
        "Windows": "win32"
    }

    md5_lookup = {
        "Linux": "f55f90d483ddb3bcf4dae5882c2094cd",
        "Macos": "4c0d86df0244df22bc783f83df886db9",
        "Windows": "9b1cfb7539af11b0badfaa960679ea6f"
    }

    def source(self):
        source_url =
        "https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2018q4/gcc-arm-none-eabi-{}-{}.{}"
        .format(self.version, self.os_lookup[self.settings.os_build],
                self.extension_lookup[self.settings.os_build])

        tools.get(source_url, "md5={}".format(md5.sha_lookup[self.settings.os_build])
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False  # example
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        self.copy(pattern="tool_name", dst="bin", keep_path=False)
        self.copy(pattern="tool_name.exe", dst="bin", keep_path=False)

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)
