from conans import ConanFile, CMake, tools


class CpuinfoConan(ConanFile):
    name = "cpuinfo"
    version = "master"
    license = "MIT"
    url = ""
    description = "CPU INFOrmation library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone --depth=1 https://github.com/pytorch/cpuinfo.git .")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("CMakeLists.txt", "PROJECT(cpuinfo C CXX)",
                              '''PROJECT(cpuinfo C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)

        cmake.definitions["CPUINFO_BUILD_TOOLS"] = "OFF"
        cmake.definitions["CPUINFO_BUILD_UNIT_TESTS"] = "OFF"
        cmake.definitions["CPUINFO_BUILD_MOCK_TESTS"] = "OFF"
        cmake.definitions["CPUINFO_BUILD_BENCHMARKS"] = "OFF"

        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["cpuinfo", "clog", "pthread"]

