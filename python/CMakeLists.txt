if(NOT HAVE_PYTHON)
  message(STATUS "Python interface is disabled or not all required dependencies found. Building without it...")
  return()
endif()

file(GLOB_RECURSE python_srcs ${PROJECT_SOURCE_DIR}/python/*.cpp)

add_library(pycaffe SHARED ${python_srcs})
#target_link_libraries(pycaffe PUBLIC ${Caffe_LINK} ${PYTHON_LIBRARIES} ${Boost_LIBRARIES})
target_link_libraries(pycaffe PUBLIC -LC:/msys64/mingw64/lib/ ${CMAKE_BINARY_DIR}/lib/libcaffe.dll.a -lglog -lgflags -lprotobuf -lpython2.7 -lboost_python-mt -lboost_system-mt -lboost_thread-mt -lboost_filesystem-mt -lboost_chrono-mt -lboost_date_time-mt -lboost_atomic-mt)
if(WIN32)
  set_target_properties(pycaffe PROPERTIES SUFFIX ".pyd")
endif()
caffe_default_properties(pycaffe)
set_target_properties(pycaffe PROPERTIES PREFIX "" OUTPUT_NAME "_caffe")
target_include_directories(pycaffe PUBLIC ${PYTHON_INCLUDE_DIRS} ${NUMPY_INCLUDE_DIR})

if(UNIX OR APPLE)
    set(__linkname "${PROJECT_SOURCE_DIR}/python/caffe/_caffe.so")
    add_custom_command(TARGET pycaffe POST_BUILD
                       COMMAND ln -sf $<TARGET_LINKER_FILE:pycaffe> "${__linkname}"
                       COMMAND ${CMAKE_COMMAND} -E make_directory ${PROJECT_SOURCE_DIR}/python/caffe/proto
                       COMMAND touch ${PROJECT_SOURCE_DIR}/python/caffe/proto/__init__.py
                       COMMAND cp ${proto_gen_folder}/*.py ${PROJECT_SOURCE_DIR}/python/caffe/proto/
                       COMMENT "Creating symlink ${__linkname} -> ${PROJECT_BINARY_DIR}/lib/_caffe${Caffe_POSTFIX}.so")
elseif(WIN32)
    add_custom_command(TARGET pycaffe POST_BUILD
                       COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:pycaffe> ${PROJECT_SOURCE_DIR}/python/caffe
                       COMMAND ${CMAKE_COMMAND} -E make_directory ${PROJECT_SOURCE_DIR}/python/caffe/proto
                       COMMAND ${CMAKE_COMMAND} -E touch ${PROJECT_SOURCE_DIR}/python/caffe/proto/__init__.py
                       COMMAND (robocopy  "\"${proto_gen_folder}\" \"${PROJECT_SOURCE_DIR}/python/caffe/proto\" *.py") ^& IF %ERRORLEVEL% LEQ 4 exit /B 0
                       COMMENT "Creating symlink ${__linkname} -> ${PROJECT_BINARY_DIR}/lib/_caffe.pyd")
endif()

# ---[ Install
# scripts
file(GLOB python_files *.py requirements.txt)
install(FILES ${python_files} DESTINATION python)

# module
install(DIRECTORY caffe
    DESTINATION python
    FILES_MATCHING
    PATTERN "*.py"
    PATTERN "ilsvrc_2012_mean.npy"
    PATTERN "test" EXCLUDE
    )

# _caffe.so
install(TARGETS pycaffe  DESTINATION python/caffe)

