# -*- coding: utf-8 -*-

from conans import ConanFile, tools, CMake
import os


class TestPackageConan(ConanFile):
    name = "test_package"
    version = "0.0.1"
    exports_sources = "*"
    generators = "virtualenv", "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_folder)
        cmake.build()

    def test(self):
        pass
