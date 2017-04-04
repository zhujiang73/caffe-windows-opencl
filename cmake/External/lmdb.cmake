if (NOT __LMDB_INCLUDED) # guard against multiple includes
  set(__LMDB_INCLUDED TRUE)

    # build directory
    set(lmdb_PREFIX ${CMAKE_BINARY_DIR}/external/lmdb-prefix)
    # install directory
    set(lmdb_INSTALL ${CMAKE_BINARY_DIR}/external/lmdb-install)

    # we build gflags statically, but want to link it into the caffe shared library
    # this requires position-independent code
    if (UNIX)
        set(lmdb_EXTRA_COMPILER_FLAGS "-fPIC")
    endif()

    set(lmdb_CXX_FLAGS ${CMAKE_CXX_FLAGS} ${lmdb_EXTRA_COMPILER_FLAGS})
    set(lmdb_C_FLAGS ${CMAKE_C_FLAGS} ${lmdb_EXTRA_COMPILER_FLAGS})

    ExternalProject_Add(lmdb
      PREFIX ${lmdb_PREFIX}
      SOURCE_DIR  "${PROJECT_SOURCE_DIR}/src/lmdb"
      INSTALL_DIR ${lmdb_INSTALL}
      CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
                 -DCMAKE_INSTALL_PREFIX=${lmdb_INSTALL}
                 -DCMAKE_C_FLAGS=${lmdb_C_FLAGS}
                 -DCMAKE_CXX_FLAGS=${lmdb_CXX_FLAGS}
      )

    set(LMDB_FOUND TRUE)
    set(LMDB_INCLUDE_DIR ${lmdb_INSTALL}/include)
    set(LMDB_LIBRARIES ${lmdb_INSTALL}/lib/liblmdb.a)
    set(lmdb_LIBRARY_DIRS ${lmdb_INSTALL}/lib)
    set(lmdb_EXTERNAL TRUE)

    list(APPEND external_project_dependencies lmdb)

    FILE(GLOB_RECURSE LMDB_H  ${CMAKE_SOURCE_DIR}/src/lmdb/src/*.h)
    INSTALL(FILES  ${LMDB_H}  DESTINATION include)

    INSTALL(FILES  ${CMAKE_BINARY_DIR}/external/lmdb-install/lib/liblmdb.a DESTINATION lib)

endif()

