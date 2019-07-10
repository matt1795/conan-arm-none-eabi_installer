# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os

class GccArmNoneEabiInstallerConan(ConanFile):
    name = "gcc-arm-none-eabi_installer"
    version = "8-2018-q4-major"
    description = "GNU ARM Embedded Toolchain"
    topics = ("conan", "embedded", "gcc", "arm")
    url = "https://github.com/bincrafters/conan-gcc-arm-none-eabi_installer"
    homepage = "https://github.com/matt1795/conan-gcc-arm-none-eabi_installer"
    author = "Matthew Knight <mgk@gmail.com>"
    license = "GPL-3.0-only"  
    exports = ["LICENSE"]      # Packages the license for the conanfile.py
    exports_sources = "toolchain.cmake"

    # Options may need to change depending on the packaged library.
    settings = {
        "os_build": ["Windows", "Linux", "Macos"]
    }

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

    sha256_lookup = {
        "Linux": "fb31fbdfe08406ece43eef5df623c0b2deb8b53e405e2c878300f7a1f303ee52",
        "Macos": "0b528ed24db9f0fa39e5efdae9bcfc56bf9e07555cb267c70ff3fee84ec98460",
        "Windows": "be5e2f68549efaecb79bdc34ff03c06f27deb2fcec3badddb5729cfb5ce43d6b"
    }

    def source(self):
        source_url = "https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2018q4/gcc-arm-none-eabi-{}-{}.{}" \
            .format(self.version, self.os_lookup[str(self.settings.os_build)], \
                self.extension_lookup[str(self.settings.os_build)])

        print("Downloading: {}".format(source_url))

        destination = "." if self.settings.os_build != "Windows" else self._source_subfolder
        tools.get(source_url, destination=destination, sha256=self.sha256_lookup[str(self.settings.os_build)])

        if self.settings.os_build != "Windows":
            self.run("ls")
            os.rename("gcc-arm-none-eabi-" + self.version, self._source_subfolder)

    def package(self):
        self.copy(pattern="*", dst=".", src=self._source_subfolder)
        self.copy(pattern="toolchain.cmake", dst=".")

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        prefix = "arm-none-eabi-{}"
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)
        
        self.env_info.CC = prefix.format("gcc")
        self.env_info.CXX = prefix.format("g++")
        self.env_info.AR = prefix.format("ar")
        self.env_info.LD = prefix.format("ld")
        self.env_info.CONAN_CMAKE_TOOLCHAIN_FILE = os.path.join(self.package_folder, "toolchain.cmake")
        self.cpp_info.exelinkflags.append("--specs=nosys.specs")
