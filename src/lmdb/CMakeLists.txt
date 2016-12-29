cmake_minimum_required(VERSION 3.0)

project(lmdb)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -D_USE_MATH_DEFINES")

include_directories("${PROJECT_SOURCE_DIR}/src")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(lmdb_srcs "${PROJECT_SOURCE_DIR}/src/mdb.c")
set(lmdb_srcs  ${lmdb_srcs}  "${PROJECT_SOURCE_DIR}/src/midl.c")

#ADD_LIBRARY(lmdb_shared SHARED ${lmdb_srcs})
ADD_LIBRARY(lmdb_static STATIC ${lmdb_srcs})

#target_link_libraries(lmdb_shared ntdll)
target_link_libraries(lmdb_static ntdll)

#SET_TARGET_PROPERTIES(lmdb_shared PROPERTIES OUTPUT_NAME "lmdb") 
SET_TARGET_PROPERTIES(lmdb_static PROPERTIES OUTPUT_NAME "lmdb") 

link_directories(${CMAKE_BINARY_DIR}/lib)

INSTALL(FILES  ${PROJECT_SOURCE_DIR}/src/lmdb.h DESTINATION include)
INSTALL(FILES  ${PROJECT_SOURCE_DIR}/src/midl.h DESTINATION include)
INSTALL(FILES  ${CMAKE_BINARY_DIR}/lib/liblmdb.a DESTINATION lib)


