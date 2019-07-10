# -*- coding: utf-8 -*-

from conans import ConanFile, tools, CMake
import os


class TestPackageConan(ConanFile):
    name = "test_package"
    version = "0.0.1"
    exports_sources = "*"
    generators = "virtualenv", "cmake"
    build_requires = "gcc-arm-none-eabi_installer/8-2018-q4-major@matt1795/testing"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_folder)
        cmake.build()

    def test(self):
        pass
