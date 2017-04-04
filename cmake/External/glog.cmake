if (NOT __GLOG_INCLUDED)
  set(__GLOG_INCLUDED TRUE)

    # build directory
    set(glog_PREFIX ${CMAKE_BINARY_DIR}/external/glog-prefix)
    # install directory
    set(glog_INSTALL ${CMAKE_BINARY_DIR}/external/glog-install)

    # we build gflags statically, but want to link it into the caffe shared library
    # this requires position-independent code
    if (UNIX)
        set(glog_EXTRA_COMPILER_FLAGS "-fPIC")
    endif()

    set(GLOG_CXX_FLAGS ${CMAKE_CXX_FLAGS} ${GLOG_EXTRA_COMPILER_FLAGS})
    set(GLOG_C_FLAGS ${CMAKE_C_FLAGS} ${GLOG_EXTRA_COMPILER_FLAGS})

    # depend on gflags if we're also building it
    if (GFLAGS_EXTERNAL)
      set(GLOG_DEPENDS gflags)
    endif()

    ExternalProject_Add(glog
      PREFIX ${glog_PREFIX}
      SOURCE_DIR  "${PROJECT_SOURCE_DIR}/src/glog"
      INSTALL_DIR ${glog_INSTALL}
      CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
                 -DCMAKE_INSTALL_PREFIX=${glog_INSTALL}
                 -DCMAKE_C_FLAGS=${GLOG_C_FLAGS}
                 -DCMAKE_CXX_FLAGS=${GLOG_CXX_FLAGS}
      )

    set(GLOG_FOUND TRUE)
    set(GLOG_INCLUDE_DIRS ${glog_INSTALL}/include)
    set(GLOG_LIBRARIES ${GFLAGS_LIBRARIES} ${glog_INSTALL}/lib/libglog.dll.a)
    set(GLOG_LIBRARY_DIRS ${glog_INSTALL}/lib)
    set(GLOG_EXTERNAL TRUE)

    list(APPEND external_project_dependencies glog)
	
    FILE(GLOB_RECURSE GLOG_H "${CMAKE_BINARY_DIR}/external/glog-install/include/glog/*.h")
    INSTALL(FILES  ${GLOG_H}  DESTINATION include/glog)
    INSTALL(FILES  ${CMAKE_BINARY_DIR}/external/glog-install/lib/libglog.dll.a  DESTINATION lib)
    INSTALL(FILES  ${CMAKE_BINARY_DIR}/external/glog-install/bin/libglog.dll  DESTINATION lib)

endif()

