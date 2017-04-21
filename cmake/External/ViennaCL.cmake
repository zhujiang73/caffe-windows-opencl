if (NOT __ViennaCL_INCLUDED) # guard against multiple includes
  set(__ViennaCL_INCLUDED TRUE)

    # build directory
    set(ViennaCL_PREFIX ${CMAKE_BINARY_DIR}/external/ViennaCL-prefix)
    # install directory
    set(ViennaCL_INSTALL ${CMAKE_BINARY_DIR}/external/ViennaCL-install)

    # we build gflags statically, but want to link it into the caffe shared library
    # this requires position-independent code
    if (UNIX)
        set(ViennaCL_EXTRA_COMPILER_FLAGS "-fPIC")
    endif()

    set(ViennaCL_CXX_FLAGS ${CMAKE_CXX_FLAGS} ${ViennaCL_EXTRA_COMPILER_FLAGS})
    set(ViennaCL_C_FLAGS ${CMAKE_C_FLAGS} ${ViennaCL_EXTRA_COMPILER_FLAGS})

    ExternalProject_Add(ViennaCL
      PREFIX ${ViennaCL_PREFIX}
      SOURCE_DIR  "${PROJECT_SOURCE_DIR}/src/viennacl"
      INSTALL_DIR ${ViennaCL_INSTALL}
      CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
                 -DCMAKE_INSTALL_PREFIX=${ViennaCL_INSTALL}
                 -DCMAKE_C_FLAGS=${ViennaCL_C_FLAGS}
                 -DCMAKE_CXX_FLAGS=${ViennaCL_CXX_FLAGS}
      )

    set(ViennaCL_FOUND TRUE)
    set(ViennaCL_INCLUDE_DIRS ${CMAKE_BINARY_DIR}/external/ViennaCL-install/include)
    set(ViennaCL_EXTERNAL TRUE)

    list(APPEND external_project_dependencies ViennaCL)

   install(DIRECTORY "${CMAKE_BINARY_DIR}/external/ViennaCL-install/include/viennacl" DESTINATION include)
   	

endif()

