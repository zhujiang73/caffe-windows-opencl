# Project setup
###############

cmake_minimum_required(VERSION 2.6 FATAL_ERROR)
#if(COMMAND cmake_policy)
#  cmake_policy(SET CMP0003 NEW)
#endif(COMMAND cmake_policy)

project(ViennaCL)

set(VERSION_MAJOR 1)
set(VERSION_MINOR 7)
set(VERSION_PATCH 1)
set(VERSION "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wno-sign-compare -Wno-unused-function -Wno-uninitialized")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-ignored-attributes -Wno-deprecated-declarations -D_USE_MATH_DEFINES")

#SET(CMAKE_VERBOSE_MAKEFILE ON)   #uncomment this line to increase CMake verbosity

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

# Add visibility of headers
# Necessary for Qt-Creator usage.
################
file( GLOB_RECURSE MAKE_HEADERS_VISIBLE_SRC
    *.hpp *.h)
add_custom_target( MAKE_HEADERS_VISIBLE SOURCES ${MAKE_HEADERS_VISIBLE_SRC} )


# Common options
################

set(VIENNACL_SRC_DIST TRUE)
include(ViennaCLCommon)

# Set release build:
IF(DEFINED CMAKE_BUILD_TYPE)
 SET (CMAKE_BUILD_TYPE "${CMAKE_BUILD_TYPE}")
ELSE()
 SET (CMAKE_BUILD_TYPE Release)
ENDIF()

# Compile options
#################

include_directories(BEFORE "${PROJECT_SOURCE_DIR}")

# Subdirectories
################

# Install
#########

install(DIRECTORY "${PROJECT_SOURCE_DIR}/viennacl" DESTINATION include)
install(FILES  ${CMAKE_BINARY_DIR}/ViennaCLConfig.cmake  DESTINATION share/ViennaCL)
install(FILES  ${CMAKE_BINARY_DIR}/ViennaCLConfigVersion.cmake  DESTINATION share/ViennaCL)

