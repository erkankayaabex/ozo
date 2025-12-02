from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.build import check_min_cppstd
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, load
import re


class OzoConan(ConanFile):
    name = "ozo"
    license = "PostgreSQL"
    topics = ("ozo", "yandex", "postgres", "postgresql", "cpp17", "database", "db", "asio")
    url = "https://github.com/erkankayaabex/ozo"
    description = "Conan package for yandex ozo"
    settings = "os", "compiler", "build_type", "arch"
    
    # Tag, branch, or full commit SHA
    
    def source(self):
        get(self,
            f"https://github.com/erkankayaabex/ozo/archive/{self.version}.zip",
            strip_root=True)
    
    def layout(self):
        cmake_layout(self)
    
    def validate(self):
        if self.settings.os == "Windows":
            raise ConanInvalidConfiguration("OZO is not compatible with Windows")
        check_min_cppstd(self, "17")
    
    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()
    
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
    
    def package(self):
        cmake = CMake(self)
        cmake.install()
    
    def requirements(self):
        self.requires("boost/1.88.0")
        self.requires("resource_pool/0.1.0", headers=True, libs=False)
        self.requires("libpq/15.5")
    
    def package_id(self):
        del self.info.settings.build_type
        del self.info.settings.compiler
    
    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        
        self.cpp_info.components["_ozo"].includedirs = ["include"]
        self.cpp_info.components["_ozo"].requires = [
            "boost::boost",
            "boost::system",
            "boost::thread",
            "boost::coroutine",
            "resource_pool::resource_pool",
            "libpq::pq",
        ]
        self.cpp_info.components["_ozo"].defines = [
            "BOOST_COROUTINES_NO_DEPRECATION_WARNING",
            "BOOST_HANA_CONFIG_ENABLE_STRING_UDL",
            "BOOST_ASIO_USE_TS_EXECUTOR_AS_DEFAULT",
        ]
        
        compiler = self.settings.compiler
        if compiler in ("clang", "apple-clang") or (compiler == "gcc" and int(str(self.settings.compiler.version).split('.')[0]) >= 9):
            self.cpp_info.components["_ozo"].cxxflags = [
                "-Wno-gnu-string-literal-operator-template",
                "-Wno-gnu-zero-variadic-macro-arguments",
            ]
        
        self.cpp_info.filenames["cmake_find_package"] = "ozo"
        self.cpp_info.filenames["cmake_find_package_multi"] = "ozo"
        self.cpp_info.names["cmake_find_package"] = "yandex"
        self.cpp_info.names["cmake_find_package_multi"] = "yandex"
        self.cpp_info.components["_ozo"].names["cmake_find_package"] = "ozo"
        self.cpp_info.components["_ozo"].names["cmake_find_package_multi"] = "ozo"
    
    def compatibility(self):
        return [
            {"settings": [("build_type", None), ("compiler", None)]},
        ]
