if (NOT __clBLAS_INCLUDED) # guard against multiple includes
  set(__clBLAS_INCLUDED TRUE)

    # build directory
    set(clBLAS_PREFIX ${CMAKE_BINARY_DIR}/external/clBLAS-prefix)
    # install directory
    set(clBLAS_INSTALL ${CMAKE_BINARY_DIR}/external/clBLAS-install)

    # we build gflags statically, but want to link it into the caffe shared library
    # this requires position-independent code
    if (UNIX)
        set(clBLAS_EXTRA_COMPILER_FLAGS "-fPIC")
    endif()

    set(clBLAS_CXX_FLAGS ${CMAKE_CXX_FLAGS} ${clBLAS_EXTRA_COMPILER_FLAGS})
    set(clBLAS_C_FLAGS ${CMAKE_C_FLAGS} ${clBLAS_EXTRA_COMPILER_FLAGS})

    ExternalProject_Add(clBLAS
      PREFIX ${clBLAS_PREFIX}
      SOURCE_DIR  "${PROJECT_SOURCE_DIR}/src/clBLAS"
      INSTALL_DIR ${clBLAS_INSTALL}
      CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
                 -DCMAKE_INSTALL_PREFIX=${clBLAS_INSTALL}
                 -DCMAKE_C_FLAGS=${clBLAS_C_FLAGS}
                 -DCMAKE_CXX_FLAGS=${clBLAS_CXX_FLAGS}
      )

    set(clBLAS_FOUND TRUE)
    set(clBLAS_INCLUDE_DIRS ${CMAKE_BINARY_DIR}/external/clBLAS-install/include)
    #set(clBLAS_LIBRARIES ${CMAKE_BINARY_DIR}/external/clBLAS-install/lib/import/libclBLAS.dll.a)
    set(clBLAS_LIBRARIES ${CMAKE_BINARY_DIR}/external/clBLAS-install/lib64/import/libclBLAS.dll.a)
    set(clBLAS_EXTERNAL TRUE)

    list(APPEND external_project_dependencies clBLAS)

    install(DIRECTORY "${CMAKE_BINARY_DIR}/external/clBLAS-install/include"  DESTINATION "./" FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp")
    install(FILES  ${CMAKE_BINARY_DIR}/external/clBLAS-install/lib64/import/libclBLAS.dll.a DESTINATION lib)
    install(FILES  ${CMAKE_BINARY_DIR}/external/clBLAS-install/bin/libclBLAS.dll DESTINATION bin RENAME clBLAS.dll)
    
endif()

