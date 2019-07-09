# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class TestPackageConan(ConanFile):
    name = "test_package"
    version = "0.0.1"

    def build(self):
        pass

    def test(self):
        pass
